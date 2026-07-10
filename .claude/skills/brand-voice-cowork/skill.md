---
name: brand-voice-cowork
description: >-
  Audit and fix Markdown files for brand-voice quality in the Cowork class (business owners,
  managers, citizen developers): em dashes, Mermaid label syntax, paragraph length, and
  topic-specific slash command tables.
  Trigger phrases: brand voice check, quality check, check writing quality, fix em dashes.
license: MIT
tools:
  - Read
  - Edit
  - Glob
  - Grep
---

# Brand Voice Quality Check (Cowork)

Enforce the writing and formatting rules documented in `references/rules.md` against one or more Markdown files in this repository. This is the Cowork-audience brand-voice skill and it stays repo-local; the audience differs from a Claude Code class, so brand voice is never installed globally. The `create-class` master skill discovers and invokes it by globbing `.claude/skills/brand-voice-*`.

## Inputs

The user will name a file, a folder, or a module (e.g. `demos/02-harness`). If no target is given, ask for one before proceeding.

## Steps

1. Read `references/rules.md` to load the current ruleset.

2. Resolve the target to a list of `readme.md` files using Glob. Skip `pptx/` subdirectories.

3. For each file, run every rule in the ruleset:
   - Read the file.
   - Check for each violation type in order: em dashes, Mermaid labels, paragraph length, slash command tables.
   - Collect all violations before editing.

4. For each file that has violations:
   - Apply all fixes in a single Edit per file where possible.
   - Report what was changed and why.

5. After all files are processed, print a one-line summary: files checked, files changed, violation types found.

## Subskills

| Trigger | Reference | Action |
|---|---|---|
| "render folder", "folder widget", "file explorer" | `references/render-folder.md` | Read the file and emit the prompt with the user's structure substituted in |
| "content strategy", "what to write", "topic clusters", "content pillars", "editorial calendar" | `references/content-strategy.md` | Read the file and apply its content-planning framework to the user's request |
| "marketing psychology", "mental models", "why people buy", "persuasion", "cognitive bias" | `references/marketing-psychology.md` | Read the file and apply the relevant mental models to the user's marketing problem |
| "social post", "LinkedIn", "Twitter thread", "content calendar", "repurpose content" | `references/social-content.md` | Read the file and apply its social-content frameworks to the user's request |

## Rule Application

Read `references/rules.md` for the precise definitions. Apply rules literally; do not invent new style preferences beyond what is documented there.

When fixing slash command tables, consult the "Topic-specific slash commands" section in `references/rules.md`. Match the module topic to its approved command set. If a module topic is not listed, keep the existing commands and flag it in the summary instead of guessing.

## Output Format

For each changed file, output:

```text
FILE: demos/02-harness/03-hooks/readme.md
  [em-dash]   line 3 fixed
  [mermaid]   line 29 \n replaced with <br/>
  [paragraph] line 84 split after sentence 4
```

End with:

```text
SUMMARY: 5 files checked, 3 changed, em-dash (7), paragraph (2), mermaid (2)
```
