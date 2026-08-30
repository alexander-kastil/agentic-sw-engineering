# Project Context

When Claude Desktop (or claude.ai in the browser) is in **Project** mode:

- The breadcrumb at the top shows `All projects > Project Name`.
- You do **not** click "New chat". To continue in the same Project, click the breadcrumb at the top to return to the project overview, then paste the next prompt into the message input.
- All prompts in the same Project share the same conversation thread. You never need to start a new chat.
- Files are attached to the Project via the **Files** section in the Project panel (right side). Click the **+** next to Files, then **Upload from device**.
- Project instructions are set and updated via the **Instructions** section in the Project panel. Click the edit button or the **+** next to Instructions.
- **To update instructions after a gap analysis:** open the Instructions dialog from the Project panel, add the new rule, and click Save. This is a UI action, not a chat prompt.
- All conversations inside the Project inherit the project's files and instructions.

## Chat project, UI navigation reference

| UI Element | How to reach it |
| --- | --- |
| All projects (back link) | Click "← All projects" at the top-left to return to the project list |
| Project name | Click the title to rename it inline |
| Share | Click the "Share" button top-right to invite collaborators |
| Star | Click the star icon top-right to pin the project to the sidebar |
| More options | Click the three-dot icon top-right for rename, duplicate, or delete |
| Message input | Click the input field ("How can I help you today?") or press `Tab` to focus; submit with `Enter`; new line with `Shift+Enter` |
| + (attach) | Click `+` in the bottom-left of the input box to attach files to the current message |
| Sonnet 4.6 / model picker | Click the model name label in the input bar to switch models |
| Adaptive / mode selector | Click "Adaptive" next to the model name to change response mode |
| Microphone | Click the microphone icon in the input bar for voice input |
| Start a task in Cowork | Click "Start a task in Cowork" below the input to open this project in Cowork mode |
| Memory (right panel) | Visible in the right panel; read-only, built automatically by Claude after a few chats |
| Instructions (right panel) | Click `+` next to Instructions to open the edit dialog; paste text and click "Save instructions" |
| Files (right panel) | Click `+` next to Files, then "Upload from device" to add knowledge files |

## Cowork project, UI navigation reference

| UI Element | How to reach it |
| --- | --- |
| Project name | Displayed at the top; click the three-dot icon next to it to rename or delete |
| Pin | Click the pin icon top-right to keep the project in the sidebar |
| Task input ("What would you like to work on?") | Click the input field or press `Tab` to focus; type `/` to invoke a skill; submit with `Enter` |
| + (attach) | Click `+` in the bottom-left of the input box to attach files or folders to the brief |
| Microphone | Click the microphone icon for voice input |
| Project folder dropdown (bottom-left) | Click the project name dropdown to switch to a different project folder |
| Ask / mode selector | Click "Ask" to switch between autonomous action and conversational step-by-step mode |
| Haiku 4.5 / model picker | Click the model name label bottom-right to switch models |
| Instructions (right panel) | Click the edit (pencil) icon or `+` next to Instructions to open the edit dialog; save with "Save" |
| Scheduled (right panel) | Click `+` next to Scheduled to configure a recurring task for this project |
| Context (right panel) | Expand "Context" to see the linked folder and project memory; click `+` to add or change the folder |
| On your computer / folder | Listed under Context; click the folder row to change the linked local directory |
| Memory (right panel) | Listed under Context; read-only, built automatically from previous sessions |

## File attachment via Project Files panel

1. Locate the **Files** section in the right-side Project panel.
2. Click the **+** (plus) button next to Files.
3. Click **Upload from device**.
4. In the file picker, paste the folder path into the **address bar** (not the filename field), press Enter.
5. Press **Ctrl+A** to select all files, click **Open**.

## Setting or updating Project instructions

1. In the Project panel (right side), locate **Instructions**.
2. Click the edit button or **+** next to Instructions.
3. In the dialog, paste the instructions text, click **Save instructions**.
4. To update: open the same dialog, add the new rule, save again.

## Midscene navigation, always two separate commands

```text
# 1. Understand the UI (no paste, no typing)
npx midscene-computer act --prompt "Describe all visible UI navigation including the breadcrumb, sidebar, Project panel, and message area"

# 2. Paste and send (no "describe" prefix, ONLY UI actions)
Set-Clipboard -Value $prompt
npx midscene-computer act --prompt "Click the message input field, press Ctrl+V, press Enter"
```

## Native in-app browser navigation

Chat projects work the same in the browser: open the Project from the sidebar, use the right-panel Files and Instructions sections, and send prompts into the shared thread. Cowork projects are a Claude Desktop feature, so use the Midscene backend for those.
