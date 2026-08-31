# Extending the CLI with MCP Servers & Skills

The Copilot CLI is not limited to shell help. Two mechanisms turn it into a domain-aware agent: MCP servers connect it to external tools and data, and Agent Skills load reusable, on-demand capabilities. Both are managed from inside the interactive shell, so you extend the agent without leaving the terminal.

## MCP servers

The `/mcp` command manages the Model Context Protocol servers available to the session. Point the CLI at a GitHub, SharePoint, database, or custom server and the agent can query and act on those systems as tools during a task. This is the same mechanism the HR Document Updates business case uses to reach SharePoint through Work IQ.

## Agent Skills

The `/skills` command manages skills, portable folders of instructions, scripts, and resources that follow the open Agent Skills standard. The CLI loads a skill on demand when a task matches it, so a capability you define once is reused across the CLI, VS Code, and coding agents without manual activation.

## Bundling both as a plugin

Managing servers and skills one command at a time works, but it does not travel. Agent Plugins 1.0 (VS Code 1.133) replaces those per-tool layouts with one open standard: a package carrying `plugin.json`, a `skills/` directory, and `mcp.json`, plus a `com.github.copilot/` namespace for agents, commands, rules, and `hooks.json`. The Copilot CLI supports that namespace, so a plugin you install brings the same servers and skills the editor gets.

Reach for a plugin when a capability is worth sharing with your team or across your own machines, and keep `/mcp` and `/skills` for the one-off servers and skills that belong to a single session. [Agent Plugins](../../../02-agentic-harness/06-plugins/) covers the format in full.

## Exercise

1. Run `/mcp` and add an MCP server (for example the GitHub server), then ask the CLI a question that requires it.
2. Run `/skills` and inspect the skills available to the session.
3. Give the CLI a task that a skill covers, and confirm it loads the skill on its own.
4. Install an agent plugin that ships both a skill and an MCP server, then confirm with `/mcp` and `/skills` that both arrived from the one package.

## Links & Resources

- [About Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) - CLI concepts including MCP and skills
- [Model Context Protocol](https://modelcontextprotocol.io/introduction) - the open standard for connecting agents to tools and data
- [VS Code 1.133 release notes](https://code.visualstudio.com/updates/v1_133) - Agent Plugins 1.0 and the `com.github.copilot` namespace the CLI supports
