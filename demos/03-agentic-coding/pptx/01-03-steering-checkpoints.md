---
slide: "01-03"
topic: 01-local-agents
title: "Steering, queueing, and checkpoints"
subtitle: "A long run is a conversation, not a submission"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/03-agentic-coding/pptx/images/01-03-steering-checkpoints.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych,
  no collage. A software engineer at a height-adjustable standing desk leans in and types a quick
  correction into a chat panel on a large monitor while an agent run progresses on screen, a relaxed
  confident expression, coffee cup beside the keyboard, a colleague glancing over with a smile.
  Bright Scandinavian-style office, subject slightly right. Modern, light, bright and friendly:
  high-key natural daylight, white and light-oak contemporary interior, soft pastel accents in light
  blue, mint and lavender, green plants, 2020s design. Screens show only soft blurred shapes and
  colours, never readable UI. 16:9 landscape 1920x1080, contemporary editorial photography. Avoid:
  readable text, logos, watermarks, dark or moody lighting, vintage or retro decor, grime, clutter.
order: 5
source: demos/03-agentic-coding/01-local-agents/readme.md
gamma_prompt: >
  Slide titled "Steering, queueing, and checkpoints". Equal split: bullets on the left, the provided
  photograph of a developer steering a running agent on the right. Use exactly the one image given
  for this card; do not generate or add any other images, icons or logos.
---

# Steering, queueing, and checkpoints

## Content

- **Steering** injects a correction into the request in flight
- **Queueing** waits for it to finish, then runs next (`chat.requestQueuing.defaultAction`)
- A `!` prefix skips the model and runs a terminal command
- **Checkpoints** roll back workspace files and chat history together; stopping does not undo

## Notes

A run that went sideways costs you the run, not the afternoon. Demo: steer mid-run, queue a follow-up, restore a checkpoint.
