# Create Guide

Author one demo or lab guide document following this repository's naming, placement, and content
conventions. Read the target folder path, guide number, title, format, and audience from the task
(when invoked by `create-class`) or from the current request. This skill owns a single guide; the
`create-class` master owns whole-module planning and calls here per guide.

Content quality is the goal; structure is flexible. Pick the format that fits the audience and the
kind of work, then write a guide a learner can follow start to finish and reach a named outcome.

---

## What makes a guide worth shipping

A guide teaches a capability and leaves the learner holding a real artifact. Judge every guide
against these before writing a line. A guide that fails any of them is not ready.

- Substantive, not procedural. The subject must be a capability worth the learner's time: a demo
  runs 15 minutes or more, a lab 20 minutes or more. Signing in, flipping a toggle, switching an
  experience, or touring tabs is setup, never a demo; fold it into Prerequisites as one line. If the
  whole guide could be replaced by a single sentence of instructions, it is not a guide.
- Produces an artifact. By the end the learner has built, configured, tuned, or shipped something
  real: a grounded agent, a tuned skill, a published workflow, a scored evaluation. Name it up front.
- Purpose-first, not concept-first. Each step opens with what it achieves and why it matters here, in
  one or two sentences. What the feature IS belongs to the topic `readme.md`; the guide links it
  rather than restating it (see "Write short, show more than you tell").
- Opens on the problem. Before the first step, the guide says what is wrong with how the learner
  works today and what they will hold at the end, in plain words with no syntax and no product
  jargon. A guide that starts at Step 1 makes the learner execute instructions whose purpose they
  will only infer later, and most never do. The terms the guide teaches are introduced by the steps
  that teach them, never in the opener.
- Copy-paste ready. Everywhere the learner must supply input (agent instructions, a skill
  description, a tool description, a test prompt, sample data), ship the exact text in a block they
  can paste. Never write "add a description" without giving the description.
- Observable at every step, as before and after. Every step ends with an Expected result that names
  the concrete on-screen signal, and the strongest form shows both states: the thing the learner
  wrote next to what came back. "A file with 11 rows" describes an artifact; the placeholder line
  above its substituted output proves the mechanism. Where a step changes something, show the change,
  not a sentence claiming it happened.
- Short enough to read. See "Write short, show more than you tell". A guide nobody finishes teaches
  nothing, and length is the most common reason one is abandoned.
- Honest. Never fabricate screenshots, tenant data, or tool output. Describe the expected on-screen
  state in words. If you did not run it, do not invent its output.

---

## The job (locked)

Naming and placement never vary:

- Path under `demos/` -> file name is `demo-<slug>.md`, no number.
- Path under `labs/` -> file name is `lab-<nn>-<slug>.md`.
- The file lands in the **owning topic folder**: the deepest numbered `NN-topic` subfolder named in
  the target. A target of `demos/03-copilot-studio/04-ui-update/03-agent-skills` places the file at
  `demos/03-copilot-studio/04-ui-update/03-agent-skills/demo-<slug>.md`, with its companion
  folder alongside. Only when the target names no numbered topic subfolder does the file sit at the
  module (or sub-module) root. Never create a nested subfolder beyond what the target names.
- A demo guide carries no number: one demo per topic folder, so ordering comes from the numbered
  topic folder and never drifts when topics are reordered. The slug is a lowercase hyphen phrase.
- Lab numbers are two-digit zero-padded and form a per-topic sequence (`lab-01` is the first lab in
  that topic folder), not the module number. When moving an existing lab into a topic, rename it to
  `lab-01` and update its self-references and its companion folder name.
- The H1 title is a polished verb-action phrase for what the learner does (for example
  `# Compile a Monthly Team Report`). Never prefix it with `Demo 01`, `Lab 03`, or any number or
  type label.

After writing the guide, update the folder TOC `readme.md` (see "Folder structure and TOC"). If it
does not exist, create it.

---

## Confirmation gate

Do not create any file until this gate passes. Batch the open decisions into one proposal (use
`AskUserQuestion`), then build only after approval. Always confirm:

- Target topic folder, guide number, title.
- Format: `prompt-recipe`, `guided`, or `walkthrough` (see "Choosing a format").
- Audience: developer, low-code maker, or business user. This drives vocabulary and format default.
- Whether the guide ships a runnable project and, if so, the runtime and stack. Offer C#/.NET,
  Node/TypeScript, and Python as equals; never label one as recommended.
