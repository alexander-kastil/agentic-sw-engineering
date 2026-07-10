---
name: author-guide
description: Author a demo or lab guide file (demo-NN-slug.md or lab-NN-slug.md) at the module root following the repository's guided or prompt-recipe structure. Creates companion asset files in real-world office formats when a demo or asset-backed lab needs them.
---

# Author Guide

Read the target folder, guide number, title, and type from the task passed to create-class.

Create a guide document following the naming and placement conventions of this repository.

**Process:**

1. Parse the task for: target folder path, guide number, and title. Type defaults to `prompt-recipe` unless the guide is about initial project setup, in which case default to `guided`. Accept an explicit `guided` or `prompt-recipe` override in the arguments.
2. Determine the file name prefix from the top-level parent of the target path:
   - Path is under `demos/` → prefix is `demo`, file name is `demo-<nn>-<slug>.md`
   - Path is under `labs/` → prefix is `lab`, file name is `lab-<nn>-<slug>.md`
3. Place the file at the location the user specifies. When no explicit subfolder is given, default to the module root — the first two path segments under `demos/` or `labs/` (e.g. target `demos/02-harness/04-mcp` → file goes in `demos/02-harness/demo-01-slug.md`). Never create a nested subfolder beyond what the user requests.
4. Run the **Confirmation gate** before creating any file. See "Confirmation gate" below for the full list of decisions to confirm (target, number, title, type, assets, step count, runtime, and file collisions).
5. If the guide needs assets (a demo, or an asset-backed lab): create a companion subfolder named with the same slug (e.g. `demo-01-monthly-report/` or `lab-01-night-at-the-reef/`) alongside the guide file. Generate asset files in that subfolder using real-world formats (see "Demo assets" below). Never use markdown files as assets.
6. After creating the guide (and assets if applicable): update the TOC `readme.md` in the same folder. If no `readme.md` exists yet, create one.
   - Under `demos/`: add the demo to the `| Topic | Demo |` table. See "Demo TOC readme" below.
   - Under `labs/`: add the lab to the `| Lab | Focus |` table. See "Labs folder structure" below.

---

## Confirmation gate

Do not create any file until you have run this gate. Use `AskUserQuestion` to batch the open decisions into one proposal, then build only after the user approves. Always confirm:

- Target folder, guide number, title, and type (`guided` or `prompt-recipe`).
- Whether companion asset files are needed and which formats they should use.
- Step count. Demos default to 3 to 4 steps; labs have a minimum of 8 steps (see "Prompt-recipe structure"). For a multi-lab request, confirm whether the step count is per lab or total.
- When the guide ships a runnable component (an MCP server, a mock web app, a CLI): the runtime and stack. Offer the choices without bias, listing C#/.NET, Node/TypeScript, and Python as equals. Never label one as recommended.

Before proposing, scan the target folder for existing guide files. If a file with the same number or the same scenario scope already exists, surface it in the proposal and ask whether to replace it, renumber the new guide, or let both coexist. Do not silently overwrite or duplicate.

When a lab needs a connector, default to a no-account, no-API-key, commonly-available server (for example the Fetch MCP server) so any learner can complete it. Reserve account-bound connectors (Microsoft 365, GitHub) for the modules that are specifically about them.

---

## Demos folder structure

When a module groups its demos in a dedicated subfolder, the layout is:

```
demos/<module>/demos/
├── readme.md                    ← TOC: 2-column topic → demo table
├── demo-01-<slug>.md            ← guide file
├── demo-01-<slug>/              ← companion assets folder (same slug)
│   ├── source-file.docx
│   └── another-file.xlsx
├── demo-02-<slug>.md
├── demo-02-<slug>/
│   └── ...
```

Rules:
- The `demos/` subfolder sits directly under the module root (e.g. `demos/01-cowork/demos/`).
- Every guide file has a companion subfolder with an identical slug containing the asset files.
- The `readme.md` is the only file at the root of the `demos/` subfolder that is not a guide file.
- Never nest demos deeper than this two-level structure.

