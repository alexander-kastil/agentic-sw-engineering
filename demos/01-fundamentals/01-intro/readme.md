# GitHub Copilot Introduction

Get started with GitHub Copilot — understand its capabilities, installation options, latest releases, and available extensions This module establishes the foundation for using AI-assisted coding in VS Code and GitHub workflows.

GitHub Copilot operates in two complementary modes. AI Assisted Coding provides real-time completions and suggestions as you type, allowing you to accept or modify highlighted code snippets directly. In contrast, Agentic Software Engineering employs specialized agents that autonomously work toward assigned goals, orchestrating multiple tools and decisions to deliver complete solutions. 

>Note: Although this class quickly introduces AI Assisted Coding, it focuses on Agentic Software Engineering.

GitHub Copilot Plans & Features provides an overview of available subscription tiers and the specific capabilities included in each plan, helping you choose the right option for your needs.

Visual Studio Code Updates tracks new VS Code releases and features that impact Copilot integration, ensuring you stay current with the latest development tools and improvements.

GitHub Copilot Extensions expands Copilot's functionality with domain-specific AI agents and tools, enabling specialized capabilities for different development domains and workflows.

GitHub Blog delivers announcements, product releases, and best practices from GitHub and the community, keeping you informed about new features and recommended usage patterns.

## Copilot Settings

Configure VS Code and development environments to optimize GitHub Copilot workflows. Settings control Copilot behavior, inline suggestions, model selection, and workspace consistency across teams.

### Essential Copilot Settings

Enable core Copilot features in your VS Code `settings.json`:

```json
{
  "github.copilot.enable": {
    "*": true,
    "markdown": true,
    "plaintext": false,
    "yaml": true
  },
  "editor.inlineSuggest.enabled": true,
  "github.copilot.chat.codesearch.enabled": true,
  "github.copilot.chat.claudeAgent.enabled": true
}
```

## Copilot Settings Location Options

- **User-level settings** (`.json`): Personal preferences applied across all workspaces
- **Workspace settings** ([.vscode/settings.json](/.vscode/settings.json)): Project-specific overrides for team consistency
- **Dev Container settings** ([.devcontainer/devcontainer.json](/.devcontainer/devcontainer.json)): Standardized environments with pre-configured extensions and tools

## Key Topics Covered in This Section

- [GitHub Copilot Plans & Features](https://docs.github.com/en/copilot/get-started/plans)
- [Visual Studio Code Updates](https://code.visualstudio.com/updates)
- [GitHub Copilot Extensions](https://github.com/marketplace?type=apps&copilot_app=true)
- [GitHub Blog](https://github.blog/)
