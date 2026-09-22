---
slide: "03-03"
topic: 01-cli/03-business-case
title: "Reading is not sending"
subtitle: "Mail.Send is a write scope a read-only Work IQ lacks"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/03-03-reading-not-sending.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Top grey Consolas box "workiq get-schema /me/sendMail", arrow down to an amber diamond
  "Schema or access denied?", three branches down to option boxes: amber "Option A" (work-iq do_action,
  Mail.Send consent plus admin allowlist) labelled "schema, and you are admin"; green "Option B" (Send-
  MgUserMail, Graph PowerShell SDK, its own consent) labelled "access denied"; blue "Option C" (Power
  Automate flow, the CLI calls its URL with curl) labelled "no admin, no workstation".
order: 8
source: demos/05-cli-sdk/01-cli/03-business-case/readme.md
gamma_prompt: >
  Slide titled "Reading is not sending". Left: four bullets. Right, wider: the provided decision diagram
  with three send options. Use exactly the one image given for this card; do not generate or add any other
  images, icons or logos.
---

# Reading is not sending

## Content

- Check first: `workiq get-schema --path /me/sendMail --method post`
- **Option A**: Work IQ sends, after `Mail.Send` consent and a tenant admin allowlist
- **Option B**: `Send-MgUserMail` from the Graph PowerShell SDK, with its own consent
- **Option C**: a Power Automate flow the CLI calls with `curl`

## Notes

Without one of these in place, asking the CLI to send produces a confident-sounding failure: the model has no tool that can send.
