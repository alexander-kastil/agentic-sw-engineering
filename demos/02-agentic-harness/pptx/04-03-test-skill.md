---
slide: "04-03"
topic: 04-skills
title: "Test the trigger, then the output"
subtitle: "Two failure modes, two tests, in that order"
layout: content
visual-weight: 1/3
visual-type: photo
media-source: nano-banana
media-file: demos/02-agentic-harness/pptx/images/04-03-test-skill.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych,
  no collage. Two engineers side by side at a light desk in a glass-walled meeting room, reviewing a
  large monitor with softly blurred green and a few red result bars; one gives a relaxed thumbs up,
  the other takes notes on a tablet. Subject on the right half. Modern, light, bright and friendly:
  high-key natural daylight, white and light-oak contemporary interior, soft pastel accents in light
  blue, mint and lavender, green plants, 2020s design. Screens show only soft blurred shapes and
  colours, never readable UI. 16:9 landscape 1920x1080, contemporary editorial photography. Avoid:
  readable text, logos, watermarks, dark or moody lighting, vintage or retro decor, grime, clutter.
order: 11
source: demos/02-agentic-harness/04-skills/readme.md
gamma_prompt: >
  Slide titled "Test the trigger, then the output". Four bullets on the left two thirds, the provided
  photograph of two engineers reviewing test results on the right third. Use exactly the one image given
  for this card; do not generate or add any other images, icons or logos.
---

# Test the trigger, then the output

## Content

- **Trigger**: about 20 prompts, half should load, half are **near-misses** that must not
- Run each prompt three times; a positive passes above a 0.5 trigger rate
- Tune the description on 60 percent, pick the best score on the other 40
- **Output**: run each eval with and without the skill and read the **delta**

## Notes

"Generate a barcode for SKU 44812" is the query that proves a QR description is precise, not just broad.
