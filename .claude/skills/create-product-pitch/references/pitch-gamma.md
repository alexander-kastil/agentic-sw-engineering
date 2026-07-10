---
name: pitch-gamma
description: Subskill of /create-product-pitch. Invokes the Gamma `generate` MCP tool. Reads each per-slide frontmatter `.md` file, takes the `gamma_prompt` field as the literal `additionalInstructions` input, and the `# Title` + `## Content` body as `inputText`. Handles the 5000-char `additionalInstructions` limit, retrieves the export URL via `get_generation_status`. Use as Stage 5 of the pitch pipeline. Triggers on "generate pitch with Gamma", "create the deck", or when invoked by [[create-product-pitch]].
metadata:
  version: 2.0.0
---

# Pitch Gamma (Subskill)

Stage 6 of [[create-product-pitch]]. The frontmatter `.md` files written by [[pitch-slides]] are the source. The brand-voice scrub gate must have passed before this runs.

## Two call patterns

### Pattern A: full-deck single call

For 6 to 7 card decks delivered as ONE PPTX. Build `inputText` by concatenating all per-slide `.md` body sections; build `additionalInstructions` by concatenating the terse `gamma_prompt` fields from each frontmatter, capped at 5000 chars total.

```
mcp__claude_ai_Gamma__generate(
  inputText: <concat of all `# Title` + `## Content` bodies, in slide order>,
  format: "presentation",
  numCards: <N from slide count>,
  textMode: "generate",
  exportAs: "pptx",
  textOptions: {
    language: "<from frontmatter or clarifying question>",
    amount: "brief",
    audience: "<from clarifying questions>",
    tone: "professional, trust-first, plain-spoken"
  },
  imageOptions: { source: "aiGenerated", stylePreset: "photorealistic" },
  additionalInstructions: <concat of each slide's gamma_prompt, ≤ 5000 chars>
)
```

### Pattern B: per-slide single-card calls (recommended for control)

For component spotlights, late-added slides, or any case where you need exact text and exact per-slide image rendering. Fire ONE Gamma call per slide, `numCards: 1`, `textMode: "preserve"`.

```
mcp__claude_ai_Gamma__generate(
  inputText: <single slide's `# Title` + body, preserve as-written>,
  format: "presentation",
  numCards: 1,
  textMode: "preserve",
  exportAs: "pptx",
  textOptions: { language, amount, audience, tone },
  imageOptions: { source: "aiGenerated", stylePreset: "photorealistic" },
  additionalInstructions: <the slide's gamma_prompt field, verbatim>
)
```

Per-slide cost is ~5 credits vs ~30 for a full deck, but you get one PPTX per slide and visual style may drift slightly between runs.

**Default: Pattern A for initial decks, Pattern B for additions or fixes.**

## Hard limits

### `additionalInstructions` ≤ 5000 characters

Returns HTTP 400 if exceeded. Before sending:

```bash
wc -c <<< "$additional_instructions"
```

If over 5000, condense by:
1. Drop decorative wording ("very", "ensure that")
2. Compress per-slide direction to 1 to 3 sentences
3. Drop slide-by-slide bullets (they're in `inputText` already)
4. Keep: per-slide image direction + "no people, recurring motif"

### Single call per deck (Pattern A)

Do not re-run for iteration. The user iterates inside the Gamma editor (returned `gammaUrl`). Each re-run costs ~30+ credits.

### Per-slide calls are additive (Pattern B)

If a deck needs new slides added later, run Pattern B for each addition. Do NOT re-run Pattern A on the full deck.

## Known Gamma quirks

- `numCards: N` + `textMode: "preserve"` + multiple H2 sections in inputText can collapse to a single card. If you need N independent cards, use Pattern B (one call per card).
- `imageOptions.stylePreset: "photorealistic"` is best-effort. Gamma's chosen theme may override to illustration. Either pre-select a photoreal theme via `get_themes` or accept the override and tell the user.
- `textMode: "preserve"` still lets Gamma insert en-dash separators (`–`) when reflowing text and may add `smartLayout` supporting boxes (extra feature tiles). Useful most of the time; if you need true literal preservation, expect minor edits in the Gamma editor.

## Retrieve the export URL

`generate` returns `generationId` immediately. The interactive widget polls; the Claude session does not need to.

Call `mcp__claude_ai_Gamma__get_generation_status(generationId)` once. If `status: "pending"`, wait 60 to 120 seconds and check once more. **Do not poll in a tight loop.**

When `status: "completed"`, the response contains:
- `gammaUrl` — editor link (share with user)
- `exportUrl` — direct PPTX download (hand to [[pitch-export]])
- `credits.deducted` and `credits.remaining` — report to user

## What to return to the caller

```
gammaUrl: https://gamma.app/docs/...
exportUrl: https://assets.api.gamma.app/export/pptx/...
credits_used: <N>
credits_remaining: <N>
slides_generated: [<NN-slug>, ...]   # for Pattern B, the list of slide slugs covered
```

[[pitch-export]] runs next.

## What NOT to do

- Don't author Gamma prompts inline in this subskill. Read the `gamma_prompt` field from each per-slide `.md` written by [[pitch-slides]]. The frontmatter is the source of truth.
- Don't bake brand-voice rules ("no em dashes") into `additionalInstructions`. The source `.md` files are clean by the time this stage runs.
- Don't request more than 12 cards in Pattern A.
- Don't re-call `generate` if visuals miss. Iterate in the Gamma editor.
- Don't pass `exportAs: "pdf"` if [[pitch-export]] is next. To deliver PDF as well, export it from the Gamma editor after the user has reviewed.
