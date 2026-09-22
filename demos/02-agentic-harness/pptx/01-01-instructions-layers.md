---
slide: "01-01"
topic: 01-instructions
title: "Instructions: always on, or scoped by file"
subtitle: "General rules plus stack rules that swap in and out"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/01-01-instructions-layers.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg (rounded rectangles, #8c959f borders, #57606a text, pastel
  fills). No heading inside the image. Two side-by-side columns, each a vertical stack of three layers.
  Left column captioned "Editing app.component.ts": top layer blue #eaf2ff "General instructions ~1 KB",
  middle layer green #e9f7ef "Angular instructions ~1.5 KB", bottom layer grey #f6f8fa "Current file
  ~2-5 KB". Right column captioned "Editing Service.cs": same top layer, middle layer purple #f3edff
  ".NET instructions ~1 KB", bottom layer grey "Current file ~3-6 KB". A curved amber #e0a534 arrow from
  the Angular layer to the .NET layer labelled "swap, not accumulate". Small file-path tags beside the
  layers: ".github/copilot-instructions.md" and ".github/instructions/*.instructions.md (applyTo)".
  Minimum 28px type.
order: 4
source: demos/02-agentic-harness/01-instructions/readme.md
gamma_prompt: >
  Slide titled "Instructions: always on, or scoped by file". Left half: four short bullets. Right half:
  the provided diagram of two instruction stacks where the Angular layer swaps for a .NET layer. White
  background. Use exactly the one image given for this card; do not generate or add any other images,
  icons or logos.
---

# Instructions: always on, or scoped by file

## Content

- **`.github/copilot-instructions.md`**: security, naming, coding philosophy, loaded every turn
- **`.github/instructions/*.instructions.md`**: one file per stack, activated by an `applyTo` glob
- Opening a .NET file swaps the Angular rules out instead of stacking both
- Enable with `chat.instructionsFilesLocations`

## Notes

Show the two stacks and ask what happens to the Angular rules when you open a C# file. The answer, they leave, is the whole point of scoping.
