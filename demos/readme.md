# Agentic Software Engineering using GitHub Copilot

Embark on a transformative four-day journey into agentic software engineering with GitHub Copilot, discovering how AI-powered tools revolutionize your coding productivity and architectural decisions. Whether you are a software engineer amplifying your capabilities, a solution architect exploring AI-assisted development, or a technical leader evaluating how AI agents enhance team workflows, this course gives you the knowledge and hands-on experience to leverage AI effectively in modern software development.

Your journey begins with GitHub Copilot Fundamentals, establishing a solid foundation in AI-assisted coding through inline suggestions, slash commands, context variables, and code review on pull requests. You will select and configure models with confidence, from hosted frontier models to bring-your-own-key endpoints, and see how Copilot Vision brings images and PDFs into chat. You will also work in the terminal the way agents do, understanding machine-readable output and command compression.

You then explore GitHub Copilot Artifacts and Tools, extending Copilot through instructions, prompt files, and the Model Context Protocol, with the GitHub MCP Registry as your discovery surface. This module introduces custom agents, agent skills, Copilot memory, and hooks so you can create personalized assistants tailored to your needs. You will shape Copilot's context window with compaction and session forking, and install prepackaged agent plugins that work across the CLI and editor from a single install.

A central focus is Agent Sessions and the Agents Window, the abstraction the product is now built around. You will run agents across multiple projects in a dedicated companion window, understand how the Agent Host Protocol keeps session state authoritative on a long-lived host, and drive remote sessions over SSH and dev tunnels for reproducible, cloud-backed environments. You will manage sessions at scale with side-by-side chats, session groups, background sends, and one-click banners that fix failing CI checks and address PR comments. You will also delegate to subagents, run the read-only `/research` agent, and troubleshoot with `/troubleshoot`.

Implementing Agentic Coding moves you from using Copilot to building sophisticated agentic solutions. You will work with local agents and Agent Mode for real-time assistance, delegate to cloud agents, and coordinate multi-agent orchestration for intricate challenges. You will use Anthropic Claude Code agents for advanced generation and analysis, and drive built-in browser tools that let agents open pages, read console errors, and verify their own web changes without an external server. The module closes with agent-led modernization, migrating a real Semantic Kernel application to the Microsoft Agent Framework.

In GitHub Copilot CLI and SDK, command-line interfaces and programmable SDKs unlock new dimensions of automation. This module presents real-world business cases, such as HR document update automation, showing how agentic workflows solve practical challenges beyond traditional coding. You will implement Copilot SDK solutions, learn that the agent host itself is built on the SDK, and integrate MCP applications to build enterprise-grade tools.

The course then steps outside the editor with the GitHub Copilot app, the desktop agents view for macOS, Windows, and Linux. You will start sessions from a GitHub issue, a freeform prompt, or an in-flight pull request, each running in its own isolated worktree. You will drive a validation loop that reviews diffs, uses the in-app browser and terminal, and merges the pull request, then turn skills and prompts into scheduled automations that run recurring work for you.

Agentic DevOps applies AI-assisted techniques to cloud automation and infrastructure as code. You will master Azure CLI automation, harness Bicep, Terraform, and the Azure Developer CLI in agentic mode, and build intelligent CI/CD with Azure DevOps Pipelines and GitHub Actions. This module shows how agents enable faster, more reliable deployments with reduced human error.

The commercial heart of the course is Governance, Cost and Observability, the content architects, team leads, and managers are here for. You will master the permission model, from Autopilot as the default level to terminal sandboxing, AI risk badges, and sensitive-prompt interception, replacing older auto-approval slash commands with a sound security posture. You will treat model choice as a budget decision under usage-based AI credits, apply enterprise managed settings via MDM and `managed-settings.json`, and instrument agents with OpenTelemetry traces feeding an Azure Managed Grafana dashboard.

