---
slide: "03-03"
topic: 03-remote-sessions
title: "The load-bearing details"
subtitle: "Start detached, stop first, clean up in order"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/03-03-remote-lifecycle.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Left-to-right lifecycle of four
  rounded boxes joined by arrows: blue '1 Start' with Consolas note 'setsid nohup ... &', green '2 Change'
  with note 'pkill first, then restart', grey '3 Reattach' with note 'server still serving', amber '4
  Clean up' with note 'stop, then delete'. Under steps 1, 2 and 4 a red #fdecec pill with #c24141 border
  hangs from a short red line naming the failure it prevents: 'dies with the shell turn', 'Address already
  in use', 'stray server on 8000'. Minimum 26px type.
order: 12
source: demos/04-agent-sessions/03-remote-sessions/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided lifecycle diagram of start, change, reattach and
  clean up with the failure each step prevents on the right. Use exactly the one image given for this
  card; do not generate or add any other images, icons or logos.
---

# The load-bearing details

## Content

- `setsid nohup ... < /dev/null &`: a plain background start **dies with the shell turn**
- **Stop before restart**, or `Address already in use` hides in the log while old code answers
- `[p]ython3` stops `pkill` from **killing the agent's own shell**
- Clean up in order: **stop, then delete**; check that the PID and `Content-Length` changed

## Notes

A 200 alone does not prove the new code is the code being served. Repeat the whole start command so each step runs on its own.
