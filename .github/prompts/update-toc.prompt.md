---
name: check-links
description: Validate and fix markdown links to repository artifacts across documentation. Scans for unlinked paths, converts deep nesting to absolute paths, and ensures all links are properly formatted.
---

# Check & Fix Markdown Links

Validate and repair markdown links to repository artifacts (`.github/`, `.vscode/`, `src/`, `demos/`, etc.) across documentation files.

## Input Parameters

Specify in your prompt:
- **`path`**: Directory or glob pattern to scan (e.g., `demos/**/readme.md`, `**/*.md`)
- **`linkPatterns`**: Repository path prefixes to validate (default: `.github/`, `.vscode/`, `src/`, `demos/`, `.devcontainer/`, `.copilot-conversation/`)
- **`fixMode`**: `true` to auto-fix links, `false` to report only (default: `true`)
- **`validateTargets`**: `true` to verify links resolve to existing files (default: `false`)

## Task Flow

### 1. Search for Unlinked Paths

Identify repository paths in normal text (outside code blocks and quotes):

```regex
(?<![\[\`])\.github/[a-zA-Z0-9._/-]+(?![.\w])
(?<![\[\`])\.vscode/[a-zA-Z0-9._/-]+(?![.\w])
(?<![\[\`])src/[a-zA-Z0-9._/-]+(?![.\w])
(?<![\[\`])demos/[a-zA-Z0-9._/\\-]+(?![.\w])
(?<![\[\`])\.devcontainer/[a-zA-Z0-9._/-]+
(?<![\[\`])\.copilot-conversation/[a-zA-Z0-9._/-]+
```

### 2. Validate Each Path

For each match, determine:
- ✓ Is it **inside a code block?** (skip - preserve examples)
- ✓ Is it **inside a quoted string?** (skip - preserve quoted text)
- ✓ Does it have **3+ `../` depth?** (convert to absolute `/.../`)
- ✓ Is the **link target valid?** (verify file/folder exists if `validateTargets=true`)

### 3. Fix or Report

**If `fixMode=true`:**
- Convert unlinked paths to markdown links: `[text](path)`
- Use absolute paths for deep nesting: `[.github/deploy.json](/.github/deploy.json)`
- Use relative paths for same-module references: `[readme.md](readme.md)`
- Preserve backticks and code formatting

**If `fixMode=false`:**
- List all findings with file, line number, and suggestion
- Flag invalid references (broken paths)
- Note excluded patterns (intentionally unlinked)

### 4. Output Report

Provide summary:
```
✅ Fixed: 15 links
✅ Validated: 42 references  
⚠️  Exceptions: 8 (in code blocks/quotes)
❌ Errors: 2 (invalid paths in [file1.md, file2.md])
```

## Conversion Rules

| Scenario | Action | Example |
|----------|--------|---------|
| **Unlinked path in text** | Create markdown link | `.github/deploy.json` → `[.github/deploy.json](/.github/deploy.json)` |
| **3+ nesting depth** | Use absolute root path | `../../../.github/` → `/.github/` |
| **Same folder relative** | Use relative link | `readme.md` → `[readme.md](readme.md)` |
| **Inside code block** | Skip (preserve) | `` `.github/config` `` → unchanged |
| **Inside quote block** | Skip (preserve) | `> Path: .github/deploy.json` → unchanged |
| **Already linked** | Skip (preserve) | `[link](/.github/deploy.json)` → unchanged |

## Best Practices

- **Preserve Examples**: Never modify paths in code blocks, JSON examples, or bash commands
- **Consistency**: Use absolute paths (`/...`) for cross-module references, relative paths for same-module
- **Validation**: When `validateTargets=true`, verify destination files exist before creating links
- **Context**: Reference nearby markdown to ensure links make semantic sense
- **Stability**: Keep intentional unlinked references (e.g., in comments about deprecated paths)