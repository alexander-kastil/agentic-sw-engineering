# Chat Context

When Claude Desktop (or claude.ai in the browser) is in **Chat** mode (not inside a Project):

- Messages are independent conversations.
- You start a new conversation by clicking **New chat** in the sidebar.
- Files are attached per-message via the paperclip icon in the input area.
- There is no shared project memory or instructions between chats.

## UI Element Navigation Reference

| UI Element | Position | How to reach it |
| --- | --- | --- |
| New Chat | Sidebar | Click "New chat" or press `Ctrl+N` |
| Projects | Sidebar | Click "Projects" in the sidebar |
| Artifacts | Sidebar | Click "Artifacts" in the sidebar |
| Customize | Sidebar | Click "Customize" at the bottom of the sidebar |
| Settings | Sidebar | Click the gear icon or your profile at the bottom of the sidebar |
| Language | Sidebar | Open Settings, then select Language |
| Get apps and extensions | Sidebar | Click "Get apps and extensions" at the bottom of the sidebar |
| + (attach) | Main | Click the `+` button in the bottom-left of the input box |
| Sonnet (model picker) | Main | Click the model name label in the bottom-right of the input box |
| Microphone | Main | Click the microphone icon in the bottom-right of the input box |
| Message input | Main | Click the input field ("How can I help you today?") or press `Tab` to focus; submit with `Enter`; new line with `Shift+Enter` |

## Midscene navigation, two separate commands

```text
# 1. Describe the UI
npx midscene-computer act --prompt "Describe the full Claude Desktop UI including all navigation elements in the sidebar and top bar."

# 2. Perform the action
npx midscene-computer act --prompt "Click New chat to start a fresh conversation"
```

## Native in-app browser navigation

Open claude.ai, then drive the same elements by role and label. Click "New chat" in the sidebar, type into the input labelled "How can I help you today?", and read the response back from the page text. The layout and labels match the table above.
