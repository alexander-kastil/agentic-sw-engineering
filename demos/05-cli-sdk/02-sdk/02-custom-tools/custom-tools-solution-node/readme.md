# Copilot SDK Demos: Worked Solution

The finished state of every program in [the topic guide](../readme.md), verified end to end against `@github/copilot-sdk` 1.0.14 and GitHub Copilot CLI 1.0.87.

Work through the guide and build the files yourself. Come here when a step does not behave, or to compare your version against one that runs.

## What is here

| File | Guide step | What it does |
|------|------------|--------------|
| `weather-agent.ts` | Steps 2 and 3 | Defines one `get_weather` tool and streams a single turn that calls it for two cities |
| `interactive-agent.ts` | Step 4 | The same tool behind a multi-turn prompt loop that survives Ctrl+C and end of input |
| `security-analyzer.ts` | Step 5 | Two tools, a system message, and a session scoped to custom tools only |

## Run it

```bash
npm install
npm run weather
npm run interactive
npm run security
```

`npm run typecheck` runs `tsc --noEmit` over all three. Do this before blaming the SDK: `tsx` executes TypeScript without typechecking it, so a type error in a tool handler stays invisible at runtime until the compiler sees it.

## Prerequisites

Node.js 20.19 or later (or 22.12 or later), and a signed-in Copilot CLI. The SDK bundles the CLI but not your credentials.

```bash
node --version
copilot --version
```

Run `copilot` and then `/login` once if you have never authenticated.

## The four things the guide's first draft got wrong

Each of these was found by running the code, not by reading it. The guide now covers all four, and they are the reason this folder exists.

| Symptom | Cause | Fix |
|---------|-------|-----|
| The agent answers "I can't access the weather API right now (permission denied)" | Every tool call goes through the session's permission gate, and a session with no handler denies it | `skipPermission: true` on a tool whose handler only computes, or an `onPermissionRequest` handler on the session |
| `tsc` reports `TS2322: Type 'unknown' is not assignable` on a handler | `defineTool` defaults its type parameter to `unknown`, so a destructured parameter has no type | Annotate the parameter, or pass the shape as `defineTool<{ city: string }>` |
| The prompt loop dies with `ERR_USE_AFTER_CLOSE: readline was closed` | End of input closes the interface while a turn is still awaiting, and the loop then prompts again | Track the `close` event and leave the loop instead of re-prompting |
| The analyzer says the environment denied reading `app.js` and never calls your tool | The session still exposes the built-in file tools, and the model prefers them over a custom tool with a similar job | `availableTools: ["custom:*"]` so only your own tools are reachable |

## Model names

`gpt-5-mini` is what these files use and what was verified. Run `/model` in the CLI, or `client.listModels()` in code, to see what your account and organization policy allow.
