# claude-analyze: session reflection (task 1)

Extract what a session taught, persist it to the repo's lessons file, propose skill/agent/doc updates. **Does not write skills, agents, docs or `CLAUDE.md`**: that is [claude-learn-distribute](claude-learn-distribute.md).

## When to use

- After a work session, to capture what happened and extract learnings
- When reviewing native JSONL or hook-captured `raw/` data for patterns
- When a session revealed skill gaps, routing mistakes, or missing handoffs
- Periodically, to cross-reference accumulated sessions for recurring issues

## Source

**Live session is the default case: you already hold it in context. Reflect directly, do not re-parse JSONL.** Parse JSONL only for a past session you were not part of.

| Source | Location | Contains |
| --- | --- | --- |
| Native JSONL (primary) | `~/.claude/projects/<project-slug>/{sessionId}.jsonl` | Full conversation: user prompts, assistant replies, `tool_use` blocks, cache metrics, git branch, entrypoint |
| Hook raw events (optional) | `.conversations-claude/raw/{YYYY-MM-DD}.jsonl` | Edits, shell commands, agent dispatches, skill invocations per day |
| Skill decisions | `.conversations-claude/analysis/decisions.jsonl` | Skill invocations with inferred category and routing reason |
| Session learnings | `.conversations-claude/analysis/{date}-{sessionId}-learnings.md` | Prior auto-generated summaries written at session end. Read before writing a new one; extend, never duplicate |
| Pattern history | `.conversations-claude/analysis/patterns.json` | Cross-session pattern counts |
| Active session id | `.conversations-claude/state/current-session.json` | Session id of the running session (removed at session end) |
| Legacy hook capture (read-only) | `.conversation/data/`, `.conversation/analysis/` | Pre-rename layout, still on disk in a few repos: per-session `history`/`tools`/`agents`/`debug` files plus `decisions.jsonl` and `delegations.jsonl`. Parse if present; never write there. A `.conversation/raw/` with no sibling `data/` or `analysis/` is a different harness, not this source |

> Everything under `.conversations-claude/` exists only where the session-tracking hooks are wired (see [claude-learn-setup](claude-learn-setup.md)). Hooks registered mid-session take effect at the next session start.

`<project-slug>` = the cwd with path separators replaced by dashes (e.g. `D--git-classes-myrepo`).

Hook-capture globs, either layout:

| Glob | Contains |
| --- | --- |
| `data/history-{sessionId}.json` | Prompt/response timeline |
| `data/tools-{sessionId}.json` | Tool calls with inputs |
| `data/agents-{agentName}-{sessionId}.json` | Subagent dispatches |
| `data/debug-{sessionId}.log` | Hook debug trace |
| `analysis/decisions.jsonl` | Skill invocations, inferred category and routing reason |
| `analysis/patterns.json` | Cross-session pattern counts |
| `analysis/{date}-{sessionId}-learnings.md` | Prior auto-generated summaries. Read before writing a new one; extend, never duplicate |

## Native JSONL format

One record per line:

| `type` | Key fields | Use for |
| --- | --- | --- |
| `user` | `message.content`, `timestamp`, `gitBranch` | Real user prompts: extract the actual text |
| `assistant` | `message.content[]` (text + `tool_use`), `message.usage` | Tool calls, replies, cache metrics |
| `ai-title` | `aiTitle` | Session topic (auto-generated) |
| `attachment` | `attachment.type` (`skill_listing`, `deferred_tools_delta`) | Skills loaded at session start |
| `queue-operation` | - | Session lifecycle; skip |
| `file-history-snapshot` | - | Pre-edit checkpoints; skip |

Tool calls are `{"type": "tool_use", "name": "Read", "input": {...}}` inside assistant messages; results return as `user` messages with content type `tool_result`.

## Procedure

### 1. Identify the session

- **Current session**: session ID from context (the scratchpad path segment), or from `.conversations-claude/state/current-session.json` where hooks are wired.
- **Recent**: sort `*.jsonl` in `~/.claude/projects/<project-slug>/` by mtime, take last N.
- **By topic**: match the `ai-title` record near the top of each file.

### 2. Reconstruct the timeline

1. Collect every `type: "user"` record whose `message.content` is a non-system string: those are the real user prompts, in order.
2. Collect every `type: "assistant"` record; extract text and `tool_use` blocks from `message.content[]`.
3. Note `gitBranch` on the first user message; flag a mid-session change.
4. Check the `entrypoint` field: `claude-vscode` versus CLI changes the context the session ran in.

Shape: `{turn} | {user intent} | {what was done}`.

### 3. Supplement with hook data

If `.conversations-claude/raw/{date}.jsonl` covers the session, cross-reference tool events for exit codes and touched files. For pre-migration sessions, fall back to `.conversation/data/tools-{sessionId}.json` and `debug-{sessionId}.log`.

