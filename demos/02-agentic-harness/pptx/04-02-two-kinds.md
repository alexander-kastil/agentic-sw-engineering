---
slide: "04-02"
topic: 04-skills
title: "Orchestration or deterministic"
subtitle: "Judgement from the model, or output from a script"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/04-02-two-kinds.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Two equal columns separated by a
  thin grey rule. Left column, purple #f3edff header "Orchestration: dotnet-conventions": a flow
  "Request" to "SKILL.md router" to a diamond "Which row?" branching to three small boxes
  "controllers.md", "efcore.md", "msal-auth.md", caption "model applies judgement, varies by design".
  Right column, green #e9f7ef header "Deterministic: qr-batch": a flow "Collect parameters" to
  "Run script --dry-run" to "Confirm" to "Run for real" to a code-style box "{ JSON result }", caption
  "same output every run". Minimum 28px type.
order: 10
source: demos/02-agentic-harness/04-skills/readme.md
gamma_prompt: >
  Slide titled "Orchestration or deterministic". The provided two-column comparison diagram fills the
  upper two thirds; three short bullets sit in a row beneath it. Use exactly the one image given for this
  card; do not generate or add any other images, icons or logos.
---

# Orchestration or deterministic

## Content

- **Orchestration**: `SKILL.md` holds the procedure, the model does the work
- **Deterministic**: the model collects parameters, a bundled script produces the output
- Bundle a script when output must be exact or the model cannot produce it (PNG, PPTX, QR code)

## Notes

Choosing wrongly is the most expensive mistake in skills. A QR code either scans or it does not; no prose makes a model emit a correct matrix.
