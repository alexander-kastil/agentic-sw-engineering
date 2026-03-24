# Agentic Software Engineering Repository

**Teaching repository** for Microsoft AZ-400 certification and agentic software engineering patterns. See [readme.md](../../readme.md) for full details and license information.

## Structure

| Folder     | Purpose                                                                     |
| ---------- | --------------------------------------------------------------------------- |
| **demos/** | 7-module curriculum covering Copilot fundamentals through capstone projects |
| **src/**   | Sample applications (Angular, React, .NET, Python) as deployment targets    |
| **infra/** | Infrastructure as Code (Bicep, Terraform)                                   |
| **.azdo/** | Azure DevOps pipelines using Workload Identity Federation                   |
| **labs/**  | Hands-on exercises complementing demo modules                               |

## Key Rules

- Write clean code. No comments. Don't over-engineer.
- No documentation unless asked. Keep docs short (max 2 heading levels).
- **Always consult Microsoft Learn MCP** when implementing/fixing code.
- **Never hardcode deployment values** — read from `.github/deploy.json`.
- Start applications from their project folders, not repository root.

## Pipelines

Use reusable templates from `.azdo/templates/` with naming: `<module>-<demo>-<description>`. All pipelines use Workload Identity Federation for secure Azure authentication.