Read `.conversations-claude/analysis/decisions.jsonl` (legacy: `.conversation/analysis/decisions.jsonl`) filtered by session: which skills were invoked, in what order, with what inferred category.

### 4. Analyze for patterns

| Signal | Means | Action |
| --- | --- | --- |
| Same file edited repeatedly, or a lint/quality fix applied after the write | Quality check not run at author time; iterative correction, so possible skill gap | Run the check before finishing the edit; note which skill should have got it right first |
| Invented feature names, versions, settings in authored content | Content not grounded in the source anchors | Constrain authoring to the supplied sources and brief |
| Subject-matter code work done on the main thread | Under-delegation | Route to the agent owning that surface |
| Agent spawned for a trivial one-liner | Over-delegation | Do it inline; simplify the workflow |
| User correction mid-session ("no", "do X instead") | Wrong direction, or a preference not yet known | Capture it as a rule in the lessons file; update the skill with the correct paths or routing |
| Large cut-only compression sweep across many files | Correct deletions still drop facts that occurred exactly once inside an otherwise redundant paragraph; a diff cannot show a fact that is now nowhere | Make every agent report the facts it dropped; after the sweep check near-empty files, emptied headings, and each reported drop |
| Skill invoked via the Skill tool errors on `disable-model-invocation` | A user-invocable master set `disable-model-invocation: true` | Remove it or set it false |
| Same tool retried 3+ times with edited args | Wrong tool, wrong path, or an unstated precondition | Record the precondition as a rule; fix the skill or agent that should have supplied it; add a troubleshooting entry |
| Skill ran, then its output hand-corrected over the next turns | Incomplete skill output, covers the happy path only | Extend that skill with the case it missed; name the skill in the lessons entry |
| Manual cleanup after a skill-like action (leftover files, half-finished rename, index not updated) | Skill stopped short of closing its own loop | Add the close-out step to the skill |
| `cache_read_input_tokens` very low | Context not warmed: prompt structure issue | Suggest a prompt-caching improvement |
| Skill category mismatch (from `decisions.jsonl`) | Wrong routing | Update the skill's trigger keywords |
| `docs/` edited with no docs handoff produced | Missing convention | Verify the handoff is wired into the active skill |

### 5. Check for missing handoffs

- For each `docs/` file touched (Read or Write/Edit tool calls): was a docs handoff block produced in the assistant output? If not, flag it.
- For each `.claude/agents/` file touched: was the owning agent notified?

### 6. Produce output

Inline summary (default):

```
## Session Analysis: {aiTitle} ({sessionId})

### Timeline
- {turn}: {user intent} -> {what was done}

### Patterns Found
1. {pattern}: {description} -> {proposed action}

### Missing Handoffs
- {file}: edited without docs handoff

### Skill / Doc Gaps
- {skill or doc}: {what it missed} -> {proposed update}

### Proposed Improvements
- [ ] {concrete action item}
```

Persisted learnings: append to the repo's lessons file (commonly `tasks/lessons.md`); create it if missing. One entry per learning:

```markdown
## {short title}

**Pattern:** {what happened}
**Rule:** {what to do next time so it does not recur}
```

When the user asks for a persisted session summary instead, write it to `.conversations-claude/analysis/{sessionId}-learnings.md`.

### 7. Update patterns.json (optional)

Only when the user asks to persist patterns:

```json
{
  "patterns": {
    "missing-docs-handoff": {
      "count": 3,
      "sessions": ["abc123"],
      "action": "Verify handoff convention is in all master skills",
      "status": "addressed"
    }
  }
}
```

### 8. Hand off

Every skill, agent, doc or `CLAUDE.md` gap goes to [claude-learn-distribute](claude-learn-distribute.md) as a concrete change. Do not write those files here.

Distribution surfaces, in preference order: `.claude/agents/`, `.claude/skills/`, `CLAUDE.md`, MCP tool config. Prefer an executable surface over prose in `docs/`: a doc is read at best, a skill or agent runs.

## Cross-session analysis

Read all `*.jsonl` in the project folder, index by `ai-title`, group findings by pattern type. **3+ occurrences = systemic** -> propose a skill or `CLAUDE.md` convention. **A pattern that recurs after being addressed = the fix did not hold** -> escalate.

## Not this leaf's job

- Writing skill/agent/doc/`CLAUDE.md` files. Gaps are proposed here and applied by `claude-learn-distribute`; skill files are proposed, the user approves.
- Inventing session data. If the native JSONL, `.conversations-claude/raw/` and legacy `.conversation/data/` are all empty and the session is not in context, report that.
- Writing `analysis/patterns.json` or `analysis/{date}-{session}-learnings.md` unless the user asks to persist. Those are hook-owned outputs, written by the sessionEnd analyzer.