- Whether companion asset files are needed and which real-world formats they use.
- Depth and runtime. A demo is 4 to 6 substantive exercises and runs 15 minutes or more; a lab is 8
  to 12 substantive steps and runs 20 minutes or more. These are floors for substance, never caps:
  every exercise must teach a capability and move the deliverable forward. If a proposed guide cannot
  fill that depth honestly, the subject is too thin to be a guide; propose folding it into a larger
  one instead.

Before proposing, scan the target topic folder for existing guide files. If one with the same number
or the same scenario scope already exists, surface it and ask whether to replace, renumber, or coexist.
Never silently overwrite or duplicate.

When a lab needs a connector, default to a no-account, no-API-key, commonly-available server so any
learner can complete it. Reserve account-bound connectors (Microsoft 365, GitHub, Copilot Studio
tenant) for the modules that are specifically about them.

---

## Choosing a format

| Format | Default for | Shape |
|--------|-------------|-------|
| `prompt-recipe` | Business users and low-code makers | Five-part steps (Overview, Research, Finding, Recipe, Expected Outcome) that teach driving Claude or Copilot with prompts |
| `guided` | Initial project or environment setup only | Explicit numbered setup steps and commands |
| `walkthrough` | Product UI (Copilot Studio, M365 portals) and developer code, Microsoft-Learn style | Exercise-based prose: business-outcome milestones, copy-paste inputs, per-exercise expected results, callouts, troubleshooting, a summary. Code sub-mode adds run commands and expected output |

Default to `prompt-recipe` unless the guide is initial project setup (`guided`) or a
Microsoft-Learn-style walkthrough of a product UI or real code (`walkthrough`). Copilot Studio and
other portal guides use `walkthrough` in its product-UI sub-mode. Accept an explicit override in the
task.

### The subject decides the format, not the module

One rule overrides the default: when the thing being taught IS a mechanism the learner must see,
the guide shows the mechanism. Config-file syntax, CLI surfaces, git state, file layout, and
process behaviour are all mechanisms. A `prompt-recipe` guide on such a subject degenerates into
asking the model questions about the topic readme, and the learner finishes without ever having
seen the thing.

Two real failures from one module. A git-worktrees demo whose steps were "read the readme and
answer three questions" never once showed two working trees existing at the same time. A
permissions demo drove `.claude/settings.json` entirely through prose prompts, so the learner never
saw a single rule's syntax or a single real refusal.

| Subject | Format | Why |
|---|---|---|
| A config file's schema | `walkthrough` | The learner must read and paste the real JSON/YAML |
| A CLI surface or flag | `walkthrough` | The learner must see the real command and its real output |
| Git or filesystem state | `walkthrough` | The state IS the lesson; it has to be on screen |
| Judgement, prompting, routing, review | `prompt-recipe` | The work genuinely is a conversation |

