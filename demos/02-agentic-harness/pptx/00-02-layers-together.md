---
slide: "00-02"
topic: 02-agentic-harness
title: "How the customization layers work together"
subtitle: "One agent loop, fed by context sources and capabilities"
layout: diagram
visual-weight: 2/3
visual-type: photo
media-source: existing
photo-link: "assets/agentic-harness-architecture.svg"
media-file: demos/02-agentic-harness/pptx/images/00-02-layers-together.png
visual-prompt: >
  Existing architecture diagram, no generation. Export assets/agentic-harness-architecture.svg to a
  1920x1080 PNG (white background, diagram centred, no cropping) for Gamma grounding.
order: 2
source: demos/02-agentic-harness/readme.md
gamma_prompt: >
  Slide titled "How the customization layers work together". The provided architecture diagram fills the
  right two thirds at full legibility; a narrow left column holds four short bullets. White background,
  no decoration over the diagram. Use exactly the one image given for this card; do not generate or add
  any other images, icons or logos.
---

# How the customization layers work together

## Content

- **Entry points**: the developer's chat request, a `/` prompt file, or a selected custom agent
- **Agent loop**: assemble context, reason, call a tool, observe, repeat until done
- **Context sources**: instructions, AGENTS.md, skills, memory
- **Capabilities and guards**: MCP servers and apps; hooks on lifecycle events

## Notes

Walk the loop once clockwise before naming any file. Every later slide zooms into one box of this picture, so keep it on screen long enough for the room to find the boxes again.
