---
name: create-guide
description: >-
  Author a single demo or lab guide for a hands-on class of any audience, in one of
  three styles chosen by audience: prompt-recipe (business/maker, the five-part step model), guided
  (initial project setup), or walkthrough (code, Microsoft-Learn style with run commands and
  expected output). Places the file at the module root as demo-NN-slug.md or lab-NN-slug.md,
  scaffolds any runnable project and companion assets, and updates the folder TOC. Peer skill the
  create-class master delegates to; also invocable directly. Trigger phrases: create a guide,
  write a demo, author a lab, demo guide, lab guide, prompt recipe, walkthrough guide, learn style
  guide, run-verified guide.
license: CC-BY-NC-SA-4.0
---

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
- Concept-first. Each exercise opens with why it matters and what the feature actually does, in plain
  prose, before any click. The learner should understand the feature, not just replay keystrokes.
- Copy-paste ready. Everywhere the learner must supply input (agent instructions, a skill
  description, a tool description, a test prompt, sample data), ship the exact text in a block they
  can paste. Never write "add a description" without giving the description.
- Observable at every step. Every step ends with an Expected result that names the concrete
  on-screen signal and how the learner knows it worked, not a restatement of the action.
- Honest. Never fabricate screenshots, tenant data, or tool output. Describe the expected on-screen
  state in words. If you did not run it, do not invent its output.

---

## The job (locked)

Naming and placement never vary:

- Path under `demos/` -> file name is `demo-<nn>-<slug>.md`.
- Path under `labs/` -> file name is `lab-<nn>-<slug>.md`.
- The file lands at the **module root**: the first two path segments under `demos/` or `labs/`.
  A target of `demos/04-copilot-studio/04-ui-update` places the file at
  `demos/04-copilot-studio/demo-<nn>-<slug>.md`. The topic subfolder gives context only; it never
  changes where the file lands. Never create a nested subfolder beyond what the user requests.
- Number is two-digit zero-padded; slug is a lowercase hyphen phrase. For labs the number is a
  per-module sequence (`lab-01` is the first lab in that module), not the module number.
- The H1 title is a polished verb-action phrase for what the learner does (for example
  `# Compile a Monthly Team Report`). Never prefix it with `Demo 01`, `Lab 03`, or any number or
  type label.

After writing the guide, update the folder TOC `readme.md` (see "Folder structure and TOC"). If it
does not exist, create it.

---

## Confirmation gate

Do not create any file until this gate passes. Batch the open decisions into one proposal (use
`AskUserQuestion`), then build only after approval. Always confirm:

- Target module root, guide number, title.
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

Before proposing, scan the module root for existing guide files. If one with the same number or the
same scenario scope already exists, surface it and ask whether to replace, renumber, or coexist.
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

---

## prompt-recipe structure (default)

Every step MUST contain all five elements in order. Omitting any element is an error. A step with
only a Recipe and Expected Outcome is incomplete.

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

<One-sentence description of what the learner will accomplish.>

## Related Topics

<Demo guides only: one paragraph linking 2 to 3 module topics with relative paths, one sentence
each on what that topic contributes. See "Related Topics".>

---

Each step follows the same pattern:

- Overview: what this step achieves
- Research / Planning / Discussion: an open prompt to reason through the problem before acting
- Finding: what to read and evaluate in the response before moving on
- Recipe: a complete implementation prompt you can use as-is or adapt from your own findings
- Expected Outcome: observable artefacts that confirm success

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

**Expected Outcome:** <Observable artefacts that confirm the step succeeded.>

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
- Use plain (non-bold) step labels and bare prompt fences (no language tag on prompt blocks); only
  real code or terminal blocks get a language tag.
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

## Related Topics

<Demo guides only: one paragraph, 2 to 3 module topics with relative links, one sentence each.>

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

## Run-verify first

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

---

## Folder structure and TOC

### Under demos/

```text
demos/<module>/
├── readme.md                    module TOC and topic overview
├── demo-01-<slug>.md            guide file
├── demo-01-<slug>/              companion assets (same slug), or
├── <slug>-py/                   runnable project for walkthrough demos
```

The demo TOC uses a two-column `| Topic | Demo |` table: Topic links to its `readme.md`, Demo links
to the guide file by its H1 title. Each demo appears exactly once under its strongest topic fit; do
not add extra columns.

### Under labs/

```text
labs/<module>/
├── readme.md                    lab TOC
├── lab-01-<slug>.md             lab guide file
├── lab-01-<slug>/               companion assets (same slug)
```

The lab TOC uses a two-column `| Lab | Focus |` table: Lab links to the guide by its H1 title, Focus
is one sentence on what the lab practises. An asset-backed lab gets a companion subfolder with an
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

## Related Topics

Include this section in every demo guide, directly after the opening description and before the
step preamble. Link 2 to 3 module topics with relative paths, one sentence each on what concept that
topic contributes in practice. Keep it to one paragraph, not a bullet list. Do not link topics that
are only tangentially related.

---

## General rules

- No bold or italic in body prose (headings and label words like **Overview** are fine). Exception:
  product-UI walkthroughs bold the exact UI labels the learner clicks (**Build**, **Add a tool**)
  and the callout keywords (**Tip:**, **Note:**, **Warning:**).
- No inline comments in code blocks; no placeholder notes.
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
