---
slide: "03-01"
topic: 03-mcp
title: "MCP: tools beyond the editor"
subtitle: "Local or remote servers, and who reads which config"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/03-01-mcp-basics.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Top row: two client boxes, left
  blue #eaf2ff "VS Code" with a file tag ".vscode/mcp.json (key: servers)", right purple #f3edff
  "Copilot CLI" with a file tag "~/.copilot/mcp-config.json (copilot mcp add)". Bottom row: three server
  boxes in green #e9f7ef: "Local stdio (npx, python)", "Remote HTTP endpoint", "MCP Registry (discover)".
  Solid arrows from both clients down to the two server boxes. A grey document icon in the middle
  labelled "mcp.json in the repo" with a solid arrow to VS Code and a red #c24141 dashed arrow to the CLI
  ending in a red cross, labelled "never loaded by the CLI" on a #fdecec pill. Minimum 28px type.
order: 6
source: demos/02-agentic-harness/03-mcp/01-basics/readme.md
gamma_prompt: >
  Slide titled "MCP: tools beyond the editor". Left half: four bullets. Right half: the provided diagram
  of VS Code and Copilot CLI reading different MCP config files, with a red crossed arrow for the file
  the CLI ignores. Use exactly the one image given for this card; do not generate or add any other
  images, icons or logos.
---

# MCP: tools beyond the editor

## Content

- MCP connects Copilot to **external tools and data**: browsers, docs, business systems
- Servers run **local** (stdio executables) or **remote** (HTTP endpoints)
- VS Code reads **`.vscode/mcp.json`**, top-level key `servers`
- The CLI reads only **`~/.copilot/mcp-config.json`**, written by `copilot mcp add`

## Notes

This is the trap slide: a server checked into the repo and then demonstrated in the CLI demonstrates nothing. Say it plainly and move on.
