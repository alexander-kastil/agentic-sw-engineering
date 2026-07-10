---
name: pitch-add-slide
description: Subskill of /create-product-pitch. Inserts ONE new slide into an existing pitch deck end-to-end. Honors the prompt → frontmatter → image rule. Writes the per-slide `.md` first, delegates to pitch-renumber if inserting (not appending), runs brand-voice scrub on the new file, fires a single-card Gamma call (Pattern B), downloads the PPTX, converts to a PNG with the matching slug name. Use when the user asks to "add a slide", "insert a slide", or wants a new card after the deck is already in place. Triggers on "add a slide", "insert a slide", "new slide", "another slide", "extra slide".
metadata:
  version: 1.0.0
---

# Pitch Add Slide (Subskill)

Handles the most common post-deck operation: inserting one new slide into an existing pitch deck. We did this three times in one session (component spotlights, then a tech architecture slide, then a parallel-containers slide) — each time the user had to re-explain the steps. This subskill encodes them.

## Inputs

- **Position** — insertion index (e.g., 7) OR a marker like "after slide 06" or "at the end".
- **Title** — the slide's `# H1` headline.
- **Content sketch** — bullets, body text, or a paragraph of intent.
- **Image direction** — the visual concept (recurring motif, mood, style, "no people" or not).
- **Slides folder** — defaults to `<product>/assets/slides/`.

## Pipeline (in order, no shortcuts)

### Step 1 — Write the frontmatter `.md` FIRST

Create `<NN>-<slug>.md` in the slides folder with the full frontmatter schema (`slide`, `topic`, `title`, `subtitle`, `layout`, `visual-weight`, `visual-type`, `visual-prompt`, `order`, `source`, `gamma_prompt`) plus the body sections (`# Title`, `## Content`, `## Notes`). Follow the schema documented in [[pitch-slides]].

**This is the source of truth for the slide. Never skip it.** See [[feedback-skill-frontmatter-first]].

### Step 2 — Renumber subsequent slides (if inserting, not appending)

If the insertion position is anywhere except the end, delegate to [[pitch-renumber]] to shift the existing `<NN>-<slug>.{md,png}` pairs upward by one. The subskill updates filenames AND the `slide:` / `order:` fields in each renumbered `.md`.

### Step 3 — Brand-voice scrub the new `.md`

Delegate to [[pitch-brand-voice]] scoped to the new file. Verify `grep -c "—"` returns 0 before continuing.

### Step 4 — Generate the image (Pattern B from [[pitch-gamma]])

Single-card Gamma call (`numCards: 1`, `textMode: "preserve"`). Read the `gamma_prompt` field from the frontmatter as the literal `additionalInstructions` input. Read the `# Title` + `## Content` body as `inputText`.

Cost: ~5 credits per slide (vs ~30 for a full-deck regeneration).

### Step 5 — Download + convert with slug naming

Delegate to [[pitch-export]] with the single-slide hint: the downloaded PPTX has one slide, convert it to `<NN>-<slug>.png` in the slides folder (matching the `.md` sibling). Use the bundled PowerShell + PowerPoint COM path on Windows.

### Step 6 — Optional: re-bundle the master PPTX

If the deck has a canonical bundled `.pptx` (e.g., `<product>/assets/<name>.pptx`), delegate to [[pitch-bundle]] to merge the new slide into the master deck at the right position.

## Stage gates

- After Step 1: the `.md` MUST exist before Step 4 runs.
- After Step 3: `grep -c "—"` on the new `.md` MUST return 0 before Step 4 runs.
- After Step 4: status check returns `completed` before Step 5 runs.

## What to return to the caller

```
new_slide: <NN>-<slug>.md + <NN>-<slug>.png
renumbered: [<list of files shifted>]
gammaUrl: https://gamma.app/docs/...
credits_used: <N>
master_pptx_updated: <true|false>
```

## What NOT to do

- Don't fire Gamma before the `.md` exists. The frontmatter is the spec, not a write-up.
- Don't reuse a previous Gamma generation for a different slide. Each slide has its own `gamma_prompt`.
- Don't skip renumbering when inserting. The numeric prefix is what gives the deck its order.
- Don't re-run a full-deck Gamma (Pattern A) for a single-slide addition. Pattern B costs ~5 credits vs ~30.
