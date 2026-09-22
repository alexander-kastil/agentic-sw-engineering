---
slide: "05-01"
topic: 05-agents
title: "Custom agents and handoffs"
subtitle: "Personas with their own tools, handing over the task"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/02-agentic-harness/pptx/images/05-01-agents-handoffs.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych,
  no collage. Two developers at a shared light-oak desk; one turns a laptop toward the other to hand
  over a task, both smiling, the second reaching for the trackpad. Bright Scandinavian-style office,
  plants on the windowsill, subject centred slightly right. Modern, light, bright and friendly: high-
  key natural daylight, white and light-oak contemporary interior, soft pastel accents in light blue,
  mint and lavender, green plants, 2020s design. Screens show only soft blurred shapes and colours,
  never readable UI. 16:9 landscape 1920x1080, contemporary editorial photography. Avoid: readable
  text, logos, watermarks, dark or moody lighting, vintage or retro decor, grime, clutter.
order: 13
source: demos/02-agentic-harness/05-agents/01-agents-overview/readme.md
gamma_prompt: >
  Slide titled "Custom agents and handoffs". Equal split: four bullets on the left, the provided
  photograph of one developer handing a task to a colleague on the right. Use exactly the one image given for this card; do
  not generate or add any other images, icons or logos.
---

# Custom agents and handoffs

## Content

- **`.agent.md`** files in `.github/agents/`: persona, instructions, tool list, model
- **Handoffs** in frontmatter: `label`, `agent`, `prompt`, optional `send` and `model`
- A handoff button moves the session on: **plan, implement, review**
- This class ships planner, coder, frontend, orchestrator, GitHub Actions, Terraform, and more

## Notes

The point: the next agent starts with a pre-filled prompt, not a blank chat. Demo the Team Planner handing off to Team Coder.
