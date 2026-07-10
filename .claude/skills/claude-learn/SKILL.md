---
name: claude-learn
description: >-
  Master skill for the reflect->capture->distribute learning loop in the "Agentic Software
  Engineering using GitHub Copilot" masterclass authoring repo: its MAIN TASK is to reflect
  on a session/task and enhance the course's durable authoring knowledge, then distribute it.
  Reflect on what a session taught while writing or restructuring the course, capture it by
  authoring/updating skills, agents, module READMEs, and tasks/lessons.md, and distribute it
  both to the team (repo-local `.claude/skills/`, committed) and across projects (global
  `~/.claude/skills/`) — push learnings up, pull skills down, or reconcile, all via the
  bundled skill-sync leaf. Delegates each step to the correct leaf skill.
  Triggers on: "reflect", "review session", "what did we do", "session summary", "learnings",
  "capture lessons", "update lessons", "improve skills", "update docs", "analyze conversation",
  "learning loop", "create skill", "update skill", "new skill", "write a skill", "global skill",
  "promote skill", "sync skills", "reconcile skills", "pull global skill", "skills out of sync",
  "drift audit", "skill drift".
license: CC-BY-NC-SA-4.0
---

# claude-learn — Reflect on the work, enhance our authoring knowledge

**The main task: reflect on what a session/task actually taught, and turn it into durable knowledge for authoring this course.** A pattern proven, a gotcha hit, a convention settled: capture it so the next person (human or agent) starts from it instead of rediscovering it. That knowledge lives in skills, agents, module READMEs, and `tasks/lessons.md`, and is distributed two ways: to the team (repo-local, committed) and across your own projects (global). Everything this router does serves that one loop:

> Reflect -> Capture -> Distribute.
> Reflect on the session (what worked, what broke, what is now known) -> Capture it by authoring/updating a skill, an agent, a README, or a lessons entry -> Distribute it by syncing local <-> global (push learnings up to global, pull skills down to the repo for the team).

Route the heavy lifting to the leaf that owns each step; do not do it inline. Reflection/analysis, doc distribution, skill authoring, and pull/push syncing are all first-class steps of the loop, and any one of them (for example a standalone "sync my skills" or "reflect on this session") is a valid entry point.

This is the repo-local, re-scoped copy of `claude-learn` for THIS repository. The paths, doc maps, and handoff targets below are specific to the course-authoring repo.

## When to Use This Skill

- After a work session, to capture what authoring or restructuring the course taught and record it in `tasks/lessons.md`
- After a correction from the user, to write a rule that prevents the same mistake (the CLAUDE.md Self-Improvement Loop)
- After a structural change to `demos/` or `.claude/`, to distribute the update to every file that references it
- When a session revealed a reusable rule/convention/gotcha that belongs in a skill (create or update a skill, local or global)
- When skills need reconciling local <-> global, after authoring skill edits or as a standalone "sync my skills" request
- When the user says "reflect", "what did we learn", "update docs", "create/update a skill", or "sync/reconcile skills"

**Trigger keywords:** `reflect`, `review session`, `learnings`, `capture lessons`, `analyze conversation`, `learning loop`, `update docs`, `what did we do`, `improve skills`, `create skill`, `update skill`, `new skill`, `write a skill`, `global skill`, `promote skill`, `sync skills`, `reconcile skills`, `pull global skill`, `skills out of sync`

## Delegate Map

| Request type | Leaf skill to invoke |
| --- | --- |
| Analyze a session for patterns, mistakes, and learnings; write them to `tasks/lessons.md` | [`claude-analyze`](references/claude-analyze.md) |
| Distribute an update across the READMEs, skills, agents, and CLAUDE.md that reference it | [`claude-learn-distribute`](references/claude-learn-distribute.md) |
| Create or update a skill (local or global) from a learning | [`claude-learn-distribute`](references/claude-learn-distribute.md) — "Creating & updating skills" section |
| Push learnings up (local -> global, additive) | [`skill-sync`](references/skill-sync.md) — "Push learnings" |
| Pull skills down (global -> local, for the team) | [`skill-sync`](references/skill-sync.md) — "Pull skills" |
| Two-way reconcile a skill local <-> global (best-of-both) | [`skill-sync`](references/skill-sync.md) — "Reconcile" |
| Report which skills are out of sync (read-only) | [`skill-sync`](references/skill-sync.md) — "List / status" |
| Bulk-reconcile a broadly drifted skill / periodic drift audit | [`skill-drift-audit`](references/skill-drift-audit.md) |

