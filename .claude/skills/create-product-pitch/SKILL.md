---
name: create-product-pitch
description: Master skill for turning a raw product idea OR existing technical/use-case docs into a polished marketing pitch deck. Optionally shapes a 3-line idea into a structured brief first, then produces a long outline plus a 6 to 7 card Gamma deck, exported to PPTX and per-slide PNG images. Delegates to idea-to-pitch, pitch-sources, pitch-outline, pitch-slides, pitch-brand-voice, pitch-gamma, and pitch-export. Use when the user invokes /create-product-pitch, or says "create a pitch", "idea to pitch", "shape this idea", "product idea pitch", "pitch deck", "marketing pitch", "Gamma pitch", "turn this into slides", "make a pitch out of X", or "create slides for a product".
metadata:
  version: 1.0.0
---

# Create Product Pitch (Master)

End-to-end pipeline: raw idea or existing product docs → polished marketing pitch deck + PNG slides.

The master's job is **orchestration with maximum parallelism** and to enforce the stage gates that prevent expensive re-runs (most importantly: scrub brand voice BEFORE invoking Gamma). When the user arrives with only a rough idea instead of a product brief, run the optional Stage 0 first to shape it.

---

## Subskills (referenced)

### Stage 0 (optional): raw idea → brief

| Stage | Subskill | Purpose |
|---|---|---|
| 0 | [[idea-to-pitch]] | Shape a 3-to-many-line idea into the `readme.md` + `usecases.md` brief the pipeline reads. Skip when a brief already exists. |

### Core pipeline (initial deck creation)

| Stage | Subskill | Purpose |
|---|---|---|
| 1 | [[pitch-sources]] | Read all reference and product source materials in parallel |
| 2 | [[pitch-outline]] | Draft the long marketing outline (single coherent narrative) |
| 3 | [[pitch-slides]] | Write per-slide frontmatter `.md` files as canonical source of truth |
| 4 | [[pitch-brand-voice]] | Scrub all per-slide `.md` files for em dashes and project-specific voice rules |
| 5 | [[pitch-gamma]] | Invoke Gamma using `gamma_prompt` from each frontmatter; 5000-char `additionalInstructions` limit |
| 6 | [[pitch-export]] | Download PPTX and convert to PNGs with slug names matching the `.md` siblings |
| 7 | [[pitch-bundle]] | Optional: assemble a master `.pptx` from per-slide source PPTXs via PowerPoint COM |

### Maintenance pipeline (existing deck modifications)

| Subskill | Purpose |
|---|---|
| [[pitch-add-slide]] | End-to-end insertion of one new slide into an existing deck (frontmatter → scrub → single-card Gamma → PNG) |
| [[pitch-renumber]] | Atomic rename of `<NN>-<slug>.{md,png}` pairs with frontmatter `slide:`/`order:` updates |
| [[pitch-bundle]] | Refresh the canonical bundled `.pptx` after slides are added or changed |

Templates and shared resources live under this skill's directory:

- `templates/outline-skeleton.md` — fillable structure for the long outline
- `templates/slides-skeleton.md` — fillable structure for the slide spec
- `scripts/pptx-to-png.ps1` — the working PowerPoint COM conversion script
- `references/lessons.md` — distilled gotchas

---

## Orchestration plan (parallelism explicit)

### Stage 0 — Shape the idea (OPTIONAL, SEQUENTIAL)

Run only when the user has a raw idea and no product brief yet. Delegate to [[idea-to-pitch]]: run its ledger-based discussion loop and write `<product>/readme.md` + `<product>/assets/usecases.md`. When a brief already exists, skip straight to Stage 1. After the brief is written, continue directly into Stage 1 with the new files as source materials, no second invocation.

### Stage 1 — Gather + Clarify (PARALLEL)

Run in one message:
- Delegate to [[pitch-sources]]: batch all `Read` calls for product docs, reference decks, brand assets, and relevant memory files in a single tool block. [[pitch-sources]] also identifies any required technology/partner logos and spawns **Logo Finder** agents in parallel for missing ones (saves to `assets/images/<slug>.svg`).
- Single `AskUserQuestion` (1–4 questions) covering: language, primary audience, use-case focus, visual theme. **Do not ask one at a time.**

Do not proceed until both finish.

### Stage 2 — Draft outline (SEQUENTIAL, OPTIONALLY FAN OUT)

- Delegate to [[pitch-outline]]. One Write to `<product>/pitch-outline-<lang>.md`.
- For 4+ use-case spotlights, optionally fan out: spawn one `Agent` per persona to draft that section in parallel, then merge. For 2–3 spotlights, draft inline.

### Stage 3 — Draft per-slide frontmatter (PARALLEL ON SLIDES, plus pre-flight)

