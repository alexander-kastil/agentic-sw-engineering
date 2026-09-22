---
slide: "03-02"
topic: 03-mcp
title: "Build your own MCP server"
subtitle: "Python or C#, one contract, tested before any client sees it"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/03-02-own-mcp-server.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Left column: three stacked server
  cards, green #e9f7ef "qr-server: Python, FastMCP, @mcp.tool", blue #eaf2ff "qr-server-cs: C#,
  ModelContextProtocol SDK, attributes", purple #f3edff "hr-mcp-server: C#, EF Core, SQLite, 5 CRUD tools".
  Middle: a vertical transport band with two labelled lanes "stdio" and "Streamable HTTP". Right: an
  amber #fff6e5 box with #e0a534 border "MCP Inspector" followed by an arrow to a final box "Copilot".
  A small caption under the Inspector box: "debug here first". Minimum 28px type.
order: 7
source: demos/02-agentic-harness/03-mcp/02-mcp-server/readme.md
gamma_prompt: >
  Slide titled "Build your own MCP server". Left half: four bullets. Right half: the provided diagram of
  three reference servers flowing through a transport choice into MCP Inspector and then Copilot. Use
  exactly the one image given for this card; do not generate or add any other images, icons or logos.
---

# Build your own MCP server

## Content

- **Python**: FastMCP, one decorator turns a function into a tool
- **C#**: the same tool contract expressed with attributes
- **State**: `hr-mcp-server` adds dependency injection, EF Core, and five CRUD tools
- Pick **stdio** or **Streamable HTTP**, then debug in the **MCP Inspector** first

## Notes

The Inspector is the habit to sell: if the tool does not work there, no client will fix it. Point at the three servers in `src/` as the ready-made starting points.
