---
name: scaffold
description: >-
  Bootstrap a new course or masterclass repository and generate its module, topic, and
  lab layout. Interactive: asks a few questions (class title, audience, module count or
  outline, whether labs are needed), then creates the base skeleton (.claude/, demos/,
  labs/, root CLAUDE.md) and numbered module folders. Can bootstrap from an outline file
  (## Module N: headings become module folders, bullets become numbered topic subfolders)
  or purely interactively, at flat or deep-nested depth. Standalone skill; also called by
  the create-class master. Trigger phrases: scaffold a class, scaffold a new class,
  bootstrap course layout, set up base repo, new class, generate modules from outline,
  create demos and labs folders, scaffold module, add topic subfolders, bootstrap course repo.
license: CC-BY-NC-SA-4.0
---

# Scaffold

Bootstrap the base repository for a hands-on course and generate its numbered module,
topic, and lab layout. This is an essential, interactive skill: it asks a few questions
first, then sets up the repo. It is invocable directly and is also the skill the
`create-class` master delegates to by name for Phase 1 (scaffold the layout). It replaces
the retired `scaffold-class` and `scaffold-module` skills.

## When to use

- A new course repository is empty or nearly empty and needs its base skeleton.
- You have an outline (a Markdown file with `## Module N:` headings) and want the whole
  folder tree generated from it.
- An existing module needs numbered topic subfolders added under it.

## Step 1 - Ask the questions first

Scaffold is interactive. Before creating anything, ask the user these questions in one
message and wait for the answers. Offer sensible defaults so the user can accept quickly.

1. Class title. Used as the H1 of `demos/readme.md` and in the root `CLAUDE.md`.
2. Audience. One of: developer, low-code maker, business user. This shapes tone and later
   enrichment; capture it even though scaffolding itself is audience-neutral.
3. Modules. Either a number of modules (for example "6") or a path to an outline file (for
   example `demos/readme.md` or `outline.md`). If a number is given, ask for a one-line
   title per module, or let the user supply titles later.
4. Labs. Whether the class needs a matching `labs/` folder per module (yes or no) and
   whether topics should be flat (one `readme.md` per module) or deep (numbered topic
   subfolders per module).

If an outline file path is given, questions 1 and 3 can be read from the file instead of
asked. Confirm the parsed title and module list with the user before proceeding.

## Step 2 - Create the base skeleton

Every class gets the same skeleton. Create these once, at the repo root, only if missing:

```text
.claude/                 (skills and config live here; create the folder if absent)
demos/
├── readme.md            (H1 = class title; index of modules)
labs/
├── readme.md            (index of labs per module; only if labs are wanted)
CLAUDE.md                (project rules, from templates/CLAUDE.md; only if missing)
```

Never overwrite an existing `.claude/`, `demos/`, `labs/`, or `CLAUDE.md`. Skip and report
each one that already exists.

## Step 3 - Plan and present the TOC

Whether the modules come from an outline or from interactive answers, build the planned
tree and present it as a table grouped by module. Stop and wait for the user to say `yes`,
`adjust` (then iterate), or `cancel`. Never scaffold without confirmation.

```text
PROPOSED SCAFFOLD

Module 01 - Fundamentals
  demos/01-fundamentals/readme.md
  demos/01-fundamentals/01-intro/readme.md        # Introduction
  demos/01-fundamentals/02-setup/readme.md        # Setup & Installation
  demos/01-fundamentals/pptx/readme.md
  labs/01-fundamentals/readme.md

Module 02 - Configure Harness
  ...

SUMMARY: 6 modules, 18 topic subfolders, 6 lab folders. Existing files are never overwritten.

Proceed? (yes / adjust / cancel)
```

## Step 4 - Bootstrap from an outline file

When an outline file is supplied, parse it into the module plan.

1. Read the file. Extract the H1 (course title), every `## Module N: <Title>` heading, and
   the bullet list under each heading.
2. For each module:
   - `num` = the `N` from `Module N:`, zero-padded to two digits. Module numbers come from
     the heading, not file order: `## Module 3: X` always becomes `03-x` even if it appears
     after `## Module 5: Y`.
   - `name` = the title after the colon.
   - `slug` = derived from `name` (see slug rules below).
   - `topics` = the bullet list, in order.
3. For each topic:
   - `topic_slug` = derived from the bullet text.
   - `topic_text` = the original bullet text, used verbatim as the topic readme H1.
4. If the file has no `## Module N:` headings, report "no modules found in source file" and
   fall back to the interactive flow rather than failing silently.

An outline with topic bullets implies deep depth for those modules. A module heading with
no bullets stays flat (module `readme.md` only).

## Step 5 - Create the structure (after "yes")

Flexible depth: the same skill produces both shapes. Drive depth from the answers and the
outline.

- Flat module: create only `demos/NN-<slug>/readme.md` from `templates/module-readme.md`.
- Deep module: also create `demos/NN-<slug>/II-<topic_slug>/readme.md` for each topic at
  1-based index `II`, with content from `templates/topic-readme.md` (`# <topic_text>`), plus
  a `demos/NN-<slug>/pptx/readme.md` slides placeholder (`# Slides`).

For each module:

1. Create `demos/NN-<slug>/readme.md` from `templates/module-readme.md`.
2. For a deep module, create each `demos/NN-<slug>/II-<topic_slug>/readme.md` and the
   `pptx/readme.md` placeholder.
3. If labs are wanted, create `labs/NN-<slug>/readme.md` from `templates/lab-readme.md`.

After all modules are processed:

4. Write or update `demos/readme.md` so its H1 is the class title and it indexes the modules.
   If the class was bootstrapped from an outline file that is not already `demos/readme.md`,
   copy the outline there (only if `demos/readme.md` does not already exist).
5. If labs are wanted, create `labs/readme.md` from `templates/labs-index.md` with a link to
   each module's lab folder.
6. If the repo root `CLAUDE.md` does not exist, create it from `templates/CLAUDE.md`.

For every file: if the target already exists, skip it and report "skipped (already exists)".
Never overwrite. Create independent folders and files in parallel.

Report a one-line summary:

```text
SCAFFOLD COMPLETE: 6 modules, 18 topics, 6 lab folders, 0 overwritten, 1 CLAUDE.md created.
```

## Add topic subfolders under an existing module

To extend a module that already exists, take a parent module path and a list of items and
create one numbered subfolder per item:

- A zero-padded numeric prefix (`01-`, `02-`, `03-`, ...), continuing from the highest
  existing number in the folder.
- A short 1-2 word folder slug derived from the item text.
- A `readme.md` inside each folder whose only content is `# <original item text>`.
- A `pptx/` subfolder containing an empty `readme.md` (`# Slides`), for slide-bearing topics.

Example input:

```text
parent folder: demos/01-fundamentals

Introduction
Setup & Installation
Editors
Context Engineering
```

## Slug derivation rules

- Lowercase, hyphen-separated.
- One or two meaningful words, max.
- Strip stop words: `the`, `and`, `of`, `with`, `for`, `to`, `a`, `an`, and any repeated
  product name that appears in every module title.
- Prefer the most distinctive noun. Examples: "Copilot Studio Fundamentals" becomes
  `fundamentals`; "Skills & Plugins" becomes `skills`; "Bundling & Distributing" becomes
  `distribution`.
- When scaffolding into a repo that already has modules, match the existing slug style.

## Templates

Templates live in `templates/` next to this file. They use `{{var}}` placeholders; replace
each placeholder with the parsed value when writing a file.

| File | Used for |
|------|----------|
| `templates/module-readme.md` | Demo module `readme.md` (H1, topic table, labs link) |
| `templates/topic-readme.md` | Demo topic `readme.md` (H1 only) |
| `templates/lab-readme.md` | Lab module `readme.md` (H1, sub-lab list) |
| `templates/labs-index.md` | Top-level `labs/readme.md` |
| `templates/CLAUDE.md` | Root project rules and workflow guidance |

## After scaffolding

Check whether the repo has a brand-voice skill by globbing `.claude/skills/brand-voice-*`.
If none exists, note in the summary that the `create-class` master can bootstrap a repo-local
`brand-voice-*` skill so later READMEs can be audited against the class house rules.

## Rules

- Ask the questions first; always present the TOC and stop before creating module content.
- Never overwrite existing files, folders, or `CLAUDE.md`. Skip and report every collision.
- Never create files outside `.claude/`, `demos/`, `labs/`, or the repo root `CLAUDE.md`.
- No em dashes in prose; use `,` `;` `:` or `()`.
- Mermaid node labels use `"quoted<br/>labels"`, never `\n`.
- Code fences declare a language. Internal links use relative paths; anchors use `#heading-name`.
- Parallelize all independent file and folder creation.
