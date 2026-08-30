---
name: claude-learn
description: >-
  Master skill for the reflect->capture->distribute->close learning loop in any repository: its
  MAIN TASK is to reflect on a session/task and turn what it taught into durable, reusable
  knowledge, then distribute it and log the session. Reflect on what a session revealed, capture it
  by authoring/updating skills, agents, docs, and a lessons file, distribute it both to the team
  (repo-local `.claude/skills/`, committed) and across projects (global `~/.claude/skills/`) via
  push learnings up, pull skills down, or reconcile through the bundled skill-sync leaf, then close
  the loop by logging the session to the repo time ledger. Delegates each step to the correct leaf.
  Triggers on: "reflect", "review session", "what did we do", "session summary", "learnings",
  "capture lessons", "update lessons", "improve skills", "update docs", "update context",
  "sync context", "doc distribution", "analyze conversation", "learning loop", "create skill",
  "update skill", "new skill", "write a skill", "global skill", "promote skill", "sync skills",
  "reconcile skills", "pull global skill", "skills out of sync", "drift audit", "skill drift",
  "audit a skill before installing", "is this skill safe", "third-party skill",
  "which skills never fire", "unused skills", "deprecate a skill", "audit CLAUDE.md", "is CLAUDE.md too long", "prune the instructions", "conflicting rules", "contradictory rules", "does Claude actually follow this", "verify adherence", "prune the lessons file", "close the loop",
  "close out the session", "log the session", "log the time", "track time", "working time",
  "harvest", "make it deterministic", "script this", "parameterize it", "turn this into a script",
  "which procedures should be scripted", "harvest registry".
license: CC-BY-NC-SA-4.0
---

# claude-learn: turn a session into durable knowledge

**Loop: Reflect -> Capture -> Harvest -> Distribute -> Close.** Reflect on the session, capture it into a skill/agent/doc/lessons entry, harvest whatever was deterministic into a script, distribute it local <-> global, close by logging the working time and mirroring it into the worktime service.

Route every step to its leaf. Do not do leaf work inline. Any single step is a valid entry point ("sync my skills", "reflect on this session").

**Repo-independent.** No project-specific paths, agents, or conventions here. Repo specifics belong in that repo's `CLAUDE.md`.

## When to use

- After a work session: capture what it taught into the repo's lessons file
- After a user correction: write the rule that prevents the repeat
- After implementing a feature or a structural change: distribute it to every doc, skill and agent that references it
- When a new skill or agent was added and the existing docs, routers and `CLAUDE.md` need to know about it
- When you want to analyze a native session JSONL (or hook-captured session data) for patterns and improvements
- When a session produced a reusable rule/convention/gotcha worth a skill (local or global)
- When skills need syncing or reconciling local <-> global, standalone or after authoring
- When a session ran a repeatable multi-step procedure: harvest it into a parameterized script so the next run only passes arguments
- Before finishing a chat: close the loop by logging the session to the time ledger

**Trigger keywords:** `reflect`, `review session`, `learnings`, `analyze conversation`, `learning loop`, `update docs`, `sync context`, `doc distribution`, `what did we do`, `improve skills`, `create skill`, `promote skill`, `sync skills`, `drift audit`, `harvest`, `make it deterministic`, `script this`, `close the loop`, `log the time`

## First use in a repo

Optional. The analyze leaf can read a hook-captured session record; on a live session you already hold the context and reflect directly. Wire hooks only if the user wants persistent cross-session tracking: run [`claude-learn-setup`](references/claude-learn-setup.md) once. Otherwise skip.

Check with: `.conversations-claude/hooks/claude-hook.sh` exists AND `.claude/settings.json` references it. The hook scripts are bundled in this skill under `scripts/hooks/`.

## The loop's tasks

