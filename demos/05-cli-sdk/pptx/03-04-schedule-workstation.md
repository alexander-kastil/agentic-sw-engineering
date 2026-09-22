---
slide: "03-04"
topic: 01-cli/03-business-case
title: "Schedule it where the tokens live"
subtitle: "A workstation task, not a hosted runner"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/05-cli-sdk/pptx/images/03-04-schedule-workstation.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych, no
  collage. A software engineer arrives at a personal workstation in the early morning, coffee cup in one
  hand, the laptop on a light-oak desk already open and showing a softly blurred table of rows that a
  scheduled job has prepared; a small desk clock and a plant beside it, a colleague in the background
  waving hello. Subject centred slightly right, calm bright window light on the left. Modern, light,
  bright and friendly: high-key natural daylight, white and light-oak contemporary interior, soft pastel
  accents in light blue, mint and lavender, green plants, 2020s design. Screens show only soft blurred
  shapes and colours, never readable UI. 16:9 landscape, contemporary editorial photography. Avoid:
  readable text, logos, watermarks, dark or moody lighting, vintage or retro decor, grime, clutter.
order: 9
source: demos/05-cli-sdk/01-cli/03-business-case/readme.md
gamma_prompt: >
  Slide titled "Schedule it where the tokens live". Four bullets on the left, the provided photograph of
  an engineer arriving at a workstation with a report already on screen as a side accent on the right. Use
  exactly the one image given for this card; do not generate or add any other images, icons or logos.
---

# Schedule it where the tokens live

## Content

- Unattended runs use `-p` with `--allow-all-tools`, never `-i`
- Task Scheduler runs `update-report.ps1` daily at 8:00
- **Run only if user is logged in**: Work IQ and Graph cache their tokens in your profile
- A GitHub Actions runner has no profile, no token cache and no registered MCP server

## Notes

Show the class the hosted-runner version that prints a plausible answer and reaches nothing. It is the most useful failure in the module.
