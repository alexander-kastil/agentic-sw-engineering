# GitHub Copilot SDK


## Embedding Agents in Your Applications

Move from using Copilot to building with it. The Copilot SDK embeds AI-powered agentic workflows directly into your own applications, and it runs on the same production-tested agent runtime as the Copilot CLI and the Copilot agent inside VS Code's agent host, so you define the behavior and Copilot handles planning, tool invocation, and execution. GitHub ships it for six stacks: TypeScript, Python, Go, .NET, Java, and Rust. Every SDK talks to the CLI over JSON-RPC and manages the CLI process for you.

The module works from the SDK fundamentals to runnable demos and then to multi-agent and hosted setups. You create a client, start a session, and define custom tools that the agent decides when to call, as the weather-assistant and code-reviewer demos show. From there you compose several agents into a coordinated system and then take the result to Azure.

| Topic | Description |
|-------|-------------|
| **[SDK Fundamentals](./01-intro/)** | Install for your stack, create a `CopilotClient`, open a session, and register custom tools the agent invokes on its own, all on the same runtime that powers the Copilot CLI and the editor's agent host. |
| **[Building Agents with Custom Tools](./02-custom-tools/)** | Two runnable TypeScript agents built step by step: a weather assistant that defines a `get_weather` tool and streams events as the agent chooses to call it, and a code reviewer that audits a codebase through tools you supply. |
| **[Building a Multi-Agent System](./03-multi-agent/)** | Compose specialized SDK agents, a researcher, a builder, a reviewer, that each run in their own session and hand work to a coordinator for parallel, isolated execution. |
| **[Deploying an SDK Agent to Azure](./04-deploy-azure/)** | Take a local agent to a hosted service on Azure Container Apps or App Service, with the same sessions and tools, secrets in Key Vault, and optional Azure OpenAI bring-your-own-model. |

Topics 02 through 04 each ship a `*-solution` folder holding the finished, runnable code for every step in that guide, pinned to the versions it was verified against. Build the files yourself as you read the guide; open the solution when a step misbehaves or to compare against something that runs.

## Available Stacks

| Language | Install Command |
|----------|-----------------|
| Node.js / TypeScript | `npm install @github/copilot-sdk` |
| Python | `pip install github-copilot-sdk` |
| Go | `go get github.com/github/copilot-sdk/go` |
| .NET | `dotnet add package GitHub.Copilot.SDK` |
| Rust | `cargo add github-copilot-sdk` |
| Java | Maven coordinates `com.github:copilot-sdk-java` |

> Note: The Node.js, Python, and .NET packages bundle the Copilot CLI, so there is nothing else to install. Go, Java, and Rust need `copilot` on your PATH.

## Key Topics covered in this module

- [GitHub Copilot SDK repository](https://github.com/github/copilot-sdk) - all six SDKs, their READMEs, and the API reference per language
- [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md) - build your first SDK app end to end
- [Copilot SDK cookbook](https://github.com/github/awesome-copilot/blob/main/cookbook/copilot-sdk/nodejs/README.md) - runnable samples, including custom tools the agent calls on its own

[← Previous: GitHub Copilot CLI](../01-cli/readme.md) | [Back to CLI & SDK](../readme.md)
