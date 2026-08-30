# CLAUDE.md

This repository is a hands-on course. Modules live under `demos/NN-<slug>/` and matching labs under `labs/NN-<slug>/`. Authoring is driven by the `create-class` skill and its peer skills (`scaffold`, `brand-voice-*`, `mermaid-*`).

## Repository Layout

- `demos/01-` ... `demos/NN-` numbered tutorial modules. Each module has a `readme.md`; modules may add numbered topic subfolders and an optional `pptx/` folder for slides.
- `labs/01-` ... `labs/NN-` matching numbered lab folders. Each module's lab folder holds one or more sub-labs.
- `src/` standalone runnable projects referenced by modules.

## Authoring Skills

Course content is created and maintained with these skills:

| Skill | Use |
|-------|-----|
| `scaffold` | Bootstrap the base repo and generate module, topic, and lab folders from an outline or interactively |
| `create-class` | Master skill: author guides, generate slides, enrich module READMEs, track completeness |
| `brand-voice-*` | Audit and fix Markdown against the repo's brand-voice rules |

## Brand Voice

All `readme.md` files in `demos/` should pass the repo's brand-voice rules. Discover the repo-local skill by globbing `.claude/skills/brand-voice-*` and run it after writing or significantly editing any README.

## Hard Rules

- Internal links use relative paths (e.g. `demos/01-fundamentals/readme.md`); anchors use `#heading-name`.
- Code fences must declare a language (`bash`, `python`, `json`, ...).
- No em dashes in prose; use `,` `;` `:` or `()` instead.
- Mermaid node labels use `"quoted<br/>labels"`, never `\n`.
- Write clean code with no noise: no inline comments, no explanatory remarks, no placeholder notes.
- No error handling in scripts unless explicitly requested.

## Workflow

1. Plan: write a plan to `tasks/todo.md` with checkable items.
2. Verify: confirm the plan before starting implementation.
3. Track: mark items complete as you go.
4. Document: append a review section to `tasks/todo.md` when done.
