# Copilot Conversation Visualization

Logs and visualizes GitHub Copilot conversations using event hooks.

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryTextColor':'#ffff00', 'primaryBorderColor':'#ffff00', 'textColor':'#ffff00'}}}%%
sequenceDiagram
    autonumber
    actor User as User
    participant Bot as GH Copilot

    Note over User,Bot: Conversation starts

    User->>Bot: Follow instructions in [describe-module.prompt.md](file:///d...
    Bot-->>User: Executed 9 actions: 6× readFile, 2× listDirectory, replaceString
    User->>Bot: ok but in the end repeat my original mermaid
    Bot-->>User: Executed: copilot_replaceString
    User->>Bot: Instead of Example Recording ... here is the prompt for the ...
    Bot-->>User: Executed: copilot_replaceString
    User->>Bot: you may enhance the prompt
    Bot-->>User: Executed: copilot_replaceString
    User->>Bot: I meant more like short explanation and the this was the pr...
    Bot-->>User: Executed: copilot_replaceString

    Note over User,Bot: Conversation ends
```

## Manual Visualization

```powershell
cd .copilot-conversation
npm run visualize                                       # all sessions → conversations/ (level 1)
node ./scripts/visualize.mjs --session <id>             # specific session → conversations/ (level 1)
node ./scripts/visualize.mjs --session <id> --level 2   # specific session at level 2 (with tools)
```

## Structure

```
.copilot-conversation/
├── data/
│   ├── history-{id}.json
│   ├── tools-{id}.json
│   ├── conv-{id}.json
│   └── debug-{id}.log
├── conversations/   
│   └── conv-{id}.md
├── scripts/         
│   ├── consolidate.mjs
│   ├── visualize.mjs
│   ├── test.mjs
│   └── *hook_scripts*.ps1        
└── package.json
```

## Hook Flow

1. **sessionStart** — generates sessionId, creates `history-` and `tools-` JSON files
2. **userPromptSubmitted** — appends user prompt to `history-{sessionId}.json`
3. **preToolUse** — appends pre-call entry to `tools-{sessionId}.json`
4. **postToolUse** — appends post-call entry with result to `tools-{sessionId}.json`
5. **subagentStarted/Stopped** — creates/updates `agents-{name}-{sessionId}.json`
6. **sessionEnd** — finalizes history, runs `scripts/visualize.mjs`, generates `conversations/conv-{sessionId}.md`

## Testing

```powershell
cd .copilot-conversation
npm test
```
