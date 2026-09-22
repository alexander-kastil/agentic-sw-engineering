---
slide: "07-01"
topic: 01-cli/07-rubber-duck
title: "/rubber-duck: a second opinion"
subtitle: "A critic that argues the opposite case"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/05-cli-sdk/pptx/images/07-01-rubber-duck.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych, no
  collage. Two software engineers at a large whiteboard wall in a bright meeting room: one presents a plan
  sketched only as plain empty boxes connected by arrows, with no words or letters anywhere on the board;
  the other stands with arms folded and a friendly, sceptical smile, raising one hand to question an arrow
  before any code is written. A plain unbranded laptop closed on a light table. People on the right half,
  clean bright wall on the left. Modern, light, bright and friendly: high-key natural daylight, white and
  light-oak contemporary interior, soft pastel accents in light blue, mint and lavender, green plants,
  2020s design. Screens show only soft blurred shapes and colours, never readable UI. 16:9 landscape,
  contemporary editorial photography. Avoid: readable text, logos, watermarks, dark or moody lighting,
  vintage or retro decor, grime, clutter. Also avoid any letters, words or numbers on the whiteboard.
order: 14
source: demos/05-cli-sdk/01-cli/07-rubber-duck/readme.md
gamma_prompt: >
  Slide titled "/rubber-duck: a second opinion". Four bullets on the right, the provided photograph of a
  colleague questioning a plan at a whiteboard as a side accent on the left. Use exactly the one image
  given for this card; do not generate or add any other images, icons or logos.
---

# /rubber-duck: a second opinion

## Content

- The agent that wrote the code is the **worst reviewer** of it
- `/rubber-duck` reads what the session did and reports what was missed
- Review only: **nothing changes on disk**
- Call it after planning and before implementing, where a bad approach is cheapest to kill

## Notes

Treat the findings as candidates, not verdicts: you decide which ones earn a follow-up turn from the working agent.
