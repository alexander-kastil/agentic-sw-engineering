---
slide: "03-01"
topic: 03-orchestration
title: "Subagents as subject-matter experts"
subtitle: "One orchestrator, a team of focused experts"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/03-agentic-coding/pptx/images/03-01-agent-team.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image.
  Minimum 26px type. Top: white "User request" box. Below it a blue "Orchestrator" box (coordinates,
  never implements). Right of it a purple "Planner" (strategy, codebase research) with a two-way
  arrow to Orchestrator. Bottom row: amber "Coder" (backend) and green "Frontend" (UI/UX, React)
  with a dashed line between labelled parallel, and a red-outlined dashed "Playwright" box (explicit
  request only). Arrows from Orchestrator down to each; no arrow crosses a box. Grey Consolas tag
  .agent.md on each expert.
order: 9
source: demos/03-agentic-coding/03-orchestration/readme.md
gamma_prompt: >
  Slide titled "Subagents as subject-matter experts". Left column: bullets. Right column: the
  provided diagram of the orchestrator and its expert team. Use exactly the one image given for this
  card; do not generate or add any other images, icons or logos.
---

# Subagents as subject-matter experts

## Content

- A subagent works in **its own transcript**, keeping the primary context clean
- Backed by an **`.agent.md`**: focused scope, instructions, curated tools, right model
- **Orchestrator** delegates to **Planner**, then **Coder** and **Frontend** in parallel
- You add capacity by adding an expert, not by growing one prompt

## Notes

Turn on chat.customAgentInSubagent.enabled. The Orchestrator only reads files, invokes agents, and manages memory.
