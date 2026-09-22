---
slide: "06-01"
topic: 06-plugins
title: "Plugins: one bundle, a portable core"
subtitle: "Agent Plugins 1.0 is an open standard"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/06-01-plugins-bundle.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. A root box on the left "plugin
  root: demo-quality" with a small grey "plugin.json" tag. Two branches to the right. Upper branch green
  #e9f7ef group "Portable core" containing "skills/demo-readme-check/SKILL.md" and "mcp.json: topic-index",
  arrow to a box "Any compliant host". Lower branch purple #f3edff group "com.github.copilot/" containing
  "agents/demo-reviewer.agent.md", "hooks/hooks.json", "commands/", arrow to a box "Copilot harness only".
  Minimum 28px type.
order: 14
source: demos/02-agentic-harness/06-plugins/readme.md
gamma_prompt: >
  Slide titled "Plugins: one bundle, a portable core". Left half: four bullets. Right half: the provided
  diagram splitting a plugin into a portable core and a Copilot-only directory. Use exactly the one image
  given for this card; do not generate or add any other images, icons or logos.
---

# Plugins: one bundle, a portable core

## Content

- One plugin bundles **skills, MCP servers, agents, hooks, and slash commands**
- **Portable**: `skills/` and `mcp.json`, understood by any compliant host
- **Copilot only**: agents, hooks, commands under `com.github.copilot/`
- Sample `demo-quality` ships a skill, an MCP server, an agent, and a hook

## Notes

Bundle the portable parts first; treat the namespaced directory as the Copilot extension of a plugin that already stands on its own.
