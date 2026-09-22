# Multi-Agent System: Worked Solution

The finished state of every program in [the topic guide](../readme.md), built and run against `@github/copilot-sdk` 1.0.14 and GitHub Copilot CLI 1.0.87. What was executed and what was not is listed below; do not read "verified" as covering the whole folder.

Build the files yourself as you read the guide. Come here when a step does not behave, or to compare your version against one that runs.

## What is here

| File | Guide step | What it does |
|------|------------|--------------|
| `coordinator.ts` | Steps 2 and 3 | Three specialists in three sessions, driven in sequence by your own code |
| `specialists.ts` | Step 4 | The same specialists as `customAgents` in one session, selected per turn over RPC |
| `fleet.ts` | Step 5 | The built-in parallel orchestration through `session.rpc.fleet.start` |
| `factory-probe.ts` | Step 6 | Shows where `defineFactory` can and cannot be used |

## Run it

```bash
npm install
npm run coordinator
npm run specialists
npm run fleet
npm run factory-probe
```

`npm run typecheck` runs `tsc --noEmit` over all four. Do this before blaming the SDK: `tsx` executes TypeScript without typechecking it, so a type error in a tool handler or a factory body stays invisible at runtime until the compiler sees it.

`coordinator.ts` prints three labelled sections, one per specialist, and the third one reviews what the second one wrote:

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

`fleet.ts` prints one `--- assistant ---` block per subagent report plus the merged table, so its output is long and interleaved. That is what parallel orchestration looks like from the outside.

## Prerequisites

Node.js 20.19 or later (or 22.12 or later), and a signed-in Copilot CLI. The SDK bundles its own CLI runtime but not your credentials.

```bash
node --version
copilot --version
```

Run `copilot` and then `/login` once if you have never authenticated.

The three SDK programs need only the SDK. Step 5 of the guide also runs `copilot --fleet` directly, and that needs a working `copilot` on your PATH. The two are independent: the SDK launches the runtime it ships with, so a broken launcher on PATH does not stop `npm run fleet`, and a working launcher does not prove the SDK install is good.

## What running this taught

Each row was found by executing the code, not by reading the types.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `session.factory.run(handle)` rejects with `Agent factories are not available for this session` | A `defineFactory` handle is registered only by `joinSession({ factories })` from `@github/copilot-sdk/extension`, and Agent Factories are additionally gated per account | Orchestrate from your own code or through `session.rpc.fleet.start`; reach for a factory only from a CLI extension on an account that has the surface enabled |
| `tsc` reports `TS2322: Type 'unknown[]' is not assignable to type 'JsonValue'` on `ctx.step` | `ctx.agent` resolves to `unknown`, so `ctx.parallel` hands back `Array<unknown \| null>` and a journaled step cannot serialize it | Narrow each result before journaling it, rather than casting the array |
| The fleet result you kept is one subagent's report rather than the merged answer | A fleet turn emits many `assistant.message` events, one per subagent plus the coordinator's own | Subscribe with `session.on` instead of relying on a single return value |

## What was verified, and what was not

Every row below says which of three things happened: Verified means it was executed and the result observed, Preconditions verified means the mechanism was confirmed but the exact printed form was not run, and Not executed names the blocker.

| Claim | Status |
|-------|--------|
| `npm run typecheck` clean across all four files | Verified |
| `coordinator.ts` end to end: three sessions, the researcher, builder and reviewer handoff, exit 0 | Verified with real model calls |
| The reviewer genuinely fails the draft it is handed | Verified: it returned `VERDICT: FAIL` and named the offending bullets |
| `specialists.ts` end to end: `agent.list`, `agent.getCurrent`, `agent.select`, two turns on one session | Verified with real model calls |
| `fleet.ts`: `session.rpc.fleet.start({ wait: true })` resolves and the merged table arrives | Verified with real model calls |
| `factory-probe.ts`: the factory run is rejected | Verified; the rejection is the expected result here, not a workaround for a broken program |
| `copilot --fleet -p "..." --allow-all-tools --model gpt-5-mini`, exactly as the guide prints it | Verified: run through the bare `copilot` launcher in this folder, 1m46s, one subagent per file, merged table returned |
| `--fleet` is documented by the CLI itself | Verified: `copilot --help` with stdout redirected to a file emitted 13527 bytes including the `--fleet` entry, byte-identical to the 1.0.87 bundle's own help |
| `/fleet` from inside an interactive session | Preconditions verified: `/fleet` is in the CLI's slash-command table and `copilot -p "/fleet ..."` is accepted and answers; no interactive TTY session was driven |
| `defineFactory` registered through `joinSession({ factories })` in a CLI extension | Not executed: Agent Factories are off for this account (`agent_factories: false` in the session init), so no `run_factory` tool reaches the model |
| Step 1 of the guide, as the two printed commands | Preconditions verified: `package.json` was written with those exact pins and `npm install` ran clean, but `npm init -y --init-type module` followed by the `npm install` line was not executed in that form |

## Model names

`gpt-5-mini` is what these files use and what was verified. Run `/model` in the CLI, or `client.listModels()` in code, to see what your account and organization policy allow.
