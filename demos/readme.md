# Agentic Software Engineering using GitHub Copilot

A four-day journey into agentic software engineering with GitHub Copilot, and how AI-powered tools reshape coding productivity and architectural decisions. Software engineers, architects, and technical leaders get the hands-on experience to leverage AI in modern software development.

Your journey begins with Fundamentals and Agent Mode Basics: prompting, inline suggestions, slash commands, context variables, and code review on pull requests. You configure models from hosted frontier to bring-your-own-key endpoints. Agent Mode arrives early, driving a local agent through multi-step work and the terminal.

You then assemble the GitHub Copilot Harness: instructions, prompt files, and the Model Context Protocol, with the MCP Registry as your discovery surface. It adds custom agents, skills, memory, and hooks, optimizes the context window with prompt caching, and installs Agent Plugins 1.0 packages that work across CLI and editor from one install.

In Implementing Agentic Coding you put agents to work: local agents in agent mode, large jobs delegated to cloud agents, and expert subagents coordinated by an orchestrator running independent work in parallel. Browser tools let agents open pages, read console errors, and verify their own web changes; an agent-led modernization from Semantic Kernel to the Microsoft Agent Framework closes the module.

Agent Sessions covers the infrastructure underneath those runs. You run agents across projects in a companion window, see how the Agent Host Protocol keeps session state authoritative on a long-lived host, and drive remote sessions over SSH and dev tunnels. Groups, background sends, and one-click banners fix failing CI checks at scale, and dedicated agents return cited research, recover stalled sessions, and give second opinions.

The GitHub Copilot CLI brings the agent to the command line: an interactive shell with slash commands and natural language, models switched on the fly, and multi-step work handed to Autopilot. An HR document-automation case over Work IQ and SharePoint MCP servers shows the payoff, and GitHub Agentic Workflows turn those jobs into versioned, scheduled runs that open pull requests.

The GitHub Copilot SDK embeds those capabilities into your own applications on the runtime that powers the CLI and the editor's agent host. In Technical Preview for Python, TypeScript, Go, and .NET, you create sessions and custom tools while Copilot plans and executes, build runnable agents, deploy one to Azure, and extend them with MCP Apps rendering interactive UIs in chat.

The GitHub Copilot app is the desktop agents view for macOS, Windows, and Linux. Sessions start from a GitHub issue, a freeform prompt, or an in-flight pull request, each in its own worktree, with a Plan tab and a side chat to steer a run without interrupting it. A validation loop reviews diffs, collects agent-attached screenshots, and merges the pull request, while skills and prompts become scheduled automations. Customize manages the plugins, personal skills, and MCP servers a session inherits, alongside the permission mode and the model it runs on.

Agentic DevOps applies these techniques to cloud automation and infrastructure as code: Azure CLI, Bicep, Terraform, and the Azure Developer CLI in agentic mode, plus CI/CD with GitHub Actions. The quality loop closes here too, with generated tests including end-to-end Playwright suites and Mermaid-diagrammed documentation.

Governance, Cost and Observability is written for architects, team leads, and managers: the permission model from Autopilot and assisted approvals to risk badges, sensitive-prompt interception, and opt-in sandboxing, model choice as a budget decision under usage-based credits, bring your own key to route work to the provider you choose, the Business and Enterprise controls that govern the harness for a whole organization, OpenTelemetry traces feeding an Azure Managed Grafana dashboard, and the compliance obligations attaching to the software your agents ship.

The course closes with Spec-Driven Development and Delivery: a constitution, specification, and technical plan, complex requirements decomposed into tasks with GitHub Spec Kit, and a product feature implemented end to end from its specification. You leave able to architect AI-assisted solutions that accelerate delivery and strengthen your team.

## Duration

4 Days

## Audience

- Software Engineers interested in leveraging AI agents to enhance their coding productivity and capabilities
- Software Architects looking to understand how to integrate and manage AI agents within software development lifecycles
- Team Leads and Managers aiming to explore how AI agents can be utilized to optimize team workflows and project outcomes

## Prerequisites & Requirements

- Experience with software development at a professional level
- A GitHub Copilot license with a credit allowance, or a configured bring-your-own-key (BYOK) endpoint. Usage-based billing makes this a required setup step, not an optional one.

## [Module 1: GitHub Copilot Fundamentals & Agent Mode Basics](./01-fundamentals/)

