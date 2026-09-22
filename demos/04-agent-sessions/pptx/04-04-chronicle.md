---
slide: "04-04"
topic: 04-session-management
title: "Session persistence and /chronicle"
subtitle: "A searchable record of what was attempted"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/04-04-chronicle.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Left-to-right flow of four boxes:
  blue 'You ask /chronicle', purple 'Reads synced session history', amber 'Filters by date, file, or PR',
  green 'Summary with links to sessions'. Above the flow a grey band 'synced to your GitHub account:
  survives reload, follows you across machines'. Below, four white Consolas pills: 'standup', 'search',
  'tips', 'reindex'. Minimum 28px type.
order: 16
source: demos/04-agent-sessions/04-session-management/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided flow diagram of /chronicle reading synced history
  on the right. Use exactly the one image given for this card; do not generate or add any other images,
  icons or logos.
---

# Session persistence and /chronicle

## Content

- Sessions **sync to your GitHub account** and survive reload
- **Cross-machine**: start on the laptop, resume on the desktop
- `/chronicle standup` and `/chronicle search` query the record, never the workspace
- `/chronicle reindex` when a query misses: **the index goes stale, not the history**

## Notes

It is a read over the record, so it never changes code.
