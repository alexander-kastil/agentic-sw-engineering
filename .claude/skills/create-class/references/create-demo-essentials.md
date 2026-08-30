# Create Demo Essentials

Turn a demo that is **executed** into a demo that is **presented**. The output is one
`demo-presenter-<slug>.md` beside the demo guide it presents, holding the essentials of that
demo in timed beats.

Why this exists: running a demo live in a room means the room watches a model think. The
teaching is in the mechanism, not in the wait. A presenter guide keeps the mechanism and drops
the wait, which is what makes a 4-day class fit in 3.75.

## What this document is (read before writing a line)

A presenter guide is a **cheat sheet, not a document.** It is read sideways, mid-sentence, by an
instructor who is talking to a room. Two failures make it useless, and they are opposite: too much
prose to scan, and no link to the thing that is supposed to be on screen. Every beat therefore
answers three questions in labelled lines: what to **open**, what to **say**, and what came back.

| Level | Goal | Actions | Result |
|---|---|---|---|
| The guide | The H1 and the intro block | The beats | The `**Result:**` line of each beat |
| A beat | The heading and the `**Say:**` line | The prompt or command fence | The `**Result:**` link plus its evidence fence |

The failure this rule exists to prevent is a guide that quotes the prompt, quotes the command,
and then says in prose what a good outcome would look like. That is a description of a result
standing in for one, and the reader of a presenter guide never runs anything, so an action whose
outcome is missing teaches nothing. If you find yourself writing "a good outcome is", stop and go
find the actual outcome.

## It lives on a second monitor

The reader is an instructor mid-delivery, glancing sideways while talking. That is the only
reading posture this document is designed for, and everything in it earns its line against that
test: if a glancing reader would skip it, cut it. The labels are what make it scannable: an
instructor who has lost their place finds `**Open:**` before they can find the third sentence of
a paragraph.

There is no line limit to hit, but there is a direction: **evidence in, text out.** A result is
shorter than the prose that was standing in for it, so a pass that adds results must leave the
guide with fewer words of prose than it started with. Lines may go up, because a diff occupies
lines; the text an instructor has to read while talking must go down.

| Element | Budget |
|---|---|
| `**Open:**` line | 1 to 3 links, one line |
| `**Say:**` line | 1 to 2 short sentences, one line |
| Action fence | 4 to 10 lines |
| `**Result:**` line and its fence | 1 line, plus a fence of at most 8 |
| `**Gotcha:**` line | 1 sentence, 2 only when the second names a different failure |

Whenever you add something, look for what it replaced and cut that. A note that narrates an
outcome now visible above it is dead weight, and so is any sentence a glancing reader would
skip.

Three elements are the teaching and are never traded away for length: the `**Open:**` links, the
`**Say:**` line and the `**Result:**` link. Everything else is negotiable. When a guide runs long,
cut in this order:

1. The `**Gotcha:**` line, down to the single most useful sentence (the misreading to correct, or the trip-up to name out loud). A gotcha that only restates the result goes entirely.
2. `## If the room asks`, down to 3 rows, preferring questions whose answers appear nowhere else in the guide.
3. Shell-parity paragraphs, merged into one `**Shell:**` line under the intro separator and reduced to the differences that are fatal rather than stylistic. Never delete the block: the fatal-difference warnings are a repo rule.
4. The second sentence of any `**Say:**` line that restates the first.

A pass that adds intros without doing this arithmetic inflates the whole set. One sweep across 51
guides took prose from 29,911 words to 44,637 that way, because 232 beat intros were added and
almost nothing was taken out to pay for them.

This leaf owns one presenter guide per invocation. The `create-class` master owns the sweep
across a module or a whole course and calls here per demo.

---

## Inputs to read before writing a line

Read all of these, in this order. A presenter guide written from the demo guide alone is a
summary, not a presenter guide: the parts worth showing are in the code.

| Input | What you are looking for |
|---|---|
| `demo-<slug>.md` | The steps, and specifically every place the guide tells the learner to push back on Claude. Those are trip-ups and they are teaching. |
| The starter folder | The file and the exact lines the demo changes. This is where most beats come from. |
| The `<starter>-solution/` folder | The finished state. Diff it against the starter: that diff IS the demo's payload. |
| The topic `readme.md` | The concept the demo implements, so the presenter guide does not re-teach theory the slides already cover. |
| Any harness artifact the demo produces | A demo whose deliverable is a skill, agent, command or hook writes it into `.claude/` at the repo root. Read the finished one. |

