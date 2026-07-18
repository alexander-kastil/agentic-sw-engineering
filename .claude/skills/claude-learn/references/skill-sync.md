# Skill Sync — pull skills, push learnings (claude-learn's Distribute step)

The **Distribute** step of claude-learn's *Reflect → Capture → Distribute* loop. Once a session has captured knowledge into a skill, this leaf moves it between the two tiers:

| Tier | What it is | Shared how |
| --- | --- | --- |
| **Local** — `<repo>/.claude/skills/<name>` | The **team-shared, git-committed** copy. Teammates get skills by pulling the repo. | Via git (commit local edits) |
| **Global** — `~/.claude/skills/<name>` | Your **personal, cross-project** library. Not git-tracked, one machine. | Only to you, across all repos |

Two directions, four operations:

| Operation | Direction | Use when |
| --- | --- | --- |
| **Push learnings** | local → global, additive | A pattern proven in this repo should reach your *other* repos. Nothing in global is deleted. |
| **Pull skills** | global → local, destructive mirror | Bring a proven global skill down so the *team* gets it (then commit); local drift is discarded. |
| **Reconcile** | two-way, best-of-both | Both sides drifted; converge to one identical best version per file. |
| **List / status** | read-only | See what's synced / diverged / one-sided before choosing a direction. |

> This leaf integrates what were four standalone global skills (`skills-merge-global`, `skills-pull-global`, `skills-sync`, `skills-list-global`) — now owned by claude-learn so the whole team gets the sync workflow through the repo.

## Shared procedure (applies to every operation)

1. **Resolve paths.** Global root `~/.claude/skills` (`$HOME/.claude/skills` in Bash). Local root `<repo-root>/.claude/skills`, repo root via `git rev-parse --show-toplevel`.
2. **Inputs / no-argument auto-discovery.** Accept one or more skill names. With **no argument**, discover candidates: `git status --short .claude/skills/` → the modified/untracked top-level skill folders. **Do NOT intersect with folders that already exist in global** — a brand-new local skill (no global counterpart yet) is a *prime* Push candidate, and the whole point of Push is to promote it up; the intersection filter belongs to Pull only (Pull needs a global source to mirror from). Include local-only new folders in the Push/Reconcile candidate list. Confirm the list via `AskUserQuestion` (multiSelect) — never operate on all folders silently. This is claude-learn's integration point: approved skill edits show up here as an ordinary git diff.
   - **A skill is its whole folder tree.** When a candidate is selected, the unit of sync is the entire folder — every `SKILL.md`, every nested subskill folder, every `references/*.md` and `templates/*` file, at any depth. Never sync only the top-level `SKILL.md`. If the skill is new to global, create the full tree; if it exists, cover every file (added, differing, and one-sided) per the operation's rules below.
3. **Collision guard.** Compare `description:` frontmatter on both sides before touching anything. A shared folder name is not proof it's the same skill — if the two clearly describe unrelated capabilities, stop and warn (for the read-only list, just annotate `⚠ possible name collision`).
4. **Recursive, subskill-aware diff** — never just the top-level `SKILL.md`:
   ```bash
   diff -rq "<global-path>" "<local-path>"
   ```
   A skill's value is the *full proven pattern*, and the detail lives in `references/*.md` / leaf files. Every operation covers the **whole folder tree**.
   - **Ignore line-ending-only differences.** git normalizes local files to LF while a global copy may carry CRLF, so `diff -rq` flags byte differences that are not real content divergence. Confirm before treating a file as diverged: `diff -q <(tr -d '\r' < A) <(tr -d '\r' < B)` — if that is clean, the files are content-identical; skip them (do not rewrite the global copy just to flip line endings).
5. **Back up global before ANY write to it** (global has no version control — mandatory, not optional):
   ```bash
   mkdir -p "$HOME/.claude/skills/.skill-sync-backups/<name>/<timestamp>"   # date +%Y%m%d-%H%M%S
   cp -r "<global-path>" "$HOME/.claude/skills/.skill-sync-backups/<name>/<timestamp>/"
   ```
   Local writes rely on git as the safety net instead.

## Push learnings (local → global, additive)

Promote genuinely new/improved local content up; leave anything that exists only in global untouched. **Nothing is ever deleted from global.**

