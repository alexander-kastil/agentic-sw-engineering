---
slide: "04-05"
topic: 04-session-management
title: "Diagnosing a session with /troubleshoot"
subtitle: "Name the failing step, not the error text"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/04-agent-sessions/pptx/images/04-05-troubleshoot.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych, no
  collage. Two software engineers side by side at a shared white desk in a bright team area, calmly
  looking at a laptop with a softly blurred step list where one row is highlighted in soft coral; one
  explains with an open hand, the other nods and takes a note. Friendly, problem-solving mood, plants and
  daylight. Modern, light, bright and friendly: high-key natural daylight, white and light-oak
  contemporary interior, soft pastel accents in light blue, mint and lavender, green plants, 2020s design.
  Screens show only soft blurred shapes and colours, never readable UI. 16:9 landscape 1920x1080,
  contemporary editorial photography. Avoid: readable text, logos, watermarks, dark or moody lighting,
  vintage or retro decor, grime, clutter.
order: 17
source: demos/04-agent-sessions/04-session-management/readme.md
gamma_prompt: >
  Equal split: bullets on the left, the provided photograph of two engineers calmly diagnosing a session
  on a laptop on the right. Use exactly the one image given for this card; do not generate or add any
  other images, icons or logos.
---

# Diagnosing a session with /troubleshoot

## Content

- Reads the **session's own record**: prompts, tool calls, failures
- Reports **what went wrong and where**, with a likely cause and fix
- For **stalls**, **failed tool calls**, and runs that end with no visible reason
- Works in local and **Copilot CLI** sessions: the diagnosis travels with the session

## Notes

Give the agent a task certain to hit a wall, resist reading the raw logs first, then let /troubleshoot name the step.
