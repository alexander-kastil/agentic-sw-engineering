---
name: Summarize Copilot Conversation
description: Instructs Copilot to summarize a conversation based on the provided session data, including user prompts and tool usage and context window. 
---
You are summarizing a GitHub Copilot chat session so it can be resumed in a new chat. Produce a markdown file named sessionId.md.

Requirements
- Use clear, compact markdown with ASCII characters only.
- Do not include speculation. Only include facts in the session data.
- Filter out activities that resulted in errors or were later undone. If they are relevant, mention them only as brief exclusions.
- Preserve the sequence of user prompts and assistant responses at a high level.
- Include the full context window summary (system, developer, repo instructions, files opened, selections, environment).
- Include all tool usage with timestamps if available, inputs, and outputs summarized.
- Capture all decisions, constraints, and open questions.
- If data is missing, state "Unknown".

Output format
# Session Summary

## Session Metadata
- Session ID: {{sessionId}}
- Date: {{date}}
- Workspace: {{workspacePath}}
- Branch: {{gitBranch}}
- Model: {{modelName}}

## Context Window
### System Instructions
<summary>

### Developer Instructions
<summary>

### Repo Instructions
<summary>

### Environment
- OS: <value>
- Terminals: <summary>
- Open files: <summary>
- Selections: <summary>

## Conversation Flow
1. User: <prompt>
	Assistant: <response summary>
2. User: <prompt>
	Assistant: <response summary>

## Tool Usage
- <timestamp> <toolName>
  - Input: <summary>
  - Output: <summary>

## Artifacts and File Changes
- Created: <files>
- Updated: <files>
- Deleted: <files>

## Decisions and Constraints
- <decision or constraint>

## Open Questions / Follow-ups
- <question>

## Next Steps
- <action>