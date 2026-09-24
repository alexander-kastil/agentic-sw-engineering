# Update Agent Framework to Latest Version

The agent checks Microsoft Learn MCP for newer Microsoft Agent Framework and Microsoft Foundry packages, updates the dependency files, creates the Python environment, and writes an upgrade report of every change.

## Prompt

```text
Examine demos\01-fundamentals\05-agent-mode-basics\03-update\agentfw_tools-knowledge-py. Use your microsoft learn mcp to check if there are updated libraries available that allow updating all agents implemented in files with prefix agentfw_ this to the latest libraries and show the agents in the new Microsoft Foundry. Your tasks:
Pin down the library version to latest possible
Update pyproject.toml and requirements.txt. No need to upgrade pip
Create and activate the Python environment and install dependecies
Create an upgrade-report.md in the folder
```
