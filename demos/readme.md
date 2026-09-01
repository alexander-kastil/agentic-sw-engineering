# Agentic Software Engineering using GitHub Copilot

A four-day journey into agentic software engineering with GitHub Copilot, and how AI-powered tools reshape coding productivity and architectural decisions. Software engineers, architects, and technical leaders get the hands-on experience to leverage AI in modern software development.

Your journey begins with Fundamentals and Agent Mode Basics: prompting, inline suggestions, slash commands, context variables, and code review on pull requests. You configure models from hosted frontier to bring-your-own-key endpoints, and Copilot Vision brings images and PDFs into chat. Agent Mode arrives early, driving a local agent through multi-step work and the terminal.

You then assemble the GitHub Copilot Harness: instructions, prompt files, and the Model Context Protocol, with the MCP Registry as your discovery surface. It adds custom agents, skills, memory, and hooks, optimizes the context window with prompt caching, and installs Agent Plugins 1.0 packages that work across CLI and editor from one install.

In Implementing Agentic Coding you put agents to work: local agents in agent mode, large jobs delegated to cloud agents, and expert subagents coordinated by an orchestrator running independent work in parallel. Browser tools let agents open pages, read console errors, and verify their own web changes; an agent-led modernization from Semantic Kernel to the Microsoft Agent Framework closes the module.

Agent Sessions covers the infrastructure underneath those runs. You run agents across projects in a companion window, see how the Agent Host Protocol keeps session state authoritative on a long-lived host, and drive remote sessions over SSH and dev tunnels. Groups, background sends, and one-click banners fix failing CI checks at scale, and dedicated agents return cited research, recover stalled sessions, and give second opinions.

The GitHub Copilot CLI brings the agent to the command line: an interactive shell with slash commands and natural language, models switched on the fly, and multi-step work handed to Autopilot. An HR document-automation case over Work IQ and SharePoint MCP servers shows the payoff, and GitHub Agentic Workflows turn those jobs into versioned, scheduled runs that open pull requests.

The GitHub Copilot SDK embeds those capabilities into your own applications on the runtime that powers the CLI and the editor's agent host. In Technical Preview for Python, TypeScript, Go, and .NET, you create sessions and custom tools while Copilot plans and executes, build runnable agents, deploy one to Azure, and extend them with MCP Apps rendering interactive UIs in chat.

The GitHub Copilot app is the desktop agents view for macOS, Windows, and Linux. Sessions start from a GitHub issue, a freeform prompt, or an in-flight pull request, each in its own worktree, with a Plan tab and a side chat to steer a run without interrupting it. A validation loop reviews diffs, collects agent-attached screenshots, and merges the pull request, while skills and prompts become scheduled automations. Customize manages the plugins, personal skills, and MCP servers a session inherits, alongside the permission mode and the model it runs on.

Agentic DevOps applies these techniques to cloud automation and infrastructure as code: Azure CLI, Bicep, Terraform, and the Azure Developer CLI in agentic mode, plus CI/CD with GitHub Actions. The quality loop closes here too, with generated tests including end-to-end Playwright suites and Mermaid-diagrammed documentation.

Governance, Cost and Observability is written for architects, team leads, and managers: the permission model from Autopilot and assisted approvals to risk badges, sensitive-prompt interception, and opt-in sandboxing, model choice as a budget decision under usage-based credits, open-source models to cut that cost, enterprise managed settings via MDM, OpenTelemetry traces feeding an Azure Managed Grafana dashboard, and the compliance obligations attaching to the software your agents ship.

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

- [Getting Started with Copilot & Vision](01-fundamentals/01-intro/)
- [Selecting & Configuring Models](01-fundamentals/02-models/)
- [Shaping the Context Window](01-fundamentals/03-context-window/)
- [AI-Assisted Coding Essentials](01-fundamentals/04-ai-assisted-coding/)
- [Agent Mode Basics](01-fundamentals/05-agent-mode-basics/)
- [Pull Requests & Code Reviews](01-fundamentals/06-pr-code-review/)
- [Configuring & Governing Copilot](01-fundamentals/07-mgmt-settings/)
- [Working in the Terminal](01-fundamentals/08-terminal/)

## [Module 2: GitHub Copilot Harness](./02-agentic-harness/)

- [Copilot Instructions](02-agentic-harness/01-instructions/)
- [Prompt Files](02-agentic-harness/02-prompts/)
- [Model Context Protocol & MCP Registry](02-agentic-harness/03-mcp/)
  - [MCP Basics & the MCP Registry](02-agentic-harness/03-mcp/01-basics/)
  - [Implementing MCP Servers](02-agentic-harness/03-mcp/02-implementing/)
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
- [Session Management](04-agent-sessions/04-session-management/)
- [Session Persistence & /chronicle](04-agent-sessions/05-persistence/)
- [Deep Research with /research](04-agent-sessions/06-research/)
- [Troubleshooting Agent Sessions](04-agent-sessions/07-troubleshooting/)
- [A Second Opinion with /rubber-duck](04-agent-sessions/08-rubber-duck/)

