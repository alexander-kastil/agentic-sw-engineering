# skill-sync: the four local ↔ global operations

| Tier | What it is | Shared how |
| --- | --- | --- |
| **Local**: `<repo>/.claude/skills/<name>` | Team-shared, git-committed copy. Teammates get skills by pulling the repo. | Via git (commit local edits) |
| **Global**: `~/.claude/skills/<name>` | Personal cross-project library. Not git-tracked, one machine. | Only to you, across all repos |

| Operation | Direction | Use when |
| --- | --- | --- |
| **Push learnings** | local → global, additive | A pattern proven here should reach your *other* repos. Nothing in global is deleted. |
| **Pull skills** | global → local, destructive mirror | Bring a proven global skill down so the *team* gets it (then commit); local drift is discarded. |
| **Reconcile** | two-way, best-of-both | Both sides drifted; converge to one identical best version per file. |
| **List / status** | read-only | See what is synced / diverged / one-sided before choosing a direction. |

## Shared procedure (every operation)

1. **Resolve paths.** Global root `~/.claude/skills` (`$HOME/.claude/skills` in Bash). Local root `<repo-root>/.claude/skills`, repo root via `git rev-parse --show-toplevel`.
2. **Inputs / no-argument auto-discovery.** Accept one or more skill names. With no argument, discover candidates: `git status --short .claude/skills/` → the modified/untracked top-level skill folders. **Do NOT intersect with folders that already exist in global**: a brand-new local skill with no global counterpart is a *prime* Push candidate; the intersection filter belongs to Pull only (Pull needs a global source to mirror from). Include local-only new folders in the Push/Reconcile candidate list. Confirm via `AskUserQuestion` (multiSelect); never operate on all folders silently.
   - **A skill is its whole folder tree.** The unit of sync is the entire folder: every `SKILL.md`, every `references/*.md`, every `templates/*` file, at any depth. Never sync only the top-level `SKILL.md`. New to global → create the full tree; exists → cover every file (added, differing, one-sided) per the operation's rules.
3. **Collision guard.** Compare `description:` frontmatter on both sides before touching anything. A shared folder name is not proof it is the same skill: if the two describe unrelated capabilities, stop and warn (for List, annotate `⚠ possible name collision`).
4. **Recursive, subskill-aware diff**: never just the top-level `SKILL.md`:
   ```bash
   diff -rq "<global-path>" "<local-path>"
   ```
   - **Ignore line-ending-only differences.** git normalizes local files to LF while a global copy may carry CRLF, so `diff -rq` flags byte differences that are not content divergence. Confirm before treating a file as diverged: `diff -q <(tr -d '\r' < A) <(tr -d '\r' < B)`: clean means content-identical; skip it (do not rewrite the global copy just to flip line endings).
5. **Back up global before ANY write to it** (global has no version control: mandatory):
   ```bash
   mkdir -p "$HOME/.claude/skills/.skill-sync-backups/<name>/<timestamp>"   # date +%Y%m%d-%H%M%S
   cp -r "<global-path>" "$HOME/.claude/skills/.skill-sync-backups/<name>/<timestamp>/"
   ```
   Local writes rely on git as the safety net instead.

## Push learnings (local → global, additive)

Promote new/improved local content up; leave global-only content untouched. **Nothing is ever deleted from global.**

1. Shared procedure 1-4.
2. **Classify** from the diff: only in local → add; differs on both → update; only in global → leave alone; identical → skip.
3. **Screen every candidate for project-specific content.** Read it; exclude anything that only makes sense in this repo (repo/project name, hardcoded local paths, customer/business names, links to this repo's docs). Global content is loaded by every repo. A mostly generic file with one project-specific example: prefer generalizing the example, but if that needs real rewriting rather than a straight copy, flag it for the user instead of silently rewriting.
4. Shared procedure 5 (backup), then **apply**: copy each approved local-only file into global at the same relative path (creating dirs); overwrite each approved differing file in global with the local version.
5. **Report** three lists: promoted, skipped as project-specific (one-line reasons), global-only left untouched. Never drop a candidate without naming it.

## Pull skills (global → local, destructive mirror)

Global wins; local-only content in that folder is discarded (recoverable via git).

1. Shared procedure 1-3.
2. **Dirty-tree check.** `git status --short <local-path>`: if anything is pending, show `git diff <local-path>` and confirm before continuing; those edits are about to be discarded and git is their only backup.
3. **Mirror:**
   ```bash
   rm -rf "<local-path>"; cp -r "<global-path>" "<local-path>"
   ```
4. **Confirm** `diff -rq "<global-path>" "<local-path>"` reports nothing.
5. **Report** which local files were added/changed/removed (pre-pull `git status`/`git diff` plus a post-pull `git status --short`). Do **not** commit: leave it staged for the team.

## Reconcile (two-way, best-of-both)

1. Shared procedure 1-4.
2. **Union one-sided files**: copy any file existing on only one side to the missing side, so no leaf/detail is lost (common case: a `references/*.md` present locally but not global, or vice versa).
3. **Resolve two-sided differences per file.** mtime is a **weak hint only** (`stat -c %Y`; `git checkout` resets mtimes, so a fresh clone makes stale content look newest). **Read both versions**; content overrides the hint (more complete / more correct wins). Genuinely ambiguous → ask with a short diff excerpt. Apply the winner to **both** sides.
4. **Screen for project-specific content** (as in Push): never converge a repo-specific file up into global; leave that file deliberately divergent and say so.
5. Shared procedure 5 (backup) before any global write.
6. **Verify** `diff -rq` clean except files intentionally left divergent (name them).
7. **Report:** unioned to global, unioned to local, conflicts resolved (which side won and why), left intentionally divergent.

### Contain the divergence in a section, never in the examples

A local copy that carries repo facts by **rewriting the generic examples** (its own DbContext, entity
names, ports and namespaces substituted throughout) turns every future sync into a manual re-merge of
every file, forever, and it drifts: one conventions skill sat 15 files and ~200 lines behind global
because nobody wanted to redo the substitution.

Keep the divergence in one place instead. Take the global content verbatim, then append a single
`## In this repo` section per file carrying the facts that are actually repo-bound: project paths,
namespaces, which launch profile is mandatory, which service must not be restarted, which schema
regime applies. Examples stay generic. Every later sync is then a straight Pull plus a re-append,
and the drill-down (`ONLY-G 0` on every file) proves nothing generic was lost.

Screen the same way in the other direction: the `## In this repo` section is exactly what must never
be pushed up.

### Measuring before choosing a direction

`scripts/skill-drift.sh <repo-root>` prints the List / status table; adding skill names drills into
those skills and prints per file how many lines exist on only one side. **`ONLY-L > 0` means a Pull
would delete local content**, so the file needs a Reconcile, not a mirror. Read-only, safe to run
before deciding anything.

## List / status (read-only inventory)

Never writes.

1. Shared procedure 1. List folder names on both sides (`ls "$HOME/.claude/skills"`, `ls .claude/skills`); ignore non-skill entries (no `SKILL.md`, dotdirs like `.skill-sync-backups`).
2. **Classify** every name in the union: global-only (not pulled here yet), local-only (normal for project-specific skills: state as fact, do not imply it needs promotion), both + `diff -rq` empty → **synced**, both + non-empty → **diverged** (note the count of differing/missing files).
3. **Collision check** on every "both present" name (frontmatter descriptions) → `⚠ possible name collision`, informational only.
4. **Report as a table**, actionable first: diverged → global-only → local-only → synced. Suggest the next step per row: diverged → Reconcile (or a specific direction); global-only → Pull; local-only → none by default.

## Safety (all operations)

- Global is not git-tracked: the **backup before any global write is mandatory**, never optional.
- Push and Reconcile **never delete from global**; only add/update. Pull deletes only *inside* the named local folder(s), never outside.
- Never resolve a conflict on mtime alone without reading both versions.
- Never silently drop a file. Every file lands in exactly one bucket: unioned, conflict-resolved, skipped-identical, promoted, or intentionally-left-divergent.
- Hygiene gate before syncing: `bash ~/.claude/scripts/lint-claude-config.sh <repo-root>` (the script appends `/.claude` itself, so pass the repo root, not the `.claude` dir).
- Local skill edits are the team's artifact: leave them staged in the working tree for the user to commit. Never auto-commit or push.
