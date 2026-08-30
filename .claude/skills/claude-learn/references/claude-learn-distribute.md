# claude-learn-distribute: capture and propagate (task 2)

Take a change (from an implementation or from [claude-analyze](claude-analyze.md)) and propagate it to every file that references it: docs, skills, agents, `CLAUDE.md`. Small doc edits inline; surface-specific writes to the agent or skill that owns the surface.

## When to use

- A doc was written and its parent index, cross-links or quality gate need reconciling.
- A new skill or agent was added and `CLAUDE.md` must reference it.
- Repo structure changed and multiple files (index, cross-links, tables) must follow.
- After `claude-analyze` reports a skill/doc gap.

## Prerequisites

- Know which files changed, from the implementation or from the analysis output.
- Know which docs and agents are affected, from the repo's own doc map if it keeps one.

## Procedure

### 1. Identify changed files

List everything created or modified. **On any rename or move of a folder, skill or agent, run a stale-reference sweep** across `docs/`, `.claude/skills/`, `.claude/agents/` and `CLAUDE.md` before closing. Agent files carry their own lists of docs they read and skills they invoke, so re-read each one under `.claude/agents/` and fix stale paths/names. The roster is per-repo; do not assume one.

**A rename chain that frees a name and later reuses it defeats the sweep.** Renaming `a.md` to `b.md` and then `c.md` to `a.md` leaves every inbound `a.md` link resolving, and a grep cannot tell a link that meant the old occupant from one that means the new. Sequence the chain so the freed name is reused only after its old meaning has been retargeted everywhere, then check the surviving hits one by one and say in the report which were retargeted and which legitimately point at the new occupant. A path that still exists is not evidence its references still mean what they meant.

**Sweep for stale claims, not only stale paths.** A control file's sentences decay the same way its links do, and the worst case is a claim that something was REMOVED: the natural check, grepping for the thing, returns the skill that describes it generically plus dated historical logs, and that output reads as perfectly consistent with the removal. A negative claim is the one class a search cannot confirm. Disprove it by enumerating what it says is absent: `ls` the tree, read the config keys, list the workflow files. This matters most in `CLAUDE.md` and `.claude/agents/`, which steer every session and get quoted rather than checked, so a wrong removal claim there silently scopes an agent out of a surface it still owns. Fix it in the same pass and grep for its copies; a removal note is usually pasted into more than one file. The mirror-image error is reading `git ls-files` as history: it lists the current index, so a file deleted last week returns nothing and looks like it never existed. Use `git log --all --diff-filter=A -- <path>` before saying a path was never there.

**A rewrite to a narrower shape orphans whatever the shape excludes.** A spec that says what a file becomes says nothing about what it held. Before rewriting, list what the current file carries that the new shape has no slot for, rehome it first, and only then re-point inbound references at the new home rather than at the renamed file. Search for those references outside `docs/` too: a compose header comment, a slash command and a top-level readme all link to docs and none of them appears in a docs-only search. Require the writing agent to report what it dropped as a named list, because a rewrite is not a diff a reader can audit.

### 2. Map to affected targets

| Changed area | Targets |
| --- | --- |
| A content doc / README | Parent index or table listing it; verify with the repo's quality/brand skill if one exists |
| Repo folder structure (add/rename/remove) | Top-level index/TOC and cross-links; every link resolves, no duplicate ordering prefix |
| A runnable project or example folder | The doc referencing it; check stale `cd`/relative paths |
| `.claude/skills/` | `CLAUDE.md` skill usage / authoring hygiene; run the config lint |
| `.claude/agents/` | `CLAUDE.md` delegation discipline / agent roster |
| A `CLAUDE.md` convention change | The affected docs and skills |

### 3. Apply the update

- **Generated docs / guides**: route to the authoring skill that owns them, then verify with the repo's quality/brand skill if one exists.
- **`CLAUDE.md`, config, lessons file**: surgical main-thread edits; author-owned control files, not generated content.
- **Code**: delegate to the owning agent from the repo's `.claude/agents/` roster. No matching agent → main thread or the relevant skill.

Leave everything in the working tree; never auto-commit.