---

## Demo TOC readme

Every `demos/` subfolder must contain a `readme.md` that maps module topics to demos. When you create a new demo, add its row to this file. If the file does not exist, create it.

**Format:**

```markdown
# Demos

<One or two sentences describing what the demos folder contains and how to use it.>

| Topic | Demo |
|-------|------|
| [Topic title](../NN-topic/readme.md) | [Demo title](./demo-NN-slug.md) |
```

**Rules:**
- Two columns only: Topic (linked to its `readme.md`) and Demo (linked to its guide file).
- Each demo appears exactly once. Choose the topic where the conceptual fit is strongest.
- Order rows by the natural learning sequence, not by demo number.
- Topic column uses the topic title (not the folder name). Demo column uses the guide H1 title (not the filename).
- Do not add a description column, a "why" column, or any other column. The links carry the context.

---

## Labs folder structure

Labs live directly under their module root, mirroring the demos layout:

```
labs/<module>/
├── readme.md                        ← TOC: 2-column Lab → Focus table
├── lab-01-<slug>.md                 ← lab guide file
├── lab-01-<slug>/                   ← companion assets folder (same slug)
│   ├── guest-list.xlsx
│   └── vendor-quotes.docx
├── lab-02-<slug>.md
```

Rules:
- The lab number is a per-module sequence: the first lab in a module is `lab-01-<slug>.md`, regardless of the module number. Do not number labs by the module.
- An asset-backed lab gets a companion subfolder with an identical slug, next to the lab file. The learner points Cowork at this folder once; the files are then available without re-attaching.
- The lab TOC `readme.md` uses a two-column `| Lab | Focus |` table (not the demos `| Topic | Demo |` table). The Lab column links to the lab file using its H1 title; the Focus column is one sentence on what the lab practises.
- Labs may also ship runnable projects under `src/<slug>/` (see "Running the Lab Starter").

### Composite lab structure

A composite lab exercises an entire module in one connected scenario. Use this layout for the lab body:

```markdown
# <Verb-action title for the whole lab>

<Paragraph one: the real job the learner is taking on.>

<Paragraph two: the fictional setting, the persona the learner plays, and the files provided.>

---

Each step follows the same pattern:

- Overview: what this step achieves
- Research / Planning / Discussion: an open prompt to reason through the problem before acting
- Finding: what to read and evaluate in Claude's response before moving on
- Recipe: a complete implementation prompt you can use as-is or adapt from your own findings
- Expected Outcome: observable artefacts that confirm success

---

## What This Lab Covers

| Step | Feature practised | Module topic |
|------|-------------------|--------------|
| 1. <step title> | <feature> | [<topic title>](../../demos/<module>/<nn>-topic/readme.md) |

---

## Lab Files

All files live in the `lab-<nn>-<slug>` folder next to this guide. You point Cowork at this folder in Step <n>, after which every step can read them without re-attaching.

| File | What it represents |
|------|--------------------|
| `filename.xlsx` | ... |

---

## Before You Start

<Any prerequisites: plugins to install, accounts, a local service to start.>
```

Rules for labs:
- Use plain (non-bold) step labels (`Overview:`, `Recipe:`) and bare prompt fences (no language tag on Research or Recipe prompt blocks), matching the established sibling labs. Only real code or terminal blocks get a language tag.
- The `What This Lab Covers` table maps every step to the module topic it practises, with the topic linked. A composite lab covers every topic in the module.
- Reference labs: `labs/04-cowork/lab-01-night-at-the-reef.md` and `labs/07-m365-integration/lab-01-optimize-quarterly-deck.md`.

### Multiple labs from one module

When asked to produce several independent labs covering a whole module:
- Read every topic `readme.md` in the module first.
- Produce a topic-coverage table in the proposal proving all topics are covered across the labs.
- Share one fictional world (same company, same period) across the labs so figures feel consistent, while keeping each lab fully self-contained with its own companion asset folder.
- Step count is per lab (minimum 8). Confirm per-lab-vs-total in the Confirmation gate.
- Add one row per lab to the lab TOC `readme.md`.

