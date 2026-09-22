---
slide: "03-03"
topic: 03-mcp
title: "MCP Apps: UI inside the chat"
subtitle: "A tool result that renders instead of printing"
layout: mixed
visual-weight: 2/3
visual-type: photo
media-source: existing
photo-link: "demos/02-agentic-harness/03-mcp/03-mcp-apps/_images/mcp-app.jpg"
media-file: demos/02-agentic-harness/pptx/images/03-03-mcp-apps.jpg
visual-prompt: >
  Existing screenshot, no generation. Copy demos/02-agentic-harness/03-mcp/03-mcp-apps/_images/mcp-app.jpg
  unchanged for Gamma grounding.
order: 8
source: demos/02-agentic-harness/03-mcp/03-mcp-apps/readme.md
gamma_prompt: >
  Slide titled "MCP Apps: UI inside the chat". The provided screenshot of an interactive QR code rendered
  inside Copilot Chat takes the right two thirds with a thin frame; three short bullets on the left. Use
  exactly the one image given for this card; do not generate or add any other images, icons or logos.
---

# MCP Apps: UI inside the chat

## Content

- The server declares a **`ui://` resource** next to its tool
- The chat renders it as an **interactive UI**: charts, forms, QR codes
- Demo: a Python FastMCP server that draws its QR code in Copilot Chat

## Notes

Contrast with the previous slide: same protocol, but the answer is a surface you can click. Keep this short and run the live demo instead.
