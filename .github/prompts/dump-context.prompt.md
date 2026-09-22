---
name: dump-context
description: Use this prompt to capture the full conversation history of the current session and write it to a log.md file in the repository root. Useful for archiving, handoff, or resuming work.
---

Write the complete conversation history of this session to a file named `log.md` in the repository root (`d:\git-classes\agentic-sw-engineering\log.md`).

Requirements:
- Include every user message and every assistant response in order.
- Preserve the exact wording of each message — do not summarize or paraphrase.
- Label each entry clearly as **User** or **Assistant**.
- Include the session date at the top.
- Use plain markdown. No extra commentary, no preamble, no conclusion — only the log content.

Output format:

```markdown
# Conversation Log

**Date:** <today's date>

---

**User:** <exact message>

**Assistant:** <exact response>

---

**User:** <exact message>

**Assistant:** <exact response>
```

Write this file now using the create or edit file tool. Do not print the content to chat.