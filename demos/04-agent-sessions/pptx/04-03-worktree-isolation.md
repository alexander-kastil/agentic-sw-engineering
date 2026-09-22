---
slide: "04-03"
topic: 04-session-management
title: "Isolation, diffs, and side chats"
subtitle: "Two sessions on one working tree is a race"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/04-03-worktree-isolation.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Two halves. Left: 'Session A' and
  'Session B' in blue both pointing to one grey 'working tree' box, red #fdecec pill 'race'. Right: the
  same two sessions each pointing to its own green #e9f7ef 'worktree A' and 'worktree B', both linked to a
  white 'repository' box, green pill 'worktree checkbox'. Bottom strip: per-file diff stats '+120 / -34'
  in Consolas. Minimum 28px type.
order: 15
source: demos/04-agent-sessions/04-session-management/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided diagram contrasting a shared working tree with one
  worktree per session on the right. Use exactly the one image given for this card; do not generate or add
  any other images, icons or logos.
---

# Isolation, diffs, and side chats

## Content

- The **worktree checkbox** puts a session in its own Git worktree, on every harness
- **File-level diff stats** and a compact multi-file diff view for long runs
- `/btw` side chats share the turn's **context and prompt cache**
- **Find in Chat** (`Ctrl+F`) searches collapsed work summaries too

## Notes

Chat references hand one session's output to the next without copying text. The prompt timeline puts one dot per prompt in the gutter.
