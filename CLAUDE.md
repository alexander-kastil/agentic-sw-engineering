# CLAUDE.md

Companion material for **"Agentic Software Engineering using GitHub Copilot"**, a 4-day, 9-module masterclass by Alexander Kastil (see `readme.md`, `demos/readme.md`). GitHub Copilot is the subject of the class, so the `.github/` Copilot-facing config (skills, agents, instructions, prompts) is deliberate content, not dead weight. The parallel `.claude/` harness is the author's own tooling for maintaining the class.

## Layout

- `demos/01-` … `demos/09-` are the modules in learning order (fundamentals → agentic-harness → agentic-coding → agent-sessions → cli-sdk → copilot-app → agentic-devops → governance → spec-driven-dev). Do not reorganize or renumber.
- Each module has a `readme.md` plus numbered topic subfolders with their own `readme.md` and copy-paste templates.
- `labs/01-` … `labs/09-` hold the hands-on exercises, one folder per lab with a `readme.md` plus any starter or solution assets. Lab numbers follow the schedule in `demos/readme.md`, not the module numbers (Lab 03 belongs to module `02-agentic-harness`). Demo topic readmes teach and demonstrate; they do not carry the exercises.
- `src/` holds the standalone runnable projects the modules reference (`qr-server`, `hr-mcp-server`, `doubler-api`, `tasks-api-py`, `tasks-ui`, `food-app`, `angular`, `react`).

## Brand Voice

Every `readme.md` under `demos/` must pass `.claude/skills/brand-voice-gh-copilot/references/rules.md`. Run the `brand-voice-gh-copilot` skill after writing or significantly editing a README. The skill stays repo-local because this class writes for software engineers; `create-class` finds it by globbing `.claude/skills/brand-voice-*`.

## Copilot Harness

The class teaches the GitHub Copilot harness and runs on it, so `.github/` and `.vscode/` are the reference implementation, not incidental config. Read them before authoring any demo that ships harness files; this repo is the ground truth and outranks a vendor `--help`.

| Component | Where | Read by |
|-----------|-------|---------|
| Skills | `.github/skills/<name>/SKILL.md` | CLI and VS Code |
| Agents | `.github/agents/<name>.agent.md` | CLI and VS Code |
| Instructions | `.github/instructions/*.instructions.md`, `.github/copilot-instructions.md` | CLI and VS Code |
| Prompts | `.github/prompts/*.prompt.md` | VS Code |
| Hooks | `.github/hooks/hooks.json` | CLI |
| Settings | `.github/copilot/settings.json` | CLI |
| MCP servers | `.vscode/mcp.json`, top-level key `servers` | VS Code only |
| MCP servers | `~/.copilot/mcp-config.json`, written by `copilot mcp add` | CLI only |

The two MCP rows are the trap. The CLI never loads a server from a file in the repository: not `.mcp.json`, not `.github/mcp.json`, not a plugin's `mcp.json`. Only `copilot mcp add` and an installed plugin register one, so a demo that checks a server into the workspace and then demonstrates it on the command line demonstrates nothing. `demos/02-agentic-harness/03-mcp/01-basics/readme.md` already teaches this.

A demo's `*-solution/` folder mirrors this layout so the CLI discovers it when launched from that folder. Verify with `copilot skill list` run from the solution folder: the skill appears under `Project skills` or it is not wired.

## Hard Rules

- Issue independent tool calls, reads, searches, and subagent tasks in one parallel batch. Sequential execution of independent work is a bug.
- Never commit or push without an explicit request.
- Internal links are relative paths (`demos/01-fundamentals/readme.md`); anchors are `#heading-name`.
- Every code fence declares a language.
- Fix the underlying issue when a quality check fails. Never bypass with `--no-verify`.
- Clean code only: no inline comments, no explanatory remarks, no placeholder notes.
- No error handling in scripts unless asked.

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
