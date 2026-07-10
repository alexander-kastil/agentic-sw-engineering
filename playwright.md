# Conversation Log

**Date:** May 8, 2026

---

**User:** /create-agent that is a playwrigt expert. this agent shall only be used for e2e not for checking code results. reflect on the tools that we could assign to this agent

**Assistant:** Done. Here's a summary of the key decisions:

**Tools assigned**: `['read', 'edit', 'search', 'execute', 'web', 'todo']`

| Tool | Reason |
|---|---|
| `read` + `search` | Understand app routes, components, selectors before writing tests |
| `edit` | Author `.spec.ts` files and `playwright.config.ts` |
| `execute` | Run `npx playwright test`, codegen, reports |
| `web` | Fetch current Playwright docs / migration guides |
| `todo` | Track coverage gaps across a feature |

**Excluded**: `playwright/*` MCP (browser inspection — prohibited per your preferences), `chrome-devtools/*` (not its job), `agent` (no orchestration needed), cloud tools.

**Try it with prompts like:**
- *"Write e2e tests for the login flow in the food-shop app"*
- *"Add Playwright coverage for the tasks-ui checkout page"*
- *"Fix the failing e2e tests in the angular-devops project"*

The agent file was saved to `.github/agents/team-playwright.agent.md`.
