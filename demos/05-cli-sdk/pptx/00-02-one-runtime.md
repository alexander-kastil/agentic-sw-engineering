---
slide: "00-02"
topic: 05-cli-sdk
title: "One runtime, two surfaces"
subtitle: "The CLI in your terminal, the SDK in your code"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/00-02-one-runtime.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Left column of three entry boxes: blue #eaf2ff "Terminal" (copilot, copilot -p), amber
  #fff6e5 "GitHub Actions" (gh aw workflow), green #e9f7ef "Your application" (Copilot SDK, six stacks),
  each with a horizontal arrow into a tall purple #f3edff box "Copilot agent runtime" with a Consolas tag
  "Copilot CLI" and the lines plans, calls tools, executes. The application arrow is labelled JSON-RPC.
  From the runtime, arrows right to a grey "Model" box and a green "Tools" box (MCP servers, skills,
  custom tools).
order: 2
source: demos/05-cli-sdk/readme.md
gamma_prompt: >
  Slide titled "One runtime, two surfaces". Left: four bullets. Right, wider: the provided diagram of
  terminal, GitHub Actions and your application feeding one Copilot agent runtime. Use exactly the one
  image given for this card; do not generate or add any other images, icons or logos.
---

# One runtime, two surfaces

## Content

- The **Copilot CLI** drives the agent from an interactive shell or a headless `-p` run
- **GitHub Agentic Workflows** put a CLI-driven agent on an Actions runner
- The **SDK** embeds the same production-tested runtime in your own apps
- Every SDK talks to the CLI over **JSON-RPC** and manages that process for you

## Notes

Draw the line from the application box first: the SDK is not a second agent, it is a client of the same runtime the terminal uses.
