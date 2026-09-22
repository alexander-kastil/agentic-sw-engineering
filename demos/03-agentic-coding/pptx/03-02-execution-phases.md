---
slide: "03-02"
topic: 03-orchestration
title: "Parallel phases without file conflicts"
subtitle: "Different files run together, shared files wait"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/03-agentic-coding/pptx/images/03-02-execution-phases.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image.
  Minimum 26px type. Three phase columns left to right (the dark mode example), each a grey #f6f8fa
  panel with a header "Phase 1", "Phase 2", "Phase 3". Phase 1: green "Frontend: palette and toggle
  UI design" and amber "Coder: theme groundwork". Phase 2: amber "Coder: ThemeContext.tsx,
  useTheme.ts" and green "Frontend: toggle component". Phase 3: amber "Coder: apply theme tokens
  across components". Arrows between panels only. Above: blue strip "Planner returns the plan,
  Orchestrator splits it by file". Below: red #fdecec pill "same file in two agents = conflict" and
  green pill "describe the outcome, not the method".
order: 10
source: demos/03-agentic-coding/03-orchestration/readme.md
gamma_prompt: >
  Slide titled "Parallel phases without file conflicts". Left column: bullets. Right column: the
  provided diagram of three execution phases. Use exactly the one image given for this card; do not
  generate or add any other images, icons or logos.
---

# Parallel phases without file conflicts

## Content

- Orchestrator: **plan, parse phases, execute, verify**
- Tasks with **no overlapping files** run in parallel
- Tasks with **shared files** run sequentially
- Scope each agent to **distinct files**

## Notes

Walk the dark mode example: palette and toggle design, then context and toggle component, then apply tokens everywhere.
