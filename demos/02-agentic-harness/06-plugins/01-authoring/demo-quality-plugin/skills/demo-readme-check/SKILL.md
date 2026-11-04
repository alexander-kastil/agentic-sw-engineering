---
name: demo-readme-check
description: 'Check a demo or lab readme in this masterclass against the class brand-voice rules: no em dashes, every code fence declares a language, internal links are relative. Use before committing a new or edited readme under demos/ or labs/, or when asked to review guide quality.'
---

# Demo Readme Check

Run the checker over the readme in question, then fix what it reports.

## Run it

```powershell
pwsh -NoProfile -File skills/demo-readme-check/check-readme.ps1 -Path demos/02-agentic-harness/06-plugins/readme.md
```

The script prints `OK: <path>` and exits 0 when the file is clean. It prints `FAIL: <path>` followed by one line per finding and exits 1 otherwise, so it also works as a gate in a script or a workflow.

## What it checks

| Rule | Why |
|------|-----|
| No em dashes | House style for every guide in this class. Use a colon, comma, semicolon or parentheses. |
| Every code fence declares a language | Unlabelled fences lose syntax highlighting and break the docs build. A directory tree is `text`. |
| Internal links are relative | An absolute path breaks as soon as the repository is cloned to a different root or served from a subpath. |

Content inside code fences is skipped, so a sample that legitimately contains an em dash or an absolute path does not trip the check.

## Fixing findings

Rewrite rather than delete. An em dash almost always wants a colon when it introduces a list or an explanation, and a comma or parentheses when it brackets an aside. An unlabelled fence needs the language it actually contains, not `text` as a default.
