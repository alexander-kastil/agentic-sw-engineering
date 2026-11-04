---
paths:
  - ".github/**"
  - ".vscode/**"
  - "demos/**"
  - "labs/**"
---

# Copilot harness

The class teaches the GitHub Copilot harness and runs on it, so `.github/` and `.vscode/` are the reference implementation, not incidental config.

- Skills: `.github/skills/<name>/SKILL.md`, read by the CLI and VS Code.
- Agents: `.github/agents/<name>.agent.md`, read by the CLI and VS Code.
- Instructions: `.github/instructions/*.instructions.md` and `.github/copilot-instructions.md`, read by the CLI and VS Code.
- Prompts: `.github/prompts/*.prompt.md`, read by VS Code.
- Hooks: `.github/hooks/hooks.json`, read by the CLI.
- Settings: `.github/copilot/settings.json`, read by the CLI.
- MCP servers for VS Code only: `.vscode/mcp.json`, top-level key `servers`.
- MCP servers for the CLI only: `~/.copilot/mcp-config.json`, written by `copilot mcp add`.
- The two MCP homes are the trap: the CLI never loads a server from a file in the repository (not `.mcp.json`, not `.github/mcp.json`, not a plugin's `mcp.json`); only `copilot mcp add` and an installed plugin register one, so a demo that checks a server into the workspace and then demonstrates it on the command line demonstrates nothing. `demos/02-agentic-harness/03-mcp/01-basics/readme.md` already teaches this.
- A demo's `*-solution/` folder mirrors this layout so the CLI discovers it when launched from that folder.
- Verify with `copilot skill list` run from the solution folder: the skill appears under `Project skills` or it is not wired.
