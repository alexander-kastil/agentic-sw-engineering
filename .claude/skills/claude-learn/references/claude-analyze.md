# claude-analyze — Conversation Session Analysis

Reflect on a session and turn it into durable knowledge. This leaf reads the session record, extracts patterns and mistakes, and writes learnings to the repo's lessons file. It proposes skill/agent/doc updates but does not write them itself; that is the distribute leaf.

## Data Source

| Source | Location | Contains |
| --- | --- | --- |
| **Native JSONL** (primary) | `~/.claude/projects/<project-slug>/{sessionId}.jsonl` | Full conversation: user prompts, assistant replies, tool_use blocks, cache metrics, git branch, entrypoint |
| **Hook capture** (optional) | `.conversations-claude/raw/{date}.jsonl` and `.conversations-claude/analysis/` | Present only when session-tracking hooks are wired (see `claude-learn-setup`) |

The `<project-slug>` is the current working directory with path separators replaced by dashes (for example `D--git-classes-myrepo`). When claude-learn runs on the current, live session (the common case), you already hold the session in context; reflect directly rather than re-parsing the JSONL. Parse the JSONL when reviewing a past session you were not part of.

## Native JSONL Format

Each line in `{sessionId}.jsonl` is one of:

| `type` | Key fields | Use for |
| --- | --- | --- |
| `user` | `message.content`, `timestamp`, `gitBranch` | User prompts — extract the actual text |
| `assistant` | `message.content[]` (text + tool_use blocks), `message.usage` | Tool calls, responses, cache metrics |
| `ai-title` | `aiTitle` | Session topic summary (auto-generated) |
| `attachment` | `attachment.type` (`skill_listing`, `deferred_tools_delta`) | Skills loaded at session start |
| `queue-operation` | — | Session lifecycle (skip for analysis) |
| `file-history-snapshot` | — | Pre-edit checkpoints (skip for analysis) |

Tool use blocks inside assistant messages look like `{"type": "tool_use", "name": "Read", "input": {...}}`. Tool results come back as user messages with content type `tool_result`.

## Step-by-Step Workflow

### 1. Identify Session to Analyze

- **Current session**: use the session ID from the conversation context (the scratchpad path segment is the session ID).
- **Recent sessions**: sort `*.jsonl` in `~/.claude/projects/<project-slug>/` by modified time, take last N.
- **By topic**: use the `ai-title` record near the top of each JSONL.

### 2. Reconstruct the Timeline

Collect the real `user` prompts in order, then the `assistant` text and tool_use blocks. Note the `gitBranch` on the first user message and flag if it changes mid-session. Build a timeline: `{turn} | {user intent} | {what was done}`.

### 3. Analyze for Patterns

| Signal | What it means | Action |
| --- | --- | --- |
| Same file edited repeatedly, or a quality/lint fix applied after a file was written | The quality check was not run at author time | Run the check before finishing the edit |
| `git mv` fails with Windows "Permission denied" on a folder | Build artifacts (for example a `.NET` project's `bin`/`obj` DLLs) are locked by a language server or an active build | Clear the gitignored `bin`/`obj` and use atomic clear-and-rename in one command; do not mass-kill dev processes |
| A skill invoked via the Skill tool errors on `disable-model-invocation` | A user-invocable master skill set `disable-model-invocation: true` | Remove it or set it false |
| Invented feature names, versions, or settings in authored content | Content not grounded in the source anchors | Constrain authoring to the provided sources and brief |
| Subject-matter code work done on the main thread | Under-delegation | Route to the subagent that owns the surface |
| Agent spawned for a trivial one-liner | Over-delegation | Do it inline |
| User correction mid-session ("no", "do X instead") | Wrong direction or a preference not yet known | Capture the preference as a rule in the lessons file |

### 4. Produce Output

**Inline summary** (default):
```
## Session Analysis: {aiTitle} ({sessionId})

### Timeline
- {turn}: {user intent} -> {what was done}

### Patterns Found
1. {pattern}: {description} -> {proposed action}

### Skill / Doc Gaps
- {skill or doc}: {what it missed} -> {proposed update}

### Proposed Improvements
- [ ] {concrete action item}
```

**Persisted learnings**: append to the repo's lessons file (commonly `tasks/lessons.md`). Create the file if it does not exist. Each entry captures the pattern, then a rule that prevents recurrence.

```markdown
## {short title}

**Pattern:** {what happened}
**Rule:** {what to do next time so it does not recur}
```

### 5. Hand Off

For every skill, agent, doc, or `CLAUDE.md` gap the analysis found, hand the concrete change to [`claude-learn-distribute`](claude-learn-distribute.md). Do not write those files from this leaf.

## Cross-Session Analysis

Read all `*.jsonl` in the native project folder, index them by `ai-title`, and group findings by pattern. If a pattern appears 3+ times it is systemic: propose a skill or `CLAUDE.md` convention update. If a pattern was addressed but recurs, the fix did not hold: escalate.

## What This Skill Does NOT Do

- Does not write skill, agent, doc, or `CLAUDE.md` files directly — that is `claude-learn-distribute`.
- Does not invent session data — if the native JSONL is empty and the session is not in context, report that.