Run in one message:
- Delegate to [[pitch-slides]]: write ONE `<NN>-<slug>.md` frontmatter file per slide into `<product>/assets/slides/`. All N writes can be batched in a single message since each file is independent.
- Probe export tooling availability (one Bash call: `command -v soffice; command -v pdftoppm; powershell -Command "try {...PowerPoint COM...}"`).
- The `<product>/assets/slides/` directory is created as part of the writes.

**Rule:** prompt → frontmatter → slide/image. Never generate a Gamma image before the per-slide `.md` exists. See [[feedback-skill-frontmatter-first]] if it exists in project memory.

### Stage 4 — Brand voice scrub (PARALLEL ON FILES)

Delegate to [[pitch-brand-voice]]. The subskill scrubs all per-slide `.md` files in one message (parallel Edit calls) plus the outline, and verifies zero violations remain with `grep -c "—" <product>/assets/slides/*.md`.

**STAGE GATE:** Do not advance to Stage 5 until grep returns 0 across all slide files. An em dash leaking through wastes Gamma credits.

### Stage 5 — Story Review (SEQUENTIAL, USER GATE)

Assemble the deck story from the per-slide `.md` files and present it as a single markdown document. This is the last free checkpoint before Gamma credits are spent.

**How to assemble:** Read all `<product>/assets/slides/<NN>-<slug>.md` in order. For each slide render a compact block:

```markdown
### Slide N — <title>
**Subtitle:** <subtitle>  |  **Layout:** <layout>  |  **Visual:** <visual-type>

<bullets from ## Content>

> <speaker notes — one sentence>
```

Output the assembled story inline in the conversation (do not write to disk unless the user asks). Follow immediately with a single `AskUserQuestion`:
- Question: "Does the slide story read correctly? Any slides to adjust before Gamma runs?"
- Options: "Looks good — proceed to Gamma" / "I have changes"

If the user requests changes: apply edits to the affected `.md` files, re-run [[pitch-brand-voice]] on changed files only, then re-present the corrected story and ask again.

**STAGE GATE:** Do not advance to Stage 6 without explicit user approval.

### Stage 6 — Generate (SEQUENTIAL)

Delegate to [[pitch-gamma]]. One Gamma call. After it returns the `generationId`, the subskill's recipe explains when to check status (the interactive widget polls, but the export URL is retrieved via `get_generation_status` once `status == "completed"`).

### Stage 7 — Download + Export (PARALLEL THEN SEQUENTIAL)

- In parallel: curl the PPTX export URL into `<product>/assets/<name>.pptx`, and (if not already done) stage the conversion script.
- Then sequentially: delegate to [[pitch-export]] which runs the PowerShell+PowerPoint COM conversion.

### Stage 8 — Verify (PARALLEL)

In one message: `Read` 3–5 representative slide PNGs to confirm image direction was honored (especially "no people" slides). Surface any obvious misses to the user — do not re-run Gamma; users iterate in the Gamma editor.

---

## Inputs the master collects (Stage 1)

Bundled into one `AskUserQuestion`:

1. **Language** — match the language of any existing reference deck unless overridden. Default DE if Austrian audience.
2. **Audience** — end customers vs. resellers/IT partners vs. mixed/investor.
3. **Use-case focus** — which personas get full-slide spotlights vs. matrix treatment.
4. **Visual theme** — match the existing reference deck, new theme, or let Gamma pick.

Always offer "let Gamma pick" as a low-friction default for theme.

---

## Output contract (what the user gets)

- `<product>/pitch-outline-<lang>.md` — long marketing outline
- `<product>/pitch-slides-prompt-<lang>.md` — 6–7 card slide spec with per-slide image direction
- `<product>/assets/<name>.pptx` — Gamma-generated deck
- `<product>/assets/slides/slide-{1..N}.png` — 1920×1080 slide images
- Gamma editor URL for live iteration

End-of-turn summary: list these paths + the Gamma editor URL + the Gamma credit cost.

---

## Hard rules

- **Always run [[pitch-brand-voice]] before [[pitch-gamma]].** This is the single most expensive mistake to repeat.
- **Single Gamma call per deck.** The user iterates visuals in Gamma's editor, not via re-generation.
- **Honor existing CLAUDE.md project rules.** If the project has `tasks/lessons.md` or a brand-voice memory entry, the brand-voice subskill must consult it.
- **No experimental files in repo root.** Pitch artifacts live under the product's own directory (e.g., `<product>/`, `<product>/assets/`).
- **Don't re-Read freshly written files** to verify — `Write`/`Edit` would have errored if it failed.

---

## Lessons learned from prior runs

See [[references/lessons.md]] for the distilled list. The top three:

1. Gamma's `additionalInstructions` parameter has a hard 5000-character limit. Trim aggressively before sending.
2. Gamma's image `stylePreset` is best-effort; the chosen theme can override it. "no people" must be stated explicitly per slide direction.
3. PowerPoint COM enum `[Microsoft.Office.Core.MsoTriState]::msoTrue` fails to resolve without loading the Office assembly. Use the numeric value `-1` instead.
