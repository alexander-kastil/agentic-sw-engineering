---
name: use-claude-app (reference for run-guide-browser)
description: >-
  Drive Claude Desktop, Claude Code, and any desktop app with Midscene visual automation.
  Covers tool installation, model configuration, window management, multi-monitor setup,
  and Claude Desktop interaction patterns, all from Claude Code.
  Trigger phrases: use claude desktop, control claude desktop, automate claude, claude computer use,
  midscene setup, desktop automation setup, configure midscene, interact with claude app.
allowed-tools:
  - Bash
  - PowerShell
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Claude-Use: Automate Claude Desktop from Claude Code

Automate Claude Desktop (or any desktop app) from Claude Code using Midscene visual AI. This skill covers full setup, correct model configuration, Windows-specific fixes, and reliable interaction patterns. It powers the Midscene backend of the `run-guide-browser` skill.

## Tool Stack

| Tool | Purpose | How to get it |
|------|---------|---------------|
| `@midscene/computer` | Visual AI desktop control (click, type, screenshot) | Install once per project: `npm install @midscene/computer@1` in `.sandbox/`, then call `npx midscene-computer <cmd>` from `.sandbox/` |
| PowerShell Win32 API | Move, resize, focus windows across monitors | Built-in to Windows PowerShell |
| Clipboard (`Set-Clipboard`) | Pass long text into desktop apps without typing | Built-in to PowerShell |

---

## Step 1: Configure the Model

Midscene requires a **vision-language model (VL model)**. Set four environment variables before every Midscene command.

### Required Variables

```powershell
$env:MIDSCENE_MODEL_NAME    = "Qwen/Qwen3-VL-235B-A22B-Instruct"
$env:MIDSCENE_MODEL_BASE_URL = "https://api.deepinfra.com/v1/openai"
$env:MIDSCENE_MODEL_API_KEY  = "<your-deepinfra-key>"
$env:MIDSCENE_MODEL_FAMILY   = "qwen3-vl"
```

> Note: `MIDSCENE_OPENAI_BASE_URL` and `MIDSCENE_OPENAI_API_KEY` are **not** the correct variable names. Midscene only reads `MIDSCENE_MODEL_*` prefixed variables.

### Valid Model Families (v1.8.6+)

Midscene rejects unknown family strings. Use one of these exact values:

```text
doubao-vision  doubao-seed  gemini
qwen2.5-vl     qwen3-vl     qwen3.5    qwen3.6
vlm-ui-tars    vlm-ui-tars-doubao    vlm-ui-tars-doubao-1.5
glm-v          auto-glm    auto-glm-multilingual    gpt-5
```

### Recommended Models (DeepInfra, May 2026)

| Model ID | Family | Notes |
|----------|--------|-------|
| `Qwen/Qwen3-VL-235B-A22B-Instruct` | `qwen3-vl` | **Recommended**, follows Midscene's action type names correctly |
| `Qwen/Qwen3-VL-30B-A3B-Instruct` | `qwen3-vl` | Fast but outputs `Click` instead of `Tap`, use PowerShell fallback |

> Note: `Qwen/Qwen2-VL-72B-Instruct` and `Qwen/Qwen2.5-VL-72B-Instruct` are no longer available on DeepInfra.

### List Available Models on DeepInfra

```powershell
$h = @{Authorization = "Bearer <your-key>"}
(Invoke-RestMethod "https://api.deepinfra.com/v1/openai/models" -Headers $h).data |
  Where-Object {$_.id -like "*VL*" -or $_.id -like "*vision*"} |
  Select-Object id
```

---

## Step 2: Fix Windows PATH for Screenshots

Midscene on Windows uses a compiled C# screen-capture helper. The batch file that calls it does **not** include the directory in the exe path, so cmd.exe cannot find it unless the directory is in `PATH`.

Add this before every Midscene command:

```powershell
$env:PATH = "C:\Users\$env:USERNAME\AppData\Local\Temp\screenCapture;" + $env:PATH
```

Combine it with the model vars into a single reusable block:

```powershell
$env:PATH = "C:\Users\$env:USERNAME\AppData\Local\Temp\screenCapture;" + $env:PATH
$env:MIDSCENE_MODEL_NAME     = "Qwen/Qwen3-VL-235B-A22B-Instruct"
$env:MIDSCENE_MODEL_BASE_URL = "https://api.deepinfra.com/v1/openai"
$env:MIDSCENE_MODEL_API_KEY  = "<key>"
$env:MIDSCENE_MODEL_FAMILY   = "qwen3-vl"
```

---

## Step 3: Bring the Target Window to the Primary Display

Midscene's `act` command operates on whichever display Midscene connects to. For reliable interaction, move the target window to the primary display before issuing any `act` commands.

### Find a Window by Process Name

