# CLAUDE.md

Companion material for **"Agentic Software Engineering using GitHub Copilot"**, a 4-day, 9-module masterclass by Alexander Kastil (see `readme.md`, `demos/readme.md`). GitHub Copilot is the subject of the class, so the `.github/` Copilot-facing config (skills, agents, instructions, prompts) is deliberate content, not dead weight. The parallel `.claude/` harness is the author's own tooling for maintaining the class.

## Layout

- `demos/01-` … `demos/09-` are the modules in learning order (fundamentals → agentic-harness → agentic-coding → agent-sessions → cli-sdk → copilot-app → agentic-devops → governance → spec-driven-dev). Do not reorganize or renumber.
- Each module has a `readme.md` plus numbered topic subfolders with their own `readme.md` and copy-paste templates. Exercises live as "Exercise" sections inside a topic readme, never in a separate `labs/` folder.
- `src/` holds the standalone runnable projects the modules reference (`qr-server`, `hr-mcp-server`, `doubler-api`, `tasks-api-py`, `tasks-ui`, `food-app`, `angular`, `react`).

## Brand Voice

Every `readme.md` under `demos/` must pass `.claude/skills/brand-voice-gh-copilot/references/rules.md`. Run the `brand-voice-gh-copilot` skill after writing or significantly editing a README. The skill stays repo-local because this class writes for software engineers; `create-class` finds it by globbing `.claude/skills/brand-voice-*`.

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
