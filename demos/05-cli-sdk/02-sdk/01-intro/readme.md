# SDK Fundamentals

The GitHub Copilot SDK enables you to embed AI-powered agentic workflows directly into your applications. Built on the same production-tested agent runtime as Copilot CLI and the Copilot agent in VS Code's agent host, the SDK handles planning, tool invocation, and code execution: you define the behavior and Copilot handles the complexity. Each SDK drives a Copilot CLI running in server mode over JSON-RPC, and manages that process for you.

## Use Cases

- Build intelligent assistants that can understand code context and execute complex tasks autonomously.
- Integrate AI agents into development tools, IDEs, and code analysis platforms without building custom orchestration.
- Create custom agents tailored to specific workflows: code review agents, documentation generators, or deployment helpers.
- Enable agents to interact with external services and repositories through Model Context Protocol (MCP) servers.
- Develop terminal-based or web-based applications that delegate coding tasks to AI-powered agents.

## Available Stacks

| Language             | Install Command                              |
| -------------------- | -------------------------------------------- |
| Node.js / TypeScript | `npm install @github/copilot-sdk`            |
| Python               | `pip install github-copilot-sdk`             |
| Go                   | `go get github.com/github/copilot-sdk/go`    |
| .NET                 | `dotnet add package GitHub.Copilot.SDK`      |
| Rust                 | `cargo add github-copilot-sdk`               |
| Java                 | Maven coordinates `com.github:copilot-sdk-java` |

All six are first-party and released together from the `github/copilot-sdk` repository.

## Getting Started

### Prerequisites

The Node.js, Python, and .NET packages bundle the Copilot CLI, so you only need to be signed in. The Go, Java, and Rust SDKs expect `copilot` on your PATH.

```bash
copilot --version
copilot
```

Run `/login` inside the shell once, or export `GITHUB_TOKEN`, `GH_TOKEN`, or `COPILOT_GITHUB_TOKEN` when your app runs unattended. For the runtimes: the Node.js package requires Node 20.19 or later (or 22.12 or later), and the .NET package targets net8.0, net10.0, and netstandard2.0.

### Basic Usage

Create a client, start a session, and send your first message. Here's a minimal example in TypeScript:

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({ model: "gpt-5-mini" });
const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);
await client.stop();
```

### Core Features

- Send messages and receive responses with `sendAndWait()`, or fire and forget with `send()`.
- Stream responses in real time by subscribing to `assistant.message_delta` events and reading `event.data.deltaContent`.
- Create custom tools that Copilot can call using `defineTool()` with a name, description, parameter schema, and handler.
- Connect to MCP servers to extend agent capabilities with pre-built tools.
- Define custom agents with specialized system messages and behaviors.
- Ask the runtime which models your account can use with `client.listModels()` rather than hardcoding one.

### Key Concepts

Copilot manages the entire agent lifecycle: when you define a tool, Copilot decides when to call it based on the user's prompt. The SDK handles parameter validation, handler execution, and response integration.

For a complete tutorial with examples, see the [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md).

## Demo

| Name                                                   | Description                                                                                 |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| **[Copilot SDK Console Demo](./copilot-sdk-console/)** | Simple .NET 10 console application demonstrating the GitHub Copilot SDK with OpenAI models. |

## Links & Resources

- [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md) - client, session, and first message in every supported language
- [Authenticating the SDK](https://github.com/github/copilot-sdk/blob/main/docs/auth/authenticate.md) - interactive login, tokens, and unattended service auth
- [Bring your own key](https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md) - point a session at your own model provider
- [MCP in the SDK](https://github.com/github/copilot-sdk/blob/main/docs/features/mcp.md) - register MCP servers on a session and filter their tools
