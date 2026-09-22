---
name: code-reviewer
description: Use this skill to review code. It supports both local changes (staged or working tree) and remote Pull Requests (by ID or URL). It focuses on correctness, maintainability, and adherence to project standards.
---

# Code Reviewer

This skill guides Claude Code in conducting professional and thorough code reviews for both local development and remote Pull Requests.

## Workflow

### 1. Determine Review Target

- **Remote PR**: If the user provides a PR number or URL (e.g., "Review PR #123"), target that remote PR.
- **Local Changes**: If no specific PR is mentioned, or if the user asks to "review my changes", target the current local file system state (staged and unstaged changes).

### 2. Preparation

#### For Remote PRs

1. **Checkout**: Use the GitHub CLI to checkout the PR.

   ```bash
   gh pr checkout <PR_NUMBER>
   ```

2. **Preflight**: Run the project's verification suite to catch automated failures early. Look in `package.json`, `Makefile`, `pyproject.toml`, or the project README for the canonical command (common options: `npm test`, `npm run lint`, `pytest`, `dotnet test`). If none is defined, skip this step.
3. **Context**: Read the PR description and any existing comments with `gh pr view <PR_NUMBER>` to understand the goal and history.

#### For Local Changes

1. **Identify Changes**:
   - Check status: `git status`
   - Read diffs: `git diff` (working tree) and `git diff --staged` (staged).
2. **Preflight (Optional)**: If the changes are substantial, ask the user if they want to run the project's verification command before reviewing.

### 3. In-Depth Analysis

Analyze the code changes based on the following pillars:

- **Correctness**: Does the code achieve its stated purpose without bugs or logical errors?
- **Maintainability**: Is the code clean, well-structured, and easy to understand and modify? Consider clarity, modularity, and adherence to established design patterns.
- **Readability**: Is the code well-named, well-commented where necessary, and consistently formatted according to the project's style?
- **Efficiency**: Are there obvious performance bottlenecks or resource inefficiencies introduced by the changes?
- **Security**: Are there potential security vulnerabilities or insecure coding practices? (See OWASP top 10: injection, XSS, secrets in code, unsafe deserialization, etc.)
- **Edge Cases and Error Handling**: Does the code appropriately handle edge cases and potential errors?
- **Testability**: Is the new or modified code adequately covered by tests? Suggest additional test cases that would improve coverage or robustness.
- **Project Conventions**: Does the change respect rules in `CLAUDE.md`, contributing guides, or other repo-level conventions?

### 4. Provide Feedback

#### Structure

- **Summary**: A high-level overview of the review.
- **Findings**:
  - **Critical**: Bugs, security issues, or breaking changes that block merge.
  - **Improvements**: Suggestions for better code quality, performance, or design.
  - **Nitpicks**: Formatting or minor style issues (optional).
- **Conclusion**: Clear recommendation (Approved / Request Changes).

Reference specific code with `file_path:line_number` so the user can jump directly to each finding.

#### Tone

- Be constructive, professional, and friendly.
- Explain *why* a change is requested, not just *what* to change.
- For approvals, acknowledge the specific value of the contribution.

### 5. Cleanup (Remote PRs only)

After the review, ask the user if they want to switch back to the default branch (e.g., `main` or `master`).
