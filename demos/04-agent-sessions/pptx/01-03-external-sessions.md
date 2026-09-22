---
slide: "01-03"
topic: 01-agents-window
title: "Sessions started somewhere else"
subtitle: "Continue CLI and app sessions in VS Code"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/01-03-external-sessions.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Left column: purple #f3edff source
  boxes 'Copilot CLI', 'GitHub Copilot app', 'Claude session'. Arrows converge into a central blue #eaf2ff
  'Sessions list' box with a white Consolas tag 'chat.agentSessions.showExternal' and a grey note 'submenu
  filters external sessions'. Arrow right to a green #e9f7ef box 'Continue in VS Code' with secondary text
  'your own Copilot subscription'. Minimum 28px type.
order: 6
source: demos/04-agent-sessions/01-agents-window/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided diagram of external sessions flowing into the
  Sessions list and continuing in VS Code on the right. Use exactly the one image given for this card; do
  not generate or add any other images, icons or logos.
---

# Sessions started somewhere else

## Content

- `chat.agentSessions.showExternal` shows **Copilot or Claude sessions** from other applications
- Sources include the **Copilot CLI** and the standalone **GitHub Copilot app**
- Select one to see its conversation and **continue it** against your own subscription
- The Sessions list submenu **filters** what appears on a busy machine

## Notes

Start a session in the CLI, then find it in the Sessions list and continue it here.
