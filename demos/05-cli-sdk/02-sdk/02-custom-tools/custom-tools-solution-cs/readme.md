# Copilot SDK Demos: Worked Solution (C#)

The finished state of every program in [the topic guide](../readme.md), verified end to end against `GitHub.Copilot.SDK` 1.0.14 and GitHub Copilot CLI 1.0.85.

Work through the guide and build the projects yourself. Come here when a step does not behave, or to compare your version against one that runs.

## What is here

| Project | Guide step | What it does |
|---------|------------|--------------|
| `weather-agent/` | Steps 2 and 3 | Defines one `get_weather` tool and streams a single turn that calls it for two cities |
| `interactive-agent/` | Step 4 | The same tool behind a multi-turn prompt loop that survives Ctrl+C and end of input |
| `security-analyzer/` | Step 5 | Two tools, a system message, and a session scoped to custom tools only |

Each project is a standalone console app with its own `.csproj`. `custom-tools-solution-cs.slnx` groups all three so an IDE opens them together; the CLI does not need it.

## Run it

```bash
dotnet build
dotnet run --project weather-agent
dotnet run --project interactive-agent
dotnet run --project security-analyzer
```

## Prerequisites

.NET 10 SDK, and a signed-in Copilot CLI. `GitHub.Copilot.SDK` bundles the CLI runtime, so a separate install is optional; run `copilot` once and `/login`, or set `GITHUB_TOKEN` for an unattended run.

```bash
dotnet --version
copilot --version
```

## The three things the TypeScript guide's fixes look like in C#

| Symptom | Cause | Fix |
|---------|-------|-----|
| The agent answers that it cannot access the weather API (permission denied) | Every tool call goes through the session's permission gate, and a session with no handler denies it | `CopilotToolOptions.SkipPermission = true` on a tool whose handler only computes, or `OnPermissionRequest` on the session |
| The interactive loop hangs waiting for input instead of exiting after piped input runs out | `Console.ReadLine()` returns `null` at end of input rather than throwing | Check for `null` in the `while` condition and let the loop end instead of looping on a closed stream |
| The analyzer reports that the environment denied reading `app.js` and never calls your tool | The session still exposes the built-in file tools, and the model prefers them over a custom tool with a similar job | `AvailableTools = new ToolSet().AddCustom("*")` so only your own tools are reachable |

There is no equivalent of TypeScript's `TS2322: Type 'unknown' is not assignable` defect here: `CopilotTool.DefineTool` infers each parameter's type directly from the C# lambda signature, so a handler with the wrong shape is a compile error at the call site rather than a runtime one.

## Model names

`gpt-5-mini` is what these projects use and what was verified. Run `/model` in the CLI, or `client.ListModelsAsync()` in code, to see what your account and organization policy allow.
