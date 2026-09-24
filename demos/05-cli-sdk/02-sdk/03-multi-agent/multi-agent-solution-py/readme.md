# Multi-Agent System: Worked Solution (Python)

The Python port of every program in [the topic guide](../readme.md), built and run against `github-copilot-sdk` 1.0.14 on Python 3.12. It carries the same prompts, model, tools and orchestration routes as the [Node.js solution](../multi-agent-solution-node/readme.md). What was executed and what was not is listed below; do not read "verified" as covering the whole folder.

Build the files yourself as you read the guide. Come here when a step does not behave, or to compare your version against one that runs.

## What is here

| File | Guide step | What it does |
|------|------------|--------------|
| `coordinator.py` | Steps 2 and 3 | Three specialists in three sessions, driven in sequence by your own code |
| `specialists.py` | Step 4 | The same specialists as `custom_agents` in one session, selected per turn over RPC |
| `fleet.py` | Step 5 | The built-in parallel orchestration through `session.rpc.fleet.start` |
| `factory_probe.py` | Step 6 | Shows that a Python program cannot define or register a factory |

## Run it

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -X utf8 coordinator.py
.venv\Scripts\python -X utf8 specialists.py
.venv\Scripts\python -X utf8 fleet.py
.venv\Scripts\python -X utf8 factory_probe.py
```

On macOS or Linux the interpreter is `.venv/bin/python` and `-X utf8` is harmless but not needed.

`coordinator.py` prints three labelled sections, one per specialist, and the third one reviews what the second one wrote:

```text
--- researcher ---
...
--- builder ---
## Unreleased
...
--- reviewer ---
VERDICT: FAIL
...
```

On the verified run the model separated each id from its summary with an em dash, so the reviewer flagged all four bullets for the em dash and for not naming their area.

`specialists.py` lists both agents, reports `researcher` as the starting agent, then switches to `reviewer` for the second turn:

```text
registered agents:
  researcher: Retrieves repository facts and reports them without commentary
  reviewer: Checks a draft against the house style and returns a verdict

selected at start: researcher

--- researcher ---
Found 3 merged changes since tag v2.1:

- a91f2c (cli): add --fleet to the prompt runner
...

selected for the next turn: reviewer

--- reviewer ---
VERDICT: PASS
```

`fleet.py` prints one `--- assistant ---` block per subagent report plus the merged table, so its output is long and interleaved. That is what parallel orchestration looks like from the outside. A run took about 1m25s and ended with:

```text
| File | Model string | SDK sessions created |
|------|--------------|----------------------|
| coordinator.py | "gpt-5-mini" | 3 |
| specialists.py | "gpt-5-mini" | 1 |
| fleet.py | "gpt-5-mini" | 2 |

fleet started: True
```

The session counts are the subagents' own reading of the code and vary between runs.

`factory_probe.py` prints:

```text
define_factory exported: False
session.rpc.factory.run available: True

session.rpc.factory.run rejected: JSON-RPC Error -32601: Agent factories are not available for this session
```

## Prerequisites

Python 3.11 or later, and a signed-in Copilot CLI. The SDK bundles its own CLI runtime but not your credentials.

```bash
python --version
copilot --version
```

Run `copilot` and then `/login` once if you have never authenticated.

## How the TypeScript API maps to Python

| TypeScript | Python |
|------------|--------|
| `client.createSession({ ... })` | `await client.create_session(...)` with keyword arguments, after `await client.start()` |
| `defineTool<{ since: string }>("list_changes", { parameters, handler })` | `@define_tool("list_changes", ...)` on a handler whose parameter is a Pydantic model |
| `skipPermission`, `availableTools`, `systemMessage`, `customAgents`, `workingDirectory` | `skip_permission`, `available_tools`, `system_message`, `custom_agents`, `working_directory` |
| `CustomAgentConfig` with `displayName` | `copilot.session.CustomAgentConfig`, a `TypedDict` with `display_name` |
| `session.sendAndWait({ prompt }, 180_000)` | `await session.send_and_wait(prompt, timeout=180.0)` |
| `session.rpc.agent.getCurrent()`, `select({ name })` | `session.rpc.agent.get_current()`, `select(AgentSelectRequest(name=...))` |
| `session.rpc.fleet.start({ prompt, wait: true })` | `session.rpc.fleet.start(FleetStartRequest(prompt=..., wait=True))` |
| `onPermissionRequest: approveAll` | `on_permission_request=PermissionHandler.approve_all` |
| `defineFactory` plus `session.factory.run(handle)` | No `define_factory`; only the raw `session.rpc.factory.run(FactoryRunRequest(name=..., args=...))` |

## What running this taught

Each row was found by executing the code or reading the installed package, not by reading the Node.js types.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ImportError: cannot import name 'CustomAgentConfig' from 'copilot'` | 1.0.14 does not re-export it from the package root | Import it from `copilot.session` |
| `TypeError` when passing a dict to `create_session` | 1.0.14 takes keyword-only arguments; older samples pass one config dict | Call `create_session(model=..., tools=...)` |
| `UnicodeEncodeError: 'charmap' codec can't encode character '✅'` in the fleet output, with the message silently missing | Redirected stdout on Windows uses cp1252, the fleet coordinator writes emoji, and the SDK logs the handler's exception instead of raising it | Run with `python -X utf8` or set `PYTHONUTF8=1` |
| A traceback is printed even though `factory_probe.py` catches the rejection | The SDK's JSON-RPC layer logs every failed request before re-raising it | Expected; the program still exits 0 |
| No way to hand `session.rpc.factory.run` a factory | The package has no `define_factory` and no extension module with `join_session`; a `FactoryHandler` slot exists in `copilot/generated/rpc.py`, but nothing in `client.py` or `session.py` sets it | Orchestrate from your own code or through `session.rpc.fleet.start` |

## What was verified, and what was not

| Claim | Status |
|-------|--------|
| `coordinator.py` end to end: three sessions, the researcher, builder and reviewer handoff, exit 0 | Verified with real model calls |
| The reviewer genuinely fails the draft it is handed | Verified: it returned `VERDICT: FAIL` and named every bullet for its em dash and missing area |
| `specialists.py` end to end: `agent.list`, `agent.get_current`, `agent.select`, two turns on one session | Verified with real model calls; the reviewer returned `VERDICT: PASS` on that run |
| `fleet.py`: `session.rpc.fleet.start` with `wait=True` resolves and the merged table arrives | Verified with real model calls; the run wrote no files to the folder |
| `factory_probe.py`: the factory run is rejected | Verified; the rejection is the expected result here |
| `define_factory` in the Python SDK | Not available in 1.0.14: `grep -rn "define_factory\|join_session" copilot/` over the installed package returns nothing |

## Model names

`gpt-5-mini` is what these files use and what was verified. Run `/model` in the CLI, or `await client.list_models()` in code, to see what your account and organization policy allow.
