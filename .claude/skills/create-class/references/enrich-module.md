---
name: enrich-module
description: Enrich a module README with structured content, a topic-specific slash command table, and key documentation links.
---

# Enrich Module

Read the target module readme path from the task passed to create-class. Focus on that markdown file and the content in its sub-folders.

**Process:**

1. Read a reference document if provided for tone or style guidance.
2. Read source files in the module folder and its sub-folders to extract key features and technologies.
3. Rewrite or enhance the description with what it does plus its use case and notable features (technology stack and standout features).

**Output structure (in order):**

1. Description content
2. `## Helpful Claude Slash Commands`, a 2-column table (Command | Usage) listing slash commands relevant to this module's topic. Never include `/create-class`, `/create-learning`, `/create-teaching`, or `/create-lab`; these are internal authoring commands.
3. `## Key Topics covered in this module`, with relevant documentation links. Keep and update existing links, or add the most relevant official docs if none exist.

**Rules:**

- The slash command table must be topic-specific to this module. Never repeat a generic set of slash commands across modules; each table reflects the technologies and tasks of its own module.
- For each item describe its use case, technology stack, and 1-2 standout technical details.
- Separate multiple items with a paragraph.
- Reference files and scripts by name with links where possible. Use repo-absolute paths (starting with `/`) for assets outside the module's folder, and relative paths for assets within it.
- Validate image links, fix broken ones, add descriptive captions, and place images in the text flow where they fit.
- Include code snippets only if relevant, and update outdated ones inside fenced code blocks.
- Add prompts in fenced code blocks.
- No bold or italic in descriptions.
- Max 3 sentences per paragraph.
- Always use markdown tables. Never use HTML tables (`<table>`, `<colgroup>`, `<tr>`, and similar).
