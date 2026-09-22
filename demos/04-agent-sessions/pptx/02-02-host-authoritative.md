---
slide: "02-02"
topic: 02-host-protocol
title: "Host-authoritative state"
subtitle: "Built on the Copilot SDK, shared by every harness"
layout: diagram
visual-weight: 1/2
visual-type: diagram
media-source: opus-svg
media-file: demos/04-agent-sessions/pptx/images/02-02-host-authoritative.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Top: two blue #eaf2ff client boxes
  'VS Code window A' and 'VS Code window B', each secondary 'view'. Centre: a large green #e9f7ef box
  'Long-lived agent host', secondary 'authoritative state', holding three white chips 'Copilot', 'Claude',
  'Codex'. Beneath the host a purple #f3edff base bar 'Copilot SDK'. Solid arrows from host up to each
  client and dashed grey return arrows labelled 'reconnects', routed beside each other, never through
  labels. Minimum 28px type.
order: 8
source: demos/04-agent-sessions/02-host-protocol/readme.md
gamma_prompt: >
  Slide with four bullets on the left and the provided diagram of one long-lived host serving two client
  views on the right. Use exactly the one image given for this card; do not generate or add any other
  images, icons or logos.
---

# Host-authoritative state

## Content

- Every Agents window session **already runs on the host**; nothing to switch on
- Copilot, Claude, and Codex **share the same host**
- The Copilot agent is powered by the **Copilot SDK**, matching the CLI and the Copilot app
- Settings control **which harnesses and hosts** are offered, not the protocol

## Notes

The SDK is load-bearing for this whole module: it links directly to module 5. Mention chat.agentHost.claudeAgent.enabled, codexAgent.enabled, forwardSSHAgent and devContainer.enabled as the knobs.
