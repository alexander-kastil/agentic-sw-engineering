---
name: create-issue
description: Turn a feature request or a finished implementation plan into GitHub issues grounded in the real code, then create them with the gh CLI. A plan with several tasks becomes one parent issue with one sub-issue per task. Use when the user says "create an issue", "file this as issues", "turn the plan into issues", "open issues with sub-issues", or "track this plan on GitHub".
license: MIT
compatibility: Requires the gh CLI, authenticated against the repository's GitHub remote
metadata:
  author: integrations.at
  version: "1.0"
---

# Create Issue

Convert a request or a plan into issues someone can pick up without re-reading the conversation. The value is grounding: every issue names real files and the existing pattern to follow.

## Repository and labels

Derive the repository from the checkout, never from this file:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

Read the label set with `gh label list`. When the user names a label that does not exist, create it once:

```bash
gh label create planning --description "Work item produced by a planning session" --color 0E8A16
```

## Research shallow, write sharp

1. Collision check first: search the code for the request's own nouns. State in the issue whether the thing already exists, partially exists, or collides with an existing name.
2. Find the closest existing pattern and capture real `path:line` anchors. Read a handful of files at most.
3. Search open issues for duplicates: `gh issue list --search "<key terms>"`.

When the input is a plan file, the plan is the research: verify only the file paths it cites exist.

## Issue body

Use only the sections that carry signal:

```markdown
## Summary
One or two sentences: what changes and why.

## Context
What exists today, with file paths, and the pattern to follow.

## Proposed approach
Short bullets per layer touched.

## Acceptance criteria
- [ ] Observable, testable outcomes.

## Out of scope
What this issue deliberately leaves out.
```

## One issue, or a parent with sub-issues

A single request becomes one issue. A plan with several tasks becomes a parent issue that carries the summary, the overall acceptance criteria and the task order, plus one sub-issue per task.

Write each body to a file under `.github/tmp/`, create the issue, and keep the number `gh` prints:

```bash
gh issue create --title "<imperative title>" --label planning --body-file .github/tmp/parent.md
```

Sub-issues are linked through the REST API, which takes the child's database id, not its number:

```bash
child_id=$(gh api repos/{owner}/{repo}/issues/<child-number> --jq .id)
gh api -X POST repos/{owner}/{repo}/issues/<parent-number>/sub_issues -F sub_issue_id=$child_id
```

Create the parent first, then each child, then link each child. Remove `.github/tmp/` when done.

## Confirm before creating

Issues are public on the repository. Show the titles, labels and parent-child tree first, and create them only after the user approves, unless the prompt already says to create them directly.

## Report

List every issue URL, marking the parent and its sub-issues, and confirm the link with:

```bash
gh api repos/{owner}/{repo}/issues/<parent-number>/sub_issues --jq '.[].number'
```

## Guardrails

- Never implement: this skill produces issues, not code or branches.
- Never invent a file path or symbol; verify each one before citing it.
- Write issues in US English.
