# Copilot Plugins

## Agent plugins in VS Code (Preview)

Agent plugins are prepackaged bundles of chat customizations that you can discover and install from plugin marketplaces in Visual Studio Code. A single plugin can provide any combination of slash commands, agent skills, custom agents, hooks, and MCP servers.

Plugins work alongside your locally defined customizations. When you install a plugin, its commands, skills, agents, hooks, and MCP servers appear in chat.

> **Note:** Agent plugins are currently in preview. Enable or disable support for agent plugins with the `chat.plugins.enabled` setting.

## What plugins provide

An agent plugin can bundle one or more of the following customization types:

| Type               | Description                                                                |
| ------------------ | -------------------------------------------------------------------------- |
| **Slash commands** | Additional commands you can invoke with `/` in chat                        |
| **Skills**         | Agent skills with instructions, scripts, and resources that load on-demand |
| **Agents**         | Custom agents with specialized personas and tool configurations            |
| **Hooks**          | Hooks that execute shell commands at agent lifecycle points                |
| **MCP servers**    | MCP servers for external tool integrations                                 |

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

## Discovering and installing plugins

Search for `@agentPlugins` in the Extensions view, or run **Chat: Plugins** from the Command Palette (`Ctrl+Shift+P`).

## Links & Resources

- [Agent Plugins documentation](https://code.visualstudio.com/docs/copilot/customization/agent-plugins)
- [Awesome Copilot plugins](https://github.com/github/awesome-copilot)
