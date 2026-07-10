---
name: scaffold
description: Bootstrap a whole class layout from an outline, or add numbered module/topic folders under an existing module.
---

# Scaffold

This leaf is loaded by the master skill `create-class`; it is not invoked directly. It covers two scaffolding modes: bootstrapping an entire course layout from a single outline file, and adding numbered topic subfolders under an existing module path.

## Scaffold a whole class from an outline

Bootstrap a complete course layout from a single outline file. The source file lists modules as H2 headings, each followed by a bulleted topic list. This mode parses it, plans the folder tree, asks for confirmation, and creates everything in one go.

### When to use

Use this when a new course repository is empty (or nearly empty) and you have an outline ready. A typical input file looks like `demos/readme.md`:

```markdown
# Demos

## Module 1: Claude Code Fundamentals

- Introduction to Claude Code
- Setup & Installation
- Editors
- Permissions

## Module 2: Claude Code Configure Harness

- Settings Hierarchy
- Slash Commands
- ...
```

Each `## Module N: <Title>` heading becomes a module folder. Each bullet becomes a numbered topic subfolder inside that module.

### What gets created

Given an outline with N modules:

```text
demos/
├── readme.md                       (copy of the source outline)
├── 01-<module-slug>/
│   ├── readme.md                   (H1, topic table, labs link)
│   ├── 01-<topic-slug>/readme.md   (# <original topic text>)
│   ├── 02-<topic-slug>/readme.md
│   ├── ...
│   └── pptx/readme.md              (empty placeholder for slides)
├── 02-<module-slug>/
│   └── ...
labs/
├── readme.md                       (index of labs per module)
├── 01-<module-slug>/readme.md      (lab landing page)
├── 02-<module-slug>/readme.md
├── ...
CLAUDE.md                           (project rules, created only if missing)
dashboard/
└── dashboard.json                  (module list pre-populated; only if missing)
```

The folder slug `<module-slug>` is derived from the module title (lowercase, hyphen-separated, 1-2 words). Topic slugs follow the same pattern.

### Workflow

#### Step 1 - Read and parse the source file

1. Read the parent folder path and source file path from the task passed to `create-class`. Default suggestion: `demos/readme.md`.

2. Read the source file. Extract:
   - The H1 title (used as the course title)
   - Every `## Module N: <Title>` heading
   - The bullet list under each module heading

3. For each module:
   - `num` = the `N` from `Module N:`, zero-padded to two digits
   - `name` = the title after the colon
   - `slug` = derived from `name` (lowercase, hyphenated, max 2 words). Strip filler words like "Claude Code", "the", "and".
   - `topics` = the bullet list, in order

4. For each topic:
   - `topic_slug` = derived from the bullet text (lowercase, hyphenated, max 2 meaningful words)
   - `topic_text` = the original bullet text (used verbatim as the topic readme H1)

#### Step 2 - Plan and present TOC

Print a table grouped by module showing the proposed folder layout:

```text
PROPOSED SCAFFOLD

Module 01 - Claude Code Fundamentals
  demos/01-fundamentals/readme.md
  demos/01-fundamentals/01-intro/readme.md       # Introduction to Claude Code
  demos/01-fundamentals/02-setup/readme.md       # Setup & Installation
  demos/01-fundamentals/03-editors/readme.md     # Editors
  demos/01-fundamentals/04-permissions/readme.md # Permissions
  demos/01-fundamentals/pptx/readme.md
  labs/01-fundamentals/readme.md

Module 02 - Configure Harness
  ...

SUMMARY: 13 modules, 87 topic subfolders, 13 lab folders, dashboard.json with 13 modules.
Existing files will not be overwritten.

Proceed? (yes / adjust / cancel)
```

Stop here. Wait for the user to say `yes`, `adjust` (then iterate), or `cancel`.

#### Step 3 - Create the structure (after "yes")

For each module:

1. Create `demos/NN-<slug>/readme.md` from the module readme template (see below).
2. For each topic at index `i` (1-based):
   - Create `demos/NN-<slug>/II-<topic_slug>/readme.md` with content `# <topic_text>\n`.
3. Create `demos/NN-<slug>/pptx/readme.md` (empty placeholder, content `# Slides\n`).
4. Create `labs/NN-<slug>/readme.md` from the lab readme template.

After all modules are processed:

5. Copy the source outline file to `demos/readme.md` if it is not already there.
6. Create `labs/readme.md` from the labs-index template (links to each module's lab folder).
7. If `CLAUDE.md` does not exist at the repo root, create it from the `templates/scaffold/CLAUDE.md` template.
8. If `dashboard/dashboard.json` does not exist, create it from the `templates/dashboard/dashboard.json` template with the parsed module list pre-populated.

For every file: skip and report "skipped (already exists)" if the target file already exists. Do not overwrite.

Report a one-line summary:

```text
SCAFFOLD COMPLETE: 13 modules, 87 topics, 13 lab folders, 0 overwritten, 1 CLAUDE.md created.
```

### Templates

Templates live in `templates/scaffold/` (relative to the `create-class` skill root):

| File | Used for |
|------|----------|
| `module-readme.md` | Demo module `readme.md` (H1, topic table, labs link) |
| `topic-readme.md` | Demo topic `readme.md` (H1 only) |
| `lab-readme.md` | Lab module `readme.md` (H1, sub-lab list) |
| `labs-index.md` | Top-level `labs/readme.md` |
| `CLAUDE.md` | Project rules + workflow guidance |
| `dashboard.json` | Owned by the dashboard leaf at `templates/dashboard/dashboard.json`; reused here pre-populated with modules |

Templates use `{{var}}` placeholders. Replace placeholders with parsed values when writing each file.

### Slug derivation rules

- Lowercase, hyphenated.
- One or two meaningful words, max.
- Strip stop words: `the`, `and`, `of`, `with`, `for`, `to`, `a`, `an`, `claude`, `code`.
- Prefer the most distinctive noun. Example: "Claude Code Fundamentals" becomes `fundamentals`; "Skills & Plugins" becomes `skills`; "Agentic CLI & Headless Execution" becomes `cli`; "Bundling & Distributing Plugins" becomes `distribution`.
- Use existing slugs as a reference when scaffolding into a repo that already has some modules.

### Rules

- Always present the TOC and stop. Never scaffold without confirmation.
- Never overwrite existing files. Always skip and report.
- Never create files outside `demos/`, `labs/`, `dashboard/`, or the repo root `CLAUDE.md`.
- Module numbers come from the source heading, not from the order in the file. `## Module 3: X` always becomes `03-x` even if it appears after `## Module 5: Y` in the source.
- If the source file has no `## Module N:` headings, fail with "no modules found in source file" and exit.

## Scaffold module/topic folders under an existing module

Create numbered topic subfolders with `readme.md` and `pptx/` stubs under a given module path.

Read the parent folder path and item list from the task passed to `create-class`. Given the parent folder path and list of items, create one subfolder per item with:

- A zero-padded numeric prefix (01-, 02-, 03-, …)
- A short 1-2 word folder name derived from the item's essence
- A `readme.md` inside each folder whose only content is `# <original item text>`
- A `pptx/` subfolder inside each folder, containing an empty `readme.md`

Rules:

- Folder names: lowercase, hyphen-separated, 1-2 meaningful words max
- File name: exactly `readme.md` (lowercase)
- Heading: exact original item text, prefixed with `# `
- No extra content in the readme files
- Create all folders and files in parallel

Expected usage:

```text
parent folder: demos/01-fundamentals

Introduction to Claude Code
Setup & Installation
Editors
Context Engineering
```
