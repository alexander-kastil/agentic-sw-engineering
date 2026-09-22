---
slide: "11-01"
topic: 02-sdk/01-intro
title: "The SDK: the agent inside your app"
subtitle: "Six stacks on the same runtime"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/11-01-sdk-runtime.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Large blue "Your application" box with six white stack chips (TypeScript, Python, Go, .NET,
  Java, Rust) and a Consolas bar "CopilotClient → session" with "sendAndWait() · defineTool()". Arrow
  labelled JSON-RPC to a purple "Copilot CLI" box (server mode; plans, calls tools, executes), arrow to a
  grey "Model" box. Bottom pills: green "CLI bundled: Node.js · Python · .NET", amber "copilot on PATH: Go
  · Java · Rust".
order: 15
source: demos/05-cli-sdk/02-sdk/01-intro/readme.md
gamma_prompt: >
  Slide titled "The SDK: the agent inside your app". Left: four bullets. Right, wider: the provided
  diagram of an application talking to the Copilot CLI over JSON-RPC. Use exactly the one image given for
  this card; do not generate or add any other images, icons or logos.
---

# The SDK: the agent inside your app

## Content

- One first-party package per stack: TypeScript, Python, Go, .NET, Java, Rust
- Node.js, Python and .NET **bundle the CLI**; Go, Java and Rust need `copilot` on PATH
- Create a **`CopilotClient`**, open a **session**, send with `sendAndWait()` or stream deltas
- `client.listModels()` asks the runtime which models your account may use

## Notes

You define the behaviour; Copilot handles planning, tool invocation and execution. Nothing about the agent loop is yours to write.
