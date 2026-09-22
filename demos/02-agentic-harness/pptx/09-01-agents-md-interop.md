---
slide: "09-01"
topic: 09-agent-interop
title: "One repository, two harnesses"
subtitle: "AGENTS.md is the rule you write once"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/02-agentic-harness/pptx/images/09-01-agents-md-interop.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg. No heading inside the image. Two columns of paired rows, left
  header blue #eaf2ff "GitHub Copilot", right header purple #f3edff "Claude Code". Rows:
  ".github/copilot-instructions.md" and "CLAUDE.md"; ".github/instructions/*.instructions.md" and a grey
  dashed empty box "no equivalent"; ".github/agents/*.agent.md" and ".claude/agents/*.md";
  ".github/prompts/*.prompt.md" and ".claude/skills/*/SKILL.md"; ".github/hooks/hooks.json" and a grey
  dashed box "no hooks here". Centred above the column headers, a green #e9f7ef box "AGENTS.md" with
  arrows to both headers and a small caption "also read by Codex, Cursor". Minimum 26px type.
order: 19
source: demos/02-agentic-harness/09-agent-interop/readme.md
gamma_prompt: >
  Slide titled "One repository, two harnesses", subtitle "AGENTS.md is the rule you write once". Left
  half: four bullets. Right half: the provided mapping diagram between Copilot and Claude Code files with
  AGENTS.md shared above both. Use exactly the one image given for this card; do not generate or add any
  other images, icons or logos.
---

# One repository, two harnesses

## Content

- Each harness reads **different filenames for the same job**: a mapping, not a merge
- **`AGENTS.md`**: plain Markdown, always on, read by Copilot, Claude Code, Codex, Cursor
- The nearest `AGENTS.md` wins; enable with `chat.useAgentsMdFile`
- A rule in both `copilot-instructions.md` and `CLAUDE.md` is **paid twice** on every turn

## Notes

Optional topic. Mention the VS Code Session Target picker: same instructions, a different engine per session.
