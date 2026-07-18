---
name: run-demo
description: >-
  Guide the user through running and verifying any code demo in this repo, then
  fold what worked back into the demo guide. Auto-detects the stack (.NET, Python,
  Node), prepares the environment (config, deps, build), and hands the user the
  exact terminal commands. Does not run interactive or long-running scripts
  directly. Errors are read from logs and resolved collaboratively. Delegates to
  run-foundry-demo when the demo is an Azure AI Foundry / Agent Framework demo.
  Triggers on: "run demo", "run the demo", "run this demo", "start demo",
  "execute demo", "verify code demo", "evaluate code demo", "run dotnet demo",
  "run python demo", "run node demo", "does the demo work".
---

# run-demo

**This skill is always a /goal.** State the goal before doing anything:

> Goal: Prepare, run-verify, and document `<demo-folder>` (`<stack>`) so a learner can reproduce it from the guide.

## Guiding principle

A demo is verified when it runs the way the guide claims, on this machine. The demo may be interactive (a prompt loop, a dev server, a watched build): those run in the user's terminal, not a background process. This skill prepares everything, hands off clear commands, reads the logs and errors the user pastes back, and resolves them together. Do not try to fully automate an interactive or long-running run. Non-interactive one-shot steps (restore, build, install, a unit-test pass) may be run directly to catch failures early.

## Step 0: Is this a Foundry demo?

If the demo targets Azure AI Foundry or the Microsoft Agent Framework (a `*-py/` agent project, a `PROJECT_ENDPOINT` / `MODEL_DEPLOYMENT_NAME` config, a `provision.azcli`, or imports of `azure.ai.projects` / `agent_framework`), stop here and use the `run-foundry-demo` skill instead. It owns the Foundry-specific provisioning, RBAC, and model checks. Return to this skill only for non-Foundry demos.

## Step 1: Locate the demo

Identify the target project folder (usually under `src/`, sometimes referenced from a `demos/` guide). If not clear from context, ask.

## Step 2: Detect the stack

Detect from marker files in the demo folder:

| Marker | Stack | Verify tooling |
|---|---|---|
| `*.csproj`, `*.sln` | .NET | `dotnet` |
| `requirements.txt`, `pyproject.toml`, `*.py` + `.env.example` | Python | `python` + venv |
| `package.json` | Node | `npm` (or `pnpm` if `pnpm-lock.yaml`) |

If several markers coexist (for example a .NET API with a Node front end), treat each as its own demo and verify them in dependency order (backend before the UI that calls it).

## Step 3: Collect config, never invent values

Read the guide's `readme.md` and any `.env.example`, `appsettings*.json`, or `.env` to list required settings. Cross-reference with what already exists. Ask the user for any value not covered (endpoints, keys, connection strings); do not invent them. Write resolved secrets into the stack's local config, never into a tracked file:

- .NET: `dotnet user-secrets` or a git-ignored `appsettings.Development.json`, or `ConnectionStrings__X` env vars
- Python: a `.env` in the demo folder
- Node: a `.env` / `.env.local` in the demo folder

## Step 4: Ensure a .gitignore

Add a `.gitignore` in the demo folder if one is missing, covering the stack's local artifacts and secrets:

```gitignore
# secrets
.env
.env.local
appsettings.Development.json

# python
.venv/
__pycache__/
*.pyc

# node
node_modules/

# dotnet
bin/
obj/
```

## Step 5: Prepare the environment

Run the non-interactive preparation for the detected stack. These are safe to run directly:

```bash
# .NET
cd <demo-folder>
dotnet restore
dotnet build
```

```bash
# Python (Windows)
cd <demo-folder>
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

```bash
# Node
cd <demo-folder>
npm install     # or: pnpm install
```

If a build or install fails, that is a real finding: resolve it now before handoff.

## Step 6: Code quality checks before handoff

For any demo with an interactive loop or a script the user starts by hand, verify and fix before giving run commands:

**A. Graceful interrupt:** the demo must exit cleanly on Ctrl+C without a raw traceback.

- Python sync: wrap the top-level call in `try/except KeyboardInterrupt: print("\nInterrupted.")`
- Python async (`asyncio.run`): also catch `asyncio.CancelledError` inside `main()` and suppress cleanup errors with `try/except (asyncio.CancelledError, Exception): pass`
- .NET console: register `Console.CancelKeyPress` (or honour a `CancellationToken`) so shutdown is clean
- Node: handle `process.on("SIGINT", ...)` to close servers/clients before exit

**B. Default prompts from the guide:** read `readme.md` for suggested inputs. For each interactive prompt, show the default in the prompt string (`[default: <text>]`) and use it when the user just presses Enter.

## Step 7: Hand off terminal commands

Give the user the exact commands to run in their VS Code terminal (`Ctrl+\``). Do not run interactive or long-running commands yourself.

```powershell
# .NET
cd <demo-folder>
dotnet run
# tests only:
dotnet test
```

```powershell
# Python
cd <demo-folder>
.venv\Scripts\Activate.ps1
python <script>.py
```

```powershell
# Node
cd <demo-folder>
npm run <script>   # e.g. dev, start
```

For a server or watched build, tell the user which URL to open and what a healthy startup line looks like.

## Step 8: Errors: read the logs, discuss, then fix

When the user pastes an error or log, diagnose before changing anything:

| Error type | Resolution |
|---|---|
| Dependency / import / package error | Confirm the version and API in `mcp__microsoft-learn__microsoft_docs_search` (or the package docs) before editing |
| Missing config / env value | Point to the exact setting; ask the user for the value. Never hardcode a secret into a tracked file |
| .NET build error (missing SDK, target framework, package restore) | Check `dotnet --info` against the `*.csproj` `TargetFramework`; restore then build to isolate compile vs runtime failures |
| Port already in use | A prior run left a listener. Re-use the healthy instance or stop the stale PID, then re-run |
| `UnicodeEncodeError` / `charmap` codec on emoji (Windows Python) | stdout defaults to `cp1252`. Call `sys.stdout.reconfigure(encoding="utf-8")` and set `PYTHONIOENCODING=utf-8` |
| Node `ERR_MODULE_NOT_FOUND` / version mismatch | Delete `node_modules`, reinstall; confirm the `engines` Node version matches the local runtime |
| Auth / 401 / 403 against a service | Verify the credential and its scope; confirm the account has the required role before touching code |

Discuss the finding with the user before applying a fix. Do not guess.

## Step 9: Lock versions on success

After the user confirms a clean run, freeze the dependency set so the guide stays reproducible:

- Python: `.venv/Scripts/pip freeze > requirements.txt`
- Node: commit the lockfile (`package-lock.json` / `pnpm-lock.yaml`)
- .NET: pin package versions in the `*.csproj` (no floating `*` versions)

## Step 10: Fold findings back into the demo guide

Update the demo's `readme.md` (or the referencing guide under `demos/`) with what the run actually required:

- The exact prepare and run commands that worked
- Any prerequisites, config values, or accounts the learner needs
- Errors encountered and the fixes applied
- Expected output or the healthy startup line
- No AI reasoning, no em dashes

After editing any `readme.md` under `demos/`, discover and run the repo-local `brand-voice-*` skill to verify it.
