---
slide: "03-02"
topic: 03-remote-sessions
title: "Hello world on a Raspberry Pi"
subtitle: "Nothing installed on the laptop"
layout: content
visual-weight: 1/2
visual-type: photo
media-source: nano-banana
media-file: demos/04-agent-sessions/pptx/images/03-02-raspberry-pi.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych, no
  collage. A cheerful software engineer at a bright white desk with a laptop showing a softly blurred
  terminal and chat, and next to the laptop a small bare single-board computer with a green circuit board
  and a short network cable, a tiny status LED glowing. She points at the board while typing. Overhead
  natural light, plants, subject centred slightly right. Modern, light, bright and friendly: high-key
  natural daylight, white and light-oak contemporary interior, soft pastel accents in light blue, mint and
  lavender, green plants, 2020s design. Screens show only soft blurred shapes and colours, never readable
  UI. 16:9 landscape 1920x1080, contemporary editorial photography. Avoid: readable text, logos,
  watermarks, dark or moody lighting, vintage or retro decor, grime, clutter.
order: 11
source: demos/04-agent-sessions/03-remote-sessions/readme.md
gamma_prompt: >
  Equal split: bullets on the left, the provided photograph of an engineer driving a small single-board
  computer from a laptop on the right. Use exactly the one image given for this card; do not generate or
  add any other images, icons or logos.
---

# Hello world on a Raspberry Pi

## Content

- An entry in `~/.ssh/config` makes `raspi-4` **selectable by name**; pin the key with `IdentityFile`
- Workspace chip: **Local** to **Remote** tab, pick the host, select `/home/alex`
- First connect installs the **VS Code CLI on the Pi**; nothing else
- The agent writes, runs, and curls the service **on the Pi**; port 8000 is forwarded to you

## Notes

The laptop never runs the code. The reader reads the diff locally while the edit, restart and test happen remote.
