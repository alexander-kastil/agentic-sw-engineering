# Gap Backlog

Actionable work, ordered for a later `/create-class` pass. Every feature claim traces to a source in the brief's Section 1 (VS Code release notes 1.119 to 1.128, the GitHub Copilot app page, the GitHub MCP Registry). Do not author a feature not traceable to those sources.

## Priority 0: repo hygiene (cheap, unblocks navigation)

| ID | Action | Where |
|----|--------|-------|
| H1 | Resolve "four-day" vs "3 Days": set Duration to 4 days | `demos/readme.md` (done in this pass) |
| H2 | Fix typo "Using Local Agents **akn** Agent Mode" to "and" | `demos/readme.md` TOC (done) |
| H3 | Rename folder `04-advanced-topics/05-sdk-buiness-case` to `...-business...` and its link | folder + readme |
| H4/H5 | Module 5 (now M7) azd: the TOC listed a non-existent `01-azd-agentic/`; azd actually lives at `02-IaC/01-azd`. Fix TOC + add azd to prose | `demos/readme.md` (done) |
| H6 | Remove the dangling `10-debug-panel` link, replace intent with M3 Troubleshooting | `demos/readme.md` (done) |
| H7 | Expand Prerequisites: add "a Copilot license with credit allowance, or a BYOK endpoint" | `demos/readme.md` (done) |
| - | Fix Module 6 landing H1 mis-titled "Module 1: Spec-Driven..." | `06-spec-driven-dev/readme.md` |
| - | Fix stale paths: `04-sdk/copilot-sdk-console` `cd`, `01-azure-cli` `demos\06-...` | topic readmes |

## Priority 1: removals (reduce surface before adding)

| ID | Action | Detail |
|----|--------|--------|
| R1 | Delete `01-fundamentals/00-codespaces/` and all Codespaces references | 6 files touch "codespace"; also `02-prompts/01-transform-readme` is built on it. Flag deletions for owner confirmation per house rules. |
| R2 | Rewrite `04-slash-commands` off `/autoApprove` and `/yolo` | Only the readme intro prose uses them today; reframe as permission levels, point to M8. |
| R3 | Remove `03-agentic-coding/03-background` as a standalone topic | Migrate the concept into M3 (background send, remote host, subagents are session properties now). |
| R4 | Verify no Edit-mode lesson content | Already clean: grep hits are code identifiers only. Guard against reintroduction. |
| R5 | Retitle Agent Debug Panel to Troubleshooting Agent Sessions | Land in M3 `08-troubleshooting` as `/troubleshoot`. |

## Priority 2: new modules and topics (the bulk)

Ranked by the brief. Full source anchors live in [target-structure.md](target-structure.md).

1. **M3 Agent Sessions & Agents Window** (new module, 8 topics). Highest priority, nothing covers it today. Build the lab around session management (A1.4). Lowest-risk first exercise: `/research` (read-only).
2. **M8 Governance, Cost & Observability** (new module, 4 topics). Highest commercial value. OTel is the strongest Azure tie-in. Safety content (sandboxing, permission levels) must not be compressed.
3. **M6 GitHub Copilot App** (new module, 5 topics). Lab: promote the M2 Agent Skill into a scheduled automation, closing an open loop.
4. **M1 `02-models` full rewrite** (A3). Stale in every direction; also fix the invented, inconsistent model names currently in the file.
5. **M4 `05-browser-tools`** (new/expand, A4). GA on-by-default, promote from a bullet to a full lab.
6. **M1 `08-terminal`** (new). `VSCODE_AGENT`, output compression.

## Priority 3: smaller additions (A6)

| Where (new path) | Add |
|------------------|-----|
| `02-agentic-harness/03-mcp/` | GitHub MCP Registry (github.com/mcp) as the discovery surface |
| `01-fundamentals/01-intro/` | Copilot Vision GA: images and PDFs into chat by paste, drag, or tool call |
| `01-fundamentals/08-terminal/` | `VSCODE_AGENT` env var; terminal output compression for test runners, build tools, linters, Docker, package managers |
| `09-spec-driven-dev/08-documentation/` | Mermaid built into Markdown preview, notebooks, chat; Markdown preview for diffs |
| `02-agentic-harness/06-plugins/` | `copilot plugin install` auto-discovery (one install covers CLI + editor), cross-link M8 plugin governance |
| `05-cli-sdk/04-sdk/` | Explicit "the agent host is built on the Copilot SDK" statement, cross-link M3 AHP |

## Priority 4: expand thin content already present

| Topic (new path) | Action |
|------------------|--------|
| `01-fundamentals/06-pr-code-review/` | Stub to full guide with an exercise |
| `04-agentic-coding/04-claude-code/` | Add a runnable lab |
| `07-agentic-devops/02-IaC/02-bicep` and `03-terraform` | Prompt-only, add generated artifacts; fill 0-byte `azd-intro/src/readme.md` |
| `07-agentic-devops/03-pipelines/` | Add runnable Azure DevOps + GitHub Actions YAML |
| `09-spec-driven-dev/07-testing/02-e2e` | Playwright stub to full |
| `09-spec-driven-dev/08-documentation` | Fill title-only `blob-console-spring` and 0-byte `net-api` readmes; reconcile net6/8/10 drift |
| `09-spec-driven-dev/05-requirements` | Dedupe vs `01-introduction` |

## Runnable assets to preserve through the restructure

These build and should be carried into their new homes, not rewritten:

- `03-agentic-coding/01-local/02-fix-err/foundry-sdk-cs` and `03-update/agentfw_tools-knowledge-py`
- `04-advanced-topics/04-sdk/copilot-sdk-console` (.NET 10 SDK console)
- `04-advanced-topics/06-mcp-apps/qr-server` (Python FastMCP)
- `05-agentic-devops` `picture-optimizer` Function, `azd-intro` project + Bicep + `simple-api`
- capstone `03-upgrading` `sk-students-ai` and `maf-students-ai` (to M4)
- capstone `04-testing/food-app` polyglot suite (to M9 testing)
- capstone `05-docs` `blob-console-spring`, `net-api`, `food-ui` (to M9 documentation)
- capstone `01-planning` react-md-editor and `02-implementation` currency-converter (reusable demo assets)

## Verification checklist (brief Section 7)

Run before declaring the update done:

- [ ] `grep -ri "codespace" demos/` returns nothing outside an archive folder (currently 6 hits)
- [ ] `grep -ri "yolo\|autoApprove" demos/` every hit is in a permission-levels context (currently 1, the readme intro, fixed in this pass)
- [ ] `grep -ri "edit mode\|editMode" demos/` no lesson content (currently only code identifiers, OK)
- [ ] Every TOC link in `demos/readme.md` resolves to an existing directory
- [ ] No folder has a duplicate numeric prefix within its parent
- [ ] Every module folder in the target map exists
- [ ] Schedule table sums to the stated total and matches the stated percentage split
- [ ] Every feature claim in new lesson content traces to a Section 1 URL
- [ ] Labs assume Autopilot is on by default
- [ ] Labs that need write access state the permission level required

## Open items for the owner

- Confirm the R1 Codespaces folder deletion (house rules require explicit sign-off before removing files).
- Confirm exact placement of relocated capstone testing (proposed M9) versus a home in M4.
- Decide whether `05-cli-sdk/05-sdk-demos` should gain a buildable project or stay snippet-only.
