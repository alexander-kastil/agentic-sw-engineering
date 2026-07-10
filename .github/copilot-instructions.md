# Agentic Software Engineering Repository

**Teaching repository** for Microsoft AZ-400 certification and agentic software engineering patterns. See [readme.md](../readme.md) for full details and license information.

## Structure

| Folder        | Purpose                                                                              |
| ------------- | ------------------------------------------------------------------------------------ |
| **demos/**    | 7-module curriculum (01-fundamentals → 07-capstone-project)                          |
| **src/**      | Sample apps: `angular/`, `react/`, `copilot-api/`, `hr-mcp-server/`, `qr-server/`, `food-app/`, `tasks-api-py/`, `tasks-ui/`, `tasks-lab/` |
| **infra/**    | Infrastructure as Code (Bicep — `main.bicep`)                                        |
| **.azdo/**    | Azure DevOps pipelines and reusable templates in `.azdo/templates/`                  |
| **.github/**  | Workflows, instructions, skills, prompts, agents, hooks, and `deploy.json`           |
| **labs/**     | Hands-on exercises complementing demo modules                                        |
| **docs/**     | Specs and architecture documents                                                      |

## Key Rules

- Write clean code. No comments. Don't over-engineer.
- No documentation unless asked. Keep docs short (max 2 heading levels).
- **Always consult Microsoft Learn MCP** when implementing/fixing code.
- **Never hardcode deployment values** — read from `.github/deploy.json`.
- Start applications from their project folders, not repository root.

## Pipelines

Pipeline files live in `.azdo/` with reusable templates in `.azdo/templates/`. Naming convention: `<module>-<demo>-<description>`. All pipelines use Workload Identity Federation for secure Azure authentication.
