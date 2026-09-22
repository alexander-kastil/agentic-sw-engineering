---
slide: "02-02"
topic: 02-cloud
title: "What the cloud agent cannot see"
subtitle: "The repository has to carry the context"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/03-agentic-coding/pptx/images/02-02-cloud-cannot-see.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image.
  Minimum 26px type. Two columns. Left blue #eaf2ff panel "Your IDE" with rows: terminal output,
  Problems diagnostics, extension tools, local credentials. Right purple #f3edff panel "Cloud
  session" with rows: tools, MCP servers and models of the cloud service. Between them each left row
  ends in a short red #c24141 dashed stub with a red cross. Below both, a green #e9f7ef wide box
  with Consolas .github/copilot-instructions.md and text "build, test, conventions" with a solid
  arrow up into the cloud panel.
order: 7
source: demos/03-agentic-coding/02-cloud/readme.md
gamma_prompt: >
  Slide titled "What the cloud agent cannot see". Left column: bullets. Right column: the provided
  diagram of local context that never reaches the cloud session. Use exactly the one image given for
  this card; do not generate or add any other images, icons or logos.
---

# What the cloud agent cannot see

## Content

- Cloud sessions use the **cloud service's** tools, MCP servers, and models
- No terminal output, no Problems panel, no extension tools, **no local credentials**
- **`.github/copilot-instructions.md`** carries build, test, and conventions
- Most disappointing cloud runs trace back to missing context

## Notes

Compare the same task locally and in the cloud and note which context the agent had to be told.
