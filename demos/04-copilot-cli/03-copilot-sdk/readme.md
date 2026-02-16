# GitHub Copilot SDK

The GitHub Copilot SDK enables you to embed AI-powered agentic workflows directly into your applications. Built on the same production-tested agent runtime as Copilot CLI, the SDK handles planning, tool invocation, and code execution—you define the behavior and Copilot handles the complexity. Available in Technical Preview for Python, TypeScript, Go, and .NET.

## Use Cases

- Build intelligent assistants that can understand code context and execute complex tasks autonomously.
- Integrate AI agents into development tools, IDEs, and code analysis platforms without building custom orchestration.
- Create custom agents tailored to specific workflows—code review agents, documentation generators, or deployment helpers.
- Enable agents to interact with external services and repositories through Model Context Protocol (MCP) servers.
- Develop terminal-based or web-based applications that delegate coding tasks to AI-powered agents.

## Available Stacks

| Language | Install Command |
|----------|-----------------|
| Node.js / TypeScript | `npm install @github/copilot-sdk` |
| Python | `pip install github-copilot-sdk` |
| Go | `go get github.com/github/copilot-sdk/go` |
| .NET | `dotnet add package GitHub.Copilot.SDK` |

Community-maintained SDKs for Java, Rust, C++, and Clojure are also available but not officially supported by GitHub.

## Getting Started

### Prerequisites

Install the Copilot CLI and authenticate with your GitHub account:

```bash
copilot --version
```

Ensure you have your preferred language runtime installed (Node.js 18+, Python 3.8+, Go 1.21+, or .NET 8.0+).

### Basic Usage

Create a client, start a session, and send your first message. Here's a minimal example in TypeScript:

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({ model: "gpt-4.1" });
const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);
await client.stop();
```

### Core Features

- Send messages and receive responses with `sendAndWait()` or through streaming events.
- Stream responses in real-time by subscribing to `assistant.message_delta` events.
- Create custom tools that Copilot can call using `defineTool()` with a name, description, and handler function.
- Connect to MCP servers to extend agent capabilities with pre-built tools.
- Define custom agents with specialized system messages and behaviors.

### Key Concepts

Copilot manages the entire agent lifecycle—when you define a tool, Copilot decides when to call it based on the user's prompt. The SDK handles parameter validation, handler execution, and response integration.

For a complete tutorial with examples, see the [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md).

## Key Topics Covered in This Section

- [GitHub Copilot SDK Repository](https://github.com/github/copilot-sdk)
- [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md)
- [Authentication Documentation](https://github.com/github/copilot-sdk/blob/main/docs/auth/index.md)
- [BYOK (Bring Your Own Key)](https://github.com/github/copilot-sdk/blob/main/docs/auth/byok.md)
- [MCP (Model Context Protocol)](https://github.com/github/copilot-sdk/blob/main/docs/mcp/overview.md)