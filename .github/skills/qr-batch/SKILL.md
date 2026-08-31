---
name: qr-batch
description: Render a batch of QR code PNG files from a list of URLs, one image per link, with a shared size and error-correction setting. Use when the user needs QR codes for conference badges, printed handouts, product labels, stickers, or a set of campaign links, even if they do not say "QR" and only describe wanting scannable images for a list of URLs.
license: MIT
compatibility: Requires uv (or pipx) to run the bundled Python script
metadata:
  author: integrations.at
  version: "1.0"
---

# QR Batch

Turn a list of URLs into one PNG QR code per URL. The image bytes come from
[scripts/generate_qr_batch.py](scripts/generate_qr_batch.py), never from the model.

## Workflow

1. Collect four parameters from the conversation. Ask only for what is missing.

   | Parameter | Required | Default | Notes |
   |-----------|----------|---------|-------|
   | Links | Yes | none | One `slug` and one `url` per code. Derive the slug from the URL when the user gives no name. |
   | Output directory | Yes | none | Where the PNG files land. |
   | Box size | No | `10` | Pixels per module. Print needs 12 or more, screen is fine at 6. |
   | Error correction | No | `M` | Use `H` when the code will be printed on fabric or overprinted with a logo. |

2. Write the links to a manifest file as a JSON list of `{slug, url}` objects.

   ```json
   [
     { "slug": "class-repo", "url": "https://github.com/alexander-kastil/agentic-sw-engineering" },
     { "slug": "homepage", "url": "https://www.integrations.at" }
   ]
   ```

3. Preview the plan before writing any file:

   ```bash
   uv run scripts/generate_qr_batch.py --manifest links.json --out-dir out --dry-run
   ```

4. Show the user the planned file list, then run the same command without `--dry-run`.

5. Report the `count` and the paths from the script's JSON output. Do not describe what the
   images look like; you cannot see them.

## Gotchas

- Slugs become file names, so reject spaces and slashes and replace them with hyphens.
  A duplicate slug silently overwrites the earlier PNG.
- The script rounds nothing: `--box-size 10` on a long URL can exceed 1000 pixels per side.
  Long URLs plus `--error-correction H` grow fastest.
- Never hand-write a QR matrix or emit SVG paths yourself. A code that scans is the entire
  deliverable, and the model cannot verify one.