The course closes with Spec-Driven Development and Delivery, approaching agentic solution design with clarity and purpose. You will learn specification-driven workflows, author a constitution, specification, and technical plan, and decompose complex requirements into actionable tasks with GitHub Spec Kit. You will then close the delivery loop by generating tests, including end-to-end Playwright suites, and producing documentation with Mermaid diagrams rendered in the Markdown preview, notebooks, and chat. By completing this course, you will architect AI-assisted solutions that drive innovation, accelerate development cycles, and enhance team capabilities across your organization.

## Duration

4 Days

## Audience

- Software Engineers interested in leveraging AI agents to enhance their coding productivity and capabilities
- Software Architects looking to understand how to integrate and manage AI agents within software development lifecycles
- Team Leads and Managers aiming to explore how AI agents can be utilized to optimize team workflows and project outcomes

## Prerequisites & Requirements

- Experience with software development at a professional level
- A GitHub Copilot license with a credit allowance, or a configured bring-your-own-key (BYOK) endpoint. Usage-based billing makes this a required setup step, not an optional one.

## [Module 1: GitHub Copilot Fundamentals](./01-fundamentals/)

- [Introduction & Copilot Vision](01-fundamentals/01-intro/)
- [Selecting & Configuring Models](01-fundamentals/02-models/)
- [AI Assisted Coding](01-fundamentals/03-ai-assisted-coding/)
- [Slash Commands](01-fundamentals/04-slash-commands/)
- [Context Variables](01-fundamentals/05-context-variables/)
- [Pull Requests & Code Reviews](01-fundamentals/06-pr-code-review/)
- [Management and Settings](01-fundamentals/07-mgmt-settings/)
- [Working in the Terminal](01-fundamentals/08-terminal/)

## [Module 2: GitHub Copilot Artifacts & Tools](./02-copilot-tools/)

- [Copilot Instructions](02-copilot-tools/01-instructions/)
- [Prompt Files](02-copilot-tools/02-prompts/)
- [Model Context Protocol & MCP Registry](02-copilot-tools/03-mcp/)
- [Custom Agents](02-copilot-tools/04-agents/)
  - [Agents Overview](02-copilot-tools/04-agents/01-agents-overview/)
  - [Repository Agents](02-copilot-tools/04-agents/02-repo-agents/)
  - [Claude Agents](02-copilot-tools/04-agents/03-claude-agents/)
