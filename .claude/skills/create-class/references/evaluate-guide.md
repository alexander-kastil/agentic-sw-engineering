---
name: evaluate-guide
description: Evaluate a demo guide by executing it as a business owner, manager, or citizen developer inside the live Claude Desktop app using Midscene + Qwen3-VL, auditing context, walking every step, resolving failures, and rewriting the guide from what actually worked.
---

# Evaluate Guide

Walk through a demo guide as a real user would, inside the live Claude Desktop app.
Fix the guide based on what actually happens, not on static rules.

This leaf is loaded by the `create-class` master skill. It is not invoked directly.

## Input

The target is a path to a single guide file (e.g. `demos/01-cowork/demos/demo-01-first-chat.md`)
or a module `demos/` folder. Process one file at a time.

## Prerequisites

Read `references/evaluate-guide/use-claude-app.md` for Midscene environment setup, window positioning,
connect/disconnect patterns, and the clipboard paste pattern.

When the guide uses a specific context, read the corresponding reference. Each file contains a UI navigation table with click targets and keyboard shortcuts for that mode:

- `references/evaluate-guide/chat-context.md` — Chat mode navigation table (new chat, input, model picker, attach, sidebar items)
- `references/evaluate-guide/project-context.md` — Chat project and Cowork project navigation tables (right panel, Instructions, Files, Context folder)
- `references/evaluate-guide/cowork-context.md` — Cowork mode navigation table (task input, Work in a project, Ask, model picker, sidebar items)
- `references/evaluate-guide/attach-files.md` — How to attach files to a Project vs chat

## Phase 1: Context audit (before touching Claude Desktop)

Read the entire guide. Identify every piece of context the guide's prompts depend on:

**Files:** Every file a prompt references (a `.docx`, `.pdf`, spreadsheet, etc.).
For each file, check whether the guide includes a step that attaches it via the `+` button
before the prompt is sent. If any prompt says "read X" or "use X" without a preceding
attachment step, the guide is broken. Rewrite that section to add the attachment step first.

**Projects:** If the guide uses a Claude Desktop Project (e.g. "open the Marketing project"),
check that the guide tells the user how to create or open that project and load the required
files into it before the first prompt that depends on it.

**Cowork folders:** If the guide uses a Cowork folder, check that the guide tells the user
to set the folder before sending any prompt that depends on files in it.

**Goal:** No prompt should be sent with missing context. If context is not set up, rewrite the
guide to set it up first. Fix all issues found in Phase 1 before proceeding.

## Phase 2: Create tasks ledger

Before connecting to Claude Desktop, create a task ledger file at `tasks/evaluate-guide.md`
with every action you plan to take during execution. Break each guide step into concrete,
single-action tasks. Example:

```markdown
# Tasks Ledger: demo-03-department-project.md

| # | Task | Status | Attempts | Result |
|---|------|--------|----------|--------|
| 1 | Connect Midscene and health check | pending | 0 | — |
| 2 | Create Project "Vantage Group" | pending | 0 | — |
| 3 | Attach team-charter.docx to Project | pending | 0 | — |
| 4 | Attach competitive-analysis-brief.docx to Project | pending | 0 | — |
| 5 | Attach supplier-review-brief.docx to Project | pending | 0 | — |
| 6 | Send Step 1 Research prompt | pending | 0 | — |
| 7 | Send Step 1 Recipe prompt | pending | 0 | — |
| 8 | Send Step 2 Research prompt | pending | 0 | — |
| 9 | Send Step 2 Recipe prompt | pending | 0 | — |
| 10 | Send Step 3 Research prompt | pending | 0 | — |
| 11 | Send Step 3 Recipe prompt | pending | 0 | — |
| 12 | Disconnect Midscene | pending | 0 | — |
```

**Work one task at a time.** Mark it `in-progress` before acting, `done` when it succeeds,
or `failed` if it errors. When a task fails:

1. Read the error output from Midscene.
2. Reflect on the cause in the ledger (add a `Note` column or a row below).
3. Decide the fix: adjust the Midscene prompt, reposition the window, or rewrite the guide section.
4. If the fix is a guide change, apply it **immediately** to the guide file before retrying.
5. Increment the attempt count and retry.
6. When the task succeeds, move to the next one.

Never skip a failing task. Never continue past a task marked `failed`.

## Phase 3: Execute the guide as a real user

Set up Midscene following `references/evaluate-guide/use-claude-app.md`:

