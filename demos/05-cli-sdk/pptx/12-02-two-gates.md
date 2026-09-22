---
slide: "12-02"
topic: 02-sdk/02-custom-tools
title: "Visible, then permitted"
subtitle: "Two gates stand in front of every tool call"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/12-02-two-gates.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Row: grey "Model wants a tool" arrow to a blue diamond "Visible?" (availableTools), yes arrow
  to a purple diamond "Permitted?" (skipPermission), yes arrow to green "Your handler runs". No branches
  down: from Visible to a dashed "Never offered" box, from Permitted with a red arrow to a red #fdecec
  "Call denied" box. Captions above the diamonds: builtin:* mcp:* custom:* and or onPermissionRequest.
order: 17
source: demos/05-cli-sdk/02-sdk/02-custom-tools/readme.md
gamma_prompt: >
  Slide titled "Visible, then permitted". Left: four bullets. Right, wider: the provided two-gate decision
  diagram. Use exactly the one image given for this card; do not generate or add any other images, icons
  or logos.
---

# Visible, then permitted

## Content

- `availableTools` and `excludedTools` decide which tools the model is **offered**
- Patterns are source-qualified: `builtin:*`, `mcp:*`, `custom:*`
- A session with no `onPermissionRequest` handler **denies** the call
- `skipPermission: true` for handlers that only compute; decide per call otherwise

## Notes

A tool can be permitted and invisible, or visible and denied, and the two failures look nothing alike from the transcript.
