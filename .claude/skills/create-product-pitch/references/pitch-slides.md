---
name: pitch-slides
description: Subskill of /create-product-pitch. Writes ONE frontmatter `.md` file per slide as the canonical source of truth for that slide. Each `.md` contains the title, subtitle, layout hints, visual-prompt, gamma_prompt, content bullets, and speaker notes. PNG images are generated FROM these `.md` files later. Use as Stage 3 of the pitch pipeline. Triggers on "draft slide frontmatter", "write per-slide md", "convert outline to slides", or when invoked by [[create-product-pitch]].
metadata:
  version: 2.0.0
---

# Pitch Slides (Subskill)

Stage 3 of [[create-product-pitch]]. Write **one frontmatter `.md` file per slide** into the slides folder (typically `<product>/assets/slides/` or `<product>/slides/`). Each `.md` is the canonical source for one slide. PNG images are generated later FROM these files; the `.md` is NOT a downstream artifact.

## File naming convention

`<NN>-<slug>.md` and `<NN>-<slug>.png` (matching pair, sortable). Example:

```
01-titel-mini-ai-server.md
01-titel-mini-ai-server.png
02-problem-cloud-ki.md
02-problem-cloud-ki.png
...
```

The `NN` prefix is the order within the topic, two digits. The slug is kebab-case German or English. The `.md` is written by this subskill; the `.png` is written by [[pitch-export]].

## Frontmatter schema (mandatory)

```yaml
---
slide: "<TT-NN>"          # topic-slide, e.g. "01-04"
topic: <topic-slug>       # e.g. 01-mini-ai-server
title: "<H1 of the slide>"
subtitle: "<short subline>"
layout: <title-only | content | mixed | diagram>
visual-weight: <bg | 1/2 | 1/3 | grid | accent>
visual-type: <photo | illustration | icon | code | mermaid>
visual-prompt: >
  Multi-line concrete image direction. Photographic style, lighting, composition,
  recurring motif anchor, "no people" if applicable, "no readable text", "no logos".
order: <N>
source: <path or URL to the source content for this slide>
gamma_prompt: >
  The literal instruction block to send as Gamma's `additionalInstructions` for this
  slide. Includes layout hint, body content recap, and image direction (echoes visual-prompt).
---
```

## Body schema (mandatory)

```markdown
# <H1, mirrors frontmatter.title>

## Content

- 3 to 5 short bullets, no em dashes
- Each bullet ≤ 15 words

## Notes

Speaker notes. Pull quotes, tier recommendations, delivery timing, audience-specific
detail. 2 to 4 sentences typical.
```

## Use the template

Reference structure: `d:/git-customers/claude-code-masterclass/demos/01-fundamentals/pptx/01-01-get-started-intro.md`. This skill's `create-product-pitch/templates/slides-skeleton.md` mirrors the same shape.

## Slide-count guidance

Default 7 cards mapped from the outline:

| # | Card | Source section |
|---|---|---|
| 01 | Title | Outline §1 |
| 02 | Problem | Outline §2 |
| 03 | Solution overview | Outline §3 |
| 04–06 | Three component or persona spotlights | Outline §4 or §5 |
| 07 | Tiers + Next Steps | Outline §6 (+ §7 close) |

Expand to 10 to 12 cards for richer decks (e.g., individual component deep-dives + use-case spotlights + a tech-architecture slide). Cap at 12.

## Logo assets in slide direction

If [[pitch-sources]] downloaded any technology or partner logos to `assets/images/`, reference them explicitly in the relevant slide's `visual-prompt` and `gamma_prompt`:

- In `visual-prompt`: describe the composition using the real logo ("Docker whale-and-wordmark logo centered on a dark background, no other text").
- In `gamma_prompt`: add an image direction line such as `Image: use the official Docker logo at assets/images/docker.svg, no AI-generated substitute`.

This prevents Gamma from hallucinating an unofficial or stylised logo. For slides where no exact logo match exists, proceed with a descriptive `visual-prompt` as normal.

## Recurring motif technique

Pick ONE physical object that anchors the product visually. Reuse it across slides in different settings. This is what makes a deck feel like one product, not seven random images. Encode the motif in every per-slide `visual-prompt`.

## Brand-voice pre-flight

Author each `.md` without em dashes. The dedicated [[pitch-brand-voice]] subskill scrubs before Gamma is called, but cleaner authoring saves a scrub pass.

## What to write to disk

```
<product>/assets/slides/<NN>-<slug>.md   (one per slide)
```

## What to return to the caller

The list of `.md` paths in order. [[pitch-brand-voice]] runs next, then [[pitch-gamma]] reads each `.md`'s `gamma_prompt` field as the source for its generation call.

## What NOT to do

- Don't write a single combined slide-prompt file. The per-slide `.md` IS the spec.
- Don't generate images first and back-fill the `.md` later. Frontmatter first is the rule. See [[feedback-skill-frontmatter-first]] (if present in project memory).
- Don't put `gamma_prompt` in flowing prose. Structure it: layout hint, body recap, image direction.
- Don't request a specific Gamma theme inside the per-slide `gamma_prompt`. Theme selection happens once at the [[pitch-gamma]] call level.
- Don't exceed 12 cards. Cognitive load on a marketing deck collapses past that.
