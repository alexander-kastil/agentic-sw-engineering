---
name: pitch-bundle
description: Subskill of /create-product-pitch. Bundles N individual per-slide PPTX files into one master `.pptx` deck using PowerPoint COM `Slides.InsertFromFile`. The order is determined by the per-slide `.md` filenames in the slides folder. Use after [[pitch-add-slide]] or [[create-product-pitch]] when the canonical bundled PPTX needs to be refreshed. Triggers on "update the pptx", "bundle slides", "rebuild deck", "merge pptx", "combine slides into pptx".
metadata:
  version: 1.0.0
---

# Pitch Bundle (Subskill)

Single responsibility: take the per-slide source PPTXs (one per slide, from individual Gamma single-card calls) and assemble them into ONE master `.pptx` in the order declared by the `<NN>-<slug>.md` filename prefixes.

## Why this exists

Each new slide added via [[pitch-add-slide]] produces its own single-slide `.pptx` (saved in `<product>/assets/components/` by convention). The canonical bundled deck at `<product>/assets/<name>.pptx` grows stale. Without re-running an expensive full-deck Gamma call (~30+ credits), there is no other way to refresh it. This subskill solves that with a free PowerPoint COM merge.

## Inputs

- **Slides folder** — defaults to `<product>/assets/slides/` (where the `<NN>-<slug>.md` files live).
- **Sources map** — a list of `(<slug>, <source_pptx_path>, <source_slide_index>)` triples in the desired order. By convention:
  - Slides whose source is the original full-deck PPTX (e.g., `<product>/assets/<name>.pptx`) reference that file with the relevant slide index.
  - Slides added via [[pitch-add-slide]] reference the single-slide PPTX in `<product>/assets/components/_<slug>.pptx` with index 1.
- **Output path** — defaults to `<product>/assets/<name>.pptx` (overwriting the canonical bundled deck).

## Algorithm (recommended: open existing source as base)

**Avoid `Presentations.Add()`.** On some PowerPoint versions it returns 0 slides, on others 1 blank. The "delete the blank afterwards" approach is brittle (it can silently delete a real inserted slide). Use this instead:

1. Pick ONE source PPTX as the base — typically the original full-deck PPTX (e.g., `<product>/assets/<name>-source.pptx`).
2. Open it with `$master = $ppt.Presentations.Open($basePath, $false, $false, $false)`.
3. The base already has its N original slides. Compute the list of INSERTIONS needed (only the new slides not already in the base) and the position after which each should be inserted.
4. For each insertion in order:
   - `$master.Slides.InsertFromFile($sourcePath, $insertAfterIndex, 1, 1) | Out-Null`
5. `$master.SaveAs($outputPath)`.
6. Quit PowerPoint.

This avoids the blank-slide management entirely. Theme and master inherit from the base deck.

## Algorithm (fallback: full assembly from blank)

Only use this if no single source PPTX can serve as the base.

1. Open a fresh session and call `$master = $ppt.Presentations.Add()`.
2. Immediately check `$master.Slides.Count`. If it is 1, you have a blank to delete later. If it is 0, you do not.
3. Insert all slides via `InsertFromFile`.
4. If a blank was created, find it by checking each slide for empty `Shapes.Title` AND empty body — do NOT just delete the last slide.
5. `SaveAs` and quit.

## Reference PowerShell (recommended: open-base approach)

This is the script that worked end-to-end for a 7-slide base + 6 inserted = 13-slide deck.

```powershell
param(
    [Parameter(Mandatory=$true)][string]$BasePptx,                # the source deck to extend
    [Parameter(Mandatory=$true)][array]$Insertions,               # array of @{ Path = '...'; At = <insertAfterIndex> }
    [Parameter(Mandatory=$true)][string]$OutputPath
)

$ErrorActionPreference = 'Stop'
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = -1
try {
    $master = $ppt.Presentations.Open($BasePptx, $false, $false, $false)
    Write-Output ("Opened base deck: {0} slides" -f $master.Slides.Count)
    foreach ($ins in $Insertions) {
        $master.Slides.InsertFromFile($ins.Path, $ins.At, 1, 1) | Out-Null
        Write-Output ("Inserted {0} after position {1}" -f (Split-Path -Leaf $ins.Path), $ins.At)
    }
    Write-Output ("Total slides: {0}" -f $master.Slides.Count)
    $master.SaveAs($OutputPath)
    $master.Close()
} finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
```

Example invocation for a deck with 6 new component/architecture slides inserted between position 3 (the solution overview) and position 4 (the first use case) of an original 7-slide source:

```powershell
$insertions = @(
    @{ Path = 'components/_hugo.pptx';                       At = 3 },
    @{ Path = 'components/_mcp-brain.pptx';                  At = 4 },
    @{ Path = 'components/_hermes.pptx';                     At = 5 },
    @{ Path = 'components/_architektur.pptx';                At = 6 },
    @{ Path = 'components/_mehrere-agenten-parallel.pptx';   At = 7 },
    @{ Path = 'components/_mehrere-agenten-pillars.pptx';    At = 8 }
)
& bundle.ps1 -BasePptx 'mini-ai-server-pitch-source.pptx' `
             -Insertions $insertions `
             -OutputPath 'mini-ai-server-pitch.pptx'
```

## Critical PowerPoint COM gotchas

- `MsoTriState`: `$ppt.Visible = -1` (numeric `msoTrue`). The enum reference fails to resolve. Same gotcha as [[pitch-export]].
- `InsertFromFile` index is 0-based for the target position; source `SlideStart`/`SlideEnd` are 1-based.
- The initial blank slide from `Presentations.Add()` ends up at the LAST position after all inserts (because each insert places content before the existing slide). Delete `Item($master.Slides.Count)` after all inserts.
- `SaveAs` requires an absolute path. Resolve before passing.
- The merge preserves each source slide's theme. If sources use different themes, the master deck will have visual inconsistency. Gamma decks generated in the same session typically share the `default-light` theme, so this is rarely a problem.

## Source resolution heuristics

When the sources map is not provided explicitly, the bundle subskill can heuristically locate sources:

- For slugs matching a single-slide PPTX `_<slug>.pptx` in `<product>/assets/components/`, use that file with slide index 1.
- For slugs that are part of the original full-deck `<product>/assets/<name>.pptx`, infer the slide index from the original deck's slide order. Risky if the original deck has been edited in Gamma.

The explicit sources map is safer for production use.

## What to return to the caller

```
output: <product>/assets/<name>.pptx
slides_merged: <N>
sources_used: [<slug>: <pptx>#<index>, ...]
```

## What NOT to do

- Don't run a Gamma Pattern A call just to refresh a deck after adding one or two slides. This subskill is free and faster.
- Don't merge by editing XML directly (the `python-pptx` "deep clone" approach). PowerPoint COM `InsertFromFile` handles theme inheritance, embedded fonts, and image references correctly; XML cloning routinely breaks one of those.
- Don't overwrite the canonical bundled PPTX without keeping the original safe. Write to a temp name first, verify slide count and theme, then rename.
- Don't include the `_<slug>.pptx` working files in any cleanup. They're the source of truth for future bundle runs.