| # | Task | When | Leaf |
| --- | --- | --- | --- |
| 1 | **Analyze**: reflect on the session, extract patterns, mistakes, learnings; write them to the lessons file | "reflect", "review session", "what did we learn" | [`claude-analyze`](references/claude-analyze.md) |
| 2 | **Promote**: capture learnings into skills/agents/docs/`CLAUDE.md`, then push local -> global | "create/update a skill", "update docs", "promote skill", after task 1 | [`claude-learn-distribute`](references/claude-learn-distribute.md) (authoring) + [`skill-sync`](references/skill-sync.md) ("Push learnings") |
| 2b | **Harvest**: turn a procedure the session improvised into a parameterized script, so the next run supplies arguments instead of re-deriving steps; register it for later automated testing | Whenever the session ran a repeatable multi-step procedure end to end, scripted or not | [`determinism-harvest`](references/determinism-harvest.md) + [`harvest-registry.md`](harvest-registry.md) |
| 3 | **Reconcile**: converge local <-> global in both directions for every skill the session touched | Part of every run, the same way task 4 is. Also reachable on its own: "pull global skill", "sync skills", "reconcile skills", "which skills are out of sync" | [`skill-sync`](references/skill-sync.md) ("Pull skills" / "Reconcile" / "List / status"); bulk or periodic drift -> [`skill-drift-audit`](references/skill-drift-audit.md) |
| 4 | **Close the loop**: log the session to the repo time ledger via the `track-time` skill | before finishing any claude-learn run | [`session-closeout`](references/session-closeout.md) |
| 4b | **Harvest the offering**: write the session's *mechanism* to `.time/working-time.json` beside the ledger row, as raw material for the services catalogue | with every ledger row, in the same step as task 4 | [`offering-harvest`](references/offering-harvest.md) |
| 4c | **Mirror the ledger**: import `.time/working-time.md` and its sidecar into the worktime service, scoped to this repo | with every ledger row, in the same step as task 4, wherever the repo is registered | [`session-closeout`](references/session-closeout.md) ("Then the import") |

Two tiers, one line each: **Local** `<repo>/.claude/skills/` is the team-shared, git-committed copy; **Global** `~/.claude/skills/` is your personal cross-project library. Mechanics belong to [`skill-sync`](references/skill-sync.md); never hand-copy skill trees.

## Two gates outside the loop

Both run on demand, not as part of a session's reflect->capture->distribute->close pass.

| Gate | When | Leaf |
| --- | --- | --- |
| **Adopt**: audit a skill you did not write before it is installed | Before `npx skills add` or copying in anyone else's skill folder; "is this skill safe", "audit this skill" | [`skill-adopt-audit`](references/skill-adopt-audit.md) |
| **Registry**: which installed skills never actually fire | Beside a drift audit; "unused skills", "which skills never fire", "deprecate a skill" | [`skill-usage-registry`](references/skill-usage-registry.md) |
| **Audit**: prune the instruction surface and prove it is followed | Before adding to a never-audited `CLAUDE.md`; "audit CLAUDE.md", "is CLAUDE.md too long", "conflicting rules", "does Claude actually follow this", "prune the lessons file", "IMPORTANT everywhere", "new model released", "re-simplify the harness", "is this rule still needed", "which rules can we drop now" | [`instruction-audit`](references/instruction-audit.md) |

Drift asks whether two copies agree; the registry asks whether the skill is reachable at all. Run them on the same periodic pass.

The audit gate is the loop's only removal pass: capture and distribute both add, so without it `CLAUDE.md`, the per-turn hooks and the lessons file accumulate until their rules contradict each other. It also carries the writer/reviewer check, the only evidence that any of those rules changes behaviour rather than just reading well.

## Bundled leaves and assets

