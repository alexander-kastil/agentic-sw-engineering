# claude-learn-distribute — Documentation & Context Distribution

Take a change (from an implementation or from the analyze leaf) and propagate it to every file that references it: module READMEs, skills, agents, `CLAUDE.md`, and `.inventory/`. This repo has no documentation agent, so writes go through `create-class` + `brand-voice-gh-copilot`, the `guide-validator` agent, or direct edits.

## When to Use

- A guide or module README was written and its parent tables, `.inventory/`, or brand voice need reconciling
- A new skill or agent was added and `CLAUDE.md` needs to reference it
- The `demos/` structure changed and multiple files (TOC, crosswalk, cross-links) must reflect it
- After `claude-analyze` identifies a skill/doc gap

## Step-by-Step Workflow

### 1. Identify Changed Files

List everything created or modified. If the change renamed or moved a `demos/` folder, a skill, or an agent, run a stale-reference sweep across `demos/`, `.inventory/`, `.claude/skills/`, `.claude/agents/`, and `CLAUDE.md` before closing.

### 2. Map to Affected Targets

| Changed file area | Targets to update |
| --- | --- |
| A topic `demos/**/readme.md` | Verify with `brand-voice-gh-copilot`; sync the parent module readme topic table; update `.inventory/` if the topic's status changed |
| `demos/` folder structure (add/rename/remove a module or topic) | `demos/readme.md` TOC; `.inventory/target-structure.md` crosswalk; confirm every TOC link resolves and no duplicate numeric prefix exists |
| A runnable project under `src/` or a demo subfolder | The demo topic readme that references it; check for stale `cd`/relative paths |
| `.claude/skills/` | `CLAUDE.md` (Skill usage / authoring-hygiene references); run the config lint |
| `.claude/agents/` | `CLAUDE.md` (Delegation discipline / agent roster) |
| A `CLAUDE.md` convention change | Propagate to the affected `demos/` READMEs and skills |

### 3. Map to Affected Agents

Route code changes to the agent that owns the surface, not the main thread:

| Changed area | Owning agent |
| --- | --- |
| `.NET` / API demo code | `net-agent` |
| Angular / frontend demo code | `angular-agent` |
| CI/CD, Azure infra, deployment demos | `github-devops-agent` |
| E2E / Playwright verification | `playwright-agent` |
| A single guide needing brand-voice/author-guide validation | `guide-validator` |

### 4. Apply the Update

There is no docs agent to hand off to. Apply updates through the right channel:

- **Module READMEs and guides:** route to `create-class` (enrich-module for a module readme, author-guide for a demo/lab guide), then verify with `brand-voice-gh-copilot`. For a single guide, the `guide-validator` agent can validate in place.
- **`CLAUDE.md`, `.inventory/`, `tasks/lessons.md`:** small, surgical edits on the main thread are fine; these are author-owned control files, not generated guides.
- **`src/` code:** delegate to the owning agent from Step 3.

Leave everything staged in the working tree; never auto-commit.

## Creating & updating skills (local + global)

Session learnings that are reusable rules/conventions/gotchas (not just a one-off doc line) belong in a skill. This leaf owns the create/update, locally in `.claude/skills/` and globally in `~/.claude/skills/`.

### 1. Decide: existing skill vs new skill

- **Update an existing skill** when the learning extends a topic a skill already owns (a brand-voice rule -> `brand-voice-gh-copilot`; an authoring-flow gotcha -> `create-class`). Prefer this; do not spawn a near-duplicate.
- **Create a new skill** only when no existing skill fits and the topic is coherent enough to trigger on its own.

### 2. Decide: local vs global

| The learning is… | Target |
| --- | --- |
| Tied to THIS repo — its module paths, `demos/`/`src/` layout, course conventions | **Local** `.claude/skills/<name>/` |
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

Typical flow: prove the rule local -> lint -> (if globally useful) Push learnings -> confirm both copies converge.

### 5. Record it (close the loop)

- If a skill was created/renamed/promoted, run the stale-reference sweep (Step 1) so no router, `CLAUDE.md`, or agent points at an old name/path.
- Note the skill change in the session's learnings (`tasks/lessons.md`) so the gap is marked addressed.
