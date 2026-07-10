---
name: polish-slug
description: Polish H1 headings across the demos/ directory so every topic, demo guide, and code project readme starts with a verb, then propose a TOC for review and apply on approval.
---

# Polish Slug

Rewrites every H1 heading in `demos/` to an imperative verb phrase. Strips numbering artifacts and label prefixes, then proposes a full table of changes before touching any file. This leaf is loaded by the `create-class` master skill; it is not invoked directly. Apply it to the heading-polishing task passed to `create-class`.

## What Gets Polished

Three categories of file:

| Category | Pattern | Example path |
|----------|---------|--------------|
| Topic subfolder readmes | `demos/XX-module/YY-topic/readme.md` | `demos/05-cli/01-intro/readme.md` |
| Standalone demo guides | `demos/XX-module/NN-demo-*.md` | `demos/06-planning/01-demo-plan-mode.md` |
| Code project readmes | Non-numbered subfolder inside a topic | `demos/02-harness/04-mcp/maf-starter-solution/readme.md` |

## Naming Rules

- **Start with a strong verb**: Build, Run, Configure, Deploy, Apply, Enforce, Gate, Map, Migrate, Orchestrate, Design, Compose, Publish, Understand, Explore, Inspect, Trace, Secure, Add, Convert, Compress, Author, Decompose, Checkpoint, Persist, Delegate.
- **Strip these prefixes exactly**:
  - Numbered labels: `01:`, `02:`, `Module 13.01`, `02`, `# 04 Skills`
  - Type labels: `Demo:`, `Lab 01`, `Lab 05`, `Introduction to`, `Introduction:`
- **Be specific**: Include the technology or concept. "Build a Custom MCP Server in C#" beats "Build MCP".
- **No trailing punctuation**. No em dashes in the heading.
- **Sentence case**, not title case.

## Workflow

### Step 1: Propose TOC (always first)

1. Glob all three file categories listed above.
2. Read the first 15 lines of each file; extract the current H1 (first `# ` line). If no H1 exists (only H2), note it as "no H1".
3. Propose a polished replacement for every heading.
4. Present a table grouped by module:

```text
| File | Current | Proposed |
|------|---------|----------|
| 01-intro | Introduction to Headless Agents | Run Claude Code in Headless Mode |
```

5. **Stop here.** Wait for the user to say "go" or request adjustments.

### Step 2: Apply (after "go")

For each file:
1. Read the file to confirm the exact current H1 text.
2. Use Edit with `old_string` set to the exact current heading line, `new_string` set to the polished heading line.
3. If no H1 exists (only H2 or plain text title), insert a new H1 as the first line.
4. Report any file where the old string did not match.

At the end, print a one-line summary:

```text
SUMMARY: N headings updated across M files
```

## Rules

- Never apply changes before presenting the TOC and receiving approval.
- Never change anything other than the H1 heading line.
- If a heading is already verb-first and clean, mark it `ok` in the TOC and skip it in Step 2.
- Do not modify lab files under `labs/`; only files inside `demos/`.
- Do not rename files or folders; only edit H1 content.
