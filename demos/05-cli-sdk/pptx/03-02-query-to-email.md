---
slide: "03-02"
topic: 01-cli/03-business-case
title: "From the flagged list to an email"
subtitle: "What the agent works out through Work IQ"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/03-02-query-to-email.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. Five boxes in a row with arrows: purple "Copilot CLI" (one prompt), green "Work IQ MCP"
  (Graph as the signed-in user), blue "HR-Documents" (Needs Update flagged), grey "Report" (name,
  modified, modified by), amber "Email" (to HR leadership). Dashed connectors from Work IQ and HR-
  Documents down to a dashed Consolas box "search_paths · fetch · $expand=fields". Amber pill at the
  bottom: NeedsUpdate is not indexed: the agent filters the items itself.
order: 7
source: demos/05-cli-sdk/01-cli/03-business-case/readme.md
gamma_prompt: >
  Slide titled "From the flagged list to an email". Left: four bullets. Right, wider: the provided five-
  step flow diagram. Use exactly the one image given for this card; do not generate or add any other
  images, icons or logos.
---

# From the flagged list to an email

## Content

- The agent resolves the site, lists the libraries, reads the columns, fetches items with `$expand=fields`
- `NeedsUpdate` is not indexed, so the agent filters the items itself
- Test the query before the send: **three rows out of twelve** is a correct answer
- Verify the mail in Outlook, not in the transcript

## Notes

Let the room watch the tool calls scroll past, including the wrong turn on the hyphenated site name. It recovers on its own.
