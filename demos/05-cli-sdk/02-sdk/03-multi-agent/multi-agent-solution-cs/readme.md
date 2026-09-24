# Multi-Agent System: C# Port

The C# port of [the finished Node.js solution](../multi-agent-solution-node/), built and run against `GitHub.Copilot.SDK` 1.0.14 and GitHub Copilot CLI 1.0.85. Same [topic guide](../readme.md), same prompts, same model. What was executed and what was not is listed below; do not read "verified" as covering the whole folder.

Unlike the flat Node.js layout, each program here is its own console project so `dotnet run --project <name>` works standalone. A `.slnx` ties the four together for `dotnet build`.

## What is here

| Project | Guide step | What it does |
|---------|------------|---------------|
| `coordinator/` | Steps 2 and 3 | Three specialists in three sessions, driven in sequence by your own code |
| `specialists/` | Step 4 | The same specialists as `CustomAgents` in one session, selected per turn over RPC |
| `fleet/` | Step 5 | The built-in parallel orchestration through `session.Rpc.Fleet.StartAsync` |
| `factory-probe/` | Step 6 | Shows where a factory can and cannot be run, and that the .NET SDK has no `defineFactory` equivalent at all |

## Run it

```bash
dotnet build multi-agent-solution-cs.slnx
dotnet run --project coordinator
dotnet run --project specialists
dotnet run --project fleet
dotnet run --project factory-probe
```

`coordinator` prints three labelled sections, one per specialist, and the third one reviews what the second one wrote:

```text
--- researcher ---
- a91f2c (cli): add --fleet to the prompt runner
...
--- builder ---
## Unreleased
...
--- reviewer ---
VERDICT: FAIL
```

`fleet` prints one `--- assistant ---` block per subagent report plus the merged table, so its output is long and interleaved. That is what parallel orchestration looks like from the outside.

## Prerequisites

.NET 10 SDK, and a signed-in GitHub Copilot account. `GitHub.Copilot.SDK` bundles the CLI runtime, so a separate install is optional; run `copilot` once and `/login`, or set `GITHUB_TOKEN` for an unattended run.

## What running this taught

Each row was found by executing the code, not by reading the types.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `error CS0122: 'FactoryRunRequest' is inaccessible` when probing the RPC types directly | The concrete request/result types (`FactoryRunRequest`, `SessionAgentListResult`, ...) are internal; only the typed API surface on `session.Rpc.*` is public | Call `session.Rpc.Agent`, `session.Rpc.Fleet`, `session.Rpc.Factory` directly instead of constructing the wire types yourself |
| `error GHCP001: 'GitHub.Copilot.Rpc.AgentApi' is for evaluation purposes only` on every build that touches `session.Rpc.Agent`, `.Fleet`, or `.Factory` | The whole `session.Rpc.*` surface that the Node.js SDK calls `session.rpc.*` is marked experimental in the .NET SDK 1.0.14 and the compiler makes that an error, not a warning | Add `<NoWarn>$(NoWarn);GHCP001</NoWarn>` to any `.csproj` that uses it (`specialists`, `fleet`, `factory-probe` here); `coordinator` never touches `session.Rpc` and needs no suppression |
| `error CS0266: Cannot implicitly convert IList<AIFunction> to ICollection<AIFunctionDeclaration>` when building a small helper for the three specialist sessions | `SessionConfig.Tools` is typed `ICollection<AIFunctionDeclaration>`, not `IList<AIFunction>` as the Node.js `tools` array might suggest | Type the shared helper's parameter as `ICollection<AIFunctionDeclaration>?` |
| Fleet's own prompt, translated literally as "audit coordinator.cs, specialists.cs and fleet.cs in this directory", finds nothing | The C# port splits each program into its own project folder, so the three files are not siblings the way the three `.ts` files are in the Node.js layout | Point `WorkingDirectory` at the solution root (`AppContext.BaseDirectory` walked up four levels from `bin/Debug/net10.0/`) and reference the files by their real relative paths, `coordinator/Program.cs` and so on |
| `session.Rpc.Factory.RunAsync(name, new { files = [...] }, ...)` throws `JsonTypeInfo metadata for type '<>f__AnonymousType0...' was not provided by TypeInfoResolver` instead of the expected rejection | The SDK serializes RPC payloads through its own source-generated `JsonSerializerContext` chain, which only knows the types it was generated against; an anonymous type was never one of them | Pre-serialize the args with `JsonSerializer.SerializeToElement(new { ... })` using the default reflection-based serializer and pass the resulting `JsonElement`, which the SDK's resolver chain does know how to forward |
| `session.Rpc.Factory.RunAsync("audit-pipeline", ...)` rejects with `Agent factories are not available for this session` | There is no `defineFactory`, no `ctx.parallel`/`ctx.pipeline`/`ctx.step` builder, and no `joinSession({ factories })` extension-host API anywhere in `GitHub.Copilot.SDK.dll` (confirmed by reflecting over every public and internal type in the net10.0 build); `session.Rpc.Factory` only invokes a factory some other process already registered by name, and Agent Factories are additionally gated per account | There is nothing to fix in the .NET SDK today: orchestrate from your own code or through `session.Rpc.Fleet.StartAsync`, and reach for a factory only from a CLI extension on an account that has the surface enabled |

## What was verified, and what was not

| Claim | Status |
|-------|--------|
| `dotnet build multi-agent-solution-cs.slnx` clean across all four projects, 0 warnings, 0 errors | Verified |
| `coordinator`: three sessions, the researcher, builder and reviewer handoff, exit 0 | Verified with real model calls |
| The reviewer genuinely fails the draft it is handed | Verified: it returned `VERDICT: FAIL` and named the bullets missing an area |
| `specialists`: `Rpc.Agent.ListAsync`, `GetCurrentAsync`, `SelectAsync`, two turns on one session | Verified with real model calls |
| `specialists`: reviewer verdict on the same shared transcript | Verified: it returned `VERDICT: PASS` this run |
| `fleet`: `session.Rpc.Fleet.StartAsync(wait: true)` resolves and the merged table arrives | Verified with real model calls: three subagents dispatched in parallel over a SQL todo list, table returned for all three files |
| `factory-probe`: the factory run is rejected with the same message the Node.js guide documents | Verified; the rejection is the expected result here, not a workaround for a broken program |
| No `defineFactory`-equivalent builder exists anywhere in `GitHub.Copilot.SDK.dll` 1.0.14 (net10.0) | Verified by reflecting over the assembly: no type named anything like `DefineFactory`, `FactoryBuilder`, `JoinSession`, or an extension-hosting host API exists; only the RPC-level `FactoryApi` (`RunAsync`, `ExecuteAsync`, `AgentAsync`, `PauseAsync`, `ResumeAsync`, ...) is present |

## Model names

`gpt-5-mini` is what these files use and what was verified. Run `/model` in the CLI, or `client.ListModelsAsync()` in code, to see what your account and organization policy allow.