Run analyze first. Its findings feed the distribute leaf, which decides which READMEs, skills, and agents to touch. Skill files (local and global) are created/updated per the skill-authoring workflow in the distribute leaf; the local <-> global reconciliation is then routed to the matching sync skill above, which is the loop's final step, not optional.

## Repo Conventions This Skill Serves

- **Lessons live in `tasks/lessons.md`.** The repo CLAUDE.md Self-Improvement Loop says: after any correction, add the pattern and a rule that prevents it. This skill owns that file.
- **Brand voice is mandatory for `demos/` READMEs.** Any README write distributed by the learning loop must be verified with the repo-local `brand-voice-gh-copilot` skill (discover it by globbing `.claude/skills/brand-voice-*`).
- **Guides and module READMEs are authored via `create-class`.** The learning loop does not hand-write large guides; it routes to the `create-class` author-guide / enrich-module leaves, and can route a single flagged guide to the `guide-validator` agent.
- **No docs agent.** Unlike the Hugo/bico variants, this repo has no documentation agent. Doc writes go through `create-class` + `brand-voice-gh-copilot`, or direct edits for `CLAUDE.md`, `.inventory/`, and `tasks/lessons.md`.
- **Structural edits stay consistent.** After any change to `demos/` structure, verify every `demos/readme.md` TOC link resolves and that no folder has a duplicate numeric prefix; update `.inventory/` when the target structure moves.

## Syncing skills (local <-> global) — a main task

The two tiers, and why both exist:

| Tier | What it is | Shared how |
| --- | --- | --- |
| **Local** — `<repo>/.claude/skills/` | The team-shared, git-committed copy. Teammates get skills by pulling the repo. | Via git (commit local skill changes) |
| **Global** — `~/.claude/skills/` | Your personal, cross-project library. Not git-tracked, one machine. | Only to you, across all your repos |

We keep skills in the repo (local), not global-only, precisely because others work on this repo: a global-only skill is invisible to teammates. So the two operations are:

- **Pull skills** (global -> local): bring a proven skill from your personal library down into the repo so the team gets it (then commit). This is how a pattern proven elsewhere lands here for everyone.
- **Push learnings** (local -> global): promote what this session taught up to your personal library so your other repos benefit.

Both directions (plus two-way reconcile and read-only status) are owned by the [`skill-sync`](references/skill-sync.md) leaf; route there, never hand-copy skill trees. Local skill edits are the team's artifact: leave them staged in the working tree for the user to commit (per the never-auto-commit rule).

**Sync the whole skill, not just `SKILL.md` — every subskill counts.** A skill's value is the full proven pattern; the manifest is only a router and the detail lives in `references/*.md`. Syncing must be recursive over the entire skill folder: diff recursively (`diff -rq <global> <local>`), union one-sided files so no detail is lost, and resolve two-sided differences per file. Always run the hygiene gate after authoring, before syncing: `bash ~/.claude/scripts/lint-claude-config.sh <repo>`.

## Relationship to Other Skills and Agents

| Skill / agent | Relationship |
| --- | --- |
| `create-class` | Authors and enriches guides and module READMEs; claude-learn captures what a session taught while using it and routes README writes to it |
| `brand-voice-gh-copilot` | Verifies README quality; claude-learn requires it after any distributed README edit |
| `guide-validator` (agent) | Validates a single guide against brand-voice and author-guide rules; claude-learn routes flagged guides to it |
| Subject-matter agents (`net-agent`, `angular-agent`, `github-devops-agent`, `playwright-agent`) | Own the `src/` code the demos reference; distribute routes code changes to them, not to the main thread |

## Example Prompts

- "Reflect on this session and capture the learnings in tasks/lessons.md."
- "Review the last 2 sessions in ~/.claude/projects/D--git-classes-agentic-sw-engineering/ for recurring mistakes."
- "Distribute the Module 3 restructure to every README and skill that references the old paths."
- "We renamed a skill; sync CLAUDE.md and run the config lint."
- "Turn the Windows git-mv file-lock fix into a skill so other repos get it too."
- "Sync my skills local <-> global." / "Which skills are out of sync with global?"
