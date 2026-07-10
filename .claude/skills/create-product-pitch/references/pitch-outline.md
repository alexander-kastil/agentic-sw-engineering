---
name: pitch-outline
description: Subskill of /create-product-pitch. Drafts the long marketing outline as a single coherent narrative ready to feed Gamma as `inputText` with `textMode: generate`. Follows the Problem → Solution → How-it-works → Use Cases → Investment & Next Steps rhythm. Use as Stage 2 of the pitch pipeline. Triggers on "draft pitch outline", "write marketing outline", or when invoked by [[create-product-pitch]].
metadata:
  version: 1.0.0
---

# Pitch Outline (Subskill)

Stage 2 of [[create-product-pitch]]. Write `<product>/pitch-outline-<lang>.md` — a long, coherent marketing narrative organized into 6–8 sections.

## Structure (mandatory)

Use this section rhythm. It mirrors the proven pattern from the NRE mail-automation reference deck.

1. **Titel und Versprechen** — strong tagline + one-sentence amplification + a single short emotional anchor paragraph.
2. **Das Problem** — 3–5 bullets framing the pain; end on a stakes paragraph ("Es ist ein Berufsrisiko." / "It's no longer optional.").
3. **Die Lösung** — what it is, what it includes (3 named components), how it's deployed.
4. **Wie sie mitwächst / How it grows** — optional modules with one-line each, scaling story.
5. **Anwendungsfälle (3 spotlights)** — one section per persona. 3–5 sentences each. Each ends on a single italicized money-quote that can survive as a pull-quote on a slide.
6. **Investition und Einstieg** — 3 tiers (name + price + 1-line use case) + the next concrete step (e.g., "30-Tage-Pilot vor Ort").
7. **Universal-Versprechen** — one closing paragraph that can become the deck's closing slide subline.

For 4+ personas, **spawn one Agent per persona** to draft Stage 5 sections in parallel, then merge. For 2–3 personas, draft inline.

## Use the skeleton

Start from `create-product-pitch/templates/outline-skeleton.md`. Fill, don't rewrite. The skeleton bakes in the rhythm above.

## Voice & length

- Length target: 700–1200 words total.
- Tone: trust-first, plain-spoken, no marketing fluff, no superlatives.
- Concrete numbers wherever possible (prices, %, durations).
- Per-section transitions should be implicit (use the section heading), not narrated ("Now let's talk about…").
- One italicized money-quote per use case.

## Language handling

- Default to the language of the existing reference deck.
- Filename suffix: `-de`, `-en`, `-fr`, etc.
- Whatever the language: still no em dashes (the brand-voice subskill will catch any that slip in, but cleaner to author without them).

## What to write to disk

```
<product>/pitch-outline-<lang>.md
```

## What to return to the caller

The file path. The next subskill ([[pitch-slides]]) reads it directly.

## What NOT to do

- Don't write more than 1200 words. Gamma can expand brief text; it does not compress dense text well.
- Don't include diagrams in the outline (Mermaid, ASCII). Gamma ignores them.
- Don't summarize at the end ("In conclusion…"). The Universal-Versprechen IS the summary.
- Don't include slide-specific instructions in the outline (image direction, slide counts). Those belong in [[pitch-slides]].
