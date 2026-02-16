# GitHub Copilot Hooks

GitHub Copilot hooks allow you to extend and customize agent behavior by executing custom shell commands at key points during agent execution. Hooks run in response to specific events in the agent lifecycle, enabling you to implement logging, validation, notifications, and custom integrations without modifying the agent code.

>Note: As of 08 Feb 2026 hooks are only available in [VS Code Insiders](https://code.visualstudio.com/insiders/).

## Hook Types

| Hook | Trigger | Description |
|------|---------|-------------|
| Session Start | When a new agent session begins or when resuming an existing session | Execute initialization logic, setup logging, or prepare your environment before the agent starts |
| User Prompt Submit | When the user submits a prompt to the agent | Log user requests, validate input, or perform pre-processing before the agent processes the prompt |
| Pre-Tool Use | Before the agent uses any tool | Validate tool parameters, log tool invocations, or conditionally block tool execution |
| Post-Tool Use | After a tool completes execution successfully | Log results, update metrics, trigger notifications, or perform cleanup operations |
| Subagent Start | When a subagent is started | Track subagent lifecycle and manage resources |
| Subagent Stop | When a subagent stops | Log subagent completion or clean up state |
| Stop | When the agent stops | Finalize logs, clean up resources, or trigger completion workflows |

## Use Cases

- Audit and Monitoring: Log all agent activities with timestamps, user information, and executed actions for compliance and debugging.
- Custom Validations: Validate tool parameters before execution or enforce security policies before the agent proceeds.
- Integration: Trigger external systems, send notifications to Slack or email, or integrate with CI/CD pipelines based on agent events.
- Performance Tracking: Measure execution time, monitor tool usage, and collect metrics for optimization.
- Conditional Execution: Block dangerous operations or prevent tools from running in certain contexts using hook validation.

## Copilot Conversation Tracker

The Copilot Conversation Tracker automatically records all agent activities—user prompts, tool calls, subagent lifecycle events—into a structured JSON format stored in [.copilot-conversation](/.copilot-conversation/). This enables full conversation history, detailed execution analysis, and automated visualization of agent behavior without requiring manual logging code.

### How It Works

Hooks fire at key agent lifecycle events, with each hook executing a script that captures relevant data. When the conversation starts, the session-start hook generates a unique session ID and creates baseline JSON files. As the agent executes, hooks log user submissions, record pre/post tool execution details, and monitor subagent lifecycle. Finally, the session-stop hook finalizes the session and runs [visualize.mjs](/.copilot-conversation/scripts/visualize.mjs) to generate a markdown diagram of the entire conversation flow.

### Hook Registration

Hooks are registered in a hooks.json configuration file, which maps each lifecycle event to one or more scripts. Each hook entry specifies the event type (sessionStart, userPromptSubmitted, preToolUse, etc.), the command to execute, working directory, and timeout. The configuration ensures scripts run in sequence without blocking the agent, with a minimum timeout required for the final sessionEnd hook to complete visualization.

### Conversation Flow

The tracker captures the full conversation lifecycle as a sequence of events leading from session initialization through prompt submission, tool execution, and eventual finalization:

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant GHCopilot as "GH Copilot"

    Note over User,GHCopilot: Conversation starts
    Note over User,GHCopilot: sessionStart: Create session ID & JSON files

    User->>GHCopilot: Navigate to src/ and execute: dotnet new webapit -n copilot-...
    Note over User,GHCopilot: userPromptSubmitted: Log prompt to history
    GHCopilot->>GHCopilot: preToolUse: Record run_in_terminal
    GHCopilot-->>GHCopilot: postToolUse: Log command output
    GHCopilot->>GHCopilot: preToolUse: Record readFile calls
    GHCopilot-->>GHCopilot: postToolUse: Log file contents
    GHCopilot-->>User: Executed 30 actions: 8× run in terminal, 4× readFile, 3× replaceString

    User->>GHCopilot: while the terminal runs use chrome mcp
    Note over User,GHCopilot: Multiple preToolUse/postToolUse events
    GHCopilot-->>User: Executed 13 actions: 3× readFile, 3× chrome snapshot, 2× new page

    User->>GHCopilot: More questions and refinements
    GHCopilot-->>User: Multiple iterations with tool tracking

    Note over User,GHCopilot: Conversation ends
    Note over User,GHCopilot: sessionEnd: Finalize history & run visualize.mjs
```

The visualization generates a Mermaid sequence diagram showing the complete interaction pattern, making it easy to understand tool usage patterns, identify bottlenecks, and replay conversation flows for debugging or documentation purposes.

### Building a .NET Instructions API with Scalar UI

This example shows how hooks track a comprehensive development workflow—from project scaffolding through code refactoring, dependency injection setup, API documentation integration, build validation, and browser-based verification of a running .NET service.

Here's the prompt that generated this recorded conversation:

```
Navigate to src/ and execute: dotnet new webapi -n copilot-api
Navigate to src/copilot-api and execute: dotnet new .gitignore
In src/copilot-api i want you to apply my coding conventions for .NET and then remove all weather (controller) related data. 
Next implement a InstructionsController with model name, description as a standalone controller and register it. 
Use Microsoft Learn MCP for planning.
Provide Scalar UI in the root. 
Build run and fix all errors. while keeping the .NET app running use your Chrome Dev Tools MCP visit the HTTP URL 
and port it is configured to run on an check the result. no need to use HTTPS
```

The hooks recorded every tool call, file modification, terminal command, and browser interaction during this workflow:

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant GHCopilot as "GH Copilot"

    Note over User,GHCopilot: Conversation starts

    User->>GHCopilot: Navigate to src/ and execute: dotnet new webapit -n copilot-...
    GHCopilot-->>User: Executed 30 actions: 8× run in terminal, 4× readFile, 3× replaceString
    User->>GHCopilot: whilee the terminal runs use chrome mcp
    GHCopilot-->>User: Executed 13 actions: 3× readFile, 3× chrome-devtoo take snapshot, 2× chrome-devtoo new page
    User->>GHCopilot: questions. do this mermaids support making the tool call lay...
    GHCopilot-->>User: Executed 2 actions: get-syntax-docs-mermaid, readFile
    User->>GHCopilot: question 2. couldnt we asign more meaning to the tool call w...
    User->>GHCopilot: ok then wouldnt it make more sense to process the 3 json fil...
    GHCopilot-->>User: Executed 21 actions: 9× readFile, 7× replaceString, 2× listDirectory
    User->>GHCopilot: that is already great progress! my initial request was havin...
    GHCopilot-->>User: Executed 18 actions: 11× replaceString, 4× readFile, 3× run in terminal
    User->>GHCopilot: yes ... but i meant as a mermaid ... no need to have 1.5 ......
    GHCopilot-->>User: Executed 7 actions: 5× replaceString, run in terminal, readFile

    Note over User,GHCopilot: Conversation ends
```

## Key Topics Covered in This Section

- [Using hooks with GitHub Copilot agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/use-hooks)
- [Hooks configuration reference](https://docs.github.com/en/copilot/reference/hooks-configuration)
- [About GitHub Copilot hooks](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-hooks)