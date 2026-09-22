---
slide: "08-01"
topic: 08-hooks
title: "Hooks: policy at lifecycle events"
subtitle: "Shell commands the agent cannot skip"
layout: diagram
visual-weight: strip
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/08-01-hooks-lifecycle.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. A horizontal timeline across the
  middle with seven evenly spaced rounded nodes: "Session Start", "User Prompt Submit", "Pre-Tool Use",
  "Tool runs" (grey, not a hook), "Post-Tool Use", "Subagent Start / Stop", "Stop". Hook nodes in amber
  #fff6e5 with #e0a534 border. Under "Pre-Tool Use" a red #fdecec pill with #c24141 text "exit 2 = deny".
  Under "Post-Tool Use" a green #e9f7ef pill "additionalContext back to the agent". Above the timeline a
  thin blue #eaf2ff band "hooks.json, matcher regex scopes to edit tools". Minimum 28px type.
order: 17
source: demos/02-agentic-harness/08-hooks/readme.md
gamma_prompt: >
  Slide titled "Hooks: policy at lifecycle events". The provided timeline diagram runs as a wide band
  across the middle; three short bullets sit below it. Use exactly the one image given for this card; do
  not generate or add any other images, icons or logos.
---

# Hooks: policy at lifecycle events

## Content

- Configured in **`.github/hooks/hooks.json`**, scoped with a `matcher` regex
- **`preToolUse`** exit code `2` denies the call outright
- **`postToolUse`** returns `additionalContext`: `instructions-guard.ps1` lints the instructions file and hands findings back

## Notes

The instructions guard is the example to show: the agent sees its own violation and rewrites the section on the next turn, without a human reviewing it.