```powershell
Push-Location .sandbox

if (-not (Get-Command midscene-computer -ErrorAction SilentlyContinue)) {
    npm install -g @midscene/computer@1
}

$env:PATH = "C:\Users\$env:USERNAME\AppData\Local\Temp\screenCapture;" + $env:PATH
$env:MIDSCENE_MODEL_NAME     = "Qwen/Qwen3-VL-235B-A22B-Instruct"
$env:MIDSCENE_MODEL_BASE_URL = "https://api.deepinfra.com/v1/openai"
$env:MIDSCENE_MODEL_API_KEY  = "<key-from-use-claude-app-skill>"
$env:MIDSCENE_MODEL_FAMILY   = "qwen3-vl"
```

Position Claude Desktop and connect:

```powershell
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinCtrl {
    [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int ht, bool r);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
}
"@
$proc = Get-Process | Where-Object {$_.MainWindowTitle -ne "" -and $_.ProcessName -like "*claude*"} | Select-Object -First 1
[WinCtrl]::ShowWindow($proc.MainWindowHandle, 9)
Start-Sleep -Milliseconds 300
[WinCtrl]::MoveWindow($proc.MainWindowHandle, 100, 0, 1400, 1392, $true)
[WinCtrl]::SetForegroundWindow($proc.MainWindowHandle)

midscene-computer connect
```

If the health check fails, stop and report `SKIPPED: <filename> — Midscene health check failed`.

**Role:** You are a business owner, manager, or citizen developer. You have no technical background.
You follow the guide exactly as written, step by step, using Midscene to drive Claude Desktop.

For each step in the guide:

1. **Describe the UI first, in a SEPARATE command before pasting.** Never combine "describe" and "paste" in one `act`:
   ```powershell
   # Step A: understand the UI (no paste, no typing)
   npx midscene-computer take_screenshot
   ```
   Read the screenshot output to understand what is visible. If you need more detail:
   ```powershell
   npx midscene-computer act --prompt "Describe all visible UI navigation elements and the current state of the app"
   ```
2. Follow the guide's instructions literally.
3. **Send the prompt, in a SEPARATE command with NO "describe" prefix:**
   ```powershell
   Set-Clipboard -Value $prompt
   npx midscene-computer act --prompt "Click the message input field, press Ctrl+V, press Enter"
   ```
   The act prompt must ONLY contain UI actions (click, paste, enter). Never include "describe" or "first tell me" text.
4. Wait for Claude Desktop to finish responding. Take a screenshot.
5. Read the screenshot. If Claude Desktop shows an error or the response is wrong or incomplete:
   - Read the error message from the screenshot.
   - Determine the cause (missing context, wrong instruction, UI element not where the guide says).
   - Resolve it: attach missing files, adjust the prompt, correct the UI step.
   - Assess severity:
     - **Minor** (wrong button name, missing attachment): fix in place and continue.
     - **Major** (the whole step fails, context is wrong, project not set up): restart the guide
       execution from the beginning with the corrected version.
6. Once the step succeeds, rewrite the corresponding section of the guide to reflect what
   actually worked. Apply the fix immediately before moving to the next step.

## Phase 4: Teardown

```powershell
midscene-computer disconnect
Pop-Location
```

## Report

```
<filename> — <N> steps executed, <N> fixes applied, <N> restarts
Fixes:
  - Step N: <what was wrong> → <what was changed>
```

## Hard rules

- Only one Claude Desktop session at a time.
- Never rewrite a guide section based on assumption. Only rewrite based on what actually happened during execution.
- If a step cannot be made to work after one restart, stop and report the blocker.
- Screenshots are evidence. Take one after every step.

## Ledger rules (strict)

- **Show the full ledger after every single task.** Never proceed without displaying it.
- **One task at a time.** Complete task N completely before touching task N+1.
- **Never skip a task.** If a task fails, fix it and retry. Do not jump ahead.
- **New tasks insert at the correct position.** If execution reveals a missing step, add it between existing tasks, not at the end.
- **Describe and paste are separate commands.** Never combine UI description with clipboard paste in one `act` prompt.
- **For Project guides: updating Instructions is a UI action in the Project panel, not another chat prompt.** After gap analysis, open the Instructions dialog via the Project panel + button, paste updated rules, and click Save.
- **Demo Assets, not Demo Files.** All guide headings use "Demo Assets" for companion file tables.
- **Window size: 1400 × full working-area height.** Use `[WinCtrl]::MoveWindow($proc.MainWindowHandle, 100, 0, 1400, 1392, $true)` not 900px height.