The tell that a `prompt-recipe` guide has the wrong subject: a Recipe prompt whose deliverable is
an explanation rather than an artifact ("summarise the three-step flow", "explain the difference
between X and Y"). That is a quiz, not a demo. Research prompts may ask for reasoning; Recipe
prompts must change something.

---

## prompt-recipe structure (default)

Two shapes share this structure, and the choice is made per demo, never per module.

**Full five-part** when the learner faces a real decision: which trigger phrasing to use, which layer
to patch, which distribution route fits. The Research prompt earns its round-trip because the answer
genuinely varies, and the Finding tells the learner how to judge what came back.

**Recipe-only** (Overview, Recipe, Expected Outcome) when the step has one correct way to do it. A
Research prompt on settled mechanics degenerates into asking the model to explain the topic readme,
and the Finding then grades an explanation rather than an artifact. Writing four injected sections
with the documented syntax is recipe work; deciding what to inject is not.

The tell: draft the Research prompt and ask whether two competent learners could reasonably come back
with different answers. If not, cut Research and Finding for that step and keep the Recipe. A guide
may mix both shapes, and most good ones do: decisions early, mechanics later.

Within whichever shape a step uses, the elements appear in order and none is dropped silently. A
five-part step missing its Finding is incomplete; a recipe-only step is not.

1. Overview: what this step achieves and why it matters.
2. Research / Planning / Discussion: an open prompt to reason through the problem before acting.
   Must not contain the answer.
3. Finding: what to read and evaluate in the response before moving on. Names specific signals and
   tells the learner when to push back. Not a restatement of the goal.
4. Recipe: a complete, self-contained implementation prompt the learner can use as-is. Must not
   reference earlier conversation context; the learner must be able to skip Research and use it.
5. Expected Outcome: observable artefacts (files, responses, UI changes) that confirm success.

```markdown
# <Verb-action title>

<At most three sentences: what is wrong with how the learner works today, and what they hold at the
end. Plain words, no syntax, no jargon the steps have not taught yet.>

------

<Setup in one line: where to start and what the cleanup undoes.>

---

## Demo Files

<Demo or asset-backed guides only: a table of each asset file and what it represents. Name the
companion subfolder so the learner knows where to point the tool.>

| File | What it represents |
|------|--------------------|
| `filename.docx` | ... |

---

## Step <n>: <Title>

**Overview:** <What this step achieves and why it matters.>

**Research / Planning / Discussion:**

```
<Open-ended prompt that asks the model to read files, compare options, or reason. No answer.>
```

**Finding:** <What a good response looks like. Name specific signals: a comparison table, a
recommendation with reasoning, a file path. Tell the learner when to push back.>

**Recipe:**

```
<Complete, self-contained implementation prompt usable without the Research step.>
```

**Expected Outcome:** <Observable artefacts that confirm the step succeeded. Where the step changes
something, show the before and the after rather than describing them.>

> The recipe above is one possible prompt based on typical findings from the research above. If your
> conversation led to different conclusions, use those instead.
```

Rules:

- ATTACH-FIRST RULE: before every prompt block (Research or Recipe) that names a file, a concrete
  file-access instruction must appear directly above the block. The wording depends on the surface
  (see "Per-surface file access"). A prompt that says "Read X.docx in this folder" with no preceding
  access instruction is the single most common guide defect.
- Research prompts are open-ended: they ask the model to reason or read, not execute a fix.
- Recipe prompts are fully self-contained. Steps may build on files created in earlier steps.
- Expected Outcome names observable artefacts, not internal implementation.
- Use plain (non-bold) step labels. Every fence declares a language, with no exceptions: prompt
  blocks are ```text, and real code or terminal blocks get their own language tag.
- Labs need step cohesion: one connected storyline building toward a single named deliverable, with
  later steps consuming earlier outputs. Never a list of disconnected mini-tasks.
- Research and web-search steps target a real, searchable subject (an industry, product, or public
  standard), never the fictional company in the scenario.

### Per-surface file access

Match the instruction to the surface the step runs on:

| Surface | File-access instruction |
|---------|-------------------------|
| Plain chat (Claude Desktop, Copilot chat) | "Click the paperclip icon, select `<file>` from the `<folder>` folder, attach it, then paste and send this prompt:" |
| Projects / Copilot agent with knowledge | "Start a new chat inside the `<name>` project. The files are available from its knowledge base." |
| Cowork / workspace session | "Open the `<folder>` as your session. Files are available automatically." |

A guide that switches surfaces step to step gives the matching instruction at each switch, not once
at the top. Every asset-backed guide includes one explicit asset-loading step before the first step
that reads a file.

---

## guided structure (initial project setup only)

Use only when setting up a project, devcontainer, or environment for the first time. Do not use for
feature work, integration, or configuration.

```markdown
# <Title>

<One-sentence description of what the learner will accomplish.>

---

## Setup

<Universal setup steps. Omit OS-specific tracks unless commands actually differ.>

```bash
command
```

---

## Step <n>: <Title>

1. Numbered instruction.
2. ...

```language
command or code
```

<Expected outcome sentence.>
```

Rules:

- Numbered lists for sequential steps; bullet lists for options.
- Every terminal block declares a language (`bash`, `powershell`, ...).
- Setup is limited to package restore (`npm install`, `dotnet restore`, `pip install -r
  requirements.txt`) and starting services. Never include tool or SDK installation when the repo
  uses a devcontainer or the runtime is assumed present.
- End with a verification step the learner runs to confirm success.

---

## walkthrough structure (Microsoft-Learn style)

Two sub-modes share one quality bar (see "What makes a guide worth shipping"):

- Code walkthrough (Template A): developer guides that run real code. Run-verify first.
- Product-UI walkthrough (Template B): makers or business users driving a product UI such as Copilot
  Studio or a Microsoft 365 portal, where the work is configuration and testing, not code. This is
  the default for Copilot Studio guides.

### Template A - Code walkthrough

Prose with numbered steps, exact run commands, expected-output blocks, a verification step, and
cleanup. The pattern proven in the ai-103 course. No slide deck is forced.

```markdown
# <Verb-action title>

<One or two sentences on what the learner builds and the concept it teaches.>

## Prerequisites

<Accounts, quota, CLI logins, or a provisioned resource. Link the provisioning step below.>

## Run it

```bash
cd <slug>-py
pip install -r requirements.txt
cp .env.example .env
python <slug>.py
```

## Step <n>: <Title>

<Prose explaining what this part of the code does and why.>

```python
<the relevant snippet>
```

Expected output:

```text
<trimmed real output the learner should see>
```

## Verify

<A concrete check: a printed line, a created resource, an HTTP response, a file on disk.>

## Cleanup

```bash
<deprovision or teardown commands>
```
```

Rules:

- The runnable project is self-contained in its own per-topic folder named `<slug>-py` (Python),
  `<slug>-api` / `<slug>-ts` (Node/.NET), and so on. Each folder carries its own dependency manifest
  (`requirements.txt`, `package.json`, `*.csproj`) and its own `.env.example`. Never commit real
  `.env` files.
- Related runnable folders share a consistent prefix (for example `store-ops-agent-py` plus
  `store-ops-workiq-py`), never mismatched names like `base-agent` plus `workiq-demo-py`.
- The runnable folder is the STARTER and stays pristine (no installed dependencies, no lockfile, no
  build output). The finished, runnable result lives beside it in `<starter>-solution/`. The guide
  walks the learner through the starter and names the solution once, at the end, as the completed
  reference. The module `readme.md` states the convention once.
- Setup steps never run `git init` inside another topic's starter. If a demo needs a git repo, copy
  the project outside the course repo first, then `git init` and commit there.
- When a demo needs cloud resources, put `provision.azcli` and `deprovision.azcli` in the demo's
  parent (module) folder, not inside the `<slug>-py` subfolder. They own the full resource lifecycle
  independent of the client setup.
- Windows UTF-8: any script that prints emojis or model output must add
  `sys.stdout.reconfigure(encoding="utf-8")` at the top (and `sys.stderr` for launchers), or it
  crashes with `UnicodeEncodeError: 'charmap' codec can't encode ...`. Launchers that stream
  subprocess output spawn children with `encoding="utf-8"`, `errors="replace"`, and
  `PYTHONIOENCODING=utf-8`; multi-server launchers that signal children on Windows create them with
  `creationflags=subprocess.CREATE_NEW_PROCESS_GROUP`.
- Expected-output blocks show trimmed real output, not invented text. This is why the guide is
  run-verified before it is written (see "Run-verify first").
- A step whose outcome is a model judgement (an AI code audit, a quality gate) never promises a fixed
  exit code or verdict. State that the outcome is model-dependent and show what each branch means.

### Template B - Product-UI walkthrough

Frame the guide as a short set of Exercises, each a business-outcome milestone, never a click log.
This is the standard for Copilot Studio and portal guides. Model the depth on Microsoft's own labs
(for example the Copilot Camp and mcs-labs exercises): concept prose, copy-paste inputs, and a
described expected screen at every turn.

```markdown
# <Verb-action title>

<Two or three sentences: the business outcome and the real job this automates, then the artifact the
learner builds.>

## What you'll build

- <the artifact in 3 to 5 concrete bullets the learner can picture>

## Prerequisites

- <Accounts, roles, licenses, and any one-line setup such as turning on an experience. Setup lives
  here, never as an exercise.>

## Exercise 1: <business-outcome title>

<One or two short paragraphs: what this exercise achieves and what the feature actually does and why.
Explain the feature, not just the path to it.>

1. <Numbered action. Bold the exact UI element acted on, for example select **Add a tool**.>
2. <Next action; show the value to enter inline or in the paste block below.>

<A copy-paste block for any content the learner must supply:>

```text
<the exact instructions / description / prompt / sample data to paste>
```

Expected: <the concrete on-screen signal that proves it worked, and where to look for it.>

> **Tip:** <a real tip that saves time or prevents a common mistake.>

## Exercise <n>: <title>

<Same shape. Later exercises consume earlier outputs and build toward the named artifact.>

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| <what the learner sees go wrong> | <why it happens> | <what to do> |

## Summary

You built <the artifact>. You can now:

- <capability the learner can now perform>
- <capability>

<One sentence pointing to the next demo or lab.>
```

Rules for product-UI walkthroughs:

- Exercises are business-outcome milestones. A demo has 4 to 6; a lab has 8 to 12 and forms one
  connected storyline toward a single named deliverable, with later exercises consuming earlier
  outputs.
- Bold the exact UI labels the learner acts on (**Build**, **Add a tool**, **Publish**). This is the
  one place bold is expected in body text.
- Every exercise that needs learner input ships a copy-paste block with the real text. Never write
  "enter a description" without providing the description.
- Every exercise ends with an Expected line naming the on-screen signal, not a restatement of the
  action.
- Use `> **Tip:**`, `> **Note:**`, and `> **Warning:**` callouts for time-savers, context, and
  gotchas, sparingly (roughly one per two exercises, not every step).
- Include a Troubleshooting table (at least three real symptoms) and a Summary with a capability
  checklist.
- Never fabricate screenshots or tenant data. Describe the expected screen in words. A guide may
  reference a real image under an `_images/` folder only if that image actually exists.

---

## Setup is one command

The learner came to learn the topic, not to operate a shell. Setup is `cd` into the starter, plus
at most one dependency install. Everything else is the guide doing work the repo should have done
at authoring time.

```bash
cd demos/01-fundamentals/07-permissions/permissions-api
claude
```

Every one of these in a Setup block is a defect, and each names the fix:

| Smell | What it means | Fix |
|---|---|---|
| `printf ... > file`, `cat > file`, `echo ... >>` | The guide types a file into existence | Ship the file in the starter |
| `mkdir x && cd x && claude` | An empty folder while a starter sits beside the guide | `cd` the starter |
| `cp -r ../<other-topic>/...` | Borrowing another topic's project | Give this topic its own starter |
| `rm -rf bin obj` / `node_modules` | The starter is not pristine | Clean the starter in the repo, once |
| `git init` | Assumes no repo, but the course IS a repo | Use the repo; see below |
| A second `cp` for one extra file | An asset that belongs in the starter | Move it into the starter |

Files the learner creates mid-guide are given as a labelled content block for their editor, never
as a shell heredoc. That is shell-agnostic, diffable, and it survives a reader who is following on
Windows.

### One self-contained starter per topic

A topic that needs a project owns its starter, in its own topic folder, complete. Never point at a
sibling topic's folder: it couples two demos, and the borrowed folder arrives carrying the other
demo's artifacts. A constitution demo that borrowed the prompting topic's project shipped the
learner a finished `CLAUDE.md` before Step 2 asked them to write one.

Duplication across topics is correct here. A learner starting at module 6 must not need module 5's
folder, and a change to one topic's project must not silently alter three other demos.

### The starter must not contain the deliverable

A starter that already holds what the guide asks the learner to build teaches nothing. This is easy
to introduce by copying the solution folder and easy to detect:

```bash
diff -rq <starter> <starter>-solution
```

A near-empty diff is the alarm. If the deliverable is `policy-gate.sh` and the starter ships
`policy-gate.sh`, the starter is a solution wearing the wrong name. Audit the whole tree at once
by diffing every pair and ranking by fewest differences.

Two related shapes to check for: a `-solution` folder with no starter beside it, and a starter that
is really the finished state of an earlier demo in the same module.

### When the guide needs a git repository

Demos about worktrees, branches, or background sessions need a repo. The course repository already
is one, so use it: no `git init`, no copying out to a scratch directory, no nested repository. A
repo inside a repo works technically and confuses learners, and cleanup then needs an explicit
delete of the inner `.git` that `git clean` will never do for you.

Working in the course repo means the demo creates real branches and worktrees. Two rules keep that
safe: add `.claude/worktrees/` to the repo's `.gitignore`, and have the guide review and discard
rather than merge into the default branch. Show the merge command as what the learner would run in
their own project, explicitly not run here. Cleanup is then `git worktree remove --force` plus
`git branch -D`.

### Cross-shell by construction

Prefer commands that are byte-identical in Bash and PowerShell, which covers almost everything a
guide needs: `git`, `cd`, `cat`, `ls`, and every vendor CLI. Reach for dual Bash/PowerShell blocks
only where the shell's own commands genuinely differ.

| Bash-only | PowerShell |
|---|---|
| `printf`, `echo >` | Ship the file instead |
| `cp -r` | `Copy-Item -Recurse` |
| `rm -rf` | `Remove-Item -Recurse -Force` |
| `ls -a` | `Get-ChildItem -Force` |
| `~/path` | `$HOME\path` |

Designing setup around a shipped starter removes most of this table, which is the point: the fewer
shell commands a guide contains, the less of it is platform-specific.

#### When the shell IS the subject

The rule above assumes shell-specificity is incidental, which holds for a module that merely uses a
shell to reach the topic. A module teaching job control, exit codes, stdin, stream redirection or
process isolation inverts it: the differences ARE the lesson, and a guide that hides them behind one
shell costs the other half of the room the module. Ship every script twice as `<name>.sh` and
`<name>.ps1`, and print both blocks wherever the shell's own machinery appears.

| Bash | PowerShell |
|---|---|
| `cmd &` then `wait` | `Start-Job` then `Receive-Job -Wait -AutoRemoveJob` |
| `wait "$pid"` then `$?` | `$LASTEXITCODE` emitted as the job's last statement |
| `echo "$OUT" \| grep -q TOKEN` | `-cmatch` (plain `-match` is case-INsensitive) |
| `jq -r '.a.b'` | `ConvertFrom-Json` (built in, deletes a prerequisite) |
| `$(cat f)` | `(Get-Content f -Raw)` |
| `bash -n script.sh` | `[System.Management.Automation.Language.Parser]::ParseFile(...)` |
| `chmod +x script.sh` | No counterpart; use `pwsh -File script.ps1` |

Four of these carry teaching weight rather than syntax, so name them in the prose instead of
translating them silently. A PowerShell job reports `Completed` even when the command inside it
exited non-zero, which is the same trap as a bare `wait` returning only the last job's code arriving
from the other direction. `-match` being case-insensitive silently loosens a sentinel-token gate that
`grep -q` kept strict. `ConvertFrom-Json` removes a `jq` prerequisite the Bash guide states in its own
Setup. And `chmod` has no counterpart at all, so a guide that lists it as a step needs an execution-policy
sentence instead, not a translation.

Where the command is plain `git`, plain `claude`, or any vendor CLI, keep one block: the test is
whether the shell's own machinery appears, not whether the file has a `.sh` name.

Three traps come with dual-shell authoring:

- Duplicate starter STUBS as well as working scripts. An empty `.sh` twin needs an empty `.ps1` twin,
  or the "fill in this file" step has no file to fill in on the other platform.
- A literal `|` breaks a Markdown table cell even inside backticks, so a translation table describes
  `-split` and `IFS` in words rather than showing them.
- A timed presenter guide gets one `**Shell:**` line under its intro separator, naming the counterpart
  file and the beats where it changes shape, never a second copy of every quoted block. Doubling the
  content breaks the budget in its frontmatter, and the presenter has already chosen a shell. That
  line has one hard floor:
  it must name every form in the quoted blocks that fails OUTRIGHT on the other platform, not merely
  the interesting differences. A presenter types those live off the projected slide, and the
  silent-failure forms (`$?` printing `True`, `< /dev/null` as a parse error) are precisely the ones
  an author reaches for last.

## Shipped scripts carry presenter comments

Every script a demo ships (`.sh`, `.ps1`, hook, helper) is read aloud by someone who did not write it,
often live with a room watching. Comment the lines a competent developer cannot decode at a glance,
one short line directly above the line it explains, and nothing else. `\brm\s+-rf\b` earns a comment;
`echo "Creating worktrees..."` does not.

What earns a comment:

- regex and glob patterns: say what the metacharacters do, not what the pattern is for
- an exit code and its contract: which number blocks, which fails the build, which means no verdict
- shell machinery: `$?`, `$!`, `$PSScriptRoot`, `IFS`, `*>`, backtick continuation, `< /dev/null`
- why a value is derived instead of hardcoded: `git rev-parse --show-prefix`, `$(dirname "$0")`
- a flag whose absence changes the outcome: `--no-ff`, lowercase `git branch -d`, `-cmatch`, `-Raw`

What does not: echo lines, plain assignments, a restatement of the command in English, or anything the
surrounding guide prose already says. Two comments in a nine-line hook is right; six is noise.

A code block quoted in a guide matches the file byte for byte, comments included, because the presenter
reads one and runs the other. Where a starter and its `-solution` ship the same script, comment both
identically; where the starter ships a stub, only the solution carries comments.

Three boundaries decide what is a shipped script at all. A file the learner's agent WRITES during the
demo stays bare, because the guide quotes it as the expected output and a comment the agent never
produced makes that quotation a lie: comment the harness the demo runs, not the deliverable it
produces. Markdown that Claude itself reads (`SKILL.md`, agent files, slash commands) never gets
comments, since an HTML comment is context cost for every session that loads it and the guide already
explains the mechanism. And container or service config (Dockerfile, compose, Caddyfile) counts as
machinery when the learner only runs it, under the same "what does the room ask about" test.

A run record or verification transcript cites a symbol (`the reasons array`, `the deny() function`),
never a line number: adding one comment above a pattern shifts every number below it, and a stale
citation in a document titled "verification" is worse than no citation.

A prompt recipe that has the learner generate one of these scripts must not carry a blanket
`no inline comments` constraint: the `-solution` is the reference for what the learner just produced,
so the constraint reads "comment only a line a reader cannot decode at a glance, one short line above
it". Recipes for test files keep the bare constraint, since assertions explain themselves.

## Run-verify first

A companion asset the learner uploads into a product (a CSV test set, an import template, a config
file) is bound by that product's own template, never by its documentation. Obtain the template
first, author the asset against it, then upload it once and confirm the product accepts it. Writing
"download the template and check the columns" into the guide is not verification: it reads like
diligence while shipping an unverified file, and it hands your unfinished work to the learner. The
same rule covers any step that submits or saves; reading a UI and successfully submitting to it are
different claims. See `run-guide-browser.md` for capturing a client-side generated template without
downloading it.

For `walkthrough` guides and any guide shipping runnable code, run the code and capture real output
before writing the prose. Pair with the repo's run skills (`run-demo`, `run-foundry-demo`) to
execute in a prepared environment, then transcribe the observed commands, output, and verification
signals into the guide. Never mark a guide done on unrun code; invented output is a defect.

If a runnable project keeps evolving across a session, maintain a `state.md` live status board next
to it holding only remaining work: blockers and next steps. Remove completed items rather than
accumulating a history log; history belongs in git commits.

Renaming or moving a runnable folder means updating **every** reference: in-script error strings,
`readme.md` links, `state.md`, the guide's run commands, and any `provision`/`deprovision` paths.
Moving a Python folder breaks its `.venv` (hardcoded absolute paths), so delete and recreate the
venv after a move.

Moving or renaming a guide or topic folder also breaks its relative markdown links: rewrite
own-topic links to `./`, sibling-topic links to `../NN-topic/`, and mind the depth ripple (a lab
referencing a demo gains one extra `../` when nesting deepens). Validate every link and `#anchor`
with a resolver script after the move; on Windows a grep end-anchor `$` silently misses CRLF lines,
so use a script or drop the `$`.

---

## Sizing, compression, and time estimates

Compress a prompt-driven guide by counting MODEL ROUND-TRIPS and session restarts, not words. A
step that repeats a mechanism already taught in the same guide is typing, not teaching: the first
occurrence teaches it, every later one just costs the learner a round-trip. Cutting prose while
leaving the round-trip count untouched saves nothing a learner can feel.

Merging repeated steps is usually better pedagogy, not just shorter. An HTTP MCP entry and a stdio
MCP entry authored side by side in one file teach the contrast between the two transports; the same
two entries as separate tasks a hundred lines apart teach neither. Look for pairs that only differ
by one variable and put them next to each other.

Calibrate time estimates against any guide in the repo that budgets itself, and state the anchor you
used. Roughly 8 minutes per prompt-driven step was the observed anchor in one Claude Code course, so
a 9-step lab lands near 70 minutes, not the 30 an author guesses. Compute every table total with a
script rather than mentally: hand-summed duration columns are wrong often enough that a class
schedule built on them slips.

---

## Folder structure and TOC

### Under demos/

```text
demos/<module>/<nn-topic>/
├── readme.md                    topic learning content; links its own demo and lab
├── demo-<slug>.md               guide file, inside its topic folder
├── demo-<slug>/                 companion assets (same slug), or
├── <slug>-py/                   runnable starter for walkthrough demos
├── <slug>-py-solution/          finished, run-verified counterpart of the starter
```

The aggregate demo TOC uses a two-column `| Topic | Description |` table in the module `readme.md`:
the Topic cell names the topic and links to the demo guide, the Description cell says what the demo
does. One row per demo, under its strongest topic fit, so a topic teaching two demos contributes two
rows. Do not add extra columns. Each topic `readme.md` additionally links its own demo and lab under
Hands-On sections (the `create-teaching` skill owns that enrichment).

A guide's relative links are written from the topic folder, not the module root: a runnable project
in the same topic is `<slug>-py/`, and a sibling topic is `../NN-<topic>/`. After placing or moving a
guide, resolve every relative link in it against the file's new folder.

### Under labs/

```text
labs/<module>/<nn-topic>/
├── lab-01-<slug>.md             lab guide file, inside its topic folder
├── lab-01-<slug>/               companion assets (same slug)
```

The module lab TOC stays at `labs/<module>/readme.md` and aggregates every topic's lab in a
two-column `| Lab | Focus |` table: Lab links to the guide by its H1 title, Focus is one sentence on
what the lab practises. An asset-backed lab gets a companion subfolder with an
identical slug; the learner points the tool at it once and every step reads it without re-attaching.

---

## Demo assets

When a guide serves business users, the companion subfolder holds realistic sample files in the
formats those users actually work with. Never use `.md` files as demo assets.

| Scenario | Formats |
|----------|---------|
| Reports, policies, meeting notes, status updates | `.docx` |
| Budgets, schedules, trackers, comparison matrices | `.xlsx` |
| Decks, briefings, presentations | `.pptx` |
| Contracts, regulatory submissions, scanned forms | `.pdf` |

Rules:

- Generate assets programmatically with the right Python library (`python-docx`, `openpyxl`,
  `python-pptx`, `reportlab`). Verify the imports first, write a generation script, run it, then
  delete the script.
- Content is realistic and internally consistent: fictional but plausible names, figures, and dates.
  All assets in one demo share the same fictional setting (same company, same period).
- Give each file enough content that prompts produce differentiated output. Use real structure:
  headings, paragraphs, tables. `.xlsx` uses a header row and 8 to 15 data rows; `.pptx` uses 5 to 8
  real-layout slides.

---

## Write short, show more than you tell

**Theory lives in the topic `readme.md`, not in the guide.** The readme is the teaching: what the
feature is, why it exists, how the mechanism works, the field reference, the trade-offs. The guide is
the doing: what to type, what comes back, what it proves. When a guide starts explaining a concept,
that paragraph belongs in the readme and the guide should be running a step instead. A learner who
needs the theory is one click away and mostly arrived from there.

An Overview says what this step achieves, not what the feature is. If an Overview reads like an
encyclopedia entry, move it.

**Show the artifact rather than describing it.** A block of real output, a diff, a two-line table of
before and after: each replaces a paragraph and is more convincing than one. Prose describing what a
block would contain is the single most compressible thing in a guide. Where you have both, cut the
prose and keep the block.

**Cut anything that does not change what the learner types or looks for.** Apply it sentence by
sentence. Restated conventions, reassurance, history, alternatives not taken, and asides that begin
"note that" all fail this test. So does any sentence explaining why the guide is structured the way
it is.

Ranked, worst first, so a compression pass has an order to work in: concept explanation that
duplicates the readme, then prose describing a block that is already on the page, then
cross-references, then hedging and reassurance, then restated conventions. Delete from the top until
the guide reads fast.

Never pad to look thorough. A guide is finished when nothing can come out, not when it looks
substantial.

## What a guide does not carry

Three things were removed from every guide in one course because they sat above the first step and
competed with it. Do not reintroduce them.

- A Related Topics paragraph cross-referencing sibling topics. Who-owns-what belongs on the topic
  `readme.md`, which is where a learner goes to orient. In a guide it is context the learner cannot
  act on, placed where their attention is worth most.
- A restatement of the step structure ("Each step follows the same pattern: Overview, Research,
  Finding, ..."). The labels are visible in the steps themselves, and repeating the legend in every
  guide of a module trains the reader to skip the top of the page.
- A Setup section for a guide that installs nothing. Collapse it to one line, and open that line by
  saying there is nothing to install when that is the case.
- The starter/solution convention explained as a paragraph. The learner needs one line naming which
  folder they work in and where the finished result sits, for example "Work in `goal-demo/`; the
  finished result is beside it in `goal-demo-solution/`." What the convention IS, why starters stay
  pristine, and how the two relate is repo policy, not teaching: it belongs in `CLAUDE.md`.

---

## General rules

- No bold or italic in body prose (headings and label words like **Overview** are fine). Exception:
  product-UI walkthroughs bold the exact UI labels the learner clicks (**Build**, **Add a tool**)
  and the callout keywords (**Tip:**, **Note:**, **Warning:**).
- No placeholder notes. Comments appear only where the block mirrors a shipped script, under the rules
  in "Shipped scripts carry presenter comments"; prompt blocks and prose examples stay bare.
- Max 4 sentences per paragraph; start a new paragraph at the 5th.
- No em dashes; use `,` `;` `:` or `()` instead.
- Every code fence declares a language.
- Internal links use relative paths; anchors use `#heading-name`.
- For non-technical audiences, use plain business language. Avoid "workspace", "context window",
  "model", "prompt engineering" in the prose; describe what the user does and what they get back.

---

## Verification

After writing any guide, invoke the repo-local brand-voice skill to verify it (discover it with
Glob `.claude/skills/brand-voice-*`). Never hand-roll a grep as a substitute. Only a subset of the
brand-voice rules applies to guide files: no em dashes, and the 4-sentence paragraph cap. The
readme-only rules (Mermaid quoted labels, slash-command tables, Note callouts) target sub-module
readmes, not guide prose.

---

## Expected usage

```text
create-guide for demos/04-copilot-studio a prompt-recipe demo on agent topic design
create-guide for demos/02-chat-productivity/03-projects a business demo using docx and xlsx assets
create-guide for demos/05-maintaining a walkthrough demo on an MCP health-check server in Python
create-guide for labs/03 a guided lab on first-run environment setup
```
