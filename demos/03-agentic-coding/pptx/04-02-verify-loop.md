---
slide: "04-02"
topic: 04-browser-tools
title: "The change-then-verify loop"
subtitle: "Tab sharing and per-site consent keep you in the loop"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/03-agentic-coding/pptx/images/04-02-verify-loop.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image.
  Minimum 26px type. Loop: blue "Agent edits web app code", amber "Requests to share a tab", amber
  "You approve site permission", green "Opens page, reads console, screenshots", diamond "Change
  correct?". No branch returns along the bottom to the edit box; Yes branch to green "Reports with
  screenshot". The two amber boxes under a bracket labelled "two gates: tab sharing, per-site
  consent".
order: 14
source: demos/03-agentic-coding/04-browser-tools/readme.md
gamma_prompt: >
  Slide titled "The change-then-verify loop". Left column: bullets. Right column: the provided loop
  diagram with the two consent gates. Use exactly the one image given for this card; do not generate
  or add any other images, icons or logos.
---

# The change-then-verify loop

## Content

- The agent **never grabs a tab**: it sends a share request, you pick the tab
- First visit to a site raises a **per-site permission** prompt
- Approving `localhost` does not grant the admin portal on another host
- Nothing is shared with the agent silently

## Notes

These two gates are what make on-by-default safe. Demo: introduce a console error, let the agent find, fix, and re-verify it.
