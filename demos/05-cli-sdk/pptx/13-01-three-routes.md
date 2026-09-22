---
slide: "13-01"
topic: 02-sdk/03-multi-agent
title: "Three ways to orchestrate specialists"
subtitle: "Who decomposes the work, and who sees what"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/13-01-three-routes.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Three tall panels. Blue "Sessions from code": coordinator.ts arrow down to Researcher,
  Builder, Reviewer in a chain; footer you decompose, one transcript each. Purple "customAgents": a dashed
  "one session" frame holding Researcher, Builder, Reviewer chips; footer you select per turn, one shared
  transcript. Amber "Fleet mode": --fleet fanning out to three sub-agent chips that converge on a green
  "merged report"; footer the model decomposes, subagents in parallel.
order: 18
source: demos/05-cli-sdk/02-sdk/03-multi-agent/readme.md
gamma_prompt: >
  Slide titled "Three ways to orchestrate specialists". Left: four bullets. Right, wider: the provided
  three-panel comparison diagram. Use exactly the one image given for this card; do not generate or add
  any other images, icons or logos.
---

# Three ways to orchestrate specialists

## Content

- **Several sessions from your code**: you decompose, each specialist fully isolated
- **`customAgents` on one session**: select a persona per turn, one shared transcript
- **Fleet mode**: the model decomposes and runs subagents in parallel
- `availableTools: ["custom:*"]` keeps each specialist to the tools you gave it

## Notes

A FAIL verdict from the reviewer is a working pipeline: it applied a rule the builder was never told about.
