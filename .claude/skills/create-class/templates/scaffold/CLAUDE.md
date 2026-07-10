# CLAUDE.md

This repository is a course built with the [class-builder](https://github.com/alexander-kastil/masterclass-claude-code) plugin. Modules live under `demos/NN-<slug>/`, labs under `labs/NN-<slug>/`, and a live progress dashboard under `dashboard/`.

## Repository Layout

- `demos/01-` ... `demos/NN-` numbered tutorial modules. Each module has a `readme.md` plus numbered topic subfolders and an optional `pptx/` for slides.
- `labs/01-` ... `labs/NN-` matching numbered lab folders. Each module's lab folder has one or more sub-labs.
- `dashboard/` static web app that visualises module completeness. Auto-rendered from `dashboard/dashboard.json`.
- `src/` standalone runnable projects referenced by modules.

## Custom Slash Commands

The class-builder plugin provides these commands:

| Command | Use |
|---------|-----|
| `/scaffold-class` | Scaffold a new course layout from an outline file |
| `/scaffold-module` | Create numbered topic subfolders inside an existing module |
| `/create-learning` | Enhance a module README with topics table and slash command guidance |
| `/create-guide` | Author a single demo or lab guide file |
| `/update-class-status` | Re-evaluate every module and refresh the dashboard data |
| `/show-status` | Update status and open the dashboard in a live-reloading browser |
| `/setup-dashboard` | Copy the dashboard web app + scripts into `dashboard/` |

## Brand Voice

All `readme.md` files in `demos/` should pass this repo's brand-voice rules. Discover the repo-local brand-voice skill by globbing `.claude/skills/brand-voice-*` and run it after writing or significantly editing any README.

## Hard Rules

- Internal links use relative paths (e.g. `demos/01-fundamentals/readme.md`); anchors use `#heading-name`.
- Code fences must declare a language (`bash`, `python`, `json`, ...).
- Write clean code with no noise: no inline comments, no explanatory remarks, no placeholder notes.
- No error handling in scripts unless explicitly requested.

## Workflow

1. Plan: write a plan to `tasks/todo.md` with checkable items.
2. Verify: confirm the plan before starting implementation.
3. Track: mark items complete as you go.
4. Document: append a review section to `tasks/todo.md` when done.