## [Module 5: GitHub Copilot CLI & SDK](./05-cli-sdk/)

- [Part 1: GitHub Copilot CLI](05-cli-sdk/01-cli/)
  - [GitHub Copilot CLI](05-cli-sdk/01-cli/01-cli-intro/)
  - [Business Case: HR Document Updates Automation](05-cli-sdk/01-cli/02-cli-business-case/)
  - [GitHub Agentic Workflows](05-cli-sdk/01-cli/03-agentic-wf/)
  - [Extending the CLI with MCP Servers & Skills](05-cli-sdk/01-cli/04-mcp-skills/)
  - [Codebase Q&A and Onboarding](05-cli-sdk/01-cli/05-codebase-qa/)
- [Part 2: GitHub Copilot SDK](05-cli-sdk/02-sdk/)
  - [GitHub Copilot SDK](05-cli-sdk/02-sdk/01-sdk/)
  - [Copilot SDK Demos](05-cli-sdk/02-sdk/02-sdk-demos/)
  - [Implementing & Using MCP Apps](05-cli-sdk/02-sdk/03-mcp-apps/)
  - [Deploying an SDK Agent to Azure](05-cli-sdk/02-sdk/04-deploy-azure/)
  - [Building a Multi-Agent System](05-cli-sdk/02-sdk/05-multi-agent/)

## [Module 6: GitHub Copilot App](./06-copilot-app/)

- [Meet the Desktop Agents App](06-copilot-app/01-overview/)
- [Sessions from Issues, Prompts & Pull Requests](06-copilot-app/02-sessions/)
- [The Validation Loop](06-copilot-app/03-validation-loop/)
- [Scheduled Automations](06-copilot-app/04-automations/)
- [Syncing Skills & MCP Servers](06-copilot-app/05-sync/)
- [Configuring the App: Customize, Permissions & Models](06-copilot-app/06-configuration/)

## [Module 7: Agentic DevOps](./07-agentic-devops/)

- [IaC & Configuration (Azure CLI, SSH, Bicep & Terraform)](07-agentic-devops/01-iac-cfg/)
- [CI/CD with GitHub Actions](07-agentic-devops/02-cicd/)
- [Testing using Copilot](07-agentic-devops/03-testing/)
- [Documentation using Copilot](07-agentic-devops/04-documentation/)

## [Module 8: Governance, Cost & Observability](./08-governance/)

- [Trust, Safety & the Permission Model](08-governance/01-permissions/)
- [Cost Model & AI Credits](08-governance/02-cost/)
- [Enterprise Policy & Managed Settings](08-governance/03-enterprise-policy/)
- [Observability with OpenTelemetry](08-governance/04-observability/)
- [Cutting Token Cost with Open-Source Models](08-governance/05-open-source-models/)
  - [Using Open-Source Models in VS Code](08-governance/05-open-source-models/01-vscode/)
  - [Using Open-Source Models in the Copilot CLI](08-governance/05-open-source-models/02-copilot-cli/)
- [EU AI Act, GDPR & Accessibility Compliance](08-governance/06-compliance/)

## [Module 9: Spec-Driven Development & Delivery](./09-spec-driven-dev/)

- [Why Spec-Driven Development](09-spec-driven-dev/01-introduction/)
- [The Spec-Driven Workflow](09-spec-driven-dev/02-spec-driven-workflow/)
- [Sample Case: Implement a Product Feature](09-spec-driven-dev/03-sample-case/)

---

## Schedule

**Total duration: 4 days · 28.0 hours**
**Split: 70% instruction & demos (~19.5h) · 30% labs (~8.5h)**

| Day       | Modules                                    | Instruction & Demos |     Labs |     Total |
| --------- | ------------------------------------------ | ------------------: | -------: | --------: |
| **Day 1** | Module 1: Fundamentals & Agent Mode Basics |                2.5h |     1.0h |      3.5h |
|           | Module 2: GitHub Copilot Harness           |                3.0h |     1.5h |      4.5h |
| **Day 2** | Module 3: Implementing Agentic Coding      |                2.5h |     1.5h |      4.0h |
|           | Module 4: Agent Sessions & Agents Window   |                2.0h |     1.0h |      3.0h |
| **Day 3** | Module 5: GitHub Copilot CLI & SDK         |                1.5h |     1.0h |      2.5h |
|           | Module 6: GitHub Copilot App               |                2.0h |     0.5h |      2.5h |
|           | Module 7: Agentic DevOps                   |                2.5h |     0.5h |      3.0h |
| **Day 4** | Module 8: Governance, Cost & Obs.          |                1.5h |     0.5h |      2.0h |
|           | Module 9: Spec-Driven Dev & Delivery       |                2.0h |     1.0h |      3.0h |
| **Total** |                                            |           **19.5h** | **8.5h** | **28.0h** |

> Labs are hands-on exercises embedded at the end of each module. The lowest-risk first lab is the read-only `/research` agent in Module 4; labs that write to a repository state the permission level they require, and all labs assume Autopilot is the default permission level.
