---
name: pitch-sources
description: Subskill of /create-product-pitch. Gathers all source materials needed to draft a product pitch by batching parallel file reads. Covers product use-case docs, technical specs, existing reference decks (PDF + slide images), brand assets, and relevant memory entries. Use as Stage 1 of the pitch pipeline. Triggers on "gather pitch sources", "read product docs for pitch", or when invoked by [[create-product-pitch]].
metadata:
  version: 1.0.0
---

# Pitch Sources (Subskill)

Stage 1 of [[create-product-pitch]]. Read everything needed to draft the outline, **in parallel**, in a single message.

## What to read

Batch all of these into one tool block:

1. **Product docs** — every `*.md` under the product directory and its `assets/` (e.g., `<product>/readme.md`, `<product>/assets/*-usecases.md`, `<product>/assets/*-technical.md`).
2. **Existing reference deck** — if a sibling marketing folder has a Gamma-generated PDF (e.g., `mail-automation/mail-automation.pdf`) plus PNG slide assets, read 1–2 of the PNGs to lock in stylistic precedent (rhythm, brevity, tone).
3. **Project-level instructions** — `CLAUDE.md`, `tasks/lessons.md` if present.
4. **Memory** — the project's `MEMORY.md` and every `feedback_*.md` entry. Brand-voice rules live here.
5. **Brand assets** — logo, color swatches if present (`brand/`, `assets/brand/`, or similar).
6. **Technology / partner logos** — for any third-party tools, platforms, or cloud providers featured in the deck (e.g. Docker, Azure, NVIDIA, etc.), check whether `assets/images/<slug>.svg` or `.png` already exists. If not, spawn the **Logo Finder** agent (`subagent_type: "Logo Finder"`) for each missing logo. Run all Logo Finder calls in a single parallel message. Logos land at `assets/images/<slug>.svg` and are available for slide authoring and Gamma image direction.

## How to run

Use `Glob` to discover, then `Read` everything in a single batched message. Do not read files sequentially — every read in this stage is independent.

Example pattern:

```
# parallel:
Glob: <product>/**/*.md
Glob: <product>/assets/*
Glob: <sibling-marketing>/*.pdf

# then parallel:
Read each discovered file
Read MEMORY.md
Read each feedback_*.md
```

If a reference deck PDF is over 20 pages, pass `pages: "1-5"` to limit the read.

## What to return to the caller

A short structured digest:

- **Product name + one-line summary** (extracted from the main product doc)
- **Available personas / use cases** (titles + one-line each)
- **Hardware/pricing tiers** if present
- **Existing reference deck** — path + stylistic notes ("4 slides, German, blue-violet theme")
- **Voice rules from memory** — every `feedback_*` entry tagged `type: feedback` that touches copy/voice
- **Open questions** — anything ambiguous that the master skill should clarify with the user before drafting

Keep the digest under 400 words. The master skill uses it to plan the clarifying-question batch.

## Logo Finder invocation pattern

```
# Identify tech/partner logos needed from the product doc
# Check which are already present:
Glob: assets/images/*.svg
Glob: assets/images/*.png

# For each missing logo, spawn Logo Finder in parallel (single message):
Agent(subagent_type="Logo Finder", prompt="Find the official <Brand> logo, download it with transparent background, save to assets/images/<slug>.svg in D:\\git-customers\\ai-mini-server")
```

Report discovered logo paths in the digest so [[pitch-slides]] can reference them in `visual-prompt` fields.

## What NOT to do

- Don't read files sequentially.
- Don't read full 50+ page PDFs without `pages:` paging.
- Don't read the same file twice across batches.
- Don't include code samples or full doc transcripts in the digest — just the extracted facts.
- Don't ask Gamma to render a known brand logo as an AI-generated image. Use the downloaded file path instead.