- [Getting Started & Configuring Copilot](01-fundamentals/01-intro/)
- [Selecting Models](01-fundamentals/02-models/)
- [Shaping the Context Window](01-fundamentals/03-context-window/)
- [AI-Assisted Coding Essentials](01-fundamentals/04-ai-assisted-coding/)
- [Agent Mode Basics](01-fundamentals/05-agent-mode-basics/)
- [Pull Requests & Code Reviews](01-fundamentals/06-pr-code-review/)
- [Working in the Terminal](01-fundamentals/07-terminal/)

## [Module 2: GitHub Copilot Harness](./02-agentic-harness/)

- [Copilot Instructions](02-agentic-harness/01-instructions/)
- [Prompt Files](02-agentic-harness/02-prompts/)
- [Model Context Protocol & MCP Registry](02-agentic-harness/03-mcp/)
  - [MCP Basics & the MCP Registry](02-agentic-harness/03-mcp/01-basics/)
  - [Implementing MCP Servers](02-agentic-harness/03-mcp/02-mcp-server/)
  - [Implementing & Using MCP Apps](02-agentic-harness/03-mcp/03-mcp-apps/)
- [Agent Skills](02-agentic-harness/04-skills/)
- [Custom Agents](02-agentic-harness/05-agents/)
  - [Agents Overview](02-agentic-harness/05-agents/01-agents-overview/)
  - [Repository Agents](02-agentic-harness/05-agents/02-repo-agents/)
- [Agent Plugins](02-agentic-harness/06-plugins/)
- [Copilot Memory](02-agentic-harness/07-memory/)
- [GitHub Copilot Hooks](02-agentic-harness/08-hooks/)
- [Agent Interop](02-agentic-harness/09-agent-interop/)

## [Module 3: Implementing Agentic Coding](./03-agentic-coding/)

- [Using Local Agents and Agent Mode](03-agentic-coding/01-local-agents/)
- [Delegating Tasks to Cloud Agents](03-agentic-coding/02-cloud/)
- [Multi-Agent Orchestration with Subagents](03-agentic-coding/03-orchestration/)
- [Agentic Browser Automation](03-agentic-coding/04-browser-tools/)
- [Upgrading & Modernization](03-agentic-coding/05-upgrading/)

## [Module 4: Agent Sessions & Agents Window](./04-agent-sessions/)

- [The Agents Window](04-agent-sessions/01-agents-window/)
- [Agent Host Protocol (AHP vs ACP)](04-agent-sessions/02-host-protocol/)
- [Remote Agent Sessions over SSH & Dev Tunnels](04-agent-sessions/03-remote-sessions/)
- [Managing Sessions in the Agents Window](04-agent-sessions/04-session-management/)

## [Module 5: GitHub Copilot CLI & SDK](./05-cli-sdk/)

- [Part 1: GitHub Copilot CLI](05-cli-sdk/01-cli/)
  - [GitHub Copilot CLI](05-cli-sdk/01-cli/01-intro/)
  - [Extending the CLI with MCP Servers & Skills](05-cli-sdk/01-cli/02-mcp-skills/)
  - [Business Case: HR Document Updates Automation](05-cli-sdk/01-cli/03-business-case/)
  - [GitHub Agentic Workflows](05-cli-sdk/01-cli/04-agentic-wf/)
  - [Codebase Q&A and Onboarding (optional)](05-cli-sdk/01-cli/05-codebase-qa/)
- [Part 2: GitHub Copilot SDK](05-cli-sdk/02-sdk/)
  - [SDK Fundamentals](05-cli-sdk/02-sdk/01-intro/)
  - [Building Agents with Custom Tools](05-cli-sdk/02-sdk/02-custom-tools/)
  - [Building a Multi-Agent System](05-cli-sdk/02-sdk/03-multi-agent/)
  - [Deploying an SDK Agent to Azure](05-cli-sdk/02-sdk/04-deploy-azure/)

## [Module 6: GitHub Copilot App](./06-copilot-app/)

- [Meet the Desktop Agents App](06-copilot-app/01-overview/)
- [Set Up Your Workspace: Projects, Customize & Sync](06-copilot-app/02-setup/)
- [My Work: Picking Up the Day](06-copilot-app/03-my-work/)
- [Sessions from Issues, Prompts & Pull Requests](06-copilot-app/04-sessions/)
- [The Validation Loop](06-copilot-app/05-validation-loop/)
- [Automations: Creating Them in the UI](06-copilot-app/06-automations/)
- [Automations: Running & Maintaining Them](06-copilot-app/07-automation-runs/)

## [Module 7: Agentic DevOps](./07-agentic-devops/)

