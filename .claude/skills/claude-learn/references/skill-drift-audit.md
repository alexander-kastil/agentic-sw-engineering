# Skill Drift Audit — periodic bulk reconciliation of local↔global skill drift

The routine learning loop **creates drift by design**: each session promotes only its own changes
(the "another session's in-flight edits are not yours to promote" guardrail), pushes are additive,
and global edits made from *other* repos never flow back until someone pulls. After a few weeks a
shared-name skill can differ in 15+ reference files in both directions — none of it anyone's
mistake, all of it invisible until a session happens to diff. This leaf owns the **periodic
convergence step** the per-session loop deliberately skips.

## When to run

- `skill-sync` **List / status** shows a shared-name skill with more than ~3 diverged files.
- After a stretch of sessions (or several repos) that each pushed additive learnings.
- Before major work that leans on a drifted skill — reconcile first so the work reads the best
  version, not whichever copy this repo happens to hold.
- On explicit request: "reconcile <skill>", "skills out of sync", "drift audit".

## Why bulk reconcile is its own procedure (not N repeats of a single-file merge)

Hazards that only show up at scale — each one observed in practice:

1. **Wholesale-overwrite temptation.** With 15 differing files, copying one tree over the other
   "to be done with it" silently drops the losing side's additions. Every two-sided difference
   still gets a per-file decision; when side A has additions A′ and side B has additions B′,
   **merge both** — picking a side is only correct when one is a strict superset or plainly stale.
2. **Manifest/leaf referential integrity.** The `SKILL.md` delegate map accumulates rows pointing
   at `references/*.md`. A partial sync (manifest moved, leaves didn't — or vice versa) leaves a
   router row pointing at a file that doesn't exist on that side, which breaks routing silently.
   After reconciling, **verify every `references/*.md` linked from each side's `SKILL.md` exists
   on that side**; treat a dangling row as a sync defect to fix now, not a nit.
3. **mtime lies at scale.** `git checkout`/clones reset mtimes, so "newest" is a weak hint that
   gets *more* misleading the more files you process. Read both versions of every conflict; let
   completeness/correctness decide.
4. **Project-specific screening needs reading, not filenames.** A leaf named after a domain
   feature can still be a generic pattern write-up (promote it), and a generically named leaf can
   be repo-bound (leave it divergent, say so). Screen file-by-file for repo paths, entity/customer
   names, and links into one repo's `docs/` — judged from content.
5. **Sibling-session exclusion.** `git status` the local skills tree first; untracked/modified
   folders from another in-flight session are out of scope — reconcile only committed content
   plus this session's own edits.

## Procedure (per drifted skill)

1. **Scope**: `git status --short .claude/skills/` → exclude other sessions' in-flight folders.
   Collision-guard the frontmatter descriptions (same lineage, not a name collision).
2. **Backup global** to `~/.claude/skills/.skill-sync-backups/<name>/<timestamp>/` — mandatory,
   global has no version control.
3. **Inventory**: `diff -rq <global> <local>` → three buckets: one-sided (→ union, after
   project-specific screening for the global direction), two-sided (→ per-file read-and-merge),
   identical (skip).
4. **Converge** each file to both sides; keep intentionally divergent files on a named list with
   one-line reasons.
5. **Verify**: `diff -rq` clean except the named divergences, **plus the manifest integrity check**
   (every delegate-map row resolves to an existing file on both sides).
6. **Report**: one table — file | action (unioned→global / unioned→local / merged / side-won /
   left-divergent) | reason. Every file lands in exactly one bucket; never silently drop one.
7. Local results stay uncommitted for the user; run the hygiene gate
   (`bash ~/.claude/scripts/lint-claude-config.sh <repo>`) before closing.

## Scale guidance

- Above ~10 differing files, delegate the reconcile to a subagent carrying this procedure
  verbatim (plus the skill-sync leaf) — but keep the *decisions log* in the report so the main
  thread can audit which side won and why.
- Two skills can reconcile in one agent run; unrelated skill families should not share one run —
  a mistake in one shouldn't force re-verifying the other.
- End by re-running `skill-sync` **List / status**: the audit isn't done until the skill reads
  "synced (+ named intentional divergences)".