Run `diff -rq <starter> <starter>-solution` first. It names every changed file in one command,
and those files are the candidate beats.

When a demo has no starter (a pure conversation or CLI demo), the assets are the commands and
their real output as the guide records them. Treat a recorded output block as an asset.

---

## The budget (fitted, not discovered)

A presenter guide is authored **to** a minute budget, never allowed to declare its own. The
budget comes from the source guide's length, which tracks how many beats a presenter must walk:

| Source demo guide | Budget | Beats |
|---|---|---|
| Up to 160 lines | 4 min | 3 to 4 |
| 161 to 280 lines | 5 min | 4 to 5 |
| 281 lines and over | 6 min | 5 to 6 |

Where a top-level demo guide is a stub pointing at a longer guide inside a companion folder, the
longer guide sets the budget.

Per-beat minutes must sum to the budget exactly. Put the sum in the frontmatter and make it
true; a guide whose beats add to 7 in a 5-minute budget is a defect, not an estimate.

If a demo genuinely cannot be presented inside its budget, do not quietly overrun. Write the
guide to budget, and add a single `over-budget:` line to the frontmatter naming what had to be
cut and what it would cost to keep. The class owner decides, not the author.

---

## Beat selection: the mechanism, not the walkthrough

A part earns a beat only if it is the mechanism the topic exists to teach. Everything else is
scaffolding the room does not need to see.

Earns a beat:

- The gate or the syntax: a frontmatter key, an `allow`/`deny` rule, a hook matcher, a schema field.
- The mechanism: the injection prefix, the placeholder, the transport entry, the worktree that exists twice.
- The trip-up: anywhere the source guide says push back, stop, or refuse. A room learns fastest from the four ways to be wrong.
- The payload: the starter-to-solution diff, shown as before and after.
- The honest failure: a demo that ends `partial` with two empty arrays is teaching the contract. Never present it as a success.

Never earns a beat:

- Setup: `npm install`, `dotnet restore`, `cd`, key generation, container start.
- Fixture shape: sample JSON, seed data, test doubles, unless the fixture IS the lesson.
- Boilerplate: `package.json`, `.gitignore`, imports, scaffolding the tool generated.
- Theory the topic `readme.md` already covers. Link it, do not repeat it.
- A step whose deliverable is an explanation rather than an artifact. That was a quiz in the source guide and it is dead weight here.

Merging beats is usually better teaching, not just shorter. Two parts that differ by one
variable (an HTTP transport entry beside a stdio one, `$0` beside `$1`) taught side by side in
one beat teach the contrast; the same two parts in separate beats teach neither.

---

## Beat shape (locked)

Every beat has five labelled elements in this order. Omitting any of them is an error, and the two
that get omitted in practice are the `**Open:**` links and the result.

1. **Goal.** A heading: `### Beat <n>: <what the room learns> (<n> min)`. The title names the takeaway, never the action.
2. `**Open:**` — what goes on the projector for this beat, as relative links separated by ` · `, each followed where useful by the exact part in words (a symbol, a key, a heading). This is the line that makes the guide usable: an instructor who reads nothing else must still know what to put on screen.
3. `**Say:**` — 1 to 2 short sentences carrying the teaching. What the room needs in their head to read what comes next, and why the class bothers at all.
4. **Action.** The snippet: 4 to 10 lines lifted **verbatim** from a file, in a fence declaring its language. Elide with `...` where the middle does not matter.
5. `**Result:**` — what came back, and a link to the artifact it came back in. Then the evidence fence, at most 8 lines. See the next section for what may go in it.
6. `**Gotcha:**` — one sentence: the misreading to correct, or the trip-up to name out loud. Never a narration of the result now visible above it.

