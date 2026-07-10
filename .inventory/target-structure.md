# Target Structure

Agreed target for the modernized course: **4 days, 9 modules, no capstone**. This is the tree `/create-class` should scaffold and enrich toward. Status uses the legend in [readme.md](readme.md).

## Module map

```text
01-fundamentals                    Copilot Fundamentals
02-copilot-tools                   Copilot Artifacts & Tools
03-agent-sessions                  Agent Sessions & Agents Window   (NEW)
04-agentic-coding                  Implementing Agentic Coding
05-cli-sdk                         Copilot CLI & SDK
06-copilot-app                     GitHub Copilot App               (NEW)
07-agentic-devops                  Agentic DevOps
08-governance                      Governance, Cost & Observability (NEW)
09-spec-driven-dev                 Spec-Driven Development & Delivery
```

Note the renumbering: old `03-agentic-coding` becomes `04`, old `04-advanced-topics` splits into `05-cli-sdk` plus the new `06-copilot-app`, old `05-agentic-devops` becomes `07`, old `06-spec-driven-dev` becomes `09`. Old `07-capstone-project` is dissolved.

---

## Module 1: Copilot Fundamentals `01-fundamentals`

| Topic | Status | Notes |
|-------|--------|-------|
| `00-codespaces/` | remove | Descoped. Reproducible-environment story moves to M3 remote sessions. |
| `01-intro/` | edit | Add Copilot Vision GA (images and PDFs into chat by paste, drag, tool call). |
| `02-models/` | rewrite | BYOK without sign-in, Custom Endpoint provider (Stable 1.122), per-model `modelOptions`, utility models (`chat.utilityModel`, the BYOK utility trap), 1M-token context, unified context-size + reasoning-effort picker, Marketplace model providers, Ollama provider deprecation, cost in the model picker. |
| `03-ai-assisted-coding/` | keep | Current. |
| `04-slash-commands/` | rewrite | Drop `/autoApprove` and `/yolo` framing. Auto-approval is a permission level now, cross-link M8. |
| `05-context-variables/` | edit | Keep; fix the self-declared config bug in `maf-starter-solution`. |
| `06-pr-code-review/` | expand | Stub today, promote to a real guide with an exercise. |
| `07-mgmt-settings/` | keep | Current. |
| `08-terminal/` | new | `VSCODE_AGENT` env var (machine-readable CLI output), terminal output compression for test runners, build tools, linters, Docker, package managers. |

Also update module prerequisites (H7): a Copilot license with credit allowance, or a BYOK endpoint.

---

## Module 2: Copilot Artifacts & Tools `02-copilot-tools`

Keep the current on-disk numbering `01-instructions ... 09-hooks`. Fix the `demos/readme.md` TOC to match disk.

| Topic | Status | Notes |
|-------|--------|-------|
| `01-instructions/` | keep | |
| `02-prompts/` | edit | `01-transform-readme` is a Codespaces-linked stub, rewrite off Codespaces. |
| `03-mcp/` | edit | Add the GitHub MCP Registry (github.com/mcp) as the discovery surface. |
| `04-agents/` | keep | overview / repo / claude subtopics current. |
| `05-skills/` | edit | Prep as the source skill for the M6 scheduled-automation lab. |
| `06-plugins/` | edit | Add `copilot plugin install` auto-discovery (one install covers CLI + editor), cross-link M8 plugin governance. |
| `07-memory/` | keep | |
| `08-context-window/` | keep | |
| `09-hooks/` | keep | Watch the Insiders-only version caveat. |

Removed from this module's TOC: the dangling `10-debug-panel/` link (never existed on disk). Its intent moves to M3 as "Troubleshooting Agent Sessions".

---

## Module 3: Agent Sessions & Agents Window `03-agent-sessions` (NEW)

Highest-priority addition. Absorbs old `03-agentic-coding/03-background`.

| Topic | Status | Source anchor |
|-------|--------|---------------|
| `01-agents-window/` | new | Agents window Preview (1.120): companion window, selectable harness, remote execution, per-window overrides, `extensions.supportAgentsWindow`. |
| `02-host-protocol/` | new | Agent Host Protocol (1.121), AHP vs ACP contrast, host-authoritative state, long-lived host. Cross-link M5 SDK. |
| `03-remote-sessions/` | new | Remote sessions over SSH and dev tunnels (1.121). The Codespaces replacement. |
| `04-session-management/` | new | Side-by-side + pinning + maximize (1.123); picker Ctrl+R, background send, restore, Close All (1.124); multi-chat (1.126); server-side code-review comments `addComment`/`listComments`/`resolveComments` (1.126); session groups drag & drop, chat-input banners for failing CI and PR comments (1.127); Claude multi-chat fork + read-only subagent transcripts + workspace-less quick chats (1.128). Build the lab here. |
| `05-persistence/` | new | Session sync to the GitHub account, `/chronicle` for past-session queries and standup reports. |
| `06-subagents/` | new | Built-in subagents, read-only peer transcripts (1.128), per-subagent credit cost on hover, cross-link M8. |
| `07-research/` | new | `/research` read-only deep-research agent, cited Markdown report. Good low-risk first lab (no write permissions). |
| `08-troubleshooting/` | new | Retitle of the old Agent Debug Panel: `/troubleshoot` over local and remote agent-host sessions (1.127). |