- [IaC & Configuration (Azure CLI, SSH, Bicep & Terraform)](07-agentic-devops/01-iac/)
- [CI/CD with GitHub Actions](07-agentic-devops/02-cicd/)
- [Testing using Copilot (xUnit, Vitest, Playwright & Evaluations)](07-agentic-devops/03-testing/)
- [Documentation using Copilot](07-agentic-devops/04-documentation/)

## [Module 8: Governance, Cost & Observability](./08-governance/)

- [Trust, Safety & the Permission Model](08-governance/01-permissions/)
- [Cost, AI Credits & Bring Your Own Key](08-governance/02-cost-byok/)
  - [Bring Your Own Key in VS Code](08-governance/02-cost-byok/01-byok-vscode/)
  - [Bring Your Own Key in the Copilot CLI](08-governance/02-cost-byok/02-byok-copilot-cli/)
  - [Bring Your Own Key in the GitHub Copilot App](08-governance/02-cost-byok/03-byok-copilot-app/)
- [Enterprise Control of the Harness](08-governance/03-enterprise-control/)
  - [Observability with OpenTelemetry](08-governance/03-enterprise-control/01-observability/)
- [EU AI Act, GDPR & Accessibility Compliance](08-governance/04-compliance/)

## [Module 9: Plan, Specify, Deliver](./09-plan-spec-deliver/)

- [Brownfield Analysis: Harvest the Current State](09-plan-spec-deliver/01-analysis/)
- [Planning with Agents](09-plan-spec-deliver/02-planning/)
- [Why Spec-Driven Development](09-plan-spec-deliver/03-introduction/)
- [The Spec-Driven Workflow](09-plan-spec-deliver/04-spec-driven-workflow/)
- [Sample Case: Implement a Product Feature](09-plan-spec-deliver/05-sample-case/)

---

## Schedule

**Total duration: 4 days · 28.0 hours** · 70% instruction & demos (~19.5h) · 30% labs (~8.5h)

| Day       | Modules                              |     Demos |     Labs |     Total |
| --------- | ------------------------------------ | --------: | -------: | --------: |
| **Day 1** | Module 1 · Module 2                  |      6.0h |     1.0h |      7.0h |
| **Day 2** | Module 2 (lab) · Module 3 · Module 4 |      4.5h |     2.5h |      7.0h |
| **Day 3** | Module 4 · Module 5 · Module 6       |      4.0h |     3.0h |      7.0h |
| **Day 4** | Module 7 · Module 8 · Module 9       |      5.0h |     2.0h |      7.0h |
| **Total** |                                      | **19.5h** | **8.5h** | **28.0h** |

Each day runs 09:00 to 17:15 with a 15-minute morning break, a 45-minute lunch, and a 15-minute afternoon break.

### Day 1: Fundamentals and the Harness

| Time        |  Dur. | Type  | Content                                                                                                                                                            |
| ----------- | ----: | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 09:00-10:30 |  1.5h | Demos | [M1](01-fundamentals/) Getting Started & Configuring Copilot · Selecting Models · Shaping the Context Window                                          |
| 10:30-10:45 | 0.25h | Break |                                                                                                                                                                    |
| 10:45-11:45 |  1.0h | Demos | [M1](01-fundamentals/) AI-Assisted Coding Essentials · Agent Mode Basics · Pull Requests & Code Reviews · Working in the Terminal |
| 11:45-12:45 |  1.0h | Labs  | [Lab 01: Getting started](../labs/01-get-started/) · [Lab 02: Update a web API with Copilot](../labs/02-assisted-coding/)                                           |
| 12:45-13:30 | 0.75h | Lunch |                                                                                                                                                                    |
| 13:30-15:00 |  1.5h | Demos | [M2](02-agentic-harness/) Copilot Instructions · Prompt Files · MCP Basics & the MCP Registry · Implementing MCP Servers                                            |
| 15:00-15:15 | 0.25h | Break |                                                                                                                                                                    |
| 15:15-17:15 |  2.0h | Demos | [M2](02-agentic-harness/) Agent Skills · Custom Agents (overview, repository agents) · Agent Plugins · Copilot Memory · Hooks · Agent Interop                       |

### Day 2: Agentic Coding and Agent Sessions