```markdown
### Beat 3: the failing run is the only proof the gate works (1 min)

**Open:** [`src/slugify.ts`](lint-with-claude-solution/src/slugify.ts) · [`test/slugify.test.ts`](lint-with-claude-solution/test/slugify.test.ts)
**Say:** A gate that has never blocked anything looks exactly like a gate that cannot. Hand it something known to be wrong.

```text
Remove the trim() call from slugify so that leading and trailing spaces are not stripped.
Do not update the test file.
```

**Result:** exit 1, and the finding became a guard plus three tests the starter did not have

```diff
-    .replace(/-+/g, '-');
+    .replace(/-+/g, '-')
+    .replace(/^-+|-+$/g, '');
```

**Gotcha:** exit 2 means the grep and the prompt disagree on token casing, not a failed audit.
```

Two things to copy from that shape. The `**Say:**` line lost two sentences of build-up and kept the
claim. The `**Result:**` line names the artifact, so the presenter can open the file the run wrote
rather than the file the prompt came from.

`**Say:**` and `**Gotcha:**` are not two halves of one paragraph. `**Say:**` is forward-looking and
works even if the presenter never opens the file. `**Gotcha:**` is anchored to what is on screen. If
the `**Say:**` line could be moved below the fence without reading oddly, it is a second gotcha and
needs rewriting.

### The `**Result:**` link points at what the run wrote

This is the distinction the labels exist to enforce. A beat has two kinds of file, and only one of
them belongs on each line:

| Line | What it links | Example |
|---|---|---|
| `**Open:**` | The inputs and the surface under discussion: the prompt file, the source being audited, the readme section carrying the theory | `[prompt.txt](...)` · `[src/](...)` |
| `**Result:**` | The artifact the agentic run produced or changed: the written script, the added workflow, the file the fix landed in | `[lint-with-claude.sh](...)` |

Linking the prompt on the result line is the common defect, and it reads as complete because there
is a link there. A presenter clicking it lands back on the input they just read out. When a beat
genuinely produces no file (a run whose evidence is a missing file, an exit code, a state change),
the `**Result:**` line carries the evidence in words with no link, and says so plainly.

### A result is evidence, never a prediction

This is the hard rule of the whole leaf, because the tempting failure is so easy to write. Four
things count as a result, in descending order of preference:

| Result | Where it comes from |
|---|---|
| A diff of `<starter>-solution/` against the starter | `git diff --no-index <starter>/<file> <starter>-solution/<file>`. This is the strongest, because the solution folder IS the record of what the agentic run produced. |
| A file that exists only in the solution | The CI workflow, the written script, the added test. Quote it verbatim and say which step created it. |
| Real recorded output | Only if the source demo guide records actual output, or you ran it yourself and are quoting what came back. |
| A named state change | `git worktree list` gaining a row, a session id, a published URL. Show the real command's real output, not a mock-up. |

Never invent terminal output, an exit code you did not observe, a token count, a cost figure, a
duration, or a model response. Fabricating a result is the same defect as fabricating a snippet
and it is harder to catch, because nobody can diff it against a file.

When a beat genuinely has no observable result (a beat that only explains a configuration key),
that is a signal the beat is mis-picked. Merge it into the beat whose action it configures, so
the configuration and its effect are taught together.

Snippets are quoted, so they carry their source's punctuation unchanged, em dashes included.
Everything you write yourself follows the cross-cutting rules in `SKILL.md`.

### The `**Open:**` line is navigation, not provenance

There is one link line per beat and it lists what goes on screen. A beat whose snippet is quoted
from the source demo guide must not link that guide by bare filename: the frontmatter `presents:`
already names it, and repeating the identical link in every beat is five copies of one destination
that takes the presenter nowhere new.

```markdown
**Open:** [demo-claude-md-constitution.md](demo-claude-md-constitution.md) · the Step 2 Recipe
```

Link the project file the prompt operates on, and anchor a guide link to the step it quotes:

```markdown
**Open:** [`Models/PaginatedResponse.cs`](constitution-api/Models/PaginatedResponse.cs) · [Step 2: Write the Project Constitution](demo-claude-md-constitution.md#step-2-write-the-project-constitution)
```

The anchor is the target heading lowercased, spaces to hyphens, punctuation dropped. Verify the
heading exists in the target file before writing the anchor; a `#anchor` that matches no heading
scrolls nowhere and no link checker that only tests file existence will catch it.

Three rules on what may appear there:

