# claude-learn-distribute — Documentation & Context Distribution

Take a change (from an implementation or from the analyze leaf) and propagate it to every file that references it: docs, skills, agents, and `CLAUDE.md`. Apply small doc edits directly, and route surface-specific writes to the subagent or skill that owns that surface.

## When to Use

- A doc was written and its parent index, cross-links, or quality gate need reconciling
- A new skill or agent was added and `CLAUDE.md` needs to reference it
- The repo structure changed and multiple files (index, cross-links, tables) must reflect it
- After `claude-analyze` identifies a skill/doc gap

## Step-by-Step Workflow

### 1. Identify Changed Files

List everything created or modified. If the change renamed or moved a folder, a skill, or an agent, run a stale-reference sweep across the docs, `.claude/skills/`, `.claude/agents/`, and `CLAUDE.md` before closing.

### 2. Map to Affected Targets

| Changed file area | Targets to update |
| --- | --- |
| A content doc / README | The parent index or table that lists it; verify with the repo's quality/brand skill if one exists |
| Repo folder structure (add/rename/remove a section) | The top-level index/TOC and any cross-links; confirm every link resolves and no duplicate ordering prefix exists |
| A runnable project or example folder | The doc that references it; check for stale `cd`/relative paths |
| `.claude/skills/` | `CLAUDE.md` (Skill usage / authoring-hygiene references); run the config lint |
| `.claude/agents/` | `CLAUDE.md` (Delegation discipline / agent roster) |
| A `CLAUDE.md` convention change | Propagate to the affected docs and skills |

### 3. Map to Affected Agents

Route code changes to the subagent that owns the surface, not the main thread. Use the repo's own agent roster under `.claude/agents/`; the typical split is:

| Changed area | Owning agent (typical) |
| --- | --- |
| Backend / API code | the backend agent |
| Frontend / UI code | the frontend agent |
| CI/CD, infra, deployment | the devops agent |
| E2E / QA verification | the QA agent |

If the repo defines no matching agent, apply the change on the main thread or via the relevant skill.

### 4. Apply the Update

- **Generated docs / guides:** route to the authoring skill that owns them, then verify with the repo's quality/brand skill if one exists.
- **`CLAUDE.md`, config, lessons file:** small, surgical edits on the main thread are fine; these are author-owned control files, not generated content.
- **Code:** delegate to the owning agent from Step 3.

Leave everything staged in the working tree; never auto-commit.

## Creating & updating skills (local + global)

Session learnings that are reusable rules/conventions/gotchas (not just a one-off doc line) belong in a skill. This leaf owns the create/update, locally in `.claude/skills/` and globally in `~/.claude/skills/`.

### 1. Decide: existing skill vs new skill

- **Update an existing skill** when the learning extends a topic a skill already owns. Prefer this; do not spawn a near-duplicate.
- **Create a new skill** only when no existing skill fits and the topic is coherent enough to trigger on its own.

### 2. Decide: local vs global

| The learning is… | Target |
| --- | --- |
| Tied to THIS repo — its paths, layout, project conventions | **Local** `.claude/skills/<name>/` |
| A generally reusable rule that helps across projects (for example the Windows `git mv` bin/obj lock fix, or the `disable-model-invocation` gotcha) | **Global** `~/.claude/skills/<name>/` via local-first authoring, then Push learnings |
| Reusable but first proven here | Author/refine local, then Push learnings up |

Global edits affect every project: surface the change and get a quick confirm before writing global.

### 3. Author the skill (hygiene gate — non-negotiable)

- Manifest filename is exactly `SKILL.md` (uppercase).
- YAML frontmatter has a non-empty `name` and `description`; the description carries concrete trigger phrases.
- `name` matches the folder/file identity, no drift between frontmatter, folder, `CLAUDE.md`, and any router reference.
- Description is scoped to the right project/paths; never leave a description copied from another repo. Global skills read as project-agnostic; local skills name this repo's surfaces.
- A user-invocable master skill must not set `disable-model-invocation: true`, or the Skill tool cannot launch it.
- **Verify:** `bash ~/.claude/scripts/lint-claude-config.sh <repo>` after any skill create/update.

### 4. Local <-> global sync (route to the `skill-sync` sibling leaf)

Do not hand-copy skill trees. The four sync operations are owned by [`skill-sync`](skill-sync.md):

| Goal | Operation |
| --- | --- |
| Promote a proven local skill/edit up to global (non-destructive) | Push learnings |
| Reinstate the global version down into a drifted local copy (destructive, global wins) | Pull skills |
| Two-way reconcile local <-> global to a best-of-both identical state | Reconcile |
| See what is synced / diverged before deciding | List / status |

Sync the whole skill folder, not just `SKILL.md`: every `references/*.md`, template, and nested subskill counts. A brand-new local skill with no global counterpart is a valid Push candidate.

Typical flow: prove the rule local -> lint -> (if globally useful) Push learnings -> confirm both copies converge.

### 5. Record it (close the loop)

- If a skill was created/renamed/promoted, run the stale-reference sweep (Step 1) so no router, `CLAUDE.md`, or agent points at an old name/path.
- Note the skill change in the session's learnings (lessons file) so the gap is marked addressed.