---

## Guided structure (initial project setup only)

Use only when the lab is setting up a project, devcontainer, or development environment for the first time. Do not use for feature work, integration, or configuration tasks.

```markdown
# Lab <nn> — <Title>

<One-sentence description of what the learner will accomplish.>

---

## Setup

<Universal setup steps. Omit OS-specific sub-sections unless commands actually differ.>

```bash
command
```

---

## Step <n>: <Title>

1. Numbered instructions.
2. ...

```language
command or code
```

<Expected outcome sentence.>
```

Rules for guided labs:
- Use numbered lists for sequential steps; bullet lists for options.
- Every terminal block must declare a language (`bash`, `powershell`, etc.).
- Never include tool installation or SDK setup. This repository uses a devcontainer; all runtimes and global CLI tools are pre-installed.
- Never add OS-specific tracks. The devcontainer provides a single consistent environment for all platforms.
- Setup is limited to package restore commands (`npm install`, `dotnet restore`) and starting services.
- End with a verification step the learner can run to confirm success.

---

## Prompt-recipe structure (default)

Use for all guides except initial project setup. Each step teaches learners to drive Claude with prompts rather than follow numbered instructions.

**Every step MUST contain all five elements in order. Omitting any element is an error.** A step with only a Recipe and Expected Outcome is incomplete and must not be written that way.

Each step follows the same pattern — all five are required:

1. **Overview** — what this step achieves and why it matters
2. **Research / Planning / Discussion** — an open prompt to reason through the problem before acting. Must not contain the answer.
3. **Finding** — what to read and evaluate in Claude's response before moving on. Names specific signals and tells the learner when to push back.
4. **Recipe** — a complete, self-contained implementation prompt the learner can use as-is or adapt. Must not reference earlier conversation context.
5. **Expected Outcome** — observable artefacts (files, responses, UI changes) that confirm the step succeeded

```markdown
# <Title>

<One-sentence description of what the learner will accomplish.>

## Related Topics

<Only for demo guides: one paragraph linking to the specific module topics this demo illustrates. Name each topic with a relative link and add one sentence explaining what it contributes to this demo. See "Related Topics" rules below.>

---

Each step follows the same pattern:

- **Overview** — what this step achieves
- **Research / Planning / Discussion** — an open prompt to reason through the problem before acting
- **Finding** — what to read and evaluate in Claude's response before moving on
- **Recipe** — a complete implementation prompt you can use as-is or adapt from your own findings
- **Expected Outcome** — observable artefacts that confirm success

---

## Demo Files

<Only for demo guides: a table listing each asset file and what it represents. Reference the companion subfolder by name so the learner knows where to point Cowork.>

| File | What it represents |
|------|--------------------|
| `filename.docx` | ... |

---

## Running the Lab Starter

<Only when the guide has a pre-existing codebase to run. Provide exact, copy-paste commands with no explanation of the stack. End with one sentence describing what a successful start looks like. Omit entirely for greenfield guides or demos.>

<A lab may ship runnable projects (a mock web app, an MCP server, a CLI) under `src/<slug>/`. When it does, this section lists the exact commands to start each service and the URL or signal that confirms it is up.>

```bash
<exact commands>
```

<What a successful start looks like.>

---

## Step <n>: <Title>

**Overview:** <What this step achieves and why it matters.>

**Research / Planning / Discussion:**

```
<Open-ended prompt that asks Claude to read files, compare options, or reason through the problem. Must not contain the answer.>
```

**Finding:** <What a good response looks like. Name specific signals — a comparison table, a recommendation with reasoning, a file path. Tell the learner when to push back.>

**Recipe:**

```
<Complete, self-contained implementation prompt. The learner must be able to skip the Research step and use this directly.>
```

**Expected Outcome:** <Observable artefacts — files, server responses, or UI changes — that confirm the step succeeded.>

> The recipe above is one possible prompt based on typical findings from the research above. If your conversation led to different conclusions, use those instead.
```

