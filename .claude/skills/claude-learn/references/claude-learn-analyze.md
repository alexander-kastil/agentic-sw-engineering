# claude-learn-analyze — Conversation Session Analysis

## When to Use

- After a work session to capture what happened and extract learnings
- When you want to review `.conversation/data/` for patterns
- When a session revealed skill gaps, routing mistakes, or missing handoffs
- Periodically to cross-reference accumulated sessions for recurring issues

## Prerequisites

- `.conversation/data/` must contain session files (history, tools, agents, debug)
- Session files follow the naming pattern: `{type}-{sessionId}.json`

> **Disambiguation:** `VSCODE_TARGET_SESSION_LOG` in the system prompt is a VS Code internal debug log path — it is NOT the session history. Always read from `.conversation/data/{type}-{sessionId}.json` in the repo root.

## Input Files

| File pattern | Contains |
| --- | --- |
| `history-{id}.json` | User prompts, timestamps, events |
| `tools-{id}.json` | Tool calls made during the session |
| `agents-main-{id}.json` | Main agent data (model, mode, skills loaded) |
| `agents-subagent-{id}.json` | Sub-agent invocations |
| `debug-{id}.log` | Debug logs |

## Step-by-Step Workflow

### 1. Identify Session(s) to Analyze

- **Current session**: Use the session ID from the conversation context
- **Recent sessions**: Sort history files by `LastWriteTime`, take the last N
- **All sessions**: Process everything in `.conversation/data/`

### 2. Reconstruct the Session Timeline

Read `history-{id}.json` to get:
- All user prompts in order
- Timestamps (for pacing analysis)
- Session start/end events

Read `tools-{id}.json` to get:
- Which tools were called and how often
- Tool call sequences (same tool called repeatedly = retry)
- File paths touched (which parts of the codebase were active)

### 3. Analyze for Patterns

| Signal | What it means | Action |
| --- | --- | --- |
| Same file edited multiple times | Iterative correction — possible skill gap | Note which skill should have gotten it right the first time |
| Tool retry (same tool, same-ish args) | Failure then retry — document the fix | Add troubleshooting entry or skill improvement |
| User correction ("you looked at the wrong files") | Agent went to wrong location | Update skill with correct file paths |
| Previous-customer terms or fields appear in a new tenant's output | Tenant/domain drift | Compare the active tenant's docs/specs against inherited wording and add a terminology/data-shape lock step |
| No docs handoff after editing `docs/` | Missing handoff convention | Verify docs handoff is wired into the active skill |
| Agent spawned for trivial task | Over-delegation | Simplify the workflow |
| Manual edits after skill output | Skill output was incomplete | Update the skill with the missing step |
| User frustration ("the heck", "do what I said") | Agent resisted or over-cautioned | Note the pattern for future preference learning |

### 4. Check for Missing Handoffs

For each docs file touched during the session:
- Was a docs handoff block produced? If not, flag it.
- For each agent file touched: was the owning agent notified? If not, flag it.
- For cross-layer work (.NET ↔ MAF): were handoff triggers followed?

### 5. Produce Output

Write structured findings. Two output modes:

**Inline summary** (default — output in chat):
```
## Session Analysis: {sessionId}

### Timeline
- {timestamp}: {prompt summary} → {what agent did}

### Patterns Found
1. {pattern}: {description} → {proposed action}

### Missing Handoffs
- {file}: edited by {agent} without docs handoff

### Skill Gaps
- {skill}: {what it missed} → {proposed update}

### Proposed Improvements
- [ ] {concrete action item}
```

**Persisted summary** (when user asks to save):
Write to `.conversation/analysis/{sessionId}-learnings.md`

### 6. Update patterns.json (Optional)

If the user asks to persist patterns:

```json
{
  "patterns": {
    "missing-docs-handoff": {
      "count": 3,
      "sessions": ["abc123", "def456", "ghi789"],
      "action": "Verify docs handoff convention is in all master skills",
      "status": "addressed"
    }
  }
}
```

## Cross-Session Analysis

When analyzing multiple sessions:

1. Group findings by pattern type
2. Count occurrences across sessions
3. If a pattern appears 3+ times, it's systemic — propose a skill or convention update
4. If a pattern was addressed (skill updated) but recurs, the fix didn't work — escalate

## What This Skill Does NOT Do

- Does not write or update `docs/` files directly — that's `claude-learn-distribute` → docs agent
- Does not modify skill files directly — proposes changes, user approves
- Does not invent session data — if `.conversation/data/` is empty, report that
