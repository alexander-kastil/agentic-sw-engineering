# skill-drift-audit: periodic bulk reconciliation of local ↔ global drift

The routine loop **creates drift by design**: each session promotes only its own changes, pushes are additive, and global edits made from *other* repos never flow back until someone pulls. After weeks a shared-name skill can differ in 15+ reference files in both directions, invisible until a session happens to diff. This leaf owns the periodic convergence step the per-session loop skips.

## When to run

- [skill-sync](skill-sync.md) **List / status** shows a shared-name skill with more than ~3 diverged files.
- After a stretch of sessions (or several repos) that each pushed additive learnings.
- Before major work leaning on a drifted skill: reconcile first so the work reads the best version.
- On request: "reconcile <skill>", "skills out of sync", "drift audit".

Pair it with [skill-usage-registry](skill-usage-registry.md) on the same pass. Drift measures whether two copies agree; the registry measures whether the skill ever fires. A skill can be perfectly converged and still dead.

## Scale hazards (each observed in practice)

1. **Wholesale-overwrite temptation.** With 15 differing files, copying one tree over the other silently drops the losing side's additions. Every two-sided difference gets a per-file decision; when side A has additions A′ and side B has B′, **merge both**. Picking a side is correct only when one is a strict superset or plainly stale.
2. **Manifest/leaf referential integrity.** The `SKILL.md` delegate map accumulates rows pointing at `references/*.md`. A partial sync leaves a router row pointing at a file that does not exist on that side, breaking routing silently. After reconciling, **verify every `references/*.md` linked from each side's `SKILL.md` exists on that side**; a dangling row is a sync defect to fix now.
3. **mtime lies at scale.** `git checkout`/clones reset mtimes, so "newest" is a weak hint that gets more misleading the more files you process. Read both versions of every conflict; completeness/correctness decides.
4. **Screening needs reading, not filenames.** A leaf named after a domain feature can be a generic pattern write-up (promote it); a generically named leaf can be repo-bound (leave divergent, say so). Screen file-by-file for repo paths, entity/customer names, links into one repo's `docs/`.
5. **Sibling-session exclusion.** `git status` the local skills tree first; untracked/modified folders from another in-flight session are out of scope. Reconcile only committed content plus this session's own edits.

## Procedure (per drifted skill)

1. **Scope**: `git status --short .claude/skills/` → exclude other sessions' in-flight folders. Collision-guard the frontmatter descriptions (same lineage, not a name collision).
2. **Backup global** to `~/.claude/skills/.skill-sync-backups/<name>/<timestamp>/`: mandatory, global has no version control.
3. **Inventory**: `diff -rq <global> <local>` → three buckets: one-sided (union, after project-specific screening for the global direction), two-sided (per-file read-and-merge), identical (skip).
4. **Converge** each file to both sides; keep intentionally divergent files on a named list with one-line reasons.
5. **Verify**: `diff -rq` clean except the named divergences, **plus the manifest integrity check** (every delegate-map row resolves to an existing file on both sides).
6. **Report**: one table: file | action (unioned→global / unioned→local / merged / side-won / left-divergent) | reason. Every file lands in exactly one bucket; never silently drop one.
7. Local results stay uncommitted; run `bash ~/.claude/scripts/lint-claude-config.sh <repo>` before closing.

## Scale guidance

- Above ~10 differing files, delegate the reconcile to a subagent carrying this procedure verbatim (plus [skill-sync](skill-sync.md)), but keep the *decisions log* in the report so the main thread can audit which side won and why.
- At most two skills per agent run; unrelated skill families never share a run.
- End by re-running skill-sync **List / status**: not done until the skill reads "synced (+ named intentional divergences)".
