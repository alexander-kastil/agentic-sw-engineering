# GitHub Copilot Harness

## Copilot Customization Overview

Copilot customization enables you to tailor AI behavior for your specific workflows, team standards, and project requirements. VS Code provides multiple layers of customization, from general repository rules to reusable prompts, model context protocols, custom agents, and specialized skills, that work together to optimize both LLM context window efficiency and consistency across your organization.

## Customization Features

| Feature | Purpose |
| ------- | ------- |
| **[Copilot Instructions](./01-instructions/)** | Repository-wide and stack-specific guidelines that shape AI behavior. General instructions establish security policies, naming conventions, and coding philosophy, while stack-specific instructions (Angular, .NET, Azure CLI, Documentation) provide technology-focused conventions. Loaded on-demand to keep context efficient. |
| **[Prompt Files](./02-prompts/)** | Reusable, on-demand prompt files (`.prompt.md`) for common workflows like documentation generation, code reviews, and scaffolding. Triggered explicitly in chat and can reference custom agents, tools, and models. Enables standardized development workflows across teams. |
| **[Model Context Protocol & MCP Registry](./03-mcp/)** | MCP from both ends, in two parts. [Basics](./03-mcp/01-basics/) covers discovering and configuring servers, local executables (npx, stdio) and remote HTTP endpoints, and workspace versus global `mcp.json`. [Implementing](./03-mcp/02-implementing/) covers writing your own servers in Python and C#, transports, state, and the MCP Inspector. |
| **[Agent Skills](./04-skills/)** | Portable folders of instructions, scripts, and resources that follow the open Agent Skills standard. Load on-demand when relevant, enabling reusable capabilities across VS Code, GitHub Copilot CLI, and coding agents without manual activation. |
| **[Custom Agents](./05-agents/)** | Custom AI personas configured with specific tools, instructions, and handoffs to handle targeted development tasks. Learn about agent concepts, then explore the custom agents this repository ships. |
| **[Agent Plugins](./06-plugins/)** | Prepackaged bundles of chat customizations (skills, commands, agents, MCP servers, and hooks) that can be installed directly from the Extensions view. Search for `@agentPlugins` in the Extensions view or run `Chat: Plugins` from the Command Palette. |
| **[Copilot Memory](./07-memory/)** | Persistent context storage that enables Copilot to retain information across conversations and sessions. Use memory to store project details, team preferences, and task state, allowing AI interactions to remain consistent and contextually aware throughout extended development workflows. |
| **[Shaping the Context Window](./08-context-window/)** | Advanced techniques for structuring context to improve Copilot's understanding and suggestions. This involves understanding how Copilot processes information and optimizing your prompts and context to yield better results. |
| **[GitHub Copilot Hooks](./09-hooks/)** | Extend agent behavior by executing custom shell commands at key points during agent execution. Hooks enable logging, validation, notifications, and custom integrations by triggering on session events, tool invocations, and agent lifecycle changes without modifying agent code. |

## Links & Resources

- [VS Code Copilot Customization Overview](https://code.visualstudio.com/docs/copilot/customization/overview)
- [Awesome Copilot - Copilot Tools & Artifacts](https://github.com/github/awesome-copilot)