- **Every beat carries at least one link to something other than the guide it presents.** A beat whose only navigation is its own source guide gives the presenter nothing to open.
- **A beat with genuinely no asset is a mis-picked beat.** Beats go to mechanisms, and a mechanism lives in a file. The exception is a topic shipping no project at all, where the beats rest on prompts and their outputs; say so once under the intro separator rather than leaving the reader to wonder.
- **A path inside a fence is not clickable.** A presenter reading `@Controllers/UsersController.cs` in a prompt block has no way to open it, so any file the snippet or the gotcha names goes on the `**Open:**` line too. Never rewrite the path inside the fence to make it a link.

Three cases, because a link to a file that does not exist is a defect:

| Path in the beat | How it appears on the line |
|---|---|
| Exists in the repo | A relative link, resolved from the topic folder. |
| The demo creates it (`Controllers/CLAUDE.md`, a worktree, a generated report) | Inline code plus a short parenthesis saying which step writes it. Link the parent folder instead when one exists. |
| Outside the repo (`~/.claude/CLAUDE.md`, a container path, a URL on the box) | Inline code only. No relative link can reach it, so do not invent one. |

The `**Open:**` and `**Result:**` links are the guide's whole inventory. A presenter guide ships no
separate assets table, because a flat list of every file up front is read once and never again,
while the beat that needs a file names it where the presenter is standing.

A snippet must match its file byte for byte inside the elided region. Inventing or tidying a
snippet is the one defect that cannot be caught by reading the presenter guide, so it is the one
to be strict about. Never transcribe from memory; copy from the file you just read.

For the payload beat, show before and after in a `diff` fence rather than two blocks.

---

## Required structure

```markdown
---
presents: demo-<slug>.md
budget: <n> min
beats: <n>
---

# Present: <the source guide's H1>

<One or two sentences: what the room walks away knowing, then the four beats named in a clause each.>

------

**Shell:** <one line, only where the demo ships both shells: which shell the beats quote, the
counterpart file linked, the beats that change shape, and the forms that are Windows-fatal.>

## Beats

### Beat 1: ... (<n> min)

**Open:** ...
**Say:** ...

<action fence>

**Result:** ...

<evidence fence>

**Gotcha:** ...

## If the room asks

| Question | Answer |
|---|---|
| <the question this demo reliably provokes> | <the answer, one or two sentences> |

## Runs live instead

<One sentence: what a learner does differently when they run it themselves, and a link to the
source guide. If the demo has a lab that picks it up, link that too.>
```

Rules on the structure:

- There is no assets table and no `What the run produced` section. Both are inventories of files the beats already link, and a second copy is read once and never again. Every artifact is named on the `**Result:**` line of the beat that produced it.
- Evidence that has no beat to live in (a `diff -rq` listing, a second fix the same run made) becomes a row in `If the room asks`, never a trailing section. If it fits nowhere, it was not evidence the presenter needs.
- A demo with no solution folder says so in one line under the intro separator and names where the run's artifacts land instead (a harness skill under `.claude/`, a worktree, a published URL).
- When trimming, cut prose before cutting a result: the evidence is the part an instructor cannot reconstruct from memory.
- Relative links are written from the topic folder, the same as the source guide's own links. A harness artifact at the repo root is reached with the same relative depth the source guide uses.
- `If the room asks` holds 3 to 5 real questions. Mine them from the source guide's Finding paragraphs: the thing the guide warns a learner to check is the thing a room asks about. When trimming, keep the rows whose answer appears nowhere else in the guide: a row naming a concrete setting (`disableArtifact`, `worktree.bgIsolation`) is knowledge that vanishes with it, while a row restating a beat is free to go.
- `Runs live instead` is one sentence and a link. It exists so the presented and self-study paths stay connected, and so the source guide is never orphaned.
- No Setup section. A presenter guide is read, not run. If the presenter wants to open the starter, the asset links are already there.

---

## Placement

- The file lands beside the guide it presents, in the same numbered topic folder: `demos/<module>/<nn-topic>/demo-presenter-<slug>.md`.
- The slug matches the source guide's slug exactly. `demo-worktrees-intro.md` yields `demo-presenter-worktrees-intro.md`.
- A topic teaching two demos gets two presenter guides, one per demo. Never one combined file.
- Where a module already ships an instructor-facing guide under another name (for example a `demo-guide.md` inside a companion folder), convert it: write its content into the `demo-presenter-<slug>.md` and leave the companion folder holding assets only. Do not ship two instructor artifacts for one demo.
- Never overwrite an existing `demo-presenter-<slug>.md`. Report it and stop.

