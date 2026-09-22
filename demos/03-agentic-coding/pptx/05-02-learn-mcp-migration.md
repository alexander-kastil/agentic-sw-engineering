---
slide: "05-02"
topic: 05-upgrading
title: "Let the agent research the migration"
subtitle: "Microsoft Learn MCP for versions, APIs, and breaking changes"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/03-agentic-coding/pptx/images/05-02-learn-mcp-migration.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych,
  no collage. A pair of backend engineers at a bright shared desk, one pointing at a softly blurred
  side-by-side code comparison on a large monitor while the other scrolls documentation on a laptop,
  both engaged and smiling. Modern light-oak office with shelves of plants, subjects centred
  slightly left. Modern, light, bright and friendly: high-key natural daylight, white and light-oak
  contemporary interior, soft pastel accents in light blue, mint and lavender, green plants, 2020s
  design. Screens show only soft blurred shapes and colours, never readable UI. 16:9 landscape
  1920x1080, contemporary editorial photography. Avoid: readable text, logos, watermarks, dark or
  moody lighting, vintage or retro decor, grime, clutter.
order: 17
source: demos/03-agentic-coding/05-upgrading/readme.md
gamma_prompt: >
  Slide titled "Let the agent research the migration". Equal split: bullets on the left, the
  provided photograph of two engineers reviewing a code migration on the right. Use exactly the one
  image given for this card; do not generate or add any other images, icons or logos.
---

# Let the agent research the migration

## Content

- Ask Learn MCP for the **latest stable versions** and **breaking changes**
- Research **ChatClientAgent** before refactoring `Program.cs`
- Compare **plugins and tools** before renaming the folder
- One prompt per migration step: packages, creation, tools, auth, DI

## Notes

Grounding each step in current docs keeps the agent from migrating to a version that no longer exists.
