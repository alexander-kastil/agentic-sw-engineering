# Agent Mode Basics

Local agents execute within your current VS Code session with real-time feedback and full integration with your editor, terminal, and files. Execution is synchronous and blocking, making them ideal for focused, single-task agentic coding. Steering, queueing, and checkpoints are covered in [Local Agents](../../03-agentic-coding/01-local-agents/).

| Aspect           | Details                                                                                                  |
| ---------------- | -------------------------------------------------------------------------------------------------------- |
| Best For         | Single focused tasks, debugging, iterative exploration, and rapid iteration with immediate feedback      |
| Integration      | Direct access to workspace files, terminal, editor state, npm scripts                                    |
| Parallelism      | Single sequential task only                                                                              |
| Auth Context     | Full access to local authentication: Azure CLI credentials, Git tokens, SSH keys, environment variables  |
| Online Resources | Through local tools: GitHub API, Microsoft Learn MCP, cloud CLIs                                         |
| Limitations      | Blocks editor; limited by local resources; cannot parallelize                                            |

## Topics

| Name                                        | Description                                                                                              |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **[Scaffold .NET API](./01-scaffold-net/)** | Create a starter .NET API using a local agent workflow.                                                  |
| **[Fixing Errors](./02-fix-err/)**          | Integrate with Microsoft Foundry using keyless authentication with DefaultAzureCredential.               |
| **[Update Agent Framework](./03-update/)**  | Upgrade Python agent implementations to the latest Microsoft Agent Framework libraries and dependencies. |

[← Previous: AI-Assisted Coding Essentials](../04-ai-assisted-coding/readme.md) | [Back to Fundamentals](../readme.md) | [Next: Pull Requests & Code Reviews →](../06-pr-code-review/readme.md)
