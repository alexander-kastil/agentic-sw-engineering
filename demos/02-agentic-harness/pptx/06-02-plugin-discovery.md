---
slide: "06-02"
topic: 06-plugins
title: "Discovered by convention, not declared"
subtitle: "The manifest names the plugin, the folders name the parts"
layout: mixed
visual-weight: 1/3
visual-type: photo
media-source: nano-banana
media-file: demos/02-agentic-harness/pptx/images/06-02-plugin-discovery.jpg
visual-prompt: >
  ONE single continuous photograph taken with one camera in one moment: no split screen, no diptych,
  no collage. Top-down flat lay on a clean white desk in morning sunlight: an open laptop with a
  blurred colourful screen, a tablet, a small stack of pastel sticky notes, a USB-C hub, wireless
  earbuds case and a small succulent, every item neatly aligned in a modular grid with even spacing.
  Modern, light, bright and friendly: high-key natural daylight, white and light-oak contemporary
  interior, soft pastel accents in light blue, mint and lavender, green plants, 2020s design. Screens
  show only soft blurred shapes and colours, never readable UI. 16:9 landscape 1920x1080, contemporary
  editorial photography. Avoid: readable text, logos, watermarks, dark or moody lighting, vintage or
  retro decor, grime, clutter.
order: 15
source: demos/02-agentic-harness/06-plugins/readme.md
gamma_prompt: >
  Slide titled "Discovered by convention, not declared". Left two thirds: three bullets and a short JSON
  code block. Right third: the provided top-down photograph of a tidy developer desk laid out in a grid. Use exactly
  the one image given for this card; do not generate or add any other images, icons or logos.
---

# Discovered by convention, not declared

## Content

- `plugin.json` requires only **`$schema`** and **`name`**; extra keys are rejected
- No `skills` or `mcpServers` key: a file in the right folder is found
- VS Code: **`chat.pluginLocations`**; CLI: **`copilot --plugin-dir <path> skill list`**

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "demo-quality"
}
```

## Notes

Mention that the CLI loads a plugin's `mcp.json` only after a real install, not from `--plugin-dir`.
