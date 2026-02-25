---
name: visualize-conversation
description: Generate, update or delete Copilot conversation visualization markdown from session JSON data collected by Copilot hooks
license: MIT
---

# Visualize Conversation Skill

Generate a Mermaid sequence diagram from conversation session data collected by Copilot hooks, showing user prompts, tool calls, and sub-agent activity. Also visualize or delete conversations using Copilot's interactive question selection.

## How It Works

When you invoke this skill without specifying a session ID:

1. Copilot scans `.copilot-conversation/data` for all available session IDs
2. Uses the ask_questions feature to display sessions and ask you to select one
3. Calls visualize.js with the selected session ID
4. Generates a Mermaid sequence diagram showing the conversation flow

When a session ID is provided, it processes directly without prompting.

## Interactive Visualization (Copilot Selects Session)

The skill automatically uses `ask_questions` when no session is provided:

```powershell
# Copilot will ask which session to visualize using ask_questions
visualize
```

## Direct Visualization (Specify Session ID)

Run from the `.copilot-conversation` directory:

```powershell
cd .copilot-conversation

# Process specific session → conversations/ (level 1)
node ./scripts/visualize.js --session <id>

# Process specific session at level 2 (with tools)
node ./scripts/visualize.js --session <id> --level 2

# List all available sessions
node ./scripts/visualize.js --list
```

## Delete a Conversation

Copilot will use `ask_questions` to select which session to delete when no session ID is provided:

```powershell
# Copilot will ask which session to delete using ask_questions
delete
```

Direct deletion options (run from `.copilot-conversation`):

```powershell
cd .copilot-conversation

# Delete specific session
node ./scripts/visualize.js --delete --session <id>

# Delete all sessions
node ./scripts/visualize.js --delete --session all

# Show available sessions for deletion
node ./scripts/visualize.js --delete
```

Example output when listing available conversations:

```
Available conversations:

  [1] 3704a7c6-553c-461b-a217-c4fb1a779ba7
      "Rename .copilot-metadata..."

  [2] 3e9cac0d-f20b-4a3b-9804-ca2c2a7bf7fc
      "Add dotnet webapit template..."

  [3] 51e4aa23-8eb1-410a-9daf-d7ff9223ddda
      "Single commit in git..."
```

## What It Does

**Visualization:**

1. Reads `history-{sessionId}.json`, `tools-{sessionId}.json`, and `agents-{name}-{sessionId}.json` from `.copilot-conversation/data/`
2. Merges all events chronologically
3. Generates a Mermaid sequence diagram showing:
   - **User → GH Copilot**: conversation prompts
   - **GH Copilot → Tool Use**: tool calls and responses
   - **GH Copilot → Sub-Agent**: sub-agent lifecycle
4. Writes `conv-{sessionId}.md` to `.copilot-conversation/conversations/`

**Deletion:**

- Removes all session files: `history-{id}.json`, `tools-{id}.json`, `debug-{id}.log`, `conv-{id}.json`, `conv-{id}.md`, and any `agents-*-{id}.json` files
- When no session ID is provided, Copilot uses ask_questions to help you select which session to delete
- Supports deleting individual sessions or all sessions at once

## When To Use

**Visualization:**

- Manually regenerate a diagram after viewing or editing session data
- Visualize older sessions that weren't auto-generated
- The `sessionEnd` hook runs this automatically — use this skill if you need to re-run it

**Deletion:**

- Clean up old or unwanted conversation sessions and their associated files
- Remove test conversations to keep the conversation history clean
- Delete all sessions at once to start fresh

## Output Format

The generated `.copilot-conversation/conversations/conv-{sessionId}.md` contains:

- Session metadata (start/end time, status)
- Mermaid sequence diagram
- Tool execution metrics table
