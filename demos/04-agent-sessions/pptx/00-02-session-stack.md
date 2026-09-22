---
slide: "00-02"
topic: 04-agent-sessions
title: "The session-centric product"
subtitle: "Four topics, one stack from window to host"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/00-02-session-stack.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Four stacked horizontal layers,
  top to bottom: blue #eaf2ff 'Agents window' (companion window, harness chip, per-window overrides),
  purple #f3edff 'Session management' (layout, groups, banners, /chronicle, /troubleshoot), green #e9f7ef
  'Agent host (AHP)' (authoritative state, built on the Copilot SDK), amber #fff6e5 'Execution' split into
  two boxes 'Local machine' and 'Remote host over SSH or dev tunnel'. Right-hand pills number each layer
  with its topic. Minimum 28px type.
order: 2
source: demos/04-agent-sessions/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided diagram of the four-layer session stack on the
  right. Use exactly the one image given for this card; do not generate or add any other images, icons or
  logos.
---

# The session-centric product

## Content

- **The Agents window**: a dedicated companion window with a selectable harness
- **Agent Host Protocol**: session state lives on a long-lived host, not in the client
- **Remote sessions**: the agent runs over SSH or a dev tunnel, your editor stays local
- **Session management**: side by side, groups, background send, `/chronicle`, `/troubleshoot`

## Notes

Use this slide as the map. Every later slide zooms into one layer; subagents live in module 03 where they are used.
