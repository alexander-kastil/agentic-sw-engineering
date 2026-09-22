---
slide: "04-02"
topic: 04-session-management
title: "Groups, banners, and multi-chat"
subtitle: "Signals and responses in the same place"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/04-02-fork-turn.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Left: blue #eaf2ff box
  'Conversation turn', arrow down to purple #f3edff 'Fork', three arrows fanning down to green 'Main
  chat', green 'Peer chat' and grey dashed 'Subagent transcript' secondary 'read-only'. Right, with clear
  space: an amber #fff6e5 'Chat-input banner' box listing 'failing CI check' and 'incoming PR comment'
  with a white pill 'one-click fix'. Arrows never cross boxes. Minimum 28px type.
order: 14
source: demos/04-agent-sessions/04-session-management/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided diagram of a forked turn and a chat-input banner on
  the right. Use exactly the one image given for this card; do not generate or add any other images, icons
  or logos.
---

# Groups, banners, and multi-chat

## Content

- **Session groups** with drag and drop, like organizing files
- **Chat-input banners** surface failing CI checks and PR comments with one-click actions
- **Multi-chat** forks a turn into peer chats; Claude subagent transcripts are **read-only**
- Review threads via `addComment`, `listComments`, `resolveComments`

## Notes

Workspace-less quick chats start a session without opening a folder first.
