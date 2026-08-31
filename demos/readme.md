# Agentic Software Engineering using GitHub Copilot

Embark on a transformative four-day journey into agentic software engineering with GitHub Copilot, and discover how AI-powered tools reshape your coding productivity and architectural decisions. Whether you are a software engineer amplifying your capabilities, a solution architect exploring AI-assisted development, or a technical leader evaluating how AI agents enhance team workflows, this course gives you the knowledge and hands-on experience to leverage AI effectively in modern software development.

Your journey begins with Fundamentals and Agent Mode Basics, a solid foundation in AI-assisted coding through prompting, inline suggestions, slash commands, context variables, and code review on pull requests. You select and configure models with confidence, from hosted frontier models to bring-your-own-key endpoints, and see how Copilot Vision brings images and PDFs into chat. You move into Agent Mode early, driving a local agent through real, multi-step work, and learn to work in the terminal the way agents do.

You then assemble the GitHub Copilot Harness, extending Copilot through instructions, prompt files, and the Model Context Protocol, with the MCP Registry as your discovery surface. This module adds custom agents, reusable skills, Copilot memory, and hooks, teaches you to optimize the context window with prompt caching, and installs prepackaged plugins that work across the CLI and editor from a single install.

In Implementing Agentic Coding you put agents to work, building up from the simplest delegation. You drive local agents in agent mode, delegate large jobs to cloud agents, and coordinate a team of subject-matter-expert subagents through an orchestrator that runs independent work in parallel. You drive built-in browser tools that let agents open pages, read console errors, and verify their own web changes, then close with an agent-led modernization from Semantic Kernel to the Microsoft Agent Framework.

Agent Sessions then covers the infrastructure underneath the runs you just drove, the abstraction the product is now built around. You run agents across multiple projects in a dedicated companion window, understand how the Agent Host Protocol keeps session state authoritative on a long-lived host, and drive remote sessions over SSH and dev tunnels. You manage sessions at scale with groups, background sends, and one-click banners that fix failing CI checks, run the read-only `/research` agent for a cited report, then troubleshoot a stalled session with `/troubleshoot`.

The GitHub Copilot CLI brings the agent to the command line. You install it, drive the interactive shell with slash commands and natural language, switch models on the fly, and hand multi-step work to Autopilot. A real HR document-automation business case over Work IQ and SharePoint MCP servers shows the payoff, and GitHub Agentic Workflows turn those jobs into versioned, scheduled runs that open pull requests.

The same module continues with the GitHub Copilot SDK, which embeds those capabilities into your own applications. Running on the same production runtime as the CLI, it is available in Technical Preview for Python, TypeScript, Go, and .NET, so you create a session and define custom tools while Copilot handles planning and execution. You build runnable agents, deploy one to Azure, and extend them with MCP Apps that render interactive UIs inline in chat.

The course then steps outside the editor with the GitHub Copilot app, the desktop agents view for macOS, Windows, and Linux. You start sessions from a GitHub issue, a freeform prompt, or an in-flight pull request, each in its own isolated worktree, drive a validation loop that reviews diffs and merges the pull request, and turn skills and prompts into scheduled automations.

Agentic DevOps applies these techniques to cloud automation and infrastructure as code. You master Azure CLI automation, harness Bicep, Terraform, and the Azure Developer CLI in agentic mode, and build intelligent CI/CD with Azure DevOps Pipelines and GitHub Actions. You also close the quality loop here, generating tests including end-to-end Playwright suites and producing documentation with Mermaid diagrams.

Governance, Cost and Observability is the commercial heart for architects, team leads, and managers. You master the permission model, from Autopilot to terminal sandboxing, risk badges, and sensitive-prompt interception, treat model choice as a budget decision under usage-based credits, cut that cost with open-source models, apply enterprise managed settings via MDM, and instrument agents with OpenTelemetry traces feeding an Azure Managed Grafana dashboard. You also cover the regulatory compliance that attaches to the software your agents ship.

The course closes with Spec-Driven Development and Delivery. You learn specification-driven workflows, author a constitution, specification, and technical plan, decompose complex requirements into tasks with GitHub Spec Kit, and implement a product feature end to end from its specification. By completing this course, you will architect AI-assisted solutions that accelerate development cycles and strengthen your team's capabilities.
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
- [AI-Assisted Coding Essentials](01-fundamentals/03-ai-assisted-coding/)
- [Agent Mode Basics](01-fundamentals/04-agent-mode-basics/)
- [Pull Requests & Code Reviews](01-fundamentals/05-pr-code-review/)
- [Configuring & Governing Copilot](01-fundamentals/06-mgmt-settings/)
- [Working in the Terminal](01-fundamentals/07-terminal/)

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
- [Shaping the Context Window](02-agentic-harness/08-context-window/)
- [GitHub Copilot Hooks](02-agentic-harness/09-hooks/)

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

## [Module 7: Agentic DevOps](./07-agentic-devops/)

- [Automation using Azure CLI](07-agentic-devops/01-azure-cli/)
- [Infrastructure as Code (azd, Bicep & Terraform)](07-agentic-devops/02-IaC/)
- [Azure DevOps Pipelines & GitHub Actions](07-agentic-devops/03-pipelines/)
- [Testing using Copilot](07-agentic-devops/04-testing/)
- [Documentation using Copilot](07-agentic-devops/05-documentation/)

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

- [Spec Driven Development](09-spec-driven-dev/01-introduction/)
- [Spec-Driven Workflow](09-spec-driven-dev/02-spec-driven-workflow/)
- [Constitution, Specification and Technical Plan](09-spec-driven-dev/03-constitution/)
- [Tasks & Implementation](09-spec-driven-dev/04-tasks/)
- [Sample Case: Implement a Product Feature](09-spec-driven-dev/05-sample-case/)
- [Getting Started with GitHub Spec Kit](09-spec-driven-dev/06-requirements/)

---

## Schedule

**Total duration: 4 days · 27.5 hours**
**Split: 69% instruction & demos (~19h) · 31% labs (~8.5h)**

| Day       | Modules                                    | Instruction & Demos |     Labs |     Total |
| --------- | ------------------------------------------ | ------------------: | -------: | --------: |
| **Day 1** | Module 1: Fundamentals & Agent Mode Basics |                2.5h |     1.0h |      3.5h |
|           | Module 2: GitHub Copilot Harness           |                3.0h |     1.5h |      4.5h |
| **Day 2** | Module 3: Implementing Agentic Coding      |                2.5h |     1.5h |      4.0h |
|           | Module 4: Agent Sessions & Agents Window   |                2.0h |     1.0h |      3.0h |
| **Day 3** | Module 5: GitHub Copilot CLI & SDK         |                1.5h |     1.0h |      2.5h |
|           | Module 6: GitHub Copilot App               |                1.5h |     0.5h |      2.0h |
|           | Module 7: Agentic DevOps                   |                2.5h |     0.5h |      3.0h |
| **Day 4** | Module 8: Governance, Cost & Obs.          |                1.5h |     0.5h |      2.0h |
|           | Module 9: Spec-Driven Dev & Delivery       |                2.0h |     1.0h |      3.0h |
| **Total** |                                            |           **19.0h** | **8.5h** | **27.5h** |

> Labs are hands-on exercises embedded at the end of each module. The lowest-risk first lab is the read-only `/research` agent in Module 4; labs that write to a repository state the permission level they require, and all labs assume Autopilot is the default permission level.