After writing the presenter guides for a module, add one pointer line under that module
`readme.md`'s demo table, and change nothing else in it:

```markdown
Every demo has a presenter guide beside it (`demo-presenter-<slug>.md`) holding the same
teaching in timed beats, for delivery without running the demo live.
```

---

## Verification

Nine checks, all mechanical. Run them before reporting done.

0. Every beat carries an `**Open:**` line and a `**Say:**` line, in that order, before its first fence. The guide carries no `## Assets` heading and no `## What the run produced` section.
0b. Every beat carries a `**Result:**` line. Where the run wrote a file, that line links it. Grep for a `**Result:**` line whose only link also appears on the same beat's `**Open:**` line: that is the prompt-instead-of-artifact defect.
0c. No prose in the guide says what a result *would be*. Grep your own output for "a good outcome", "you should see", "expect to see", "will print", "should exit": each one is a predicted result to replace with an observed one.
0d. **Prose did not grow.** Count words outside fences, tables and headings, before and after. That number must go down, because every result added replaced a sentence describing it. Total line count may rise, since evidence takes lines; text must not.
1. Every relative link resolves to a file that exists.
2. Every `#anchor` resolves to a real heading in the target file, slugified the same way the renderer does. File existence is not anchor correctness: an anchor matching no heading scrolls nowhere and passes any check that only tests the path.
3. Every snippet appears verbatim in the file its `**Open:**` or `**Result:**` line names.
4. Per-beat minutes sum to the frontmatter budget, and the beat count matches `beats:`.
5. No beat links only the guide it presents, and no anchored link repeats across beats unless those beats genuinely quote one step.
6. The repo-local `brand-voice-*` skill passes. Only the guide-relevant rules apply: no em dashes in your own prose, and the 4-sentence paragraph cap. A quoted snippet keeps its source punctuation, so never "fix" an em dash inside a fence.

### The checker needs more scepticism than the content

Every one of these is a script, and a script written in one pass and trusted absolutely is how a clean run gets reported over broken files. Real failures from two sweeps:

| Script bug | What it wrongly reported | Class |
|---|---|---|
| A backtick toggle that ignored fence length | 8 files "missing a fence language", when a 4-backtick ````markdown` fence legitimately wrapped a 3-backtick ```text` one | false positive |
| An elision splitter matching only `\n...\n` | 8 snippets "fabricated", the worst defect class in the run, because the real elisions were indented | false positive |
| A minutes regex of `(\d+)\s*min` | 4 budgets "mismatched", because it could not see `1.5 min` | false positive |
| A baseline keyed on `demos\a\b.md` looked up as `demos/a/b.md`, defaulting to `[]` on every miss | **"ALL CLEAN" on 51 files, having never compared a single hash.** Caught only because a fence had just been shortened on purpose and went unflagged | **false negative** |
| A `cd` in an earlier shell call persisting into the run | "checked files: 0 ... ALL CLEAN" | **false negative** |

The last two are the dangerous class, because a false positive gets investigated and a false negative gets believed. Four rules follow. Reproduce one reported defect by hand before believing the report; if the hand check disagrees, the script is wrong. Print the input count next to the results, because a run that matched zero files otherwise looks identical to a run that passed. Make nesting, indentation and non-integer numbers explicit cases, since that is where the first three bugs lived. And never let a lookup miss default to a permissive empty value: assert the baseline is non-empty, assert every file has an entry in it, and treat a missing key as a defect rather than a pass. Before trusting any checker, break one input on purpose and confirm it is reported, since a verifier that has never failed is indistinguishable from one that cannot fail.

### Preserving snippets across a bulk edit

When a later pass edits these guides for anything other than snippet content, the fences are the invariant and the editing agents cannot prove they held it: their own reports will note there was no baseline to diff against. Hash every fence before the pass, keyed by file, and re-hash after. That establishes preservation in one command, independent of what any agent claims.

---

## Expected usage

```text
create-demo-essentials for demos/02-harness/02-commands/demo-slash-command-toolkit.md
create-demo-essentials for every demo in demos/06-planning
create-demo-essentials sweep the whole course
```