## Creating and updating skills

A learning that is a reusable rule, convention or gotcha (not a one-off doc line) belongs in a skill. This leaf owns create/update, local `.claude/skills/` and global `~/.claude/skills/`.

### 1. Existing skill vs new skill

- **Extend an existing skill** when it already owns the topic. Default; never spawn a near-duplicate.
- **New skill** only when nothing fits and the topic is coherent enough to trigger on its own.

### 2. Local vs global

| Learning | Target |
| --- | --- |
| Tied to THIS repo: its paths, layout, project conventions | **Local** `.claude/skills/<name>/` |
| Generally reusable across projects | **Global** `~/.claude/skills/<name>/` via local-first authoring, then Push learnings |
| Reusable but first proven here | Author local, then Push learnings up |

**Promoting a new learning to global is the default, not a question.** Author local, Push, then *report* what went up.

Ask first only when:

- the content is project-specific and would misdirect other repos (see Push screening), or
- the promotion would **overwrite or delete** existing global content rather than add to it.

Adding a new file to global, or extending a global rule with a case it did not cover, needs no permission.

### 3. Worth-authoring gate (run before writing anything)

Decide skill-worthiness with fixed checks, not judgement. A learning must pass all five:

| Check | Fails when |
| --- | --- |
| Three or more concrete steps or rules | It is a single fact -> lessons file line |
| Carries a worked example or trigger phrases | Nothing would ever route to it |
| Applies beyond the occasion that produced it | One-off -> doc edit |
| Nothing existing already owns the topic | Extend that skill instead |
| You can state how a reader proves it still holds | Unverifiable -> not durable |

Any fail means the learning is a lessons entry or a doc edit, not a skill. Running this before authoring is what stops the near-duplicate skills step 1 warns about.

### 4. Hygiene gate (non-negotiable)

- Manifest filename is exactly `SKILL.md` (uppercase).
- Frontmatter has non-empty `name` and `description`; the description carries concrete trigger phrases.
- `name` matches the folder identity: no drift across frontmatter, folder, `CLAUDE.md`, router references.
- Description scoped to the right project. Global skills read project-agnostic; local skills name this repo's surfaces. Never leave a description copied from another repo.
- A user-invocable master skill must **not** set `disable-model-invocation: true`, or the Skill tool cannot launch it.
- Leaves are `references/<leaf>.md` with **no** `name`/`description` frontmatter; shared assets in a sibling `templates/`. Never nest a `SKILL.md` inside another skill's folder. A leaf that must be independently discoverable becomes a top-level peer skill.
- Every skill states how a reader proves it still holds: the command to run, the file to check, the behaviour to observe. A skill with no way to verify it rots silently and only surfaces later as drift.
- **Leaf budget: 275 lines AND 12 `##` sections. A leaf over either one gets SPLIT IN THIS RUN, not noted for later.** This is the step where the library reorganizes itself: reviewing a skill and leaving a 600-line leaf in place is how it got that way.
- **Verify:** `bash ~/.claude/scripts/lint-claude-config.sh <repo>` after any skill create/update.

#### 4a. The leaf budget, and what to do when a leaf breaks it

Both numbers, because either alone misjudges. A 210-line leaf with 5 sections is few large ideas and is fine; a 200-line leaf with 20 sections is twenty unrelated ideas sharing one file, and every arrival pays for all twenty.

```bash
for f in <skill>/references/*.md; do
  printf "%4d %3d  %s\n" "$(wc -l < "$f")" "$(grep -c '^## ' "$f")" "$(basename "$f")"
done | sort -rn
```

**The fix is a SPLIT or a DISSOLVE, never a trim. Do not delete content to get under the budget.**

1. **Dissolve first.** For each section ask which sibling leaf already owns that topic, and replace the section with a one-line link to it. Splitting before dissolving multiplies the duplicate into two files and two router rows. Before deleting, open the destination and confirm it genuinely carries the topic: it usually owns the idea but not every detail, and the details it lacks move there rather than dying.
2. **Then split, by arrival question, never by subject.** The test for a correct split: a reader with one question opens exactly one leaf and reads all of it. A section kept because it is "related" is the same failure returning.
3. **Route both layers.** Every new leaf needs a `SKILL.md` row (the edge) AND trigger phrases in the `description` frontmatter (the index). A leaf with no row is unreachable; a row pointing at a moved leaf is a dead edge. Both fail silently.

