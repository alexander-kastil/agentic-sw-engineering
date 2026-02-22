---
name: update-toc
description: Validate and synchronize Table of Contents (TOCs) in demos/*/readme.md files. Ensures TOCs match the filesystem structure, using subfolder readme.md H1 headings as titles when available. Filesystem is the source of truth.
---

# Validate & Sync Demo TOCs

Traverse all `readme.md` files starting from `demos/*` and validate that their Tables of Contents (TOCs) are in sync with the filesystem. The filesystem is the source of truth.

## Input Parameters

Specify in your prompt:

- **`path`**: Directory pattern to scan (default: `demos/*/readme.md`)
- **`fixMode`**: `true` to auto-update TOCs, `false` to report only (default: `false`)
- **`depth`**: Maximum nesting depth for TOC entries (default: `2`)
  - `1`: List only immediate subfolders (flat list)
  - `2`: Include one level deeper (nested), showing sub-topics under parent items
  - `n`: Recursive nesting for all levels with subdirectories

## Task Flow

### 1. Scan for Module Readme Files

Find all `readme.md` files at `demos/*/readme.md` (e.g., `demos/01-fundamentals/readme.md`).

### 2. Extract Existing TOC

Identify the current TOC in each file:

- Find markdown sections that list links to subfolders
- Extract all `[text](./subfolder/)` or `[text](subfolder/)` patterns
- Record the link text, path, and position in the file

### 3. Scan Filesystem for Subfolders

List all immediate subfolders in the module directory that are not documentation:

- Include: numbered folders (e.g., `01-local`, `02-cloud`)
- Exclude: `_images`, `_templates`, other non-topic folders
- Sort alphabetically by folder name

### 4. Extract Heading Titles

For each subfolder, determine the TOC entry title:

- Extract folder name (e.g., `07-context-window`)
- Convert to readable format: remove numeric prefix, replace hyphens with spaces, capitalize words
  - `01-local` → `Local`
  - `07-context-window` → `Context Window`
  - `03-ai-assisted-coding` → `AI Assisted Coding`
- If readme.md H1 exists: extract the heading
- Compare folder-derived name vs H1
  - If H1 sounds more polished/accurate, use H1
  - If folder name is clearer/shorter, use folder name
  - Decision rule: **pick whichever is most readable and professional**
- Never use a label that is NEITHER the folder name NOR the H1

### 5. Build Expected TOC

Create the authoritative TOC based on filesystem:

- Format: `- [Title](./subfolder/)`
- Use relative links with `./` prefix
- Order by folder name (alphanumeric)
- One entry per subfolder (no recursive listing)
- **Top-level TOC (demos/readme.md)**: Show only the main topics/sections (the class structure), NO demos
- **Module-level TOCs** (demos/XX-module/readme.md): Can show nested topics and their demos in a "## Topics" table
- Nested items appear as indented bullet lists only (visual hierarchy via indentation, not headers)

### 6. Validate & Compare

Check if existing TOC matches expected TOC:

- ✓ All filesystem subfolders are listed
- ✓ All TOC entries exist as subfolders (no orphaned links)
- ✓ Titles are either folder-derived OR readme.md H1 (never made-up labels)
- ✓ Links use consistent relative format

### 7. Fix or Report

**If `fixMode=true`:**

- Remove outdated TOC entries
- Add missing entries for new subfolders
- Update titles to match either folder name OR readme.md H1 (whichever reads better)
- Preserve TOC location (usually after module h2)
- Use consistent section header: `## Topics` at second/third-level modules (no "## Demos", "## Demo Prompts", etc.)
- Maintain markdown formatting

**If `fixMode=false`:**

- List findings for each file
- Show what changed (additions, removals, title updates)
- Flag orphaned or broken links

### 8. Output Report

Provide summary:

```
demos/01-fundamentals/readme.md:
  ✓ In sync (8 entries)

demos/03-agentic-coding/readme.md:
  ⚠️ Updates needed:
    - Added: Cloud Agents (02-cloud)
    - Removed: Old Topic (obsolete folder)
    - Updated: Local Agents heading (was "Local")
```

## Entry Selection Rules

| Scenario                        | Action                | Example                                                                                  |
| ------------------------------- | --------------------- | ---------------------------------------------------------------------------------------- |
| **Folder with readme.md**       | Use folder name or H1 | `01-local/` → `[Local](./01-local/)` OR better H1 if available                           |
| **Folder without readme.md**    | Use folder name       | `07-context-window/` → `[Context Window](./07-context-window/)`                          |
| **Numeric prefix in name**      | Extract digits        | `01-fundamentals` → `Fundamentals` (remove 01-)                                          |
| **Hyphens in folder name**      | Convert spaces        | `ai-assisted-coding` → `AI Assisted Coding`                                              |
| **Short folder name + good H1** | Prefer H1             | `04-sdk/` → `SDK` (folder) vs `# GitHub Copilot SDK` (H1) → use **`GitHub Copilot SDK`** |
| **Multiple words**              | Capitalize each       | `pull-requests-code-review` → `Pull Requests Code Review`                                |

## Best Practices

- Filesystem is authoritative: Folder names are the starting point for TOC titles
- Derive titles from folder names: Remove numeric prefixes, convert hyphens to spaces, capitalize words
- If readme.md H1 sounds better: Use the H1 instead (readability and professionalism first)
- Never use labels that are neither folder name NOR H1 - this indicates a made-up title
- Consistent format: Use `[Title](./folder/)` where Title comes from folder structure or readme H1
- Single level: In most cases, list subfolders without going deeper into demos
- Exclude utility folders: Skip `_images`, `_templates`, `.assets`, etc.
- Preserve context: Keep TOC near module heading, maintain spacing