1. Shared procedure 1–4.
2. **Classify** from the diff: *only in local* → candidate to add; *differs on both* → candidate to update; *only in global* → leave alone; *identical* → skip.
3. **Screen every candidate for project-specific content** — read it, and exclude anything that only makes sense in this one repo (repo/project name, hardcoded local paths, customer/business names, links to this repo's docs). Global content is loaded by every repo, so leaking specifics misdirects them all. If a file is mostly generic with one project-specific example, prefer generalizing the example over dropping the file — but if that needs real rewriting rather than a straight copy, flag it for the user, don't silently rewrite.
4. Shared procedure 5 (backup), then **apply**: copy each approved local-only file into global at the same relative path (creating dirs); overwrite each approved differing file in global with the local version.
5. **Report** three lists: promoted (added/updated in global), skipped as project-specific (with one-line reasons), global-only left untouched. Never drop a candidate without naming it.

## Pull skills (global → local, destructive mirror)

Global always wins; local-only content in that folder is discarded (recoverable via git).

1. Shared procedure 1–3.
2. **Dirty-tree check.** `git status --short <local-path>` — if anything is pending, show `git diff <local-path>` and confirm before continuing; those edits are about to be discarded and git is their only backup.
3. **Mirror:**
   ```bash
   rm -rf "<local-path>"; cp -r "<global-path>" "<local-path>"
   ```
4. **Confirm** `diff -rq "<global-path>" "<local-path>"` reports nothing (identical).
5. **Report** which local files were added/changed/removed (from the pre-pull `git status`/`git diff` plus a post-pull `git status --short`). Do **not** commit — leave it staged for the team to review/commit.

## Reconcile (two-way, best-of-both)

Pick the better version of each file regardless of side; leave both copies byte-identical.

1. Shared procedure 1–4.
2. **Union one-sided files** — copy any file that exists on only one side to the missing side, so **no subskill/detail is lost** (the common case: a `references/*.md` present locally but not global, or vice-versa).
3. **Resolve two-sided differences per file:** mtime is a **weak default hint only** (`stat -c %Y` — `git checkout` resets mtimes, so a fresh clone can make stale content look "newest"); **read both versions** and let content override the hint (more complete / more correct wins). If genuinely ambiguous, ask with a short diff excerpt rather than guessing. Apply the winner to **both** sides.
4. **Screen for project-specific content** (as in Push): never converge a repo-specific file up into global — leave that one file deliberately divergent and say so explicitly.
5. Shared procedure 5 (backup) before any global write.
6. **Verify** `diff -rq` is clean except files intentionally left divergent (name them).
7. **Report:** files unioned to global, unioned to local, conflicts resolved (which side won and why), and anything left intentionally divergent.

## List / status (read-only inventory)

Never writes. Reports state so you can choose a direction.

1. Shared procedure 1. List folder names on both sides (`ls "$HOME/.claude/skills"`, `ls .claude/skills`); ignore non-skill entries (no `SKILL.md`, dotdirs like `.skill-sync-backups`).
2. **Classify** every name in the union: *global-only* (not pulled here yet), *local-only* (normal for project-specific skills — state as fact, don't imply it needs promotion), *both + `diff -rq` empty* → **synced**, *both + non-empty* → **diverged** (note the count of differing/missing files).
3. **Collision check** on every "both present" name (frontmatter descriptions) → `⚠ possible name collision` note if unrelated; informational only.
4. **Report as a table**, actionable first: diverged → global-only → local-only → synced. Suggest the next step per row — diverged → **Reconcile** (or a specific direction); global-only → **Pull**; local-only → none by default.

## Safety (all operations)

- Global is not git-tracked — the **backup before any global write is mandatory**, never optional.
- Push and Reconcile **never delete from global**; only add/update. Pull deletes only *inside* the named local folder(s), never outside.
- Never resolve a conflict on mtime alone without reading both versions.
- Never silently drop a file — every file lands in exactly one bucket: unioned, conflict-resolved, skipped-identical, promoted, or intentionally-left-divergent.
- **Local skill edits are the team's artifact — leave them staged in the working tree for the user to commit** (never auto-commit/push).
- After authoring and before syncing, run the hygiene gate: `bash ~/.claude/scripts/lint-claude-config.sh <repo>`.
