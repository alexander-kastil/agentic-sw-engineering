---
slide: "01-01"
topic: 01-cli/01-intro
title: "The Copilot CLI in your terminal"
subtitle: "Install, sign in, ask in plain language"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: existing
photo-link: "demos/05-cli-sdk/01-cli/01-intro/_images/copilot-cli-terminal.jpg"
media-file: demos/05-cli-sdk/01-cli/01-intro/_images/copilot-cli-terminal.jpg
visual-prompt: >
  Existing screenshot of the Copilot CLI interactive shell, no generation. Referenced at its repo path.
order: 3
source: demos/05-cli-sdk/01-cli/01-intro/readme.md
gamma_prompt: >
  Slide titled "The Copilot CLI in your terminal". Left: four bullets. Right, wider: the provided
  screenshot of the Copilot CLI shell at its natural aspect ratio. Use exactly the one image given for
  this card; do not generate or add any other images, icons or logos.
---

# The Copilot CLI in your terminal

## Content

- Install with `npm install -g @github/copilot` or `winget install GitHub.Copilot`
- Start `copilot`, then run **`/login`** once
- `@` pulls a file into context, `!` runs a shell command yourself
- `/model` picks the model; the list depends on your plan and organization policy

## Notes

There is no /explain command: ask in natural language. The same agent also runs in the VS Code integrated terminal.