| Time        |  Dur. | Type  | Content                                                                                                                         |
| ----------- | ----: | ----- | ------------------------------------------------------------------------------------------------------------------------------- |
| 09:00-10:30 |  1.5h | Lab   | [Lab 03: Copilot instructions & custom agents](../labs/03-harness/)                                                             |
| 10:30-10:45 | 0.25h | Break |                                                                                                                                 |
| 10:45-12:45 |  2.0h | Demos | [M3](03-agentic-coding/) Local Agents & Agent Mode · Delegating Tasks to Cloud Agents · Multi-Agent Orchestration with Subagents |
| 12:45-13:30 | 0.75h | Lunch |                                                                                                                                 |
| 13:30-14:30 |  1.0h | Demos | [M3](03-agentic-coding/) Agentic Browser Automation · Upgrading & Modernization                                                  |
| 14:30-14:45 | 0.25h | Break |                                                                                                                                 |
| 14:45-15:45 |  1.0h | Lab   | [Lab 04: Orchestrate a multi-agent build with one prompt](../labs/04-orchestration/)                                            |
| 15:45-17:15 |  1.5h | Demos | [M4](04-agent-sessions/) The Agents Window · Agent Host Protocol (AHP vs ACP) · Remote Agent Sessions over SSH & Dev Tunnels     |

### Day 3: CLI, SDK and the Copilot App

| Time        |  Dur. | Type  | Content                                                                                                                                                                         |
| ----------- | ----: | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 09:00-09:30 |  0.5h | Demos | [M4](04-agent-sessions/) Managing Sessions in the Agents Window              |
| 09:30-10:30 |  1.0h | Lab   | [Lab 05: Run two isolated agent sessions](../labs/05-agent-sessions/)                                                                                                            |
| 10:30-10:45 | 0.25h | Break |                                                                                                                                                                                 |
| 10:45-12:45 |  2.0h | Demos | [M5](05-cli-sdk/) CLI · HR Automation Business Case · Agentic Workflows · MCP Servers & Skills · Codebase Q&A · SDK · SDK Demos · MCP Apps · Deploy to Azure · Multi-Agent System |
| 12:45-13:30 | 0.75h | Lunch |                                                                                                                                                                                 |
| 13:30-14:30 |  1.0h | Lab   | [Lab 06: Integrate an AI agent using the Copilot SDK](../labs/06-copilot-sdk/)                                                                                                   |
| 14:30-14:45 | 0.25h | Break |                                                                                                                                                                                 |
| 14:45-16:15 |  1.5h | Demos | [M6](06-copilot-app/) Desktop Agents App · Workspace Setup · My Work · Sessions · Validation Loop · Creating Automations · Running Automations             |
| 16:15-17:15 |  1.0h | Lab   | [Lab 07: Ship a verified pull request from the desktop app](../labs/07-copilot-app/)                                                                                             |

### Day 4: DevOps, Governance and Spec-Driven Delivery

| Time        |  Dur. | Type  | Content                                                                                                                                                                    |
| ----------- | ----: | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 09:00-10:30 |  1.5h | Demos | [M7](07-agentic-devops/) IaC & Configuration (Azure CLI, SSH, Bicep & Terraform) · CI/CD with GitHub Actions                                                                |
| 10:30-10:45 | 0.25h | Break |                                                                                                                                                                            |
| 10:45-11:15 |  0.5h | Demos | [M7](07-agentic-devops/) Testing using Copilot · Documentation using Copilot                                                                                                |
| 11:15-12:15 |  1.0h | Lab   | [Lab 08: Resolve GitHub issues using Copilot](../labs/08-devops/)                                                                                                           |
| 12:15-13:00 | 0.75h | Lunch |                                                                                                                                                                            |
| 13:00-14:30 |  1.5h | Demos | [M8](08-governance/) Permission Model · Cost & Bring Your Own Key · Enterprise Control · Observability with OpenTelemetry · EU AI Act, GDPR & Accessibility     |
| 14:30-14:45 | 0.25h | Break |                                                                                                                                                                            |
| 14:45-16:15 |  1.5h | Demos | [M9](09-plan-spec-deliver/) Brownfield Analysis · Planning with Agents · Why Spec-Driven Development · The Spec-Driven Workflow · Sample Case: Implement a Product Feature                          |
| 16:15-17:15 |  1.0h | Lab   | [Lab 09: Harvest the current state · Ship a feature with GitHub Spec Kit](../labs/09-plan-spec-deliver/)                                                                     |

> Labs live in [`labs/`](../labs/) and run at the point in the schedule shown above. The lowest-risk first lab is the read-only `/research` session in Lab 05; labs that write to a repository state the permission level they require, and all labs assume Autopilot is the default permission level.
