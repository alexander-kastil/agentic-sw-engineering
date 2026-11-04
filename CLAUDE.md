# CLAUDE.md

Companion material for **"Agentic Software Engineering using GitHub Copilot"**, a 4-day, 9-module masterclass by Alexander Kastil (see `readme.md`, `demos/readme.md`). GitHub Copilot is the subject of the class, so the `.github/` Copilot-facing config (skills, agents, instructions, prompts) is deliberate content, not dead weight. The parallel `.claude/` harness is the author's own tooling for maintaining the class.

Author with the global `create-class` skill, build slides with the `deck-creation:create-pptx` skill, and run the `brand-voice-gh-copilot` skill after writing or editing a readme or guide.

## Layout

```text
demos/readme.md                      class readme: Duration, Audience, Prerequisites, Modules, Schedule
demos/NN-<module>/readme.md          module readme with the topic table
demos/NN-<module>/NN-<topic>/        readme.md (teaching), copy-paste templates, demo-<slug>.md, <name>-solution/
demos/NN-<module>/pptx/              slide specs NN-MM-<slug>.md, images/, topics.json, NN-<module>.pptx
demos/pptx/                          00 class deck, days.json, images/
labs/readme.md                       lab index with durations
labs/NN-<lab>/                       readme.md (readme-py.md for the Python track), starters, <name>-solution/
src/                                 standalone runnable projects the modules reference
tasks/                               todo.md, lessons.md
```

- `demos/01-` to `demos/09-` are the modules in learning order: fundamentals, agentic-harness, agentic-coding, agent-sessions, cli-sdk, copilot-app, agentic-devops, governance, plan-spec-deliver. Do not reorganize or renumber.
- Lab numbers follow the schedule in `demos/readme.md`, not the module numbers (Lab 03 belongs to module `02-agentic-harness`). Demo topic readmes teach and demonstrate; they do not carry the exercises.
- `src/` holds `copilot-api`, `devops-app` (Angular and React), `doubler-api`, `food-app` (polyglot), `hr-mcp-server`, `qr-server-cs`, `qr-server-py` and `qr-server-ts`.

## Brand Voice

Every `readme.md` and guide under `demos/` and `labs/` follows `.claude/skills/brand-voice-gh-copilot/references/rules.md`. Check a file against it after writing or significantly editing it. The skill stays repo-local because this class writes for software engineers; `create-class` finds it by globbing `.claude/skills/brand-voice-*`.

## Harness

Orchestration runs in the installed plugins and the house rules in `~/.claude/CLAUDE.md` apply as they stand; this file repeats neither.

## Hard Rules

- `.github/` and `.vscode/` are the Copilot harness the class teaches and runs on: read them and `.claude/rules/copilot-harness.md` (where Copilot reads each file, the CLI MCP trap, `copilot skill list` in solution folders) before authoring any demo that ships harness files; this repo is the ground truth and outranks a vendor `--help`.
- Internal links are relative paths (`demos/01-fundamentals/readme.md`); anchors are `#heading-name`.
- Every code fence declares a language.
- Fix the underlying issue when a quality check fails. Never bypass with `--no-verify`.
- Clean code only: no inline comments, no explanatory remarks, no placeholder notes.
- No error handling in scripts unless asked.

## Working Method

- **Plan first** for anything non-trivial (3+ steps or an architectural decision): write it to `tasks/todo.md`, check in, then track progress there.
- **Verify before reporting done.** Run the check, show the command and its output. A claim is not a receipt.
- **Review `tasks/lessons.md`** at session start; `claude-learn`'s `instruction-audit` gate prunes it and this file.
- **Simplicity first**: minimal diff, root causes over patches, no rewrite to fix a typo.
- **Tutorial over library**: clear explanations and copy-paste examples beat reusable abstractions.