```powershell
Get-Process | Where-Object {$_.MainWindowTitle -ne "" -and $_.ProcessName -like "*claude*"} |
  Select-Object ProcessName, MainWindowTitle, Id
```

### Move and Focus a Window

The standard window size for Midscene guide runs is **1400 wide by the full working-area height**. On 4K monitors, full-screen windows contain too many pixels for Midscene's element-detection model to locate UI elements reliably. Resizing to 1400 px wide keeps the target app visible and the AI accurate.

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
$proc = Get-Process -Id <PID>
[WinCtrl]::ShowWindow($proc.MainWindowHandle, 9)          # SW_RESTORE
Start-Sleep -Milliseconds 300
[WinCtrl]::MoveWindow($proc.MainWindowHandle, 100, 0, 1400, 1392, $true)   # 1400 wide, full height
[WinCtrl]::SetForegroundWindow($proc.MainWindowHandle)
```

Replace `<PID>` with the process ID from the previous step.

---

## Step 4: Connect and Health Check

Midscene writes all output (logs, screenshots, reports) to a `midscene_run/` folder relative to the working directory. Run every Midscene command from `.sandbox/` so that output stays out of the repo root:

```powershell
Push-Location .sandbox
npx midscene-computer connect
```

The health check takes a screenshot, moves the mouse, and confirms both work. Proceed only if "Health check passed" appears in the output. Keep `.sandbox/` as the working directory for all subsequent Midscene commands in the session. Call `Pop-Location` after `disconnect`.

---

## Step 5: Automation Commands

Run **one command at a time**. Read the screenshot output before issuing the next command.

### Take a Screenshot

```powershell
npx midscene-computer take_screenshot
```

Read the saved PNG path from the output, then use `Read` to view it.

### Perform an Action

```powershell
npx midscene-computer act --prompt "click the input field labelled 'How can I help you today?' and type Hello"
```

Give `act` a single high-level task. It handles all sub-actions internally (click, type, wait).

### Assert Screen State

```powershell
npx midscene-computer assert --prompt "the Claude Desktop window shows a response message"
```

### Disconnect

```powershell
npx midscene-computer disconnect
Pop-Location
```

---

## Sending Long Text to a Desktop App

Do not type long content character-by-character via `act`. Use the clipboard:

```powershell
# 1. Build the message and put it on the clipboard
$message = "Your long text or file content here"
Set-Clipboard -Value $message

# 2. Click the input field and paste
npx midscene-computer act --prompt "click the message input field then press Ctrl+V then press Enter"
```

---

## Claude Desktop UI: Modes and Navigation

Claude Desktop has three modes selectable from the top of the window: Chat, Cowork, and Code. Each mode has a different input field label and right panel. Identify the current mode from the screenshot before issuing any `act` command.

| Mode | Input field label | Right panel contents | How to switch |
| --- | --- | --- | --- |
| Chat (no project) | "How can I help you today?" | None | Click "Chat" in the mode switcher |
| Chat (inside project) | "How can I help you today?" | Memory, Instructions, Files | Click a project in the sidebar or "← All projects" to navigate |
| Cowork | "What would you like to work on?" or "Type / for skills" | Instructions, Scheduled, Context (folder + memory) | Click "Cowork" in the mode switcher |

For the full list of UI elements per mode with click targets and keyboard shortcuts, read the matching context file before navigating:

- `chat-context.md`, Chat mode and Chat project navigation tables
- `project-context.md`, Chat project and Cowork project navigation tables
- `cowork-context.md`, Cowork mode navigation table

Key shortcuts that work across all modes:

| Action | Shortcut |
| --- | --- |
| New chat / New task | `Ctrl+N` |
| Submit message or brief | `Enter` |
| New line without submitting | `Shift+Enter` |
| Focus input field | `Tab` |
| Invoke a skill (Cowork) | `/` in the input field |
| Paste from clipboard | `Ctrl+V` |

> Note: Navigation between Chat, Cowork, and Code modes has no keyboard shortcut as of May 2026. Mode switching requires a mouse click on the mode switcher at the top of the window.

## Interacting with Claude Desktop

Claude Desktop is an Electron app. Treat it like any other desktop window.

### Send a Prompt to Claude Desktop

```powershell
# Move Claude Desktop to primary display first (see Step 3)
# Then paste a prompt via clipboard
$prompt = "Analyse this text and suggest improvements: ..."
Set-Clipboard -Value $prompt
npx midscene-computer act --prompt "click 'How can I help you today?' input field, press Ctrl+V, press Enter"
```

### Read Claude Desktop's Response

Claude Desktop cannot read files from a local path in a chat message. To pass file content:

```powershell
$fileContent = Get-Content "path\to\file.md" -Raw
$message = "Here is the file content, please enhance it:`n`n$fileContent"
```
