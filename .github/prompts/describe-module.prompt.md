---
name: Describe Module
description: This prompt is used to describe a module
agent: agent
model: Claude Haiku 4.5 (copilot)
---

# Documentation Enhancement Prompt

Work with the current file attached to this prompt.

Focus on the attached markdown file and the content in its folder and sub-folders.

"Describe the [N] [things] for [topic] in the style of [reference doc]. Not too detailed but if there are nice things to mention do so."

If the readme contains links add them to the bottom under a "## Key Topics covered in this module" section.

**Process:**

1. Read reference document for tone/style
2. Read source files to extract key features
3. Rewrite descriptions with: what it does + notable features

**Example:**

- What it demonstrates (use case, technology stack)
- 1-2 standout technical details
- Keep length consistent across items

**Important:**

- When there are multiple items, separate them with a paragraph.
- When references to files or scripts are present, mention them by name and link them if possible.
- If there are links to images, check if they link is valid, try to fix broken links and integrate them into the description. Each image should have a descriptive caption.
- If there are code snippets, check if they are relevant to the description and include them if they add value. If they are outdated, update them. Render them in markdown code blocks.
- Do not touch "## Links & Resources" sections unless specified.
- Do not use **bold** or _italic_ formatting in the descriptions.
- Never use more than 3 sentences per paragraph. Shorter paragraphs are easier to scroll over and digest quickly, improving readability and making content more scannable.
- When asked to add prompts always add them in a markdown code block.
