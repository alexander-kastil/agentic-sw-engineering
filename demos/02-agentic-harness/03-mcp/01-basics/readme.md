# MCP Basics & the MCP Registry

Model Context Protocol (MCP) is a standardized framework that enables GitHub Copilot to connect to external tools, services, and data sources. It acts as a bridge between Copilot and specialized systems—allowing Copilot to access real-time information, execute commands, and interact with platforms like GitHub, Azure, or deployment services. MCPs extend Copilot's capabilities beyond code generation to include infrastructure management, testing automation, and domain-specific tooling.

![VS Code MCP Server Management Interface - showing available MCP servers and their configuration status](_images/manage-mcp.png)

The MCP ecosystem provides both local executables for direct system access and remote HTTP endpoints for cloud services, enabling seamless integration of specialized capabilities into your Copilot workflows.

## Enable MCP Discovery and Auto-Start

Configure VS Code to auto-discover and start MCP servers:

```json
{
  "chat.mcp.discovery.enabled": {
    "claude-desktop": true
  },
  "chat.mcp.autostart": "newAndOutdated",
  "chat.mcp.gallery.enabled": true
}
```

## MCP Server Types & Integration

MCP servers can be integrated in multiple ways depending on their nature: **local executables** (via `npx` or `stdio` commands) and **remote HTTP endpoints** for cloud services.

You can configure MCPs in the following ways:

- **Global configuration**
  - Available across all workspaces for persistent access
  - `~/.mcp.json` on Linux/macOS,
  - `%USERPROFILE%\.mcp.json` on Windows
- **Workspace-level configuration**
  - Scoped to the current project to isolate tools for specific needs
  - (`.vscode/mcp.json` in the workspace root):

MCPs can come from:

- VS Code extensions
- npm packages
- Custom implementations

## MCP Configuration

The [mcp.json](/.vscode/mcp.json) file contains server definitions organized by name, with each server specifying its type (`stdio`, `http`), command/URL, and optional arguments. For sensitive data (API keys, passwords, organization names), MCPs support **input parameters** that prompt for values at runtime and pass them securely via environment or URL variables, preventing hardcoding of credentials.

### Structure Example

```json
{
  "servers": {
    "server-name": {
      "command": "npx",
      "args": ["@package/mcp", "--option=value"],
      "type": "stdio"
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "API_KEY",
      "description": "Your API key",
      "password": true
    }
  ]
}
```

## Common MCPs for Development Workflows

In this class we have [registered](/.vscode/mcp.json) several MCP servers that integrate with popular development tools and platforms. These MCPs enable Copilot to interact with GitHub, Azure, Microsoft 365, design systems, and remote servers directly from your VS Code environment.

| MCP             | Type            | Purpose                                                                                                  |
| --------------- | --------------- | -------------------------------------------------------------------------------------------------------- |
| Microsoft Learn | Remote (HTTP)   | Official Microsoft documentation and code samples for Azure, .NET, and Microsoft 365 services.           |
| Context7        | Remote (HTTP)   | Library documentation and code examples for any programming language or framework with up-to-date docs.  |
| Azure Deploy    | Local (`npx`)   | Infrastructure deployment and management for Azure resources with CLI-based orchestration.               |
| GitHub          | Remote (HTTP)   | GitHub API integration for repositories, issues, pull requests, and project management.                  |
| WorkIQ          | Local (`stdio`) | Microsoft 365 integration for accessing emails, meetings, files, and work context across Microsoft apps. |
| SSH MCP         | Local (`stdio`) | Remote server management via SSH for infrastructure provisioning, diagnostics, and system configuration. |
| Playwright      | Local (`stdio`) | Browser automation with vision support for automated visual testing, screenshot capture, and E2E tests.  |
| Chrome DevTools | Local (`stdio`) | Chrome DevTools protocol integration for browser debugging, performance profiling, and DOM inspection.   |
| Devcontainers   | Local (`stdio`) | Devcontainer configuration analysis and scaffolding for optimized development environments.              |

## Copilot Connectors: GitHub-Managed MCP Servers

Every server in the table above needs setup on your machine: an entry in `mcp.json`, a package to run or a URL to reach, and often a key. Copilot connectors remove that work for popular services. A Copilot connector is a GitHub-managed MCP server that connects the agent to services such as Slack, Notion and Microsoft Learn, without local server setup or MCP configuration. Since VS Code 1.144 connectors are available as a Preview.

You find them in **Browse**, the home page for Customizations. Choose **Copilot Connectors** in the source menu, select **Connect** on a service, and authorize access in the browser. You connect once, and the connection is reused across supported Copilot clients signed in with the same account. A service you authorized in VS Code therefore needs no second setup in another client.

A connector and a self-configured MCP server give the agent the same kind of capability: tools it can call. They differ in who runs the server and who owns the setup.

| Aspect | Copilot connector | Self-configured MCP server |
| ------ | ----------------- | -------------------------- |
| Where you set it up | **Browse**, with **Connect** | `mcp.json` or an extension |
| Who runs the server | GitHub manages it | You run it (`stdio`) or point at its URL (`http`) |
| Credentials | You authorize access in the browser | Input parameters you define in `mcp.json` |
| Reuse | Across supported Copilot clients on the same account | Per user or per workspace configuration file |
| Choice of server | The services listed under **Copilot Connectors** | Any MCP server, including your own |

Connectors are enabled by default on all Copilot plans, and they work only with the Copilot harness. On Business and Enterprise plans an administrator must enable Editor preview features first. The organization's MCP restrictions apply to connectors as they do to any other server, and some services require administrator approval before you can connect.

Reach for a connector when the service you need is in the list: you save the configuration file, the key handling and the update chores. Write your own `mcp.json` entry for internal systems, for local tools such as a browser or a shell, and for anything a connector does not cover. Both kinds appear to the agent as ordinary tools, so a prompt does not change between them.

> Note: Connectors are a VS Code Preview feature that needs the Copilot harness. Other IDEs and chat surfaces keep using the `mcp.json` route described above.

## MCP Use Cases & Sample Workflows

### Chrome DevTools

Chrome DevTools MCP enables browser debugging, performance profiling, and automated visual testing directly from Copilot. Use it to inspect DOM elements, capture screenshots, analyze network waterfall charts, and verify responsive design at specific breakpoints.

Sample prompt:

```text
Navigate to http://localhost:3000, take a screenshot of the homepage,
then check the CSS for accessibility colors and contrast ratios on the
primary button element using the accessibility tree.
```

### Microsoft Learn

Microsoft Learn MCP provides access to official Microsoft documentation, code samples, and best practices for Azure, .NET, and Microsoft 365 services. Use it to retrieve the latest service APIs, architecture guidance, and implementation examples during development and architecture planning.

Sample prompt:

```text
Search Microsoft Learn for Azure Cosmos DB best practices for
hierarchical partition keys and vector search, then fetch the
full documentation on modeling strategies for IoT scenarios.
```

### WorkIQ

WorkIQ MCP connects to Microsoft 365 data including emails, meetings, files, and organizational context. Use it to inspect work history, retrieve contextual information from recent communications, and integrate task management seamlessly into your development workflow.

Sample prompt:

```text
Ask WorkIQ: What are the recent emails about the deployment
project? Summarize action items and blockers mentioned in
conversations from the last week.
```

## Demo: Connect Microsoft Learn Through a Copilot Connector

### Step 1: Connect a service and use it

1. Run **Chat: Open Customizations** from the Command Palette and select **Browse**.
2. Choose **Copilot Connectors** in the source menu.
3. Select **Connect** on **Microsoft Learn** and authorize access in the browser.
4. Open a chat with the Copilot harness and send this prompt:

```text
Search Microsoft Learn for Azure Cosmos DB hierarchical partition keys and summarize the three most important design rules.
```

Then send a follow-up that reuses the same connection:

```text
Using the same source, show a short C# snippet that creates a container with such a partition key.
```

Expected result: the agent calls a Microsoft Learn tool and answers from the documentation, and no entry was added to `mcp.json`.

## Links & Resources

- [VS Code MCP Servers Documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [Copilot connectors](https://code.visualstudio.com/docs/agent-customization/copilot-connectors) - connect GitHub-managed MCP servers from Browse, availability and administrator requirements
