# Agentic Software Engineering Repository

Companion material for **"Agentic Software Engineering using GitHub Copilot"**, a 4-day, 9-module masterclass by Alexander Kastil. See [readme.md](../readme.md) for full details and license information. GitHub Copilot is the subject of the class, so the `.github/` Copilot-facing config (skills, agents, instructions, prompts) is deliberate content, not dead weight.

## Structure

| Folder       | Purpose                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------- |
| **demos/**   | 9-module curriculum in learning order (01-fundamentals → 09-spec-driven-dev)                                          |
| **src/**     | Standalone runnable projects: `angular/`, `react/`, `copilot-api/`, `copilot-api-ui/`, `doubler-api/`, `food-app/`, `hr-mcp-server/`, `qr-server/`, `qr-server-cs/` |
| **labs/**    | Hands-on exercises, `01-` … `09-`, one folder per lab                                                                 |
| **docs/**    | Specs and architecture documents                                                                                      |
| **.github/** | Workflows, instructions, skills, prompts, agents, hooks, and `deploy.json`                                            |
| **tasks/**   | `todo.md` for the active plan, `lessons.md` for recorded corrections                                                  |

`demos/01-` … `demos/09-` are the modules in learning order. Do not reorganize or renumber them. Each module has a `readme.md` plus numbered topic subfolders with their own `readme.md` and copy-paste templates.

The exercises live in `labs/`, not inside the demo readmes. Lab numbers follow the schedule in `demos/readme.md`, not the module numbers (Lab 03 belongs to module `02-agentic-harness`).

## Hard Rules

- Issue independent tool calls, reads, searches, and subagent tasks in one parallel batch. Sequential execution of independent work is a bug.
- Whenever a subject matter specialist agent is available for the task, use it. Never do specialist work on the main thread when a matching agent exists.
- Whenever a subagent is used, even a single one, create a task ledger first and record every spawn, correction, and report in it.
- Never commit or push without an explicit request.
- Internal links are relative paths (`demos/01-fundamentals/readme.md`); anchors are `#heading-name`.
- Every code fence declares a language.
- Fix the underlying issue when a quality check fails. Never bypass with `--no-verify`.
- Clean code only: no inline comments, no explanatory remarks, no placeholder notes.
- No error handling in scripts unless asked.
- No documentation unless explicitly asked. Keep docs short (max 2 heading levels).
- **Always consult Microsoft Learn MCP** when implementing or fixing code.
- **Never hardcode deployment values** — read from `.github/deploy.json`.
- Start applications from their project folders, not the repository root.

## Working Style

- Plan before any non-trivial task (3+ steps or an architectural decision). If it goes sideways, stop and re-plan.
- Write the plan to `tasks/todo.md` as checkable items, mark them off as you go, and add a review section at the end.
- After any correction from the user, record the pattern in `tasks/lessons.md`.
- Prove it works before calling it done: run it, check the output, diff the behaviour.
- Simplest change that solves the root cause, touching only what is necessary. A typo fix is a typo-sized diff.
- Tutorial over library: clear explanations and copy-paste examples beat reusable abstractions.

## Token Efficiency

- Never re-read a file you just wrote, and never re-run a command whose outcome was certain.
- Do not echo back large blocks of code or file contents unless asked.
- Do not summarize what you just did unless the result is ambiguous.

## Brand Voice

Every `readme.md` under `demos/` must pass `.claude/skills/brand-voice-gh-copilot/references/rules.md`. Apply those rules after writing or significantly editing a README.

## CICD

Workflow files live in `.github/workflows/`. Naming convention: `<module>-<demo>-<description>`. All workflows authenticate to Azure with OpenID Connect federation, never with stored secrets.
