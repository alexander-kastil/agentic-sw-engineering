# Anthropic Claude Agents

Claude agents are third-party AI agents powered by Anthropic's Claude that run directly in VS Code. Unlike custom agents defined in your repository, Claude agents are cloud-based or local sessions that provide autonomous agentic capabilities with built-in tools.

## Enable Claude Agents

Option 1: Via Settings UI

1. Press Ctrl+, to open Settings
2. Search for claudeAgent.enabled
3. Enable github.copilot.chat.claudeAgent.enabled

Option 2: Edit settings.json directly

Add this setting to your VS Code user settings:

```json
"github.copilot.chat.claudeAgent.enabled": true
```

## Start a Claude Agent Session

1. Press Ctrl+Alt+I to open Chat
2. Click New Chat (+)
3. Select Claude from the Session Type dropdown
4. Choose between Local session (runs Claude agent locally) or Cloud session (select Cloud session type, then Claude from Partner Agent dropdown)

## Features

Claude agents provide autonomous execution using their own tool set. Available slash commands include /agents, /hooks, /memory, /pr-comments, /review, and /security-review.

Permission modes allow you to choose how Claude interacts with your code: edit automatically (default), request approval for each change, or plan-only mode with no execution.

## Billing

Claude agents are included in your GitHub Copilot Pro+ subscription—no additional setup or billing required.

## Links & Resources

- [Third-party agents in Visual Studio Code](https://code.visualstudio.com/docs/copilot/agents/third-party-agents)
