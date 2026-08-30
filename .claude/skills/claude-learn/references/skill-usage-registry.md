# skill-usage-registry: does this skill ever actually fire

[skill-drift-audit](skill-drift-audit.md) asks whether two copies of a skill agree. It never asks whether the skill has ever been used. A skill can be perfectly synced, perfectly linted, and dead: the description does not match how anyone phrases the task, so the router never reaches it and the work gets done from scratch every time. This leaf is the other half of skill hygiene.

The rule: **zero invocations in 60 days means the triggers are wrong or the skill should go.** Never both fixed at once, and never a silent delete.

## When to run

- Alongside a drift audit, on the same periodic pass.
- When the library has grown past the point where you remember what is in it.
- When you catch yourself doing by hand something a skill already covers: that is one visible instance of a routing failure the registry measures in bulk.
- Before authoring a new skill in a crowded area, to see whether the neighbour you would extend has ever fired.

## Produce the registry

```bash
python ~/.claude/skills/claude-learn/scripts/skill-usage.py <repo-root> [--days 60] [--json]
```

The script scans every session transcript under `~/.claude/projects/*/*.jsonl` for `Skill` tool calls, counts them per skill name, and joins that against the skills installed in `~/.claude/skills` (global) and `<repo-root>/.claude/skills` (local). Output columns: skill, scope, last used, invocations, status.

| Status | Meaning |
| --- | --- |
| ACTIVE | Invoked inside the window |
| STALE | Invoked, but not inside the window |
| NEVER | No invocation on record, and the manifest is older than the window |
| NEW | No invocation on record, but the manifest was written inside the window, so it has not had its chance yet |

A trailing list names skills that appear in transcripts but have no folder: renamed or uninstalled. Those are a separate defect, see below.

### What the numbers do not know

State these limits when reporting, rather than presenting the table as ground truth:

- **Only this machine.** Transcripts are local, so a skill used heavily from another machine reads as NEVER here.
- **Only explicit `Skill` calls.** A skill whose content was read through a `Read` on its `SKILL.md`, or applied from memory without invocation, leaves no trace.
- **mtime is a weak hint.** The NEW guard uses the manifest's mtime, and a sync or a `git checkout` rewrites mtimes wholesale. After a big sync pass, expect NEW to be overstated: check `git log` for the local copy before trusting it.
- **Renames split a history.** A skill renamed last month reads as NEW with zero uses while its old name sits in the orphan list.

## Act on it

One decision per row, in this order.

### 1. NEVER, and you still want the capability: fix the triggers

The default diagnosis. The skill is not bad, it is unreachable. Open its `description` and compare it against how you actually phrase the task, in your own words, from the last time you did that work by hand:

- Does it carry the literal trigger phrases a person types, not the formal name of the domain?
- Is the routing sentence first, before the prose? The description is an index entry, and everything after the first line competes with every other skill's first line.
- Does a sibling skill's description already cover the same phrases and win? Two skills fighting for one trigger is one skill too many: merge them, or make the loser's description name what it does that the winner does not.

Fix the description, then re-run the registry after real use. If it still never fires, it is not a trigger problem.

### 2. NEVER, and the capability is dead: deprecate, do not delete

Deleting loses the content and the reason it existed. Deprecate instead:

- Fold anything still true into the skill that superseded it, following [claude-learn-distribute](claude-learn-distribute.md).
- Then remove the folder in the same pass that records where the content went, and run the stale-reference sweep so no router, `CLAUDE.md` or agent still points at it.
- Global has no version control: back up to `~/.claude/skills/.skill-sync-backups/<name>/<timestamp>/` before removing anything there, exactly as [skill-sync](skill-sync.md) requires for any global write.

Deleting a skill the user authored is never automatic. Propose the list, get the nod, then act.

### 3. Orphans: invoked but not installed

Each name in that list was reachable once. Decide which it is:

- **Renamed**: harmless history, note it and move on.
- **Removed on purpose**: same.
- **Removed by accident, or a local skill never promoted**: that is a real loss. Recover it from the backups folder or from git history in the repo that held it.

### 4. Report

One table, actionable first: NEVER, then STALE, then the orphans. Per row: the verdict (triggers rewritten / deprecated / kept as-is / recovered) and one line of reasoning. Never drop a row silently, and never report a status without the caveat that applies to it.

## Verify

Re-run the script after the pass. Rows you rewrote triggers for stay NEVER until real use moves them, so the check is not the status flipping: it is that every NEVER row now carries a recorded decision, and the orphan list is empty or explained.
