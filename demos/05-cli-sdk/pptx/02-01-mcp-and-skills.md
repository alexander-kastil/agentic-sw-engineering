---
slide: "02-01"
topic: 01-cli/02-mcp-skills
title: "MCP servers and skills in the CLI"
subtitle: "Skills are shared by both hosts, MCP registries are not"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/02-01-mcp-and-skills.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Left column of three Consolas file boxes: blue ".vscode/mcp.json" (MCP servers, key:
  servers), green ".github/skills/" (skills, shared by both hosts), purple "~/.copilot/mcp-config.json"
  (written by copilot mcp add). Right: blue host box "VS Code" and purple host box "Copilot CLI" (/mcp,
  /skills, /env). Arrows: mcp.json to VS Code, skills to both hosts, mcp-config.json to the CLI; no
  crossings. Footer: An Agent Plugin carries skills/ and mcp.json to both hosts.
order: 5
source: demos/05-cli-sdk/01-cli/02-mcp-skills/readme.md
gamma_prompt: >
  Slide titled "MCP servers and skills in the CLI". Left: four bullets. Right, wider: the provided diagram
  of which host reads which file. Use exactly the one image given for this card; do not generate or add
  any other images, icons or logos.
---

# MCP servers and skills in the CLI

## Content

- `/mcp` in the shell, or `copilot mcp add`, `list`, `get`, `remove` from your normal shell
- The CLI reads **`~/.copilot/mcp-config.json`**, VS Code reads **`.vscode/mcp.json`**
- `/skills` or `copilot skill list`: discovered from `.github/skills/` in the working directory
- `/env` shows what actually reached the session; a plugin bundles servers and skills for both hosts

## Notes

Run copilot skill list from the solution folder and then from your home directory: discovery is scoped to where you launch.
