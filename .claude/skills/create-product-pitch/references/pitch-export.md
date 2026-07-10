---
name: pitch-export
description: Subskill of /create-product-pitch. Downloads a Gamma-generated PPTX from its exportUrl and converts every slide to a 1920×1080 PNG image using PowerPoint COM automation (Windows). Fallback paths documented for LibreOffice (Linux/macOS) and manual PowerPoint Save-As. Use as Stage 6 of the pitch pipeline. Triggers on "export slides", "pptx to png", "slide images", "convert deck", or when invoked by [[create-product-pitch]].
metadata:
  version: 1.0.0
---

# Pitch Export (Subskill)

Stage 7 of [[create-product-pitch]]. Two steps: download PPTX, convert to per-slide PNG.

## Inputs

- `exportUrl` — direct PPTX URL returned by [[pitch-gamma]]
- The list of per-slide `.md` files written by [[pitch-slides]] — their slugs determine the PNG filenames
- `<product>/assets/slides/` — target directory (where the `.md` files already live)

## Naming convention

The PNG MUST be named to match its `.md` sibling. For a frontmatter file at `04-komponente-hugo.md`, the PNG is `04-komponente-hugo.png` in the same directory. After conversion, rename `slide-1.png`, `slide-2.png`, ... from the bundled script to the slug names, in the order specified by the slide list. For per-slide Pattern B calls, the source PPTX has one slide and the output PNG goes straight to `<NN>-<slug>.png`.

## Step 1: Download PPTX

Single Bash call:

```bash
mkdir -p <product>/assets/slides
curl -sL -o "<product>/assets/<name>.pptx" "<exportUrl>"
ls -la <product>/assets/<name>.pptx
```

The Gamma exportUrl is a signed public URL. No auth headers needed. Expect 5–30 MB.

## Step 2: Convert PPTX to PNGs

### Primary path: PowerShell + PowerPoint COM (Windows)

Use the bundled script `create-product-pitch/scripts/pptx-to-png.ps1`. Copy or invoke it directly:

```powershell
& "<path-to-create-product-pitch>/scripts/pptx-to-png.ps1" `
    -PptxPath "<product>/assets/<name>.pptx" `
    -OutDir "<product>/assets/slides"
```

Output: `slide-1.png`, `slide-2.png`, ... at 1920×1080.

### Critical gotcha — `MsoTriState` enum

`$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue` fails with `Unable to find type` because the Office interop assembly is not loaded by default in PowerShell. **Use the numeric value `-1` for `msoTrue`** instead:

```powershell
$ppt.Visible = -1  # msoTrue
```

PowerPoint COM **refuses to operate fully invisible** — `$true` does not work either. `-1` is correct.

### Fallback path: LibreOffice headless (Linux/macOS)

```bash
soffice --headless --convert-to pdf --outdir <product>/assets <product>/assets/<name>.pptx
pdftoppm -png -r 150 <product>/assets/<name>.pdf <product>/assets/slides/slide
```

Requires both `libreoffice` (or `soffice`) and `poppler-utils` (`pdftoppm`). Check first:

```bash
command -v soffice && command -v pdftoppm
```

### Fallback path: manual (when no tooling available)

Tell the user:

> Open `<product>/assets/<name>.pptx` in PowerPoint. File → Export → Change File Type → PNG → Save All Slides → choose `<product>/assets/slides/`.

## Probe before promising

Before running, probe the environment **once** (not per slide):

```bash
command -v soffice; command -v pdftoppm; powershell -NoProfile -Command "try { \$ppt = New-Object -ComObject PowerPoint.Application -ErrorAction Stop; Write-Output 'POWERPOINT_OK'; \$ppt.Quit() } catch { Write-Output 'NO_POWERPOINT' }"
```

Pick the path that's available. Don't waste a turn trying soffice on a machine where only PowerPoint exists.

## Verification

After conversion, in a single message read 3 representative slide images (title, a use-case slide, the tiers slide) to confirm:

- Each PNG exists and is non-zero size
- Title slide image matches the requested motif
- "No people" constraint was honored on use-case slides

Surface obvious misses to the user; do not regenerate.

## What to return to the caller

```
pptx: <product>/assets/<name>.pptx (XX MB)
slides: <product>/assets/slides/slide-{1..N}.png
verified: slide-1, slide-4, slide-7 spot-checked
```

## What NOT to do

- Don't run the PowerShell script per slide. The bundled script loops internally.
- Don't poll a guessed Gamma URL endpoint for download status — the exportUrl from `get_generation_status` is already final.
- Don't auto-clean up the intermediate PDF (LibreOffice path) without asking — it's sometimes useful.
- Don't promise PDF + images from a single Gamma call. Gamma's `exportAs` accepts only one format. If PDF is needed, export it from the Gamma editor after the user has reviewed.
