# claude-learn-setup: first-use bootstrap (optional)

Run this check the first time `claude-learn` is invoked in a repo. Already wired -> skip silently, continue with the requested leaf.

## Detection

Setup is needed when either holds:

1. `.conversations-claude/hooks/claude-hook.sh` does not exist in the repo root
2. `.claude/settings.json` has no hook entry containing `claude-hook.sh`

```bash
test -f .conversations-claude/hooks/claude-hook.sh && grep -q "claude-hook.sh" .claude/settings.json && echo WIRED || echo SETUP-NEEDED
```

## Setup steps

### 1. Install the hook scripts

Copy the bundled scripts from this skill into the repo root:

```bash
mkdir -p .conversations-claude/hooks
cp .claude/skills/claude-learn/scripts/hooks/* .conversations-claude/hooks/ 2>/dev/null \
  || cp ~/.claude/skills/claude-learn/scripts/hooks/* .conversations-claude/hooks/
```

The repo-local source only resolves when the skill was pulled into the repo; otherwise the global copy is the source.

The scripts must live at `.conversations-claude/hooks/`: `hook-utils.js` resolves the repo root as two directories above its own location, and `claude-hook.sh` hardcodes that path. Never run them from the skill folder.

### 2. Register the hooks in `.claude/settings.json`

Merge these entries into the existing `hooks` object. Create the file with an empty `permissions` block if it does not exist. Never overwrite entries already present.

```json
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "bash \"$CLAUDE_PROJECT_DIR/.conversations-claude/hooks/claude-hook.sh\" sessionStart",
          "timeout": 10
        }
      ]
    }
  ],
  "PreToolUse": [
    {
      "matcher": "Skill",
      "hooks": [
        {
          "type": "command",
          "command": "bash \"$CLAUDE_PROJECT_DIR/.conversations-claude/hooks/claude-hook.sh\" preToolUse",
          "timeout": 10
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Edit|Write|NotebookEdit|Bash|Agent",
      "hooks": [
        {
          "type": "command",
          "command": "bash \"$CLAUDE_PROJECT_DIR/.conversations-claude/hooks/claude-hook.sh\" postToolUse",
          "timeout": 10
        }
      ]
    }
  ],
  "SessionEnd": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "bash \"$CLAUDE_PROJECT_DIR/.conversations-claude/hooks/claude-hook.sh\" sessionEnd",
          "timeout": 30
        }
      ]
    }
  ]
}
```

The matchers mirror what `claude-hook.js` acts on: `preToolUse` captures Skill invocations only; `postToolUse` captures file edits, shell commands, and agent dispatches only.

### 3. Gitignore the data directories

```bash
grep -q "^\.conversations-claude/" .gitignore 2>/dev/null || printf '.conversations-claude/raw/\n.conversations-claude/state/\n.conversations-claude/analysis/\n' >> .gitignore
```

Hook scripts stay tracked; raw session data, state, and analysis output do not.

### 4. Verify

```bash
echo '{"session_id":"setup-check","tool_name":"Skill","tool_input":{"skill":"claude-learn","description":"setup check"}}' | bash .conversations-claude/hooks/claude-hook.sh preToolUse && tail -1 .conversations-claude/analysis/decisions.jsonl
```

Expect a JSON decision record with `"session":"setup-check"`. Then clear the test artifacts:

```bash
rm -f .conversations-claude/analysis/decisions.jsonl .conversations-claude/state/current-session.json .conversations-claude/raw/*.jsonl
```

Tell the user hooks take effect at the next session start (Claude Code snapshots hooks at startup).

## What the hooks produce

| Output | Written by | Contains |
| --- | --- | --- |
| `.conversations-claude/raw/{YYYY-MM-DD}.jsonl` | pre/post tool hooks | Edits, shell commands, agent dispatches, skill invocations |
| `.conversations-claude/analysis/decisions.jsonl` | preToolUse | Skill invocations with inferred category and reason |
| `.conversations-claude/analysis/{date}-{session}-learnings.md` | sessionEnd analyzer | Auto-generated session summary |
| `.conversations-claude/analysis/patterns.json` | sessionEnd analyzer | Cross-session pattern counts |
| `.conversations-claude/state/current-session.json` | sessionStart | Active session id (removed at session end) |

## Requirements

- Node.js on PATH (`node` or `node.exe`); the hook exits silently if absent
- Git Bash on Windows (hook commands invoke `bash`)
