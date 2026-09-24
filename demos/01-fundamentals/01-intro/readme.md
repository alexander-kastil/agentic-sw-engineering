# Getting Started & Configuring Copilot

GitHub Copilot operates in two complementary modes. AI Assisted Coding provides real-time completions and suggestions as you type, allowing you to accept or modify highlighted code snippets directly. Agentic Software Engineering employs agents that autonomously work toward assigned goals, orchestrating multiple tools and decisions to deliver complete solutions.

> Note: Although this class quickly introduces AI Assisted Coding, it focuses on Agentic Software Engineering.

## Copilot Settings

Settings control Copilot behavior, inline suggestions, and model selection. Enable the core features in your VS Code `settings.json`, and switch Copilot off for files that hold secrets:

```json
{
  "github.copilot.enable": {
    "*": true,
    "markdown": true,
    "plaintext": false,
    ".env": false,
    "*.secrets": false
  },
  "editor.inlineSuggest.enabled": true,
  "chat.agent.enabled": true
}
```

Settings apply at three levels:

- **User settings**: personal preferences applied across all workspaces
- **Workspace settings** ([.vscode/settings.json](/.vscode/settings.json)): project-specific overrides for team consistency
- **Dev Container settings** ([.devcontainer/devcontainer.json](/.devcontainer/devcontainer.json)): standardized environments with pre-configured extensions and tools

## Keeping Secrets Out

Copilot sees open editor files, workspace content, terminal output shown in VS Code, and whatever you attach to a chat. Keeping credentials out of that view is your job, and these controls cover it:

| Method                 | Scope          | Control Level                                                      |
| ---------------------- | -------------- | ------------------------------------------------------------------ |
| `.gitignore` exclusion | Workspace      | Prevents secrets from being tracked or shared                      |
| VS Code file disabling | Editor         | Disables Copilot for specific file patterns (`.env`, `*.secrets`)  |
| Custom instructions    | Agent behavior | Tells the agent never to write credentials, only placeholders      |
| Workspace trust        | IDE level      | Untrusted workspaces limit extension functionality                 |
| Environment isolation  | System level   | Secrets stored separately from workspace context                   |

Reference environment variables by name rather than value, and use placeholders such as `PLACEHOLDER_KEY` in examples. Organization policies, content exclusions, and the public code filter are covered in [Governance](../../08-governance/03-enterprise-control/).

## Links & Resources

- [GitHub Copilot Plans & Features](https://docs.github.com/en/copilot/get-started/plans)
- [Visual Studio Code Updates](https://code.visualstudio.com/updates)
- [GitHub Blog](https://github.blog/)

[← Back to Fundamentals](../readme.md) | [Next: Selecting Models →](../02-models/readme.md)
