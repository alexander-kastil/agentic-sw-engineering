---
slide: "04-01"
topic: 01-cli/04-agentic-wf
title: "GitHub Agentic Workflows"
subtitle: "A prompt compiled into an Actions workflow"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/04-01-agentic-workflow.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Top row: blue "workflow.md" (frontmatter + prompt) arrow to grey "gh aw compile" arrow to
  blue ".lock.yml" (the Actions workflow); a path over the top from compile to a dashed "actions-
  lock.json" (SHA pins) with a dashed arrow back into .lock.yml. A diagonal from .lock.yml to the run row:
  grey "activation" (schedule or manual dispatch), purple "agent" (read-only token), grey "safeoutputs"
  (requests create_issue), amber "detection" (sanitize and validate), green "safe_outputs" (write token,
  creates the issue). Green "github · chrome-devtools" MCP servers box feeds the agent from below; "GitHub
  Issue" below safe_outputs.
order: 10
source: demos/05-cli-sdk/01-cli/04-agentic-wf/readme.md
gamma_prompt: >
  Slide titled "GitHub Agentic Workflows". Left: four bullets. Right, wider: the provided compile and run
  pipeline diagram. Use exactly the one image given for this card; do not generate or add any other
  images, icons or logos.
---

# GitHub Agentic Workflows

## Content

- A Markdown file: **frontmatter** for trigger, engine, tools and permissions, the prompt below
- `gh aw compile` writes the executable **`.lock.yml`** and pins actions in `actions-lock.json`
- The agent runs with a **read-only token** and requests writes through `safe-outputs`
- A separate detection job validates the request before a write job creates the issue

## Notes

The split is the security story: a prompt injected through a page the agent visits cannot escalate into a write.
