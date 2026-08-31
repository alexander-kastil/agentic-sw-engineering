# Distributing Capabilities with Plugins

## Agent Plugins 1.0

Agent plugins are prepackaged bundles of chat customizations that you can discover and install from plugin marketplaces in Visual Studio Code. A single plugin can provide any combination of slash commands, agent skills, custom agents, hooks, and MCP servers. With Agent Plugins 1.0 (VS Code 1.133) the format is an open standard rather than a VS Code feature, so the portable parts of a plugin run in any host that implements the spec.

Portability has a boundary worth knowing before you author one. Skills and MCP servers are the portable core. The Copilot-specific pieces, custom agents and hooks and slash commands, live under the `com.github.copilot` namespace in `plugin.json` and apply only where a Copilot harness is running. Bundle the portable parts first and treat the namespaced block as the Copilot extension of a plugin that already stands on its own.

Plugins work alongside your locally defined customizations. When you install a plugin, its commands, skills, agents, hooks, and MCP servers appear in chat.

> **Note:** Agent plugins are currently in preview. Enable or disable support for agent plugins with the `chat.plugins.enabled` setting.

## What plugins provide

An agent plugin can bundle one or more of the following customization types:

| Type               | Description                                                                | Portability                    |
| ------------------ | -------------------------------------------------------------------------- | ------------------------------ |
| **Skills**         | Agent skills with instructions, scripts, and resources that load on-demand | Portable across hosts          |
| **MCP servers**    | MCP servers for external tool integrations                                 | Portable across hosts          |
| **Agents**         | Custom agents with specialized personas and tool configurations            | `com.github.copilot` namespace |
| **Hooks**          | Hooks that execute shell commands at agent lifecycle points                | `com.github.copilot` namespace |
| **Slash commands** | Additional commands you can invoke with `/` in chat                        | `com.github.copilot` namespace |

For example, a testing plugin might include a test-runner skill with scripts, a test-reviewer agent with read-only tools, and an MCP server for a test reporting dashboard. The plugin directory structure looks like this:

Text

```yaml
my-testing-plugin/
  plugin.json              # Plugin metadata and configuration
  skills/
    test-runner/
      SKILL.md             # Testing skill instructions
      run-tests.sh         # Supporting script
  agents/
    test-reviewer.agent.md # Code review agent
  hooks/
    post-test.json         # Hook to run after tests
```

The namespaced block keeps the portable manifest clean and makes the host-specific surface explicit:

```json
{
  "name": "my-testing-plugin",
  "version": "1.0.0",
  "skills": ["skills/test-runner"],
  "mcpServers": {
    "test-reports": { "command": "npx", "args": ["test-reports-mcp"] }
  },
  "com.github.copilot": {
    "agents": ["agents/test-reviewer.agent.md"],
    "hooks": ["hooks/post-test.json"]
  }
}
```

## Discovering and installing plugins

Search for `@agentPlugins` in the Extensions view, or run **Chat: Plugins** from the Command Palette (`Ctrl+Shift+P`).

## Links & Resources

- [VS Code 1.133 release notes](https://code.visualstudio.com/updates/v1_133) - Agent Plugins 1.0 as an open standard and the `com.github.copilot` namespace
- [Agent Plugins documentation](https://code.visualstudio.com/docs/copilot/customization/agent-plugins)
- [Awesome Copilot plugins](https://github.com/github/awesome-copilot)
