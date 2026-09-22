---
slide: "05-01"
topic: 05-upgrading
title: "Semantic Kernel to Agent Framework"
subtitle: "The same RAG app, migrated by an agent"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/03-agentic-coding/pptx/images/05-01-sk-to-maf.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image.
  Minimum 26px type. Mapping diagram: left column header grey pill "sk-students-ai", right column
  header green pill "maf-students-ai". Five rows, each a left grey #f6f8fa box, a short arrow, and a
  right green #e9f7ef box, Consolas text: Microsoft.SemanticKernel to Microsoft.Agents.AI;
  Kernel.CreateBuilder() to chatClient.AsAIAgent(); Plugins/ to Tools/ with
  AIFunctionFactory.Create(); API key to DefaultAzureCredential; kernel service to
  AddSingleton<AIAgent>(). Arrows within the gap only.
order: 16
source: demos/03-agentic-coding/05-upgrading/readme.md
gamma_prompt: >
  Slide titled "Semantic Kernel to Agent Framework". Left column: bullets. Right column: the
  provided before-and-after mapping diagram. Use exactly the one image given for this card; do not
  generate or add any other images, icons or logos.
---

# Semantic Kernel to Agent Framework

## Content

- **Packages**: `Microsoft.SemanticKernel` to `Microsoft.Agents.AI`
- **Creation**: kernel builder to `chatClient.AsAIAgent()`
- **Tools**: `Plugins` to `Tools` with `AIFunctionFactory.Create()`
- **Auth and DI**: `DefaultAzureCredential`, agent as a singleton

## Notes

Both versions ship side by side in the module, so the diff is the lesson.
