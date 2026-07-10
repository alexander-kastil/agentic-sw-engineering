# Current State Inventory

Snapshot of `demos/` as audited on 2026-07-10. Depth and runnable-code columns come from reading the files. Flags note what the modernization brief expects to find.

Depth: `stub` / `partial` / `full`. Runnable = actual source project files beyond markdown and templates.

---

## Module 1: `demos/01-fundamentals/`

| Path | readme | Depth | Runnable | Covers |
|------|:---:|:---:|:---:|--------|
| `01-fundamentals/` | Y | partial | N | Module index, links 8 topics |
| `00-codespaces/` | Y | full | N | Dev Containers + Codespaces, devcontainer.json walkthrough |
| `01-intro/` | Y | partial | N | AI-assisted vs agentic modes, essential settings.json, links |
| `02-models/` | Y | partial | N | Model comparison table, premium-request multipliers, AI Toolkit / Foundry / local models |
| `03-ai-assisted-coding/` | Y | partial | N | Prompting-techniques index (few-shot, CoT) |
| `03-ai-assisted-coding/01-inline-suggestions/` | Y | full | Y | Inline-completion exercises, JS/TS/Java samples + `-result` files |
| `03-ai-assisted-coding/02-prompt-with-samples/*` | Y | partial | Y | JS and Python prompt-with-sample examples |
| `03-ai-assisted-coding/03-database/*` | Y | partial | N | SQL Server and MongoDB Copilot prompting |
| `04-slash-commands/` | Y | partial | N | Chat slash-command table, empty "Demos & Examples" section |
| `05-context-variables/` | Y | full | Y | `#`/`@` context variables + two runnable demos (maf-starter, tasks-api) |
| `06-pr-code-review/` | Y | stub | N | Two prose paragraphs, no exercise |
| `07-mgmt-settings/` | Y | full | N | Org/repo/user policies, plan-tier matrices, credential security |

**Flags.** `00-codespaces/` present (remove). `02-models/` has no BYOK, no Custom Endpoint provider, no utility models, no 1M context, no Ollama deprecation; it does surface cost-in-picker but with invented, internally inconsistent model names and versions (needs full rewrite). `04-slash-commands/` does not frame `/autoApprove` or `/yolo` (they live only in the readme intro prose), and has no permission-level framing. `01-intro/` has no Copilot Vision. No terminal topic, no `VSCODE_AGENT`, no output-compression content. No real "edit mode" lesson content. `maf-starter-solution/readme.md` self-declares a config bug. `06-pr-code-review/` is a stub.

---

## Module 2: `demos/02-copilot-tools/`

| Path | readme | Depth | Runnable | Covers |
|------|:---:|:---:|:---:|--------|
| `02-copilot-tools/` | Y | full | N | Module index, 9 features |
| `01-instructions/` | Y | full | N | Instruction layers, VS Code enablement, load order |
| `02-prompts/` | Y | full | N | `.prompt.md` catalog + topics table |
| `02-prompts/01-transform-readme/` | Y | stub | N | 9 lines, Codespaces links + one prompt |
| `02-prompts/02-create-test/` | Y | partial | N | XUnit test-generation narrative |
| `03-mcp/` | Y | full | N | MCP concepts, mcp.json, 11-server table |
| `04-agents/` (+ 01-overview, 02-repo, 03-claude) | Y | full/partial | N | Agent fundamentals, repo `.agent.md` catalog, Claude agents |
| `05-skills/` | Y | full | N | Agent Skills standard, SKILL.md YAML, 16-skill catalog |
| `06-plugins/` | Y | full | N | Agent plugins (preview), plugin.json, discovery |
| `07-memory/` | Y | full | N | Copilot Memory, persistence, use cases |
| `08-context-window/` | Y | full | N | Context engineering, token sizes, strategies |
| `09-hooks/` | Y | full | N | Hook lifecycle, agent-scoped hooks, Conversation Tracker + mermaid |

**Actual numbering:** `01-instructions, 02-prompts, 03-mcp, 04-agents, 05-skills, 06-plugins, 07-memory, 08-context-window, 09-hooks`. No runnable code anywhere in the module.

**Flags.** TOC in `demos/readme.md` is wrong from 06 onward: it lists `06-memory, 07-context-window, 08-hooks, 09-agent-plugins` and a `10-debug-panel`. On disk plugins sit at `06-plugins` and shift memory/context/hooks to 07/08/09. Every TOC link 06 to 09 points at a non-existent path. `10-debug-panel/` does not exist (dangling link from Module 3 TOC). `03-mcp/` does not mention the GitHub MCP Registry (github.com/mcp). `05-skills/` has no scheduling / unattended-run content (a scheduled-automation lab needs new material). `06-plugins/` has no `copilot plugin install` auto-discovery language. `09-hooks/` carries a version caveat ("as of 08 Feb 2026, VS Code Insiders only").

