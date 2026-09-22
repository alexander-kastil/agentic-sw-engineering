---
slide: "03-01"
topic: 03-remote-sessions
title: "Remote agent sessions"
subtitle: "SSH and dev tunnels to a reproducible host"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/03-01-remote-transports.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Left: blue #eaf2ff box 'Local VS
  Code', secondary 'control surface', with a Consolas tag '~/.ssh/config'. Two parallel arrows right, each
  through a pill between the boxes: purple #f3edff 'SSH' with note 'a host you already reach', amber
  #fff6e5 'Dev tunnel' with note 'behind NAT, no inbound ports'. Both end at a green #e9f7ef box 'Remote
  host', secondary 'agent runs here', with an arrow down to a white box 'Consistent toolchain and
  workspace'. Minimum 28px type.
order: 10
source: demos/04-agent-sessions/03-remote-sessions/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided diagram of local VS Code reaching a remote host
  over SSH or a dev tunnel on the right. Use exactly the one image given for this card; do not generate or
  add any other images, icons or logos.
---

# Remote agent sessions

## Content

- The agent executes on a **consistent, cloud-backed** host, not your laptop
- **SSH**: a host you already reach, whose runtimes and credentials the agent inherits
- **Dev tunnel**: hosts behind NAT or a firewall, **no inbound ports**
- Replaces the **Codespaces and Dev Container** workflow in this course

## Notes

Editor stays local, the agent and its file system live remote. The environment is defined once and reused.
