---
slide: "07-01"
topic: 07-memory
title: "Copilot Memory"
subtitle: "Repository facts Copilot learns and keeps"
layout: mixed
visual-weight: 1/2
visual-type: photo
media-source: existing
photo-link: "demos/02-agentic-harness/07-memory/_images/copilot-memory.jpg"
media-file: demos/02-agentic-harness/pptx/images/07-01-copilot-memory.jpg
visual-prompt: >
  Existing screenshot, no generation. Copy demos/02-agentic-harness/07-memory/_images/copilot-memory.jpg
  unchanged for Gamma grounding.
order: 16
source: demos/02-agentic-harness/07-memory/readme.md
gamma_prompt: >
  Slide titled "Copilot Memory". Equal split: four bullets on the left, the provided screenshot of the
  repository memory settings on the right with a thin frame. Use exactly the one image given for this
  card; do not generate or add any other images, icons or logos.
---

# Copilot Memory

## Content

- **Repository-scoped** facts Copilot deduces, such as "deployment config always from deploy.json"
- Validated against **code citations**; deleted after **28 days** unused
- Used by the coding agent, code review, and the Copilot CLI
- Off by default: `github.copilot.chat.copilotMemory.enabled`

## Notes

Memory is the layer nobody writes by hand. Show the settings page and one memory with its citation so the room sees it is grounded, not guessed.
