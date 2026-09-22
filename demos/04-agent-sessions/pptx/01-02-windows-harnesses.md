---
slide: "01-02"
topic: 01-agents-window
title: "How one window differs from the next"
subtitle: "Each window carries its own context and target"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/01-02-windows-harnesses.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Left: grey box 'VS Code editor'.
  Two arrows right to two blue #eaf2ff window boxes stacked vertically: 'Agents window A' with a white tag
  'project X, local host, model A', and 'Agents window B' with a white tag 'project Y, remote host, model
  B'. Each window has an arrow right to its own green #e9f7ef harness box. Below, a purple #f3edff pill
  'composer chips: workspace, harness, model'. No arrow crosses a box.
order: 5
source: demos/04-agent-sessions/01-agents-window/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided diagram of two independent Agents windows, each
  with its own harness, on the right. Use exactly the one image given for this card; do not generate or
  add any other images, icons or logos.
---

# How one window differs from the next

## Content

- **New** or `Ctrl+N` opens the composer with three chips: **workspace, harness, model**
- A window overriding model and host changes **no other window**
- Several projects run **at the same time** without interfering
- `Ctrl+R` walks the Sessions picker, `Ctrl+Shift+T` reopens the last closed chat

## Notes

Demo: two sessions, two folders, two models, both running at once. Then switch the harness chip to Claude or Codex and show the window drives them the same way.
