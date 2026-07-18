# Course Modernization Inventory

Working inventory for modernizing **"Agentic Software Engineering using GitHub Copilot"** to GitHub Copilot / VS Code **1.128** (release notes 1.119 to 1.128).

Source brief: `course-modernization-brief.md` (research date 2026-07-10). This folder captures the current state of `demos/`, the agreed target structure, and a prioritized backlog. It is the input for later `/create-class` runs (scaffold, author-guide, enrich-module) that build the missing and outdated content.

## Files

| File | Purpose | Feeds |
|------|---------|-------|
| [current-state.md](current-state.md) | Full inventory of the 7 existing modules: every topic, content depth, runnable code, modernization flags | context for author-guide / enrich-module |
| [target-structure.md](target-structure.md) | The agreed 9-module, 4-day target tree with an old to new crosswalk and per-topic status | `scaffold` leaf |
| [gap-backlog.md](gap-backlog.md) | Prioritized actions (remove / rewrite / expand / new) with sources and the verification checklist | authoring order |

## Owner decisions (locked)

These answers override the open questions in the brief (Section 8) and its Option A / Option B split:

1. **Schedule:** 4 days. No compressed 3-day option.
2. **No capstone module.** Its content is relocated, not dropped: *Upgrading & Modernization* moves into Agentic Coding; *Testing* and *Documentation* move into Spec-Driven Development & Delivery.
3. **GitHub Copilot App is its own module** (not a topic inside CLI/SDK). Source: https://github.com/features/ai/github-app
4. **OpenTelemetry / Grafana** live in the new Governance, Cost & Observability module (not Agentic DevOps).
5. **Codespaces replacement** is remote agent sessions over SSH and dev tunnels, taught inside the new Agent Sessions module.

## Execution status (2026-07-10)

The structural pass is **done**. What was executed:

- **Codespaces removed**: `01-fundamentals/00-codespaces/` deleted (git rm) and all 5 references cleaned (fundamentals index, prompts topic + index, repo-agents catalog).
- **Restructure complete** via history-preserving `git mv`. Final tree is the 9-module target; every `demos/readme.md` TOC link resolves; no duplicate numeric prefixes. Renames: `03-agentic-coding`->`04-agentic-coding` (with `04-orchestration`->`03`, `05-claude-code`->`04`), `04-advanced-topics`->`05-cli-sdk` (typo `05-sdk-buiness-case`->`05-sdk-demos`), `05-agentic-devops`->`07-agentic-devops`, `06-spec-driven-dev`->`09-spec-driven-dev`. Old `03-background` folded into `03-agent-sessions/04-session-management`.
- **Capstone dissolved**: `03-upgrading`->`04-agentic-coding/06-upgrading`, `04-testing`->`09-spec-driven-dev/07-testing`, `05-docs`->`09-spec-driven-dev/08-documentation`.
- **New content scaffolded** as sourced stubs: modules `03-agent-sessions` (8 topics), `06-copilot-app` (5), `08-governance` (4), plus topics `01-fundamentals/08-terminal` and `04-agentic-coding/05-browser-tools`. Module READMEs for M4, M5, M9 updated for the new topic sets.
- Build artifacts (`bin`/`obj`) under the moved .NET projects were cleared to release Windows file locks; they regenerate on next `dotnet build`.

**Pending owner decision:** `demos/_legacy-capstone-assets/` holds the two capstone topics not named for relocation (`01-planning` react-md-editor, `02-implementation` currency-converter). Decide their home or removal.

**Content authoring pass (done 2026-07-10):** the new-module and new-topic stubs were expanded into full guides via 6 parallel authoring agents, each grounded only in the source anchors. Written: all of `03-agent-sessions` (8 topics + enriched module readme with a session-specific slash-command table), `06-copilot-app` (5 topics), `08-governance` (4 topics), plus `01-fundamentals/08-terminal`, `04-agentic-coding/05-browser-tools`, `04-agentic-coding/04-claude-code` (expanded), and a full rewrite of `01-fundamentals/02-models` (invented model names removed). Every guide has concept prose, clarifying tables, at least one Mermaid diagram, an Exercise section where hands-on, and a Links & Resources closer. Verified across 24 files: 0 em dashes, all Mermaid labels use `<br/>`, all relative cross-links resolve.

**Recommended follow-ups (not yet done):** expand the remaining thin/partial topics (e.g. `01-fundamentals/06-pr-code-review`, `07-agentic-devops/02-IaC` bicep/terraform, `03-pipelines`, `09-spec-driven-dev/07-testing` E2E stub, `08-documentation` stubs); run a check-links pass over moved content for stale relative paths (the `copilot-sdk-console` `cd` path, the `01-azure-cli` `demos\06-...` path, and any capstone-era sibling links now under M4/M9); some copilot-app doc URLs follow GitHub's docs scheme but were not individually fetched, so verify them.

## Status legend

- `keep` topic is current, minor edits only
- `edit` topic needs targeted additions or fixes
- `rewrite` topic is stale end to end, replace the content
- `expand` topic exists thin, promote to a full guide or lab
- `new` topic does not exist yet, author from scratch
- `relocate` topic moves to a different module, content largely reused
- `remove` topic is deleted

## Depth legend

- `stub` H1 or near-empty
- `partial` some content, thin, no exercise or runnable asset
- `full` substantial guide, often with runnable code or an exercise