**A PLAYBOOK is exempt from the section cap and gets a 400-line allowance.** A playbook is one sequential procedure whose `##` sections are its STEPS, so its section count measures the length of a single walk, not a count of unrelated ideas, and splitting it breaks the walk. Mark it `<!-- playbook -->`; the guard also auto-detects a majority of numbered-step headings. When a playbook does run long, extract only what is NOT part of the sequence (variants, reusable verification clusters, hygiene appendices) and never the numbered steps themselves.

The case that produced this rule: `deploy-hetzner-box/references/estate-onboarding.md`, 251 lines and 17 sections, was called the second-worst mega-note in the library on its section count. 13 of those 17 are `## Step N.` of one onboarding run. Judging it on section count alone would have shredded a working procedure. **Read what the sections ARE before counting them.**

Two causes this budget exists to catch, only one of which is about length:

- **Mega-note.** Many small ideas with no shared reader, so using one line of the leaf loads all of them.
- **Collapsed layer.** A leaf that was the concrete INSTANCE of a pattern beside a generic sibling becomes a DUPLICATE of that sibling the moment its project specifics are stripped, with no edit to its sections. **Generalizing a leaf is a re-decision of what the node is for, not a rename.**

**Aligned with the write-time guard.** `.claude/hooks/skill-leaf-guard.sh` enforces the same 275/12 on every write to `.claude/skills/*/references/*.md` in both roots, with the same three-step fix and the same orphan/dead-edge checks. Change one and change the other, or a leaf passes review here and then fails the write. Budgets and how to measure a trim: [[context-engineering]] `references/graph-engineering.md`.

### 5. Review gate: produce, critique, refine, on a score

Authoring and review are separate passes. The pass that just wrote a skill is the worst judge of whether it is worth installing. One YES/NO review is better than none, but it gives no signal about whether a second pass would help, so the gate runs as a scored loop instead.

**Critique.** Re-read the finished file cold and answer:

```
Would an experienced engineer install this skill and use it without editing it first?

Score it 1-10 on that question, then:
- one paragraph of reasoning for the score
- the single biggest thing holding it below 10
- the minimum change that would raise the score

Do not rewrite the skill.
```

**Refine.** Apply the named minimum change, nothing else. A critique that produced one objection does not license a rewrite: the loop measures whether targeted changes are still buying anything, and a rewrite destroys that measurement.

**Re-score** the changed file with the same prompt, cold.

**Stop** at either condition:

- the score reaches 9, or
- the score plateaus: a pass that raises it by nothing, or by a point the critique cannot name a concrete reason for.

A plateau below 9 is information, not failure. It means the remaining gap is structural: usually the skill is two skills fused (split it, per step 1) or the learning was never skill-worthy (step 3 should have caught it, send it back to a lessons entry or a doc edit). Iterating further on the prose will not move it.

Report the score trajectory with the promotion, for example `6 -> 8 -> 9`, so the next reader knows how much scrutiny the file has had.

### 6. Sync

The four operations (Push learnings / Pull skills / Reconcile / List) are owned by [skill-sync](skill-sync.md). Do not hand-copy skill trees.

Flow: prove the rule local → lint → Push learnings → confirm both copies converge.

### 7. Record it

- After a skill create/rename/promotion, re-run the step 1 stale-reference sweep so no router, `CLAUDE.md` or agent points at an old name.
- Mark the gap addressed in the session's lessons file.

## Docs agent handoff

When the repo defines a docs agent, route doc writes to it:

```
**Files changed:**
- {file}: {what changed}

**Affected docs:**
- {doc}: needs {update description}

**Affected agents:**
- {agent}: needs {reference update}

**Action:** verify and apply.
```

No docs agent → apply the doc edits directly. Either way leave everything staged; never auto-commit.