| File | What it is |
| --- | --- |
| [`references/claude-analyze.md`](references/claude-analyze.md) | Task 1: reflect on a session, extract patterns, write the lessons entries |
| [`references/claude-learn-distribute.md`](references/claude-learn-distribute.md) | Task 2 authoring: capture into docs, skills, agents, `CLAUDE.md`; the worth-authoring, hygiene and review gates |
| [`references/determinism-harvest.md`](references/determinism-harvest.md) | Task 2b: what qualifies as harvestable, how to script it, and what the registry statuses mean |
| [`harvest-registry.md`](harvest-registry.md) | The registry itself: one row per harvested or harvestable procedure, `candidate` -> `scripted` -> `tested` |
| [`references/claude-learn-setup.md`](references/claude-learn-setup.md) | Optional first-use bootstrap that wires the session-capture hooks |
| [`references/skill-sync.md`](references/skill-sync.md) | The four sync operations: Push learnings, Pull skills, Reconcile, List / status |
| [`references/skill-drift-audit.md`](references/skill-drift-audit.md) | Bulk or periodic local <-> global drift audit |
| [`references/skill-adopt-audit.md`](references/skill-adopt-audit.md) | Gate: audit a third-party skill before installing it |
| [`references/skill-usage-registry.md`](references/skill-usage-registry.md) | Gate: which installed skills never fire |
| [`references/instruction-audit.md`](references/instruction-audit.md) | Gate: prune `CLAUDE.md`, the per-turn hooks and the lessons file, re-simplify the surface after each model release, and verify adherence writer/reviewer |
| [`references/session-closeout.md`](references/session-closeout.md) | Task 4: log the session to the repo time ledger |
| [`references/offering-harvest.md`](references/offering-harvest.md) | Task 4b: the `.time/working-time.json` sidecar, its schema, and why the ledger's billing sentence cannot feed the catalogue |
| `scripts/skill-drift.sh` | Read-only local <-> global inventory backing skill-sync List / status and the drift audit: `bash ~/.claude/skills/claude-learn/scripts/skill-drift.sh <repo-root> [skill ...]` |
| `scripts/skill-usage.py` | Scanner backing the registry gate: `python ~/.claude/skills/claude-learn/scripts/skill-usage.py <repo-root> [--days 60] [--json]` |
| `scripts/hooks/` | Session-capture hook scripts installed by `claude-learn-setup` |

## Run order

Analyze first. Its findings feed the distribute leaf, which decides which docs, skills, and agents to touch. Task 2b runs on the back of that decision: whatever the session proved repeatable gets scripted and registered before the reconcile, so the script ships with the skill it belongs to rather than trailing it by a session. Skill files are authored per the distribute leaf, then reconciled local <-> global via `skill-sync`. The reconcile (task 3) runs before task 4, so the ledger entry describes a run whose two copies already agree. Task 4 is last and mandatory, and tasks 4b and 4c ride with it: the ledger row and its `.time/working-time.json` sidecar are written together, because the mechanism the sidecar records is knowable only while the session that built it is still in context. A run that wrote a ledger row and stopped before task 4c has not closed the loop: the files are the source of truth, but every later consumer reads the service, so an unimported row is invisible work. The run's final report lists what converged, not what diverged.

## Standing closing rule: reconcile local <-> global

**Every run ends with a full two-way reconcile of the skills the session touched.** It is a step of the run, not a proposal at the end of it: union the files that exist on only one side, converge the ones that diverged, then report what landed.

**Reporting drift is not an ending.** A difference that was detected in the run is fixed in the run, in both directions. Push learnings (local -> global) and Pull skills (global -> local) are two halves of one standing step, not two options to pick between.

Two cases, and only two, come back to the user:

1. A write that would **delete or overwrite** existing global content rather than add to it.
2. Nothing else. Content specific to this one repo is not one of them: keep it deliberately divergent, and name it in the report.

The **size or effort** of a reconcile is not one of them either. A large drift is a reason to do the work, not a reason to hand it back.

## Example prompts

- "Reflect on this session and capture the learnings in the lessons file."
- "Analyze this conversation session for learnings and skill gaps."
- "Review the last 3 sessions in `~/.claude/projects/` for patterns."
- "Distribute the folder restructure to every doc and skill that references the old paths."
- "Sync agent context after we added a new skill tree."
- "Turn the Windows git-mv file-lock fix into a skill so other repos get it too."
- "Sync my skills local <-> global." / "Which skills are out of sync with global?"
- "Close out the session and log the time."