- [Agent Skills](02-copilot-tools/05-skills/)
- [Agent Plugins](02-copilot-tools/06-plugins/)
- [Copilot Memory](02-copilot-tools/07-memory/)
- [Understanding and Shaping GitHub Copilot's Context Window](02-copilot-tools/08-context-window/)
- [GitHub Copilot Hooks](02-copilot-tools/09-hooks/)

## [Module 3: Agent Sessions & Agents Window](./03-agent-sessions/)

- [The Agents Window](03-agent-sessions/01-agents-window/)
- [Agent Host Protocol (AHP vs ACP)](03-agent-sessions/02-host-protocol/)
- [Remote Agent Sessions over SSH & Dev Tunnels](03-agent-sessions/03-remote-sessions/)
- [Session Management](03-agent-sessions/04-session-management/)
- [Session Persistence & /chronicle](03-agent-sessions/05-persistence/)
- [Subagents](03-agent-sessions/06-subagents/)
- [Deep Research with /research](03-agent-sessions/07-research/)
- [Troubleshooting Agent Sessions](03-agent-sessions/08-troubleshooting/)

## [Module 4: Implementing Agentic Coding](./04-agentic-coding/)

- [Using Local Agents and Agent Mode](04-agentic-coding/01-local/)
- [Delegating Tasks to Cloud Agents](04-agentic-coding/02-cloud/)
- [Multi-Agent Orchestration](04-agentic-coding/03-orchestration/)
- [Using Anthropic Claude Code Agents](04-agentic-coding/04-claude-code/)
- [Agentic Browser Automation](04-agentic-coding/05-browser-tools/)
- [Upgrading & Modernization](04-agentic-coding/06-upgrading/)

## [Module 5: GitHub Copilot CLI & SDK](./05-cli-sdk/)

- [GitHub Copilot CLI](05-cli-sdk/01-cli-intro/)
- [Business Case: HR Document Updates Automation](05-cli-sdk/02-cli-business-case/)
- [GitHub Agentic Workflows](05-cli-sdk/03-agentic-wf/)
- [GitHub Copilot SDK](05-cli-sdk/04-sdk/)
- [Copilot SDK Demos](05-cli-sdk/05-sdk-demos/)
- [Implementing & Using MCP Apps](05-cli-sdk/06-mcp-apps/)

## [Module 6: GitHub Copilot App](./06-copilot-app/)

- [Overview](06-copilot-app/01-overview/)
- [Sessions from Issues, Prompts & Pull Requests](06-copilot-app/02-sessions/)
- [The Validation Loop](06-copilot-app/03-validation-loop/)
- [Scheduled Automations](06-copilot-app/04-automations/)
- [Syncing Skills & MCP Servers](06-copilot-app/05-sync/)

## [Module 7: Agentic DevOps](./07-agentic-devops/)

- [Automation using Azure CLI](07-agentic-devops/01-azure-cli/)
- [Infrastructure as Code (azd, Bicep & Terraform)](07-agentic-devops/02-IaC/)
- [Azure DevOps Pipelines & GitHub Actions](07-agentic-devops/03-pipelines/)

## [Module 8: Governance, Cost & Observability](./08-governance/)

- [Trust, Safety & the Permission Model](08-governance/01-permissions/)
- [Cost Model & AI Credits](08-governance/02-cost/)
- [Enterprise Policy & Managed Settings](08-governance/03-enterprise-policy/)
- [Observability with OpenTelemetry](08-governance/04-observability/)

## [Module 9: Spec-Driven Development & Delivery](./09-spec-driven-dev/)

- [Spec Driven Development](09-spec-driven-dev/01-introduction/)
- [Spec-Driven Workflow](09-spec-driven-dev/02-spec-driven-workflow/)
- [Constitution, Specification and Technical Plan](09-spec-driven-dev/03-constitution/)
- [Tasks & Implementation](09-spec-driven-dev/04-tasks/)
- [Getting Started with GitHub Spec Kit](09-spec-driven-dev/05-requirements/)
- [Sample Case: Implement a Product Feature](09-spec-driven-dev/06-sample-case/)
- [Testing using Copilot](09-spec-driven-dev/07-testing/)
- [Documentation using Copilot](09-spec-driven-dev/08-documentation/)

---

## Schedule

**Total duration: 4 days · 27.5 hours**
**Split: 69% instruction & demos (~19h) · 31% labs (~8.5h)**

| Day       | Modules                                | Instruction & Demos |     Labs |     Total |
| --------- | -------------------------------------- | ------------------: | -------: | --------: |
| **Day 1** | Module 1: Fundamentals                 |                2.0h |     1.0h |      3.0h |
|           | Module 2: Artifacts & Tools            |                3.0h |     1.5h |      4.5h |
| **Day 2** | Module 3: Agent Sessions               |                2.5h |     1.0h |      3.5h |
|           | Module 4: Agentic Coding               |                2.5h |     1.5h |      4.0h |
| **Day 3** | Module 5: CLI & SDK                    |                1.5h |     0.5h |      2.0h |
|           | Module 6: GitHub Copilot App           |                1.5h |     0.5h |      2.0h |
|           | Module 7: Agentic DevOps               |                2.0h |     0.5h |      2.5h |
| **Day 4** | Module 8: Governance, Cost & Obs.      |                1.5h |     0.5h |      2.0h |
|           | Module 9: Spec-Driven Dev & Delivery   |                2.5h |     1.5h |      4.0h |
| **Total** |                                        |           **19.0h** | **8.5h** | **27.5h** |

> Labs are hands-on exercises embedded at the end of each module. The lowest-risk first lab is the read-only `/research` agent in Module 3; labs that write to a repository state the permission level they require, and all labs assume Autopilot is the default permission level.
