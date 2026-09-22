---
slide: "06-01"
topic: 01-cli/06-research
title: "/research: read-only and cited"
subtitle: "The lowest-risk agent in the course"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/06-01-research.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Three grey source pills on top (codebase, GitHub search, web) with arrows into a purple
  "Agent reads" box (every source read-only). Row: blue "You run /research" arrow to the agent box, arrow
  to grey "Cited report", arrow to amber "You verify the citations". Green pill under the agent: no edits,
  no approval prompt. Under verify: refine once, compare the second answer. Footer: /share keeps the
  report as a scoping artifact for an issue or a PR.
order: 13
source: demos/05-cli-sdk/01-cli/06-research/readme.md
gamma_prompt: >
  Slide titled "/research: read-only and cited". Left: four bullets. Right, wider: the provided research
  flow diagram. Use exactly the one image given for this card; do not generate or add any other images,
  icons or logos.
---

# /research: read-only and cited

## Content

- Reads across your codebase and GitHub sources; **never writes** to the repository
- No elevated permissions: nothing to approve, nothing to sandbox
- Every claim carries a **citation**: open two or three before you act
- Scope the question so a good answer must name concrete files

## Notes

The ideal first hands-on exercise: a complete agent session with zero chance of an unwanted edit.
