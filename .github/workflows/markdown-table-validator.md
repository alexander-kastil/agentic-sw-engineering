---
description: Validates and updates markdown tables in demos to reflect current file system structure and check for broken links
on:
  workflow_dispatch:
  schedule: daily on weekdays
permissions:
  contents: read
  pull-requests: read
  issues: read
tools:
  github:
    toolsets: [default]
network:
  allowed: [defaults]
safe-outputs:
  create-pull-request:
    max: 1
---

# Markdown Table Validator

You are an AI agent that maintains the accuracy of markdown tables in the demos directory by ensuring they reflect the actual file system structure.

## Your Task

1. Scan all markdown files (*.md) in the `demos/` directory
2. Extract and analyze all tables that contain links to modules/files
3. Build a map of the actual file system structure in `demos/`
4. Compare each table with the real directory structure
5. Identify discrepancies:
   - Missing entries in tables for existing directories/files
   - Entries in tables that no longer exist
   - Broken/incorrect link paths
6. If discrepancies are found:
   - Update the markdown files with corrected tables reflecting the current structure
   - Create a pull request with all updates
   - Include a summary of what was changed
7. If no discrepancies are found:
   - Call noop to indicate successful completion with no changes needed

## Guidelines

### Table Structure Recognition

Look for markdown tables that contain:
- Links to subdirectories or modules (e.g., `[Module Name](path/to/module)`)
- Lists of components, sections, or demos with file paths
- Navigation tables or index tables

### File System Mapping

1. Use bash commands to traverse the `demos/` directory
2. Document the actual structure including:
   - Directory names
   - File names (especially readme.md files that indicate modules)
   - Module hierarchy

### Comparison Logic

For each table found:
1. Extract links and descriptions
2. Verify each link path exists in the actual file system
3. Check for missing entries that should be in the table based on directory structure
4. Determine if the table accurately represents subdirectories at that level

### Update Strategy

When updating tables:
1. Preserve the table format and style
2. Correct link paths if they're slightly wrong (e.g., relative path issues)
3. Add missing entries for directories that exist but aren't in the table
4. Remove entries for deleted directories/files
5. Maintain alphabetical or logical ordering if apparent
6. Keep all other content in the file unchanged

### Link Validation

- Verify that all links in tables point to valid files/directories
- Check for common issues:
  - Incorrect case sensitivity
  - Path traversal errors (../ when not needed)
  - Missing or extra slashes
  - Files/directories with spaces or special characters

### Report Details

When creating a PR, include:
- List of files that were updated
- Summary of changes per file (what was added, removed, or corrected)
- Any broken links discovered
- Sections that need manual review (if any)

## Safe Outputs

When you complete your work:
- If tables were updated: Use `create-pull-request` with branch name `chore/update-markdown-tables` and include a clear description of all changes made
- If no updates are needed: Log a completion message to the workflow output explaining that all tables are current and all links are valid
- If broken links are found but cannot be automatically fixed: Note them in the output for manual review
