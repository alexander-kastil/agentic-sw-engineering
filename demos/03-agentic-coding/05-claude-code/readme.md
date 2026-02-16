# Claude Code Agents

Claude Code is a desktop application powered by Anthropic's Claude Agent SDK that operates autonomously within VS Code. Unlike browser-based chat, it has direct access to your file system and can read, modify, and execute code in your workspace.

Configure permission modes to control how the agent applies changes: automatically, with your approval, or by outlining a plan first. This gives you full control over how aggressively Claude Code operates in your workspace.

Claude Code manages context efficiently through persistent markdown files and parallel sub-agent execution. Each sub-agent operates in its own context window, preventing the main agent from becoming overwhelmed during complex tasks.

Use specialized slash commands for advanced workflows:

| Command          | Purpose                                                                |
| ---------------- | ---------------------------------------------------------------------- |
| /agents          | Create custom agents for specific tasks                                |
| /hooks           | Define automations at key moments like session start or tool execution |
| /memory          | Manage persistent context across sessions                              |
| /review          | Analyze and provide feedback on pull request changes                   |
| /security-review | Identify vulnerabilities in pending code changes                       |

Build reusable skills that bundle workflows with code for team sharing and cross-platform access.

Claude Code integrates with VS Code's debugging and testing tools while working within your Copilot subscription. Hand off incomplete tasks from local agents to Claude Code for autonomous cloud execution, making it ideal for large-scale refactoring, code reviews, and security audits.

## Key Topics Covered in This Section

- [VS Code Claude Agent Preview](https://code.visualstudio.com/docs/copilot/agents/third-party-agents#_claude-agent-preview)
- [Third-party Agents in VS Code](https://code.visualstudio.com/docs/copilot/agents/third-party-agents)
