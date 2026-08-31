# GitHub Copilot CLI & SDK

## Running the Agent Outside the Editor

This module covers the two ways to use the Copilot agent beyond the IDE: the CLI in your terminal and the SDK inside your own applications. The CLI installs with `npm install -g @github/copilot`, authenticates with `/login`, and drives multi-step work from an interactive shell. The SDK runs on that same production-tested agent runtime, so you define the sessions and tools and Copilot handles planning, tool invocation, and execution.

The module is split into two parts, each with its own readme. Part 1 works from CLI basics through a real HR automation business case to scheduled GitHub Agentic Workflows. Part 2 moves from SDK fundamentals to runnable agent demos and to MCP Apps that render interactive UIs inside the chat.

| Part | Description |
|------|-------------|
| **[GitHub Copilot CLI](./01-cli/)** | Install and authenticate the CLI, work in the interactive shell with slash commands and Autopilot, automate a SharePoint HR document review through MCP servers, and turn that job into a versioned `gh aw` workflow. |
| **[GitHub Copilot SDK](./02-sdk/)** | Embed the agent runtime in your own apps: create a client and a session, register custom tools the agent calls on its own, and serve interactive MCP Apps from a server. |

## Topics

- [GitHub Copilot CLI](./01-cli/)
  - [GitHub Copilot CLI](./01-cli/01-cli-intro/)
  - [Business Case: HR Document Updates Automation](./01-cli/02-cli-business-case/)
  - [GitHub Agentic Workflows](./01-cli/03-agentic-wf/)
  - [Extending the CLI with MCP Servers & Skills](./01-cli/04-mcp-skills/)
  - [Codebase Q&A and Onboarding](./01-cli/05-codebase-qa/)
- [GitHub Copilot SDK](./02-sdk/)
  - [GitHub Copilot SDK](./02-sdk/01-sdk/)
  - [Copilot SDK Demos](./02-sdk/02-sdk-demos/)
  - [Implementing & Using MCP Apps](./02-sdk/03-mcp-apps/)
  - [Deploying an SDK Agent to Azure](./02-sdk/04-deploy-azure/)
  - [Building a Multi-Agent System](./02-sdk/05-multi-agent/)
