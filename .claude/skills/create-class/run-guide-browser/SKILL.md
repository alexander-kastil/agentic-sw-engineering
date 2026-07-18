---
name: run-guide-browser
description: Run a demo or lab guide as a real user in a live browser or desktop app, observe what actually works, then rewrite the guide from that. Two backends the user picks per run: Claude Code desktop's native in-app browser (simplest, no extra stack) or Midscene plus Qwen3-VL vision automation (cheap, drives Claude Desktop or any native app). The browser and desktop counterpart to run-demo (code) and run-foundry-demo (Foundry). Peer skill the create-class master delegates to; also invocable directly. Trigger phrases: run guide in browser, evaluate guide, test guide as a user, drive claude desktop, in-app browser guide test, midscene guide test.
---

# Run Guide in Browser

Walk through a demo or lab guide the way a real user would, in a live browser or desktop app.
Fix the guide based on what actually happens, not on static rules.

This is the browser and desktop sibling of `run-demo` (runs code projects) and `run-foundry-demo` (runs Foundry agents). The `create-class` master delegates here; it is also invocable on its own.

## Input

The target is a path to a single guide file (e.g. `demos/02-chat-productivity/demo-01-first-chat.md`) or a module `demos/` folder. Process one file at a time.

## Pick a backend (per run)

Ask the user which backend to use, or infer from the guide's surface. Both drive the same guide; they differ in cost and setup.

| Backend | What drives the app | Best for | Cost | Setup |
| --- | --- | --- | --- | --- |
| **Native in-app browser** | Claude Code desktop's built-in sandboxed browser | Any web surface: claude.ai Chat and Projects, Copilot Studio, SharePoint, M365 web, docs and designs | No extra model spend | None beyond Claude Code desktop |
| **Midscene + Qwen3-VL** | External vision automation over screenshots | The native Claude Desktop app (Cowork mode, desktop-only features), or any non-browser desktop app | Cheap VL model calls (DeepInfra) | Midscene install, model env vars, window positioning |

Rule of thumb: **simplicity wins when the guide runs in a browser**, so prefer the native in-app browser. Reach for Midscene only when the guide targets the native desktop app (Cowork, local folders, Electron-only UI) or another desktop application.

### Native in-app browser

Claude Code on desktop ships a sandboxed, configurable in-app browser. It pulls up docs, designs, or any site and can read, click, type, and interact the same way it drives a local dev server; sessions optionally persist across steps. It needs no external vision stack: you observe the page directly (read page text, screenshots) and act on elements by role and label.

Drive it as its own agent loop: open the guide's URL (e.g. claude.ai), then for each step read the page, act on the element the guide names, and read the result back. The per-context UI tables in `references/` name every element and its label, so map the guide's instruction to the matching row.

### Midscene + Qwen3-VL

External vision automation with a cheap Chinese VL model (Qwen3-VL on DeepInfra) driving the app from screenshots. Full setup, model configuration, window management, and interaction patterns live in `references/use-claude-app.md`. This is the required backend for Cowork and other desktop-only surfaces.

## Prerequisites

Read the context reference that matches the guide's surface. Each file carries a UI navigation table with click targets, labels, and keyboard shortcuts, and works for either backend:

- `references/chat-context.md`, Chat mode navigation (new chat, input, model picker, attach, sidebar)
- `references/project-context.md`, Chat project and Cowork project navigation (right panel, Instructions, Files, Context folder)
- `references/cowork-context.md`, Cowork mode navigation (task input, Work in a project, Ask, model picker); Midscene backend only
- `references/attach-files.md`, attaching files to a Project versus a single chat message

For the Midscene backend, also read `references/use-claude-app.md` for environment setup, window positioning, connect and health-check, and the clipboard paste pattern.

## Phase 1: Context audit (before touching the app)

Read the entire guide. Identify every piece of context its prompts depend on, and fix gaps in the guide before running anything:

- **Files:** every file a prompt references (`.docx`, `.pdf`, spreadsheet). For each, confirm the guide has a step that attaches it (via `+`) before the prompt that uses it. A prompt that says "read X" or "use X" with no preceding attachment step is broken; add the attachment step first.
- **Projects:** if the guide uses a Project, confirm it tells the user to create or open that project and load its files before the first dependent prompt.
- **Cowork folders:** if the guide uses a Cowork folder, confirm it tells the user to set the folder before any prompt that depends on its files.

Goal: no prompt is ever sent with missing context. Fix all Phase 1 issues before proceeding.

## Phase 2: Create the tasks ledger

