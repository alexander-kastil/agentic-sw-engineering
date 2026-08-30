# Cowork Context

When Claude Desktop is in **Cowork** mode:

- Cowork runs as a collaborative workspace with folders and shared context.
- A Cowork session has an active folder set before prompts that depend on its files.
- Files are managed through the Cowork folder, not project-level attachments.
- Cowork is a Claude Desktop feature. Drive it with the Midscene backend, not the native in-app browser.

## UI Element Navigation Reference

| UI Element | Position | How to reach it |
| --- | --- | --- |
| Chat / Cowork / Code | Main (top) | Click the "Cowork" tab in the mode switcher at the top of the window |
| New task | Sidebar | Click "New task" or press `Ctrl+N` |
| Projects | Sidebar | Click "Projects" in the sidebar |
| Scheduled | Sidebar | Click "Scheduled" in the sidebar |
| Live artifacts | Sidebar | Click "Live artifacts" in the sidebar |
| Dispatch | Sidebar | Click "Dispatch" in the sidebar |
| Customize | Sidebar | Click "Customize" at the bottom of the sidebar |
| Task input | Main | Click the input field ("Type / for skills"); submit with `Enter`; type `/` to invoke a skill |
| + (attach) | Main | Click the `+` button in the bottom-left of the input box |
| Microphone | Main | Click the microphone icon in the bottom-right of the input box |
| Work in a project | Main | Click the "Work in a project" dropdown below the input box |
| Ask (mode selector) | Main | Click the "Ask" dropdown next to "Work in a project" to switch execution mode |
| Legacy Model / model picker | Main | Click the model name label in the bottom-right below the input box |
| Task suggestions | Main | Click any suggestion card ("Optimize my week", "Organize my screenshots", "Find insights in files") to prefill the brief |
| Customize with plugins | Main | Click "Customize with plugins" below the task suggestions |

## Midscene navigation, two separate commands

```text
# 1. Describe the UI
npx midscene-computer act --prompt "Describe the full Claude Desktop UI including the Cowork panel, folder structure, and all navigation elements."

# 2. Perform the action
npx midscene-computer act --prompt "Click the Cowork tab, identify the active folder and files visible"
```
