# GitHub Copilot CLI

## AI-Powered Terminal Development

GitHub Copilot CLI brings the agent to your terminal, so command discovery, code generation, and multi-step automation happen without leaving the shell. You install it with `npm install -g @github/copilot` (or WinGet on Windows), launch the interactive `copilot` shell, and authenticate with `/login`. Inside the shell you drive work with slash commands and natural-language prompts, switch models with `/model`, and press Shift+Tab for Autopilot mode when you want it to handle a multi-step task on its own.

The module moves from the basics to a real business case and then to scheduled automation. The HR Document Updates case shows the CLI orchestrating Work IQ and SharePoint MCP servers to find flagged documents and email a summary, and GitHub Agentic Workflows (the `gh aw` extension) turns that kind of job into a versioned workflow that runs on a schedule or a trigger. Together they show the CLI as both an interactive assistant and an automation engine.

| Topic | Description |
|-------|-------------|
| **[GitHub Copilot CLI](./01-cli-intro/)** | Install the CLI (`npm i -g @github/copilot` or WinGet) and authenticate with `/login`, then run the interactive shell: discover and explain commands with `/suggest` and `/explain`, switch models with `/model`, and hand multi-step tasks to Autopilot with Shift+Tab. |
| **[Business Case: HR Document Updates Automation](./02-cli-business-case/)** | A production-style automation where the CLI queries a SharePoint HR-Documents library through Work IQ and SharePoint MCP servers, collects every document flagged "Needs Update" with its metadata, and emails a formatted summary to HR leadership on demand or on a schedule. |
| **[GitHub Agentic Workflows](./03-agentic-wf/)** | Install the `gh aw` extension and turn a prompt into a versioned Markdown workflow that runs on a schedule or trigger; scaffold one with `gh aw add-wizard` and let it open a pull request with the results. |
| **[Extending the CLI with MCP Servers & Skills](./04-mcp-skills/)** | Connect the CLI to external systems with `/mcp` and load reusable Agent Skills with `/skills`, turning the shell into a domain-aware agent. |
| **[Codebase Q&A and Onboarding](./05-codebase-qa/)** | Point the CLI at an unfamiliar repo to trace how a feature works, find where behavior lives, and generate a grounded onboarding overview from the terminal. |

## Helpful Copilot CLI Commands

These are commands of the interactive `copilot` shell and the `gh aw` extension, specific to running and automating agents from the terminal.

| Command | Usage |
|---|---|
| `/login` | Authenticate the CLI with your GitHub account or a Personal Access Token |
| `/suggest <task>` | Ask Copilot to suggest a shell command for a task |
| `/explain <command>` | Ask Copilot to explain an unfamiliar shell command |
| `/model <model>` | Switch the AI model the CLI uses |
| `/mcp` | Manage MCP server configuration for the session |
| `/skills` | Manage skills that extend the CLI's capabilities |
| `gh aw add-wizard <workflow>` | Add a GitHub Agentic Workflow to the repo on a new branch via a pull request |

> Note: Autopilot mode (Shift+Tab) lets the CLI run multi-step tasks without pausing at each action. Reserve it for trusted repositories, since it acts with fewer prompts.

## Key Topics covered in this module

- [GitHub Copilot CLI Repository](https://github.com/github/copilot-cli) - source, releases, and issue tracker for the CLI
- [About Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) - official concept and usage documentation
- [GitHub Agentic Workflows](https://github.github.com/gh-aw/introduction/overview/) - the `gh aw` extension for versioned, scheduled agent workflows
