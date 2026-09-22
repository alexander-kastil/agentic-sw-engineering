---
slide: "01-02"
topic: 01-local-agents
title: "Approvals and permission levels"
subtitle: "Chosen per session, loosened deliberately"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/03-agentic-coding/pptx/images/01-02-permission-levels.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image.
  Minimum 26px type. Three stacked horizontal bars, top to bottom increasing autonomy: blue "Manual
  permissions" (default: asks for anything not auto-approved), purple "Assisted permissions"
  (experimental: an LLM judge assesses each call), amber #fff6e5 with #e0a534 "Allow all" (no
  confirmation). Below: grey code box chat.tools.terminal.autoApprove with three rows true = auto-
  approve, false = always ask, /regex/ = pattern, and a red #fdecec pill "convenience, not a
  security boundary".
order: 4
source: demos/03-agentic-coding/01-local-agents/readme.md
gamma_prompt: >
  Slide titled "Approvals and permission levels". Left column: bullets. Right column: the provided
  diagram of three permission levels and the terminal auto-approve map. Use exactly the one image
  given for this card; do not generate or add any other images, icons or logos.
---

# Approvals and permission levels

## Content

- **Manual permissions**: the default, anything not auto-approved asks
- **Assisted permissions**: an LLM judge assesses each tool call
- **Allow all**: every tool call runs without confirmation
- `chat.tools.terminal.autoApprove`: `true`, `false`, or a `/regex/`; keep delete, deploy, and push out

## Notes

Visual Studio and JetBrains expose the same prompts in their own Copilot settings. Count the harmless reads you approved, then allow those.