Rules for prompt-recipe guides:
- **All five elements (Overview, Research, Finding, Recipe, Expected Outcome) are mandatory in every step. Never omit any of them.**
- **ATTACH FIRST RULE: Before every prompt code block (Research or Recipe) that references a file by name, a concrete file-access instruction must appear above the code block. The instruction varies by module:** see "Module-specific file access patterns" below.
- Research prompts must be open-ended — they ask Claude to reason or read files, not execute a fix.
- Finding must tell the learner what a good response looks like and when to push back. It is not a restatement of the goal.
- Recipe prompts must be fully self-contained — no reference to earlier conversation context. The learner must be able to skip Research and use the Recipe directly.
- Expected Outcome describes observable artefacts, not internal implementation.
- Steps build on each other; Recipe prompts may reference files created in prior steps.
- The blockquote note always uses the same phrasing shown above.
- Step count depends on the guide type. Demos and focused single-topic guides aim for 3 to 4 steps. Labs have a minimum of 8 steps; a composite or capstone lab uses roughly one step per module topic.
- Step cohesion is mandatory for labs. The steps form one connected storyline that builds toward a single named deliverable, and later steps consume the outputs of earlier ones. They must never be a list of disconnected mini-tasks. See `labs/04-cowork/lab-01-night-at-the-reef.md` for the model.
- Research and web-search steps must target a real, searchable subject (an industry, a product, a public standard), never the fictional company in the scenario.

---

## Module-specific file access patterns

Every prompt that references a file MUST be preceded by an instruction telling the reader how to make that file available. The instruction depends on which product the demo targets:

| Module pattern | Product | File access instruction |
|---------------|---------|------------------------|
| `01-foundations` | Mixed (chat and Cowork) | Use the matching instruction for the surface the step is on; see the surface-switching note below. |
| `02-desktop` | Claude Desktop (plain chat) | "Click the paperclip icon, select `<file>` from the `<folder>` folder, attach it, then paste and send this prompt:" |
| `03-projects` | Claude Projects | Step 1 (planning): same as plain chat above. After project is set up: "Start a new chat inside the `<Project Name>` project. The files are available from the project's knowledge base." |
| `04-intro-cowork` | Cowork | "Open the `<folder>` as your Cowork session. Files are available automatically." |
| `05-harness` | Cowork (workspace demos) | Same as Cowork: "Open the `<folder>` as your Cowork session." |

Do NOT write a prompt code block that says "Read X.docx in this folder" without a preceding file-access instruction. This is the single most common guide defect.

A composite lab that switches surfaces step to step (a chat step, then a Cowork step) must give the matching file-access instruction at each switch, not once at the top. Every asset-backed lab must include one explicit asset-loading step (point Cowork at the companion folder) before the first step that reads a file.

### For Projects demos (module 03)

The Demo Files section must explain the full project setup flow:

```markdown
## Demo Files

The `<folder>` folder on your computer contains the documents for this demo.

**How to work through this demo:** In Step 1, start a plain Claude Desktop chat and click
the paperclip icon to attach each file before pasting the prompt. After planning, create a
new Project in Claude Desktop (click the + icon in the sidebar, choose Project, name it
"<name>"), upload the recommended files as knowledge files, and paste the instructions
Claude produced into the project's Instructions field. Later steps happen inside that Project.
```

Expected Outcomes must reference project setup actions (paste into Instructions field, upload to Knowledge panel) rather than file creation.

---

## Demo assets

When a guide is a demo for business users, the companion subfolder must contain realistic sample files in the formats those users actually work with. Never use `.md` files as demo assets.

**Choosing file types by scenario:**

| Scenario | Preferred asset formats |
|----------|------------------------|
| Team status updates, reports, policy documents, meeting notes | `.docx` |
| Sales data, budgets, schedules, trackers, comparison matrices | `.xlsx` |
| Slide decks, briefing materials, presentations | `.pptx` |
| Signed contracts, regulatory submissions, scanned forms | `.pdf` |
| Mixed research or multi-format input | combine two or more of the above |

