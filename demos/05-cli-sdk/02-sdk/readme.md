# GitHub Copilot SDK

## Embedding Agents in Your Applications

Move from using Copilot to building with it. The Copilot SDK embeds AI-powered agentic workflows directly into your own applications, and it runs on the same production-tested agent runtime as the Copilot CLI, so you define the behavior and Copilot handles planning, tool invocation, and execution. It is in Technical Preview across four first-party stacks (Python, TypeScript, Go, and .NET), with community SDKs for several more languages.

The module works from the SDK fundamentals to runnable demos and then to interactive MCP applications. You create a client, start a session, and define custom tools that the agent decides when to call, as the weather-assistant and code-reviewer demos show. MCP Apps then take it further, rendering interactive UIs such as charts, forms, and QR codes inline in the chat client rather than returning plain text.

| Topic | Description |
|-------|-------------|
| **[GitHub Copilot SDK](./01-sdk/)** | The SDK fundamentals: install for your stack, create a `CopilotClient`, open a session, and register custom tools the agent invokes on its own, all on the same runtime that powers the Copilot CLI, in Technical Preview for Python, TypeScript, Go, and .NET. |
| **[Copilot SDK Demos](./02-sdk-demos/)** | Two runnable TypeScript agents built step by step: a weather assistant that defines a `get_weather` tool and streams events as the agent chooses to call it, and a code reviewer that audits a codebase through tools you supply. |
| **[Implementing & Using MCP Apps](./03-mcp-apps/)** | Take MCP past plain text: a server declares a `ui://` resource so its tool renders an interactive UI (charts, forms, QR codes) inside the chat, demonstrated by a Python FastMCP QR-code server that draws its result in Copilot Chat. |
| **[Deploying an SDK Agent to Azure](./04-deploy-azure/)** | Take a local agent to a hosted service on Azure Container Apps or App Service, with the same sessions and tools, secrets in Key Vault, and optional Azure OpenAI bring-your-own-model. |
| **[Building a Multi-Agent System](./05-multi-agent/)** | Compose specialized SDK agents, a researcher, a builder, a reviewer, that each run in their own session and hand work to a coordinator for parallel, isolated execution. |

## Available Stacks

| Language | Install Command |
|----------|-----------------|
| Node.js / TypeScript | `npm install @github/copilot-sdk` |
| Python | `pip install github-copilot-sdk` |
| Go | `go get github.com/github/copilot-sdk/go` |
| .NET | `dotnet add package GitHub.Copilot.SDK` |

## Key Topics covered in this module

- [GitHub Copilot SDK Repository](https://github.com/github/copilot-sdk) - source, tutorials, and the cookbook of runnable samples
- [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md) - build your first SDK app end to end
- [Custom Tools Documentation](https://github.com/github/copilot-sdk/blob/main/docs/guides/tools.md) - define tools the agent calls on its own
- [MCP Apps Specification](https://github.com/modelcontextprotocol/ext-apps) - the standard for interactive UIs rendered from MCP servers
