---
name: create-teaching
description: >-
  Enrich a module README with a use-case intro, a topic-specific slash-command table, and key
  documentation links, adapted to the module's audience (developer, low-code maker, or business
  user). Peer skill that the create-class master delegates to by name; also invocable directly.
  Trigger phrases: enrich module readme, module readme, use case intro, slash command table,
  key links, teaching content, enhance for business owner, business audience, adapt readme for
  business users, topic-specific slash commands.
license: CC-BY-NC-SA-4.0
---

# Create Teaching

Enrich one module README so it teaches its topic well. Read the target readme path from the
task (when invoked by `create-class`) or from the current request. Focus on that markdown file
and the content in its sub-folders.

The README gets three things, in this order: a use-case intro, a topic-specific slash-command
table, and key documentation links. Every pass is adapted to the module's audience.

## Process

1. Read a reference document if one is provided, for tone or style guidance.
2. Read source files in the module folder and its sub-folders to extract the key features and
   technologies the module actually teaches.
3. Determine the audience (see Audience Adaptation) from the module topic and any hint in the
   task; when unclear, default to developer.
4. Rewrite or enhance the intro with what the module does plus its use case and notable
   features (technology stack and standout details).

## Output structure

1. Description content: the use-case intro.
2. `## Helpful Claude Slash Commands`: a 2-column table (Command | Usage) listing slash commands
   relevant to this module's topic. Never include `/create-class`, `/create-teaching`, or
   `/create-lab`; these are internal authoring commands.
3. `## Key Topics covered in this module`: relevant documentation links. Keep and update
   existing links, or add the most relevant official docs if none exist.

## Audience Adaptation

Pick one audience per module and write the whole pass in its voice.

- Developer: full technical vocabulary is fine. Name the stack, APIs, SDKs, and 1-2 standout
  technical details per item. Slash-command tables lean on build, debug, and review commands.
- Low-code maker: focus on Copilot Studio, connectors, Power Platform, and configuration over
  code. Explain a technical term the first time it appears. Emphasize what the maker assembles
  and ships without writing code.
- Business user: use plain business language and emphasize outcomes. Avoid jargon such as
  "workspace", "context window", "model", or "prompt engineering". Frame each capability as an
  outcome a business owner would react to with "wait, it can DO that?", and point at the real
  deliverable it produces (an Excel workbook, a PDF one-pager, a slide deck, a Teams message).

When the audience is business user, describe what the person sees and gets, never the mechanism.
Write "Claude builds you a presentation", not the name of the MCP tool that produced it. A
capability earns its place only when it produces a tangible deliverable or saves hours of manual
work.

## Rules

- The slash-command table must be topic-specific to this module. Never repeat a generic set of
  slash commands across modules; each table reflects the technologies and tasks of its own topic.
- For each item, describe its use case, its stack, and 1-2 standout details at the audience's
  level.
- Separate multiple items with a paragraph.
- Reference files and scripts by name with links where possible. Use repo-absolute paths
  (starting with `/`) for assets outside the module's folder, and relative paths for assets
  within it.
- Validate image links, fix broken ones, add descriptive captions, and place images in the text
  flow where they fit.
- Include code snippets only when relevant, and update outdated ones inside fenced code blocks.
- Put prompts in fenced code blocks.
- No bold or italic in descriptions.
- No em dashes in prose; use `,` `;` `:` or `()`.
- Max 3 sentences per paragraph.
- Always use Markdown tables. Never use HTML tables (`<table>`, `<colgroup>`, `<tr>`, and similar).
- Code fences must declare a language.
- After writing, invoke the repo-local brand-voice skill (Glob `.claude/skills/brand-voice-*`)
  to verify.
