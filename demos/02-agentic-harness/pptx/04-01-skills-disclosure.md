---
slide: "04-01"
topic: 04-skills
title: "Skills: knowledge that loads itself"
subtitle: "Progressive disclosure in three levels"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/04-01-skills-disclosure.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. A three-step staircase rising
  left to right. Step 1 blue #eaf2ff "Metadata: name + description", budget tag "~100 tokens", trigger
  "at startup, every skill". Step 2 purple #f3edff "SKILL.md body", budget "< 500 lines / 5000 tokens",
  trigger "request matches description". Step 3 green #e9f7ef "scripts/ references/ assets/", budget
  "no fixed limit", trigger "only when the body says so". Beside step 1 a small grey folder tree:
  "dotnet-conventions/ SKILL.md references/ scripts/ evals/ assets/". Along the bottom a thin amber
  #e0a534 callout: "40 skills installed, ~4,000 tokens idle". Minimum 28px type.
order: 9
source: demos/02-agentic-harness/04-skills/readme.md
gamma_prompt: >
  Slide titled "Skills: knowledge that loads itself", subtitle "Progressive disclosure in three levels".
  Left half: four bullets. Right half: the provided staircase diagram of the three loading levels with
  their token budgets. Use exactly the one image given for this card; do not generate or add any other
  images, icons or logos.
---

# Skills: knowledge that loads itself

## Content

- A folder with **`SKILL.md`** plus optional scripts, references, and assets
- Open **Agent Skills** standard: Copilot CLI, coding agent, code review, VS Code, Claude Code
- Only name and description load at startup; the body loads on a match
- The **`description`** is the trigger: name the user's intent, not the implementation

## Notes

"Helps with .NET code" is the most common reason a skill never fires. The instructions were fine; the model never got far enough to read them.
