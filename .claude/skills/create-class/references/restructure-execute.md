<!-- playbook -->

# Restructure execute: move a course tree onto a new outline

[module-toc-conception](module-toc-conception.md) decides what the tree should become. This leaf
performs it: turn the agreed outline into a crosswalk, move the folders without losing a byte,
prove it, then repair every index and link that pointed at the old shape.

Use it whenever module or topic folders are renumbered, reordered, merged, split or renamed. A
one-folder rename does not need the whole walk; step 1, step 4 and step 6 still apply.

Scripts live beside this skill: `scripts/renumber-tree.sh` and `scripts/link-check.sh`.

## Step 1. Read the live tree, then write the crosswalk

Derive the plan from disk, never from a doc, a roadmap or the session's own earlier listing. A tree
another session touched an hour ago is not the tree in your notes.

```bash
find demos -maxdepth 2 -mindepth 1 -type d | sort
```

Write the crosswalk as a plan file, one move per line, old then new, both relative to the repo root:

```text
# demos-renumber.plan
demos/03-agentic-coding	demos/04-agentic-coding
demos/04-agent-sessions	demos/03-agent-sessions
demos/05-cli	demos/05-cli-sdk/01-cli
demos/06-sdk	demos/05-cli-sdk/02-sdk
```

The plan is the artifact the whole run is checked against, so it is written before anything moves
and it is complete: every folder that changes position appears in it, including the ones that only
change because a sibling was inserted above them.

## Step 2. Place what the outline does not name

A customer outline is rarely exhaustive, and the gaps are not permission to improvise.

| Case | What to do |
| --- | --- |
| A topic exists on disk, the outline does not name it | Append it at the END of its module, keeping its content. Never interleave it among the named topics, never delete it |
| The outline names a topic that does not exist | Create the numbered folder so the numbering matches, with a three-line scaffold readme and no invented product facts. Record it as missing in the gap inventory |
| The outline skips a number entirely | Stop and ask. A skipped slot has several defensible readings, and they produce different trees |
| A module the outline never mentions | It keeps its current shape. Absence from the outline is not a deletion order |

The skipped-number case is worth the round trip. An outline that runs 2, 3, 4, 5, 7, 8, 9 can mean
"leave 6 empty", "the module you were told to drop moves into 6", or "the merged module was meant to
stay two modules". Offer the options with the resulting tree in each preview and let the owner pick:
a structural choice is read far faster as a tree than as a sentence, and the literal reading is not
always the one they want.

## Step 3. Move with the plan, not by hand

```bash
bash ~/.claude/skills/create-class/scripts/renumber-tree.sh --plan demos-renumber.plan --dry-run
bash ~/.claude/skills/create-class/scripts/renumber-tree.sh --plan demos-renumber.plan
```

The script validates the whole plan before touching anything (missing sources, duplicate
destinations, a destination that exists and is not itself moving), then moves every entry to a
unique temporary name before moving it to its final one. That two-pass shape is what makes a swap
safe: `03 -> 04` while `04 -> 03` collides on a naive single pass, and so does every rotation.

Doing this by hand costs a temp-name dance per cycle and gets it wrong under time pressure. The
script also prunes directories the plan emptied, and never removes one that still holds content.

## Step 4. Windows: build output holds the lock, not the editor

On Windows a `git mv` of any folder containing a .NET project fails with
`fatal: renaming '<path>' failed: Permission denied`. The handle is on the compiled output in the
gitignored `bin` and `obj`, held by the C# language server and the MSBuild node pool.

`renumber-tree.sh` recovers on its own: on a failed move it clears the untracked `bin`/`obj` under
the source, runs `dotnet build-server shutdown` once, and retries. Two things this session proved
about that recovery:

- **Deleting the artifacts once is not always enough.** A watcher re-acquires the handle within
  seconds, so the delete and the move must be a retry loop rather than two commands. A move that
  failed five times in a row succeeded on the next attempt with nothing else changed.
- **Do not mass-kill dev processes.** The locking process is usually not findable by path, and
  killing the editor is both destructive and unnecessary.

The full lock taxonomy, the Restart Manager diagnosis and the repo-rename case live in the global
`windows-project-rename` skill. Read it when the retry loop does not clear it.

## Step 5. Repair the indexes, one writer per file

The moves are mechanical and belong on the main thread. The prose repair is judgement and fans out
well: one agent per module, each given the full crosswalk, the target titles, and a hard minimal-diff
instruction.

**Every brief carries the WHOLE crosswalk verbatim, not that module's slice.** A module's readmes link
outward as often as inward, so an agent holding only its own rows cannot tell a correct link from a
stale one, and will either leave it or invent a target. Paste the plan file into each brief along
with the module title list and the rule that unnamed topics were appended at the end.

What each module agent owns:

- the module readme TOC, in the outline's order with the outline's titles
- every relative link inside its own topic readmes, verified by testing the resolved path
- prose that names a path, including backslash paths inside prompt blocks

Reserve for the coordinator, because they are cross-cutting: the master `demos/readme.md` TOC, the
narrative paragraphs that walk the modules in order, the schedule table, and the root `CLAUDE.md`
layout description.

**Give exactly one agent write authority over any given file.** A verify phase with two agents that
can both fix will have each of them see the other's edits as an unexplained concurrent writer, and
a report that says "corrected by someone else during my run" is not a verification you can quote.
A second reviewer is valuable, but it reports and the writer applies.

Depth changes bite here: a topic that moved from `demos/05-cli/03-x/` to
`demos/05-cli-sdk/01-cli/03-x/` needs every `../../` in it to become `../../../`. Say so in the
brief; it is the single most missed class of breakage.

## Step 6. Prove it, then lead the report with the proof

```bash
bash ~/.claude/skills/create-class/scripts/link-check.sh --scope demos
```

It resolves every internal markdown link against its own file's directory (root-anchored `/...`
against the repo root), checks that every numbered sibling set runs `01..NN` with no gap or
duplicate, and checks each numbered folder has a readme. The summary line is assertable:

```text
files=113 links=298 broken=3 prefix_defects=0 missing_readme=0
```

A non-zero `broken` count that predates the restructure is reported as such, with the reason it
cannot be fixed mechanically (target deleted rather than renamed), not silently carried.

**Then open the report with the loss receipt, unprompted.** A bulk rename looks exactly like a
mass deletion in a file explorer and in most git UIs, and the owner watching 600 paths disappear
will conclude the demos are gone. `renumber-tree.sh` prints the receipt, and it is two commands by
hand:

```bash
git ls-files demos | wc -l                                    # same count as before
git ls-tree -r HEAD demos | awk '{print $3}' | sort | md5sum   # same blob set as HEAD
git status --porcelain demos | awk '{print $1}' | sort | uniq -c
```

`628 R, 0 D` plus an identical blob hash is the whole argument: same files, same contents, different
paths. Put that and the old-to-new table at the top of the completion message. Extracting it later,
after the owner has asked twice whether the work was lost, costs far more than stating it first.

## Step 7. Close the loop

- Write the gap inventory: what the outline names that has no content, what exists that the outline
  does not name and where it was placed, which modules the outline never covered, and which readmes
  are thin. Facts and line counts measured with `wc -l`, no roadmap.
- Update the root `CLAUDE.md` layout section: module count, day count, the module-name chain, and any
  example path that named a folder which no longer exists.
- Run the repo's brand-voice skill over every readme the pass rewrote.
- Never commit. Leave the whole restructure in the working tree for the owner to review.