**Rules for asset files:**
- Generate all asset files programmatically using the appropriate Python library: `python-docx` for `.docx`, `openpyxl` for `.xlsx`, `python-pptx` for `.pptx`, `reportlab` or `pypdf` for `.pdf`. Verify the libraries import first (`python -c "import docx, openpyxl, pptx"`), then write a generation script, run it, and delete the script.
- Asset content must be realistic and internally consistent — use fictional but plausible company names, figures, and dates. Assets across a single demo should share the same fictional setting (same company, same time period).
- Each asset file should contain enough content that the demo prompts produce meaningfully differentiated output. A file with one paragraph of content is too thin.
- Use proper document structure: headings, paragraphs, bullet lists, and tables as appropriate for the document type. Do not dump plain text into a file.
- For `.xlsx` assets, use multiple rows and clearly labelled columns. Include at least one sheet with a header row and 8 to 15 data rows.
- For `.pptx` assets, use real slide layouts with titles and content placeholders. Aim for 5 to 8 slides per file.

---

## Related Topics section

Include a "Related Topics" section in every demo guide. Place it directly after the opening description, before the "Each step follows the same pattern" preamble.

Rules:
- Link to 2 to 3 module topics using relative paths (e.g. `../02-chat-cowork/readme.md`).
- For each linked topic, write one sentence explaining what concept from that topic this demo illustrates in practice.
- Do not link to topics that are only tangentially related. Every linked topic should be one the learner would genuinely benefit from reading before or alongside the demo.
- Keep the section to one paragraph. Do not use a bullet list.

---

## General rules

- File name prefix derives from the top-level parent: `demos/` → `demo-<nn>-<slug>.md`, `labs/` → `lab-<nn>-<slug>.md`.
- Two-digit zero-padded number, lowercase hyphen slug. For labs, the number is a per-module sequence (`lab-01` = first lab in that module), not the module number.
- H1 title is always a polished verb-action phrase describing what the learner does (e.g. `# Compile a Monthly Team Report`). Never prefix it with `Demo 01`, `Lab 03`, or any number/type label.
- No bold or italic in body prose (headings and label words like **Overview** are fine).
- No inline comments in code blocks.
- Max 4 sentences per paragraph.
- No em dashes — use `,` `;` `:` or `()` instead.
- When the audience is non-technical (business users, managers): use plain business language throughout. Avoid terms like "workspace", "context window", "model", or "prompt engineering" in the guide prose. Describe actions in terms of what the user does and what they get back.

---

## Verification

After writing any guide or lab, invoke the repo-local brand-voice skill to verify it (discover it with Glob `.claude/skills/brand-voice-*`). Never hand-roll a grep as a substitute.

Only a subset of the brand-voice rules applies to guide and lab files: no em dashes, and the 4-sentence paragraph cap. The readme-only rules (Mermaid quoted labels, topic-specific slash-command tables, the In Practice / Key Topics structure, and Note callouts) target sub-module readmes and do not apply to guide or lab prose.

---

**Expected usage:**

```
author-guide for demos/01-fundamentals/03-permissions a guided lab on devcontainer setup
author-guide for demos/02-harness/04-mcp a lab on MCP server discovery
author-guide for labs/07 a lab on orchestration patterns
author-guide for demos/01-cowork/demos a business demo on contract review using docx and xlsx assets
```

The topic subfolder in the path provides context but the output file always lands at the specified location:
- `demos/02-harness/04-mcp` → `demos/02-harness/demo-<nn>-<slug>.md`
- `labs/07-subagents/03-fan-out` → `labs/07-subagents/lab-<nn>-<slug>.md`
- `demos/01-cowork/demos` → `demos/01-cowork/demos/demo-<nn>-<slug>.md` + `demos/01-cowork/demos/demo-<nn>-<slug>/` (assets) + `demos/01-cowork/demos/readme.md` updated
