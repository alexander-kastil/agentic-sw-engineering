---
name: conventional-commit
description: "Write a Conventional Commits message for the staged changes in the current repository. Use when the user asks for a commit message, wants to describe staged work, or is about to commit."
---

# Conventional commit message

1. Run `git diff --staged` and read every staged hunk. If nothing is staged, say so and stop.
2. Pick one type: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci` or `chore`.
3. Use the top-level folder the change touches most as the scope, for example `feat(api):`.
4. Write a subject in the imperative mood, at most 72 characters, with no trailing period.
5. Add a body only when the reason for the change is not obvious from the subject, wrapped at 72 characters.
6. Add `BREAKING CHANGE:` as a footer when a public contract changes.

Return the message in one `text` block. Never run `git commit` yourself.
