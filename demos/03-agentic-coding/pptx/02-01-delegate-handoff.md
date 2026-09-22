---
slide: "02-01"
topic: 02-cloud
title: "Handing off to a cloud agent"
subtitle: "/delegate carries the conversation to the cloud"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/03-agentic-coding/pptx/images/02-01-delegate-handoff.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image.
  Minimum 26px type. Left to right flow of five boxes: blue "Local session with context", arrow
  labelled with Consolas /delegate to purple "Cloud agent, ephemeral environment", green "Commits to
  a branch", green "Pull request with session log", blue "You review locally". A dashed return arrow
  along the bottom from review back to the cloud agent labelled "iterate with a PR comment". Amber
  pill under the cloud box: "59 minute execution limit".
order: 6
source: demos/03-agentic-coding/02-cloud/readme.md
gamma_prompt: >
  Slide titled "Handing off to a cloud agent". Left column: bullets. Right column: the provided
  handoff flow diagram. Use exactly the one image given for this card; do not generate or add any
  other images, icons or logos.
---

# Handing off to a cloud agent

## Content

- Type **`/delegate`** in a running session, or pick **Cloud** as the session target
- History and context travel with the task
- The agent works on **its own branch**, commits, and opens a **pull request**
- Iterate with a PR comment instead of starting over

## Notes

The local session stays the hub. The coding agent runs on GitHub Actions, one repo and one branch per session, with a hard 59 minute limit.