---

## Module 4: Implementing Agentic Coding `04-agentic-coding`

| Topic | Status | Notes |
|-------|--------|-------|
| `01-local/` | keep | Local agents in Agent Mode. |
| `02-cloud/` | edit | Delegating to cloud agents; drop background-agent framing (migrated to M3). |
| `03-orchestration/` | keep | Was `04-orchestration`. Multi-agent orchestration. |
| `04-claude-code/` | expand | Was `05-claude-code`. Partial today, add a runnable lab. |
| `05-browser-tools/` | new/expand | Browser tools GA and on-by-default (1.127): open pages, read console, screenshots into chat, click/type/navigate without an external MCP server, device emulation, tab-sharing, per-site prompts. Cross-link `BrowserChatTools` in M8. |
| `06-upgrading/` | relocate | From capstone `03-upgrading` (SK to MAF migration + `sk-students-ai` / `maf-students-ai` runnable apps). |

Old `03-background/` is removed here (migrated into M3).

---

## Module 5: Copilot CLI & SDK `05-cli-sdk`

Old `04-advanced-topics` minus the MCP-apps-only material stays; the desktop app splits out to M6.

| Topic | Status | Notes |
|-------|--------|-------|
| `01-cli-intro/` | keep | |
| `02-cli-business-case/` | keep | HR document-update automation. |
| `03-agentic-wf/` | keep | GitHub Agentic Workflows. |
| `04-sdk/` | edit | Add the explicit statement that the agent host is built on the Copilot SDK (makes the SDK load-bearing), cross-link M3 AHP. Fix stale `cd` path in `copilot-sdk-console`. |
| `05-sdk-demos/` | edit | Rename from the typo `05-sdk-buiness-case`. Optionally add a buildable project. |
| `06-mcp-apps/` | keep | MCP Apps + qr-server. |

---

## Module 6: GitHub Copilot App `06-copilot-app` (NEW)

Its own module. Source: https://github.com/features/ai/github-app

| Topic | Status | Notes |
|-------|--------|-------|
| `01-overview/` | new | macOS / Windows / Linux, any Copilot plan or BYOK. What an agents view looks like outside the editor. |
| `02-sessions/` | new | Sessions from a GitHub issue, a freeform prompt, or an in-flight PR; isolated worktree or local clone per session. |
| `03-validation-loop/` | new | Review diffs, drive the in-app browser, use the terminal, merge the PR from inside the session. |
| `04-automations/` | new | Scheduled automations turn skills and prompts into recurring work. Lab: promote the M2 Agent Skill into a scheduled automation. |
| `05-sync/` | new | Repo MCP servers and skills sync automatically. |

---

## Module 7: Agentic DevOps `07-agentic-devops`

Unchanged content, renumbered from old `05`. OTel is deliberately NOT here (it lives in M8).

| Topic | Status | Notes |
|-------|--------|-------|
| `01-azure-cli/` | keep | Fix stale `demos\06-agentic-devops\...` path. |
| `02-IaC/` | edit | azd (fill the 0-byte `azd-intro/src/readme.md`), bicep and terraform topics are prompt-only, add generated artifacts. |
| `03-pipelines/` | edit | Azure DevOps + GitHub Actions; add runnable YAML. |

---

## Module 8: Governance, Cost & Observability `08-governance` (NEW)

Highest commercial value. Serves the Architect / Team Lead / Manager audience.

| Topic | Status | Source anchor |
|-------|--------|---------------|
| `01-permissions/` | new | Permission levels, Autopilot default-on since 1.124 (`chat.permissions.default`, `chat.tools.global.autoApprove`), Advanced Autopilot, terminal sandboxing, AI risk badges Safe/Caution/Review, sensitive-prompt interception, Restricted Mode default, `disableBypassPermissionsMode`, Claude Auto mode + `allowDangerouslySkipPermissions`. Replaces the old yolo/autoApprove framing. |
| `02-cost/` | new | Usage-based AI credits (input/output/cached tokens, model choice), cost in the model picker, session-level cost + additional-spend percentage, per-subagent credit cost. Model choice is now a budget decision, tie to M1 Models. |
| `03-enterprise-policy/` | new | Managed settings via MDM (1.125), `managed-settings.json` (1.127), plugin governance (`chat.plugins.enabledPlugins/extraMarketplaces/strictMarketplaces`), `BrowserChatTools`, `ChatAgentNetworkFilter`. |
| `04-observability/` | new | OpenTelemetry GenAI semantic conventions (1.119), span tree (`invoke_agent` root, nested `chat`/`execute_tool`/`execute_hook`, subagent spans parented to the tool span), Azure Managed Grafana dashboard (1.121), admin-mandated OTLP endpoint via the managed-settings `telemetry` block overriding env vars and user settings (1.128). |

