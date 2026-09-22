---
slide: "02-01"
topic: 02-host-protocol
title: "AHP vs ACP at a glance"
subtitle: "Where session state lives decides what survives"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/02-01-ahp-vs-acp.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Two side-by-side panels. Left
  panel, red #c24141 accents, 'Agent Client Protocol (ACP)': the client box holds the state; a dashed red
  disconnect with a red cross and a #fdecec pill 'running work at risk'. Right panel, green #e9f7ef,
  'Agent Host Protocol (AHP)': a host box holds the state with two client view boxes below, pill 'session
  survives'. Under each panel three comparison rows: state, lifetime, viewers. Minimum 28px type.
order: 7
source: demos/04-agent-sessions/02-host-protocol/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided side-by-side diagram contrasting ACP and AHP on the
  right. Use exactly the one image given for this card; do not generate or add any other images, icons or
  logos.
---

# AHP vs ACP at a glance

## Content

- **ACP**: authoritative state lives with the client; closing it risks the running work
- **AHP**: authoritative state lives on a **long-lived host** that outlives clients
- Under AHP the client is **a view**, and one session can have **several viewers**
- An **architect-track** topic: the boundary between where state lives and where you view it

## Notes

This is a concept slide, not a button tour. Internalize the contrast before the demo proves it.
