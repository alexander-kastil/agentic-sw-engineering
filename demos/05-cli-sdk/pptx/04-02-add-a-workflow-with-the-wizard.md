---
slide: "04-02"
topic: 01-cli/04-agentic-wf
title: "Add a workflow with the wizard"
subtitle: "gh aw add-wizard opens a pull request"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: existing
photo-link: "demos/05-cli-sdk/01-cli/04-agentic-wf/_images/add-wf.jpg"
media-file: demos/05-cli-sdk/01-cli/04-agentic-wf/_images/add-wf.jpg
visual-prompt: >
  Existing screenshot of gh aw add-wizard adding and running the demo workflow, no generation. Referenced
  at its repo path.
order: 11
source: demos/05-cli-sdk/01-cli/04-agentic-wf/readme.md
gamma_prompt: >
  Slide titled "Add a workflow with the wizard". Left: four bullets. Right, wider: the provided terminal
  screenshot at its natural aspect ratio. Use exactly the one image given for this card; do not generate
  or add any other images, icons or logos.
---

# Add a workflow with the wizard

## Content

- Install with `gh extension install github/gh-aw` after `gh auth login`
- `gh aw add-wizard githubnext/agentics/daily-repo-status` picks engine and secrets
- The workflow lands on a new branch and a pull request: start from a clean repo
- `gh aw run` triggers it now; run `gh aw upgrade` after every extension upgrade

## Notes

The output of the demo run is an issue in this repository. Open it live so the class sees what the agent wrote.
