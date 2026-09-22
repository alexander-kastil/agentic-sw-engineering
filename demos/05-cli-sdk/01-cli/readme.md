# GitHub Copilot CLI


## AI-Powered Terminal Development

GitHub Copilot CLI brings the agent to your terminal, so command discovery, code generation, and multi-step automation happen without leaving the shell. You install it with `npm install -g @github/copilot` (or WinGet on Windows), launch the interactive `copilot` shell, and authenticate with `/login`. Inside the shell you drive work with slash commands and natural-language prompts, switch models with `/model`, and press Shift+Tab to move between interactive, plan, and autopilot mode. For scripts and scheduled jobs the same agent runs headless with `copilot -p "<prompt>" --allow-all-tools`.

The module moves from the basics through extending the CLI with MCP servers and skills to a real business case and then to scheduled automation. The HR Document Updates case shows the CLI orchestrating Work IQ and SharePoint MCP servers to find flagged documents and email a summary, and GitHub Agentic Workflows (the `gh aw` extension) turns that kind of job into a versioned workflow that runs on a schedule or a trigger. Together they show the CLI as both an interactive assistant and an automation engine.

| Topic | Description |
|-------|-------------|
| **[GitHub Copilot CLI](./01-intro/)** | Install the CLI (`npm i -g @github/copilot` or WinGet) and authenticate with `/login`, then run the interactive shell: ask for commands and explanations in plain language, pull files in with `@`, switch models with `/model`, and hand multi-step tasks to autopilot with Shift+Tab. |
| **[Extending the CLI with MCP Servers & Skills](./02-mcp-skills/)** | Connect the CLI to external systems with `/mcp` and load reusable Agent Skills with `/skills`, then bundle both as an Agent Plugin so the same capabilities travel to the editor. |
| **[Business Case: HR Document Updates Automation](./03-business-case/)** | A production-style automation where the CLI queries a SharePoint HR-Documents library through Work IQ and SharePoint MCP servers, collects every document flagged "Needs Update" with its metadata, and emails a formatted summary to HR leadership on demand or on a schedule. |
| **[GitHub Agentic Workflows](./04-agentic-wf/)** | Install the `gh aw` extension and turn a prompt into a versioned Markdown workflow that runs on a schedule or trigger; scaffold one with `gh aw add-wizard` and let it open a pull request with the results. |
| **[Codebase Q&A and Onboarding (optional)](./05-codebase-qa/)** | Point the CLI at an unfamiliar repo to trace how a feature works, find where behavior lives, and generate a grounded onboarding overview from the terminal. |
| **[Deep Research with /research (optional)](./06-research/)** | Run the read-only research agent over GitHub search and web sources, then judge the citations behind what it reports. |
| **[A Second Opinion with /rubber-duck (optional)](./07-rubber-duck/)** | Hand a plan or a finished run to the critic agent and read what it says was missed, without changing any code. |

## Helpful Copilot CLI Commands

These are commands of the interactive `copilot` shell and the `gh aw` extension, specific to running and automating agents from the terminal.

| Command | Usage |
|---|---|
| `/login` | Log in to Copilot |
| `/model` | Select the AI model for this session |
| `/agent` | Browse and select the agent that handles the next turn |
| `/research` | Run a deep research investigation over GitHub search and web sources |
| `/rubber-duck` | Get an independent critique of the current work from the rubber duck agent |
| `/mcp` | Manage MCP server configuration for the session |
| `/skills` | Manage skills that extend the CLI's capabilities |
| `/plugin` | Manage plugins and plugin marketplaces |
| `/autopilot` | Toggle autopilot mode, or set an autopilot objective |
| `/env` | Show the instructions, servers, skills, agents, hooks, and plugins the session loaded |
| `gh aw add-wizard <workflow>` | Add a GitHub Agentic Workflow to the repo on a new branch via a pull request |

> Note: Autopilot mode (Shift+Tab, or `/autopilot`) lets the CLI run multi-step tasks without pausing at each action. Reserve it for trusted repositories, since it acts with fewer prompts.

## Key Topics covered in this module

- [About Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) - sessions, permissions, and the agent runtime behind the shell
- [Using Copilot CLI](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli) - install, sign in, and run the CLI interactively or headless
- [GitHub Agentic Workflows](https://github.github.com/gh-aw/introduction/overview/) - the `gh aw` extension for versioned, scheduled agent workflows
- [GitHub Copilot CLI repository](https://github.com/github/copilot-cli) - releases, changelog, and issue tracker for the CLI

[← Back to CLI & SDK](../readme.md) | [Next: GitHub Copilot SDK →](../02-sdk/readme.md)
