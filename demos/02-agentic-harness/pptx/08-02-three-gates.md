---
slide: "08-02"
topic: 08-hooks
title: "Three gates between agent and machine"
subtitle: "Sandbox, assisted approvals, hooks"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/02-agentic-harness/pptx/images/08-02-three-gates.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych,
  no collage. A relaxed platform engineering team in a bright modern ops area: a wall of three large
  screens showing softly blurred green pipeline stages, two engineers with coffee cups chatting in
  front of it, one seated at a light desk. Wide shot, daylight from large windows. Modern, light,
  bright and friendly: high-key natural daylight, white and light-oak contemporary interior, soft
  pastel accents in light blue, mint and lavender, green plants, 2020s design. Screens show only soft
  blurred shapes and colours, never readable UI. 16:9 landscape 1920x1080, contemporary editorial
  photography. Avoid: readable text, logos, watermarks, dark or moody lighting, vintage or retro
  decor, grime, clutter.
order: 18
source: demos/02-agentic-harness/08-hooks/readme.md
gamma_prompt: >
  Slide titled "Three gates between agent and machine". Equal split: three bullets on the left, the
  provided photograph of a platform team in front of green pipeline screens on the right. Use exactly the one image given for
  this card; do not generate or add any other images, icons or logos.
---

# Three gates between agent and machine

## Content

- **Sandbox**: what the agent process can touch at all; opt-in, off by default since VS Code 1.135
- **Assisted approvals**: a model auto-approves low-risk tool calls (`chat.assistedPermissions.enabled`, 1.130)
- **Hooks**: the policy only you can express, your conventions, audit trail, and integrations

## Notes

Do not write a `preToolUse` hook for something the sandbox or assisted approvals already handle.
