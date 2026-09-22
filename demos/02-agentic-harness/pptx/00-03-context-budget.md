---
slide: "00-03"
topic: 02-agentic-harness
title: "Context is the budget"
subtitle: "Every layer loads on a different trigger"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/00-03-context-budget.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, font Segoe UI, same visual
  language as assets/agentic-harness-architecture.svg: rounded rectangles, 2px #8c959f borders, text
  #57606a, pastel fills. No heading inside the image. Draw one wide horizontal bar across the top labelled
  "Context window" as a thin grey outline. Below it, four horizontal lanes, each a rounded band with the
  trigger on the left and the items it loads on the right: lane 1 blue #eaf2ff "Always on" with chips
  "copilot-instructions.md ~1-2 KB" and "AGENTS.md"; lane 2 green #e9f7ef "By file glob (applyTo)" with
  chips "angular.instructions.md" and "dotnet.instructions.md" (0.5-2 KB each); lane 3 purple #f3edff
  "By description match" with chips "skill metadata ~100 tokens each" and "SKILL.md body < 5000 tokens";
  lane 4 amber #fff6e5 with #e0a534 border "By explicit choice" with chips "/prompt file", "custom agent",
  "selected MCP tools". Thin arrows from each lane up into the context bar, arrow thickness proportional
  to typical size. Minimum 28px type so it reads on a projector.
order: 3
source: demos/02-agentic-harness/01-instructions/readme.md
gamma_prompt: >
  Slide titled "Context is the budget", subtitle "Every layer loads on a different trigger". Left half:
  four short bullets. Right half: the provided lane diagram showing four loading triggers feeding one
  context window. White background, calm pastel accents. Use exactly the one image given for this card;
  do not generate or add any other images, icons or logos.
---

# Context is the budget

## Content

- **Always on**: repository-wide instructions and AGENTS.md, reloaded on every turn
- **By file glob**: stack instructions activate only for matching files
- **By description**: skills cost about 100 tokens each until a request matches
- **By explicit choice**: prompt files, custom agents, selected MCP tools

## Notes

Frame the whole module as budgeting: every sentence in an always-on file is paid on every request. Ask the room which lane their current rules live in.
