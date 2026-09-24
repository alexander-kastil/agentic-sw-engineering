# GitHub Copilot App

## Agents Outside the Editor

The GitHub Copilot app is a desktop agents view for macOS, Windows, and Linux that reached general availability in June 2026 and is now open to every Copilot plan, or to no plan at all when you point it at your own model provider. It shows what agentic development looks like beyond the editor: My Work gathers the issues and pull requests worth picking up, and a session starts from one of them, from a freeform prompt, or from a pull request already in flight, running in a new working tree, your local repository, or a GitHub-hosted cloud sandbox. Interactive, Plan, and Autopilot decide how much autonomy that session gets, and a built-in validation loop lets you review diffs, drive an in-app browser and terminal, open the pull request, and merge it without leaving the session. Repository MCP servers and skills sync automatically, automations turn them into scheduled or event-triggered work, and Customize manages the plugins, skills, MCP servers, and canvases that every session inherits.

| Topic | Description |
|-------|-------------|
| [Meet the Desktop Agents App](./01-overview/) | What the desktop app is, which plans and platforms it reaches, and a tour of the sidebar. |
| [Set Up Your Workspace: Projects, Customize & Sync](./02-setup/) | How repository skills and MCP servers sync, and the plugins, skills, MCP servers, and canvases Customize adds. |
| [My Work: Picking Up the Day](./03-my-work/) | Sections, custom views, filters you describe in plain words, and the Session column. |
| [Sessions from Issues, Prompts & Pull Requests](./04-sessions/) | Three entry points, three places a session can run, the session modes, permission modes, and the model. |
| [The Validation Loop](./05-validation-loop/) | Review diffs, use the in-app browser and terminal, read Insights, open the pull request, and merge it. |
| [Automations: Creating Them in the UI](./06-automations/) | Local and cloud automations, schedules, CRON, event triggers, session automations, and shareable links. |
| [Automations: Running & Maintaining Them](./07-automation-runs/) | Recent runs, run cost, answering a run that needs you, disabling, and session cleanup. |

## Links & Resources

- [About the GitHub Copilot app](https://docs.github.com/en/copilot/concepts/agents/github-copilot-app) - the official concept page for the desktop app, its plans, modes, and capabilities
- [GitHub Copilot app how-tos](https://docs.github.com/en/copilot/how-tos/github-copilot-app) - the task guides for sessions, automations, canvases, issues and pull requests, BYOK, and deep links
- [GitHub Copilot app](https://github.com/features/ai/github-app) - the product page for the desktop agents experience
- [GitHub Copilot app changelog](https://github.com/github/app/blob/main/changelog.md) - release notes for the desktop app, current through v1.1.23
