---
slide: "01-02"
topic: 01-cli/01-intro
title: "Three modes, three ways to run"
subtitle: "Interactive, plan and autopilot; shell, -i and -p"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/01-02-modes-and-runs.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Top row: three mode boxes, blue "Interactive" (you approve each action), purple "Plan" (a
  plan before any code), amber "Autopilot" (no pause per action), arrows left to right and a curved return
  arrow from Autopilot back to Interactive labelled "Shift+Tab cycles the modes". Bottom row: three green
  invocation boxes in Consolas: "copilot" (the interactive shell), "copilot -i" (shell with a prompt
  running), "copilot -p" (one headless run, then exit) with a red #fdecec pill "--allow-all-tools" under
  it. Footer: copilot --continue or --resume picks a session back up.
order: 4
source: demos/05-cli-sdk/01-cli/01-intro/readme.md
gamma_prompt: >
  Slide titled "Three modes, three ways to run". Left: four bullets. Right, wider: the provided diagram of
  the three modes and the three invocations. Use exactly the one image given for this card; do not
  generate or add any other images, icons or logos.
---

# Three modes, three ways to run

## Content

- **Shift+Tab** cycles interactive, plan and autopilot mode
- **Autopilot** works through multi-step tasks without pausing: trusted repositories only
- `copilot -i "<prompt>"` opens the shell with a prompt already running
- `copilot -p "<prompt>" --allow-all-tools` runs headless and exits; add `-s` for scripts

## Notes

Nobody is at the keyboard in a -p run, so nobody approves tool calls. That is why --allow-all-tools is not optional there.
