---
slide: "03-01"
topic: 01-cli/03-business-case
title: "HR document updates, automated"
subtitle: "A SharePoint library with a Needs Update flag"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: existing
photo-link: "demos/05-cli-sdk/01-cli/03-business-case/_images/sharepoint-list.jpg"
media-file: demos/05-cli-sdk/01-cli/03-business-case/_images/sharepoint-list.jpg
visual-prompt: >
  Existing screenshot of the SharePoint HR-Documents library with the Needs Update column, no generation.
  Referenced at its repo path.
order: 6
source: demos/05-cli-sdk/01-cli/03-business-case/readme.md
gamma_prompt: >
  Slide titled "HR document updates, automated". Left: four bullets. Right, wider: the provided SharePoint
  library screenshot at its natural aspect ratio. Use exactly the one image given for this card; do not
  generate or add any other images, icons or logos.
---

# HR document updates, automated

## Content

- The HR-Documents library flags stale policies in a **Needs Update** column
- Manual checks are slow; update notifications are delayed or missed
- Copilot CLI queries the library through the **Work IQ MCP server**, as the signed-in user
- It collects name, modified date and modified by, then mails a summary to HR leadership

## Notes

A real business case, not a toy: seven policy documents, one boolean column, and a leadership team that wants one mail.