---

## Module 3: `demos/03-agentic-coding/`

| Path | readme | Depth | Runnable | Covers |
|------|:---:|:---:|:---:|--------|
| `03-agentic-coding/` | Y | full | N | Module index, agent-type comparison |
| `01-local/` | Y | full | N | Local agents in Agent Mode, aspect table, `team.md`, steering image |
| `01-local/01-scaffold-net/` | Y | partial | N | Prompt-only .NET webapi + Scalar scaffold |
| `01-local/02-fix-err/` | Y | full | Y | Fix C# console app (`foundry-sdk-cs/`), keyless Foundry auth |
| `01-local/03-update/` | Y | full | Y | Upgrade Python Agent Framework project (`agentfw_tools-knowledge-py/`) |
| `02-cloud/` | Y | partial | N | Delegating to cloud agents (Azure Container Apps), concept only |
| `03-background/` | Y | partial | N | Background agents, single conceptual page, no code |
| `04-orchestration/` | Y | full | N | Multi-agent orchestration, mermaid, links to `.github/agents/*` |
| `05-claude-code/` | Y | partial | N | Claude Code agents, permission modes, slash-command table |

**Flags.** `06-browser-tools/` does not exist (must be created from scratch). No Agent Sessions / Agents Window content anywhere. No `/troubleshoot`, no Agent Debug Panel. No real edit-mode content. `03-background/` is purely conceptual (safe to migrate into the new Agent Sessions module). `05-claude-code/` is partial with no runnable lab.

---

## Module 4: `demos/04-advanced-topics/`

| Path | readme | Depth | Runnable | Covers |
|------|:---:|:---:|:---:|--------|
| `04-advanced-topics/` | Y | partial | N | Module index, 6 topics |
| `01-cli-intro/` | Y | full | N | Copilot CLI intro, install/auth, terminal assistance |
| `02-cli-business-case/` | Y | full | N | HR SharePoint document-update automation |
| `03-agentic-wf/` | Y | full | N | GitHub Agentic Workflows |
| `04-sdk/` | Y | full | N | Copilot SDK overview (TS/Python/Go/.NET) |
| `04-sdk/copilot-sdk-console/` | Y | full | Y | .NET 10 console app using `GitHub.Copilot.SDK` |
| `05-sdk-buiness-case/` | Y | full | N | TS/Node tutorial (weather agent, security analyzer), inline snippets only |
| `06-mcp-apps/` | Y | full | N | MCP Apps concept (`ui://` resources rendered in chat) |
| `06-mcp-apps/qr-server/` | Y | full | Y | Python FastMCP QR-code server |

**Flags.** Folder `05-sdk-buiness-case` is misspelled (`buiness` should be `business`). `04-sdk/` does not state "agent host is built on the Copilot SDK". No Copilot desktop-app content. `copilot-sdk-console` readme has a stale `cd` path (`demos/04-copilot-cli/...`, old module name). `05-sdk-buiness-case` has no buildable project, only inline TypeScript.

---

## Module 5: `demos/05-agentic-devops/`

| Path | readme | Depth | Runnable | Covers |
|------|:---:|:---:|:---:|--------|
| `05-agentic-devops/` | Y | full | N | Module index, 3 topics |
| `01-azure-cli/` | Y | full | Y | Generate/convert Azure CLI scripts, 2 `.azcli` + a .NET 10 blob-trigger Function (`picture-optimizer`) |
| `02-IaC/` | Y | full | Y | IaC overview + `create-workload-identity.azcli` (WIF OIDC) |
| `02-IaC/01-azd/` | Y | partial | N | azd concept page |
| `02-IaC/01-azd/azd-intro/` | Y | full | Y | Working azd project (`azure.yaml`, Bicep `infra/`, `src/simple-api` .NET 10) |
| `02-IaC/02-bicep/` | Y | partial | N | Prose + prompt, no `.bicep` files |
| `02-IaC/03-terraform/` | Y | partial | N | Prose + prompt, no `.tf` files |
| `03-pipelines/` | Y | partial | N | Azure DevOps + GitHub Actions prose, no YAML |

**Flags.** Actual top-level folders are exactly `01-azure-cli`, `02-IaC`, `03-pipelines` (azd is nested at `02-IaC/01-azd`). The `demos/readme.md` TOC is wrong: it lists a duplicate `01-azd-agentic/` that does not exist. No OpenTelemetry / Grafana / Application Insights observability content. `azd-intro/src/readme.md` is a 0-byte stub. `01-azure-cli/readme.md` has a stale `demos\06-agentic-devops\...` path.

