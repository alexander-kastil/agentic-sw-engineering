---
name: enhance-business
description: Audit all demos in a masterclass repo, propose business-relevant enhancements per module, rank them by wow-factor and real deliverable value, then implement the top picks as prompt-recipe demo guides with realistic asset files.
---

# Enhance for Business Owner

This leaf is loaded by the `create-class` master skill. It is not invoked directly.

Scan every module in this masterclass, identify which demos lack a tangible business output, and implement the highest-impact upgrades as new demo guides written for managers, business owners, and citizen developers.

---

## Phase 1: Parallel Module Audit

Launch one Sonnet subagent per module group (3 modules each). Each subagent reads every `readme.md` under its assigned module folders and proposes 1-2 enhancements per demo.

Each subagent returns a table:

| module | demo name | current approach | proposed enhancement | tool/MCP/skill | effort |
|--------|-----------|-----------------|---------------------|----------------|--------|

Enhancement criteria, each proposal must use one or more of:
- Gamma MCP: generate a polished presentation from analysis output
- Microsoft 365 MCP: read real email, calendar, SharePoint, or Teams data
- Playwright MCP: automate browser actions and capture screenshots as proof
- xlsx/pdf/docx skills: produce a formatted, downloadable deliverable
- schedule skill: turn a manual recurring task into a hands-free cron job
- Agent tool (subagents): run parallel research that would take a person hours

---

## Phase 2: Business Re-Ranking

After all subagents return, launch a single Sonnet subagent with all proposals. That subagent filters to the top 10 by applying this lens:

- Would a business owner say "wait, it can DO that?"
- Does it produce a real deliverable (Excel workbook, PDF one-pager, slide deck, Teams message)?
- Does it save hours of weekly manual work?
- Is it immediately usable by someone who is not a developer?

Discard proposals that are primarily developer concerns: hooks, session logs, git commits, error handling.

Return a numbered shortlist:
1. Title (module / demo)
2. One sentence: what the business person sees (no jargon)
3. Tool/skill
4. Effort S/M/L

---

## Phase 3: Implementation

For each approved enhancement, create a new demo guide at `demos/<module>/demos/demo-NN-<slug>.md` following the prompt-recipe structure from the author-guide leaf (references/author-guide.md):

- Prompt-recipe format: 3 to 4 steps, each with Overview, Research, Finding, Recipe, Expected Outcome
- Business language throughout: no terms like "workspace", "context window", "model", "hook", or "prompt engineering" in the prose
- Related Topics section linking to 2-3 module topics
- Demo Files table listing companion assets
- Companion subfolder `demo-NN-<slug>/` with realistic asset files generated via Python (python-docx, openpyxl, python-pptx, reportlab)
- Updated `demos/<module>/demos/readme.md` TOC

Asset files must be realistic: plausible company names, figures, dates. A file with one paragraph is too thin; aim for a document a real team would recognise.

---

## Rules

- Implement enhancements in the same module sequentially to avoid numbering conflicts; enhancements in different modules run in parallel.
- Never reference fictional external URLs (e.g. `https://orders.somecompany.com/form`) in demo recipes. For browser-automation demos, create a local HTML mock file in the companion subfolder and reference it as a local file instead. The mock must implement the same form fields the recipe exercises and must show a realistic confirmation state after submission.
- All guide prose follows brand-voice rules: no em dashes, max 4 sentences per paragraph, `> Note:` for tips.
- Never add technical jargon to the guide prose. If the step uses the Gamma MCP, write "Claude builds you a presentation" not "Claude calls mcp__claude_ai_Gamma__generate".
- Invoke the repo-local brand-voice skill (Glob `.claude/skills/brand-voice-*`) after writing each guide.
