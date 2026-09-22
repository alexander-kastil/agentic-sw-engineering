---
slide: "02-01"
topic: 02-prompts
title: "Prompt files: workflows on demand"
subtitle: "A request you package once and fire with a slash"
layout: content
visual-weight: 1/3
visual-type: photo
media-source: nano-banana
media-file: demos/02-agentic-harness/pptx/images/02-01-prompt-files.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych,
  no collage. A smiling developer at a white standing desk in a sunlit co-working loft, typing on a
  keyboard in front of a large monitor with a blurred chat panel, a ceramic mug and an open notebook
  beside the keyboard. Subject on the right half, airy blurred workspace on the left. Modern, light,
  bright and friendly: high-key natural daylight, white and light-oak contemporary interior, soft
  pastel accents in light blue, mint and lavender, green plants, 2020s design. Screens show only soft
  blurred shapes and colours, never readable UI. 16:9 landscape 1920x1080, contemporary editorial
  photography. Avoid: readable text, logos, watermarks, dark or moody lighting, vintage or retro
  decor, grime, clutter.
order: 5
source: demos/02-agentic-harness/02-prompts/readme.md
gamma_prompt: >
  Slide titled "Prompt files: workflows on demand". Four bullets on the left two thirds, the provided
  photograph of a developer at a standing desk in a sunlit loft on the right third. Clean light layout. Use exactly
  the one image given for this card; do not generate or add any other images, icons or logos.
---

# Prompt files: workflows on demand

## Content

- **`.prompt.md`** files in `.github/prompts/`, run by typing `/name` in chat
- Frontmatter can pin an agent, tools, and a model
- All documentation in this class repo was produced with `/describe-module`
- VS Code 1.129 **migrates prompt files to skills** (`chat.customizations.promptMigration.enabled`)

## Notes

Migrate the ones CI agents also need; keep editor-only ones as prompt files.