Before connecting, create a ledger at `tasks/run-guide-browser.md` with every action you plan to take. Break each guide step into concrete single-action tasks.

```markdown
# Tasks Ledger: demo-03-department-project.md (backend: native in-app browser)

| # | Task | Status | Attempts | Result |
|---|------|--------|----------|--------|
| 1 | Open claude.ai and confirm signed in | pending | 0 | (none) |
| 2 | Create Project "Vantage Group" | pending | 0 | (none) |
| 3 | Attach team-charter.docx to Project | pending | 0 | (none) |
| 4 | Attach competitive-analysis-brief.docx to Project | pending | 0 | (none) |
| 5 | Send Step 1 Research prompt | pending | 0 | (none) |
| 6 | Send Step 1 Recipe prompt | pending | 0 | (none) |
| 7 | Send Step 2 Research prompt | pending | 0 | (none) |
| 8 | Close the session | pending | 0 | (none) |
```

Work one task at a time. Mark it `in-progress` before acting, `done` on success, `failed` on error. When a task fails:

1. Read the error output (Midscene log, or the page text and a screenshot).
2. Reflect on the cause in the ledger.
3. Decide the fix: adjust the action prompt, reposition the window, or rewrite the guide section.
4. If the fix is a guide change, apply it to the guide file immediately, before retrying.
5. Increment the attempt count and retry.

Never skip a failing task. Never continue past a task marked `failed`.

## Phase 3: Execute the guide as a real user

**Role:** you are a business owner, manager, or citizen developer with no technical background. You follow the guide exactly as written, step by step.

### Setup

- **Native in-app browser:** open the guide's starting URL in the in-app browser. If sessions persist, confirm the user is signed in before Step 1.
- **Midscene:** follow `references/use-claude-app.md` to set the model env vars and PATH, position the Claude Desktop window (1400 wide, full height), then `npx midscene-computer connect`. If the health check fails, stop and report `SKIPPED: <filename>: Midscene health check failed`.

### Per step

1. **Observe the UI first, as a separate action.** Never combine "observe" and "send" in one command.
   - Native: read the page text or take a screenshot to understand the current state.
   - Midscene: `npx midscene-computer take_screenshot`, then read the PNG; use a describe-only `act` if you need more detail.
2. Follow the guide's instruction literally, mapping it to the matching row in the context table.
3. **Send the prompt as a separate action with UI actions only (click, paste, enter), no "describe" text.**
   - Native: focus the input the guide names, enter the prompt text, submit.
   - Midscene: `Set-Clipboard -Value $prompt`, then `npx midscene-computer act --prompt "Click the message input field, press Ctrl+V, press Enter"`.
4. Wait for the app to finish responding, then observe (page read or screenshot).
5. If the app shows an error or the response is wrong or incomplete: read the error, determine the cause (missing context, wrong instruction, UI element not where the guide says), and resolve it (attach missing files, adjust the prompt, correct the UI step). Assess severity:
   - **Minor** (wrong button name, missing attachment): fix in place and continue.
   - **Major** (whole step fails, wrong context, project not set up): restart execution from the beginning with the corrected version.
6. Once the step succeeds, rewrite the matching guide section to reflect what actually worked. Apply the fix immediately before moving on.

## Phase 4: Teardown

- **Native in-app browser:** close the tab or session.
- **Midscene:**

```powershell
npx midscene-computer disconnect
Pop-Location
```

## Report

```text
<filename> (backend: <native|midscene>): <N> steps executed, <N> fixes applied, <N> restarts
Fixes:
  - Step N: <what was wrong> -> <what was changed>
```

## Hard rules

- One live session at a time.
- Never rewrite a guide section from assumption. Only rewrite from what actually happened during execution.
- If a step cannot be made to work after one restart, stop and report the blocker.
- Evidence after every step: a page read or a screenshot.

## Ledger rules (strict)

- Show the full ledger after every single task. Never proceed without displaying it.
- One task at a time. Complete task N before touching task N+1.
- Never skip a task. If it fails, fix it and retry; do not jump ahead.
- New tasks insert at the correct position, between existing tasks, not at the end.
- Observe and send are separate actions. Never fold UI observation into the send command.
- For Project guides, updating Instructions is a UI action in the Project panel, not a chat prompt. After gap analysis, open the Instructions dialog via the panel `+`, paste the updated rules, and Save.
- Companion file tables use the heading "Demo Assets", not "Demo Files".
- Midscene window size is 1400 wide by full working-area height, not 900 px tall.
