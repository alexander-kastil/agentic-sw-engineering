---
slide: "01-01"
topic: 01-local-agents
title: "The agent loop"
subtitle: "Reason, call a tool, observe, repeat"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/03-agentic-coding/pptx/images/01-01-agent-loop.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image.
  Minimum 26px type. Loop left to right: white "Your prompt" box, blue "Model reasons over context",
  green "Calls a tool: read, edit, run", amber diamond "Approval needed?". Yes branch down to amber-
  outlined "You confirm" box, then back to reasons along the bottom; No branch arcs back over the
  top to reasons. Arrows never cross boxes. Caption: repeat until done, blocked on you, or stopped.
order: 3
source: demos/03-agentic-coding/01-local-agents/readme.md
gamma_prompt: >
  Slide titled "The agent loop". Left column: bullets. Right column: the provided loop diagram with
  the approval gate. Use exactly the one image given for this card; do not generate or add any other
  images, icons or logos.
---

# The agent loop

## Content

- An agent turn is **not one model call**: it reasons, calls a tool, reads the result, reasons again
- Tools are the **verbs**: read a file, edit a file, run a command, call an MCP server
- Some verbs change your machine, so the loop has an **approval gate**
- The gate is the part you configure

## Notes

The gate decides whether a run is productive or a babysitting session. Set that up before the permission slide.
