---
slide: "12-01"
topic: 02-sdk/02-custom-tools
title: "Custom tools the agent decides to call"
subtitle: "A weather assistant and a code reviewer in TypeScript"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/05-cli-sdk/pptx/images/12-01-custom-tools.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych, no
  collage. A software developer at a sit-stand desk building an app with two monitors: the left monitor
  shows a heavily blurred code editor of soft coloured lines, the right monitor shows a heavily out-of-
  focus weather app made only of soft sun and cloud shapes and pastel colour tiles, no digits and no
  words; the developer smiles while typing, headphones around the neck. Bright loft-style workspace,
  subject slightly right of centre, shallow depth of field so the screens are soft. Modern, light, bright
  and friendly: high-key natural daylight, white and light-oak contemporary interior, soft pastel accents
  in light blue, mint and lavender, green plants, 2020s design. Screens show only soft blurred shapes and
  colours, never readable UI. 16:9 landscape, contemporary editorial photography. Avoid: readable text,
  logos, watermarks, dark or moody lighting, vintage or retro decor, grime, clutter. Also avoid numbers,
  degree signs and words on screens.
order: 16
source: demos/05-cli-sdk/02-sdk/02-custom-tools/readme.md
gamma_prompt: >
  Slide titled "Custom tools the agent decides to call". Four bullets on the left, the provided photograph
  of a developer building a weather assistant as a side accent on the right. Use exactly the one image
  given for this card; do not generate or add any other images, icons or logos.
---

# Custom tools the agent decides to call

## Content

- `defineTool()` takes a name, a description, a parameter schema and a handler
- Copilot decides **when** to call the tool from the user's prompt
- Stream with `assistant.message_delta` and read `event.data.deltaContent`
- The temperatures come from **your handler**, not from the model

## Notes

Run npx tsc --noEmit whenever a handler behaves oddly: tsx executes TypeScript without typechecking it.