---

## Module 9: Spec-Driven Development & Delivery `09-spec-driven-dev`

Old `06-spec-driven-dev` plus the relocated Testing and Documentation phases from the dissolved capstone.

| Topic | Status | Notes |
|-------|--------|-------|
| `01-introduction/` | edit | Fix mis-titled H1; reconcile `/specify` to `/speckit.*` naming. |
| `02-spec-driven-workflow/` | keep | |
| `03-constitution/` | keep | |
| `04-tasks/` | keep | |
| `05-requirements/` | edit | Dedupe against `01-introduction`, or fold in and rename to match "Getting Started" content. |
| `06-sample-case/` | edit | External-repo dependency, add a local fallback. |
| `07-testing/` | relocate | From capstone `04-testing`: unit tests, E2E Playwright (currently a stub, expand), the polyglot `food-app`. |
| `08-documentation/` | relocate | From capstone `05-docs`: doc-generation prompts + the new brief item, Mermaid built into Markdown preview, notebooks and chat, plus Markdown preview for diffs (reviewing agent-generated docs). Fill the 0-byte and title-only stubs. |

---

## Old to new crosswalk

| Old path | New path | Action |
|----------|----------|--------|
| `01-fundamentals/00-codespaces/` | (deleted) | remove |
| `01-fundamentals/*` (01 to 07) | `01-fundamentals/*` | keep/edit/rewrite per table |
| (none) | `01-fundamentals/08-terminal/` | new |
| `02-copilot-tools/*` | `02-copilot-tools/*` | keep, fix TOC |
| `02-copilot-tools/10-debug-panel` (TOC only) | `03-agent-sessions/08-troubleshooting/` | new, replaces dangling link |
| `03-agentic-coding/03-background/` | `03-agent-sessions/` (folded) | relocate into new module |
| `03-agentic-coding/01-local` | `04-agentic-coding/01-local` | keep |
| `03-agentic-coding/02-cloud` | `04-agentic-coding/02-cloud` | edit |
| `03-agentic-coding/04-orchestration` | `04-agentic-coding/03-orchestration` | keep |
| `03-agentic-coding/05-claude-code` | `04-agentic-coding/04-claude-code` | expand |
| (none) | `04-agentic-coding/05-browser-tools/` | new |
| `07-capstone-project/03-upgrading` | `04-agentic-coding/06-upgrading/` | relocate |
| `04-advanced-topics/01..04, 06` | `05-cli-sdk/01..04, 06` | keep/edit |
| `04-advanced-topics/05-sdk-buiness-case` | `05-cli-sdk/05-sdk-demos` | rename (fix typo) |
| (none) | `06-copilot-app/` | new module |
| `05-agentic-devops/*` | `07-agentic-devops/*` | keep/edit, renumber |
| (none) | `08-governance/` | new module |
| `06-spec-driven-dev/*` | `09-spec-driven-dev/01..06` | keep/edit, renumber |
| `07-capstone-project/04-testing` | `09-spec-driven-dev/07-testing/` | relocate |
| `07-capstone-project/05-docs` | `09-spec-driven-dev/08-documentation/` | relocate |
| `07-capstone-project/01-planning` | reuse assets | react-md-editor scaffold reusable as a demo asset where fitting |
| `07-capstone-project/02-implementation` | reuse assets | currency-converter function reusable as a demo asset where fitting |

---

## Schedule (4 days)

| Module | Instr | Labs | Total |
|--------|------:|-----:|------:|
| M1 Fundamentals | 2.0 | 1.0 | 3.0 |
| M2 Artifacts & Tools | 3.0 | 1.5 | 4.5 |
| M3 Agent Sessions | 2.5 | 1.0 | 3.5 |
| M4 Agentic Coding | 2.5 | 1.5 | 4.0 |
| M5 CLI & SDK | 1.5 | 0.5 | 2.0 |
| M6 Copilot App | 1.5 | 0.5 | 2.0 |
| M7 Agentic DevOps | 2.0 | 0.5 | 2.5 |
| M8 Governance, Cost & Obs | 1.5 | 0.5 | 2.0 |
| M9 Spec-Driven & Delivery | 2.5 | 1.5 | 4.0 |
| **Total** | **19.0** | **8.5** | **27.5** |

Split: 69% instruction / 31% labs. Day grouping: Day 1 = M1 + M2 (7.5h); Day 2 = M3 + M4 (7.5h); Day 3 = M5 + M6 + M7 (6.5h); Day 4 = M8 + M9 (6.0h).