---

## Module 6: `demos/06-spec-driven-dev/`

| Path | readme | Depth | Runnable | Covers |
|------|:---:|:---:|:---:|--------|
| `06-spec-driven-dev/` | Y | full | N | Module landing, index of 6 topics |
| `01-introduction/` | Y | full | N | SDD concepts, four-phase workflow, Spec Kit install |
| `02-spec-driven-workflow/` | Y | full | N | Spec Kit deep-dive, `.specify/` layout, `/speckit.*` table |
| `03-constitution/` | Y | full | N | constitution.md, spec.md, plan.md |
| `04-tasks/` | Y | full | N | Task breakdown, `/speckit.tasks` + `/speckit.implement` |
| `05-requirements/` | Y | partial | N | "Getting Started" that largely duplicates 01-introduction |
| `06-sample-case/` | Y | partial | N | Pointer to an external lab repo, no local content |

**Flags.** Module landing H1 mis-titled "Module 1: Spec-Driven Development Foundations" (should be its module number). Command-naming inconsistency: `01` and `05` use bare `/specify /plan /tasks /implement`, while `02/03/04` use namespaced `/speckit.*`. `05-requirements/` duplicates `01-introduction` and its slug does not match its "Getting Started" content. `06-sample-case/` depends entirely on an external repo (`github.com/alexander-kastil/spec-drive-development-lab`), no local fallback.

---

## Module 7: `demos/07-capstone-project/`

| Path | readme | Depth | Runnable | Covers |
|------|:---:|:---:|:---:|--------|
| `07-capstone-project/` | Y | full | N | 5-phase lifecycle landing |
| `01-planning/` (+ `01-md-editor`, `react-md-editor`) | Y | full | Y | React + Angular markdown-editor prompts + Vite/React/TS scaffold |
| `02-implementation/01-az-func/` (+ `currency-converter-func-ts`) | Y | full | Y | Azure Functions v4 TS currency converter |
| `03-upgrading/` (+ `sk-students-ai`, `maf-students-ai`) | Y | full | Y | SK to MAF migration guide + two runnable ASP.NET Razor apps (net10.0) |
| `04-testing/01-unit-tests/` | Y | partial | N | Angular 21 test guidance, `.agent.md`, MCP config |
| `04-testing/02-e2e/` | Y | stub | N | One line, "Agentic E2E Testing using Playwright" |
| `04-testing/food-app/` | Y | full | Y | Polyglot food-shop: C#/Java/Python/TS catalog APIs + Angular/React UIs |
| `05-docs/` | Y | full | N | Copilot documentation prompts, FoodController example |
| `05-docs/blob-console-spring/` | Y | stub | Y | Title-only readme + runnable Spring Boot app |
| `05-docs/net-api/` (+ `catalog-service`, `food-app-common`) | Y (empty) | stub/full | Y | 0-byte index over two .NET projects (net8.0 / net6.0) |
| `05-docs/food-ui/` | N | full | Y | Angular food UI |

**Flags.** Stubs: `04-testing/02-e2e/` (Playwright title only), `05-docs/blob-console-spring/` (22 bytes), `05-docs/net-api/readme.md` (0 bytes). `05-docs/` has no Mermaid-in-Markdown-preview, notebooks, chat diagrams, or Markdown-preview-for-diffs. Framework-version drift across the module: net10.0 in upgrading/testing, net8.0 and net6.0 in `05-docs/net-api`. React sample under `04-testing` has zero tests. This module is dissolved in the target (see [target-structure.md](target-structure.md)); its runnable apps are reused where the content lands.

---

## Repo-wide verification greps (2026-07-10)

- `codespace` (case-insensitive) in `demos/`: 6 files (the folder plus references in `demos/readme.md`, `01-fundamentals/readme.md`, `02-copilot-tools/02-prompts/readme.md` and `.../01-transform-readme/`, `02-copilot-tools/04-agents/02-repo-agents/`).
- `yolo|autoApprove`: one hit only, `demos/readme.md` line 5 (intro prose). No slash-command lesson uses them.
- `edit mode|editMode`: hits are all legitimate code identifiers (React `aria-label` string, C# `EditModel` page classes). No lesson content teaches the deprecated Edit mode, so R4 is effectively already satisfied; only verify no new content reintroduces it.
- `background agent`: 4 files (`demos/readme.md`, `03-agentic-coding/readme.md`, `.../03-background/`, `.../02-cloud/`).
