# run-demo

**This skill is always a /goal.** State the goal before doing anything:

> Goal: Prepare, run-verify, and document `<demo-folder>` (`<stack>`) so a learner can reproduce it from the guide.

## Guiding principle

A demo is verified when it runs the way the guide claims, on this machine. The demo may be interactive (a prompt loop, a dev server, a watched build): those run in the user's terminal, not a background process. This skill prepares everything, hands off clear commands, reads the logs and errors the user pastes back, and resolves them together. Do not try to fully automate an interactive or long-running run. Non-interactive one-shot steps (restore, build, install, a unit-test pass) may be run directly to catch failures early.

## Step 0: Is this a Foundry demo?

If the demo targets Microsoft Foundry or the Microsoft Agent Framework (a `*-py/` agent project, a `PROJECT_ENDPOINT` / `MODEL_DEPLOYMENT_NAME` config, a `provision.azcli`, or imports of `azure.ai.projects` / `agent_framework`), stop here and use the `run-foundry-demo` skill instead. It owns the Foundry-specific provisioning, RBAC, and model checks. Return to this skill only for non-Foundry demos.

## Step 1: Locate the demo

Identify the target project folder (usually under `src/`, sometimes referenced from a `demos/` guide). If not clear from context, ask.

## Step 1b: Run in the solution folder, keep the starter pristine

The demo folder the guide walks through is the STARTER. It stays as the learner receives it: no `node_modules`, no lockfile, no build output, no logs, no finished code.

- Copy the starter to a sibling `<starter>-solution/` inside the same topic folder (for example `goal-demo/` and `goal-demo-solution/`), then install, build, run and iterate there.
- If a run already left artifacts in a starter, move them into the solution folder.
- A broken asset gets fixed in BOTH: the starter must be a correct starting point, the solution carries the worked-out result.
- The solution folder must run end to end from a clean copy. A solution that needs a project from another topic is not self-contained: either embed the copy or state the copy step in the guide.
- Guides keep pointing the learner at the starter and name the solution folder once as the completed reference. The module `readme.md` states the convention once.
- A starter is not merely unrun: it must be independently installable and testable from a clean copy. Verify that, or the pristine starter is untested scaffolding.
- The solution may keep its local artifacts on disk after verification (`.venv/`, `node_modules/`, a database, caches). Each solution folder ships its own `.gitignore` covering them, so `git status` stays clean.
- When the runnable project is shared (several topics drive one project under `src/`, or the same starter is duplicated per topic), the guide names the exact shared starter path and the module `readme.md` explains why the copies exist and how the solutions differ.
- A demo that ships its own `.claude/skills/` or `.claude/agents/` tree is discovered as a live skill or agent of the course repo, in the starter and again in the solution copy. Decide deliberately: either keep the demo config out of `.claude/` naming, or state in the topic `readme.md` that the roster entry is demo content.

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

**Windows: this check cannot be executed from Git Bash, so do not report it as passing.** Windows raises a console CTRL_C_EVENT, which a POSIX signal does not produce. Both plausible routes fail silently: `kill -INT <pid>` returns rc=0 while the process runs to completion and exits 0, and `process.kill(process.pid, "SIGINT")` terminates the process without ever invoking the listener. Confirm the platform rather than the code by running the same probe against a trivial handler; if that control also fails to print, the environment is the blocker. Add the handler, confirm it compiles and is registered, then report it as "handler registered, interrupt behaviour not verifiable on Windows". A registered handler is not a verified handler.

**B. Default prompts from the guide:** read `readme.md` for suggested inputs. For each interactive prompt, show the default in the prompt string (`[default: <text>]`) and use it when the user just presses Enter.

## Step 6b: Demos that drive an agent

When the demo itself calls `claude -p` (a CI gate, a worktree lane, a goal loop), separate what you can prove from what you cannot:

| What | How to verify | How to report it |
|---|---|---|
| Script plumbing (argument construction, backgrounding, `wait`, exit codes, JSON parsing, merges, cleanup) | Put a stub `claude` earlier on `PATH` that edits a file and commits, then run the script end to end | Verified |
| A single headless call and its JSON envelope | One real `claude -p` run with `--max-turns` and an allow-list | Verified |
| A model judgement (an AI audit that "exits 0 on clean code") | Cannot be pinned. Live runs legitimately disagree | The guide states the outcome is model-dependent, never promises a fixed exit code |
| Interactive REPL steps, GitHub Actions jobs, multi-agent parallel runs | Not runnable locally | Labelled as not executed, with the reason |

The defect classes these scripts fail on (invented CLI surface, unsupported frontmatter, a variadic flag eating the positional argument, a misplaced manifest, exit codes lost to a subshell, command substitution inside a quoted YAML string, platform assumptions, stale build output, project-scoped harness discovery) live in `verify-by-execution.md`, together with the stub-the-model, JSON-RPC and hook-stdin techniques. Read it before handing off any demo that ships a script, a hook, a workflow, or harness config, and check every class.

A packaging or archiving step built on `zip` deserves its own mention here: `zip` is not on PATH in Git Bash on Windows and fails with exit 127. Use `powershell Compress-Archive` in any guide a Windows learner runs, and verify the archive by unpacking it.

## Step 6c: A step that succeeds and then crashes is still a pass

Judge a step by whether the payload arrived, not by whether the process exited cleanly. The two are separate claims and both belong in the report.

Tools legitimately print a correct result and then die in teardown. The MCP Inspector CLI on Windows prints a complete, correct `tools/list` and then aborts with `Assertion failed: !(handle->flags & UV_HANDLE_CLOSING), file src\win\async.c, line 76` and exit code 3221226505, a libuv teardown bug in the client rather than a fault in the demo server. A learner who is not warned reads that dump as a failed demo and starts debugging working code.

When this happens, say so at the step itself, not only in a troubleshooting section, and keep "the data was correct" distinct from "the process exited cleanly" in the findings.

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
| `npm` `ERESOLVE` peer dependency conflict | A floating version resolved to a release whose peer range the demo's own pin no longer satisfies (for example an SDK that moved to `zod ^4` while the demo pinned `zod ^3`). Read the peer range in the error, raise the demo's pin to match, then pin the SDK itself per Step 9. Never resolve it with `--legacy-peer-deps` in a course demo: that ships a dependency set the learner's install will not reproduce |
| ESM-only package required from a CommonJS file (`TS1479`) | Add `"type": "module"` to the demo `package.json`, or switch the file to `import` with an ESM-aware tsconfig. Check this before blaming the SDK version |
| Exported type not found after an SDK bump (`TS2305` / `TS2724`) | The package renamed or moved its exports. Read the installed `.d.ts` rather than guessing: the compiler's "did you mean" hint usually names the new symbol. Fix the demo source AND any guide snippet that shows the old name |
| Auth / 401 / 403 against a service | Verify the credential and its scope; confirm the account has the required role before touching code |

Discuss the finding with the user before applying a fix. Do not guess.

## Step 9: Lock versions on success

After the user confirms a clean run, freeze the dependency set so the guide stays reproducible:

- Python: `.venv/Scripts/pip freeze > requirements.txt`
- Node: commit the lockfile (`package-lock.json` / `pnpm-lock.yaml`)
- .NET: pin package versions in the `*.csproj` (no floating `*` versions)

Lockfiles and frozen dependency sets belong to the solution folder. The starter keeps none of them.

**A course demo never floats a dependency version.** `"latest"` (or `*`, or a bare major range on a fast-moving SDK) means the demo a learner installs is not the demo that was verified. Replace it with the exact resolved version in the starter AND the solution, so the starter is installable on its own and the solution reproduces the verified run.

This is the single most common way a demo that nobody edited stops working: the ecosystem moves underneath it. One session found both Agent SDK demos uninstallable because the floating SDK had advanced to a release requiring a new `zod` major, and the same drift had also renamed two exported types the guide still showed. Treat "the guide is unchanged" as no evidence that the guide still runs: re-run install and typecheck before a class, not just a prose review.

## Step 10: Fold findings back into the demo guide

Update the demo's `readme.md` (or the referencing guide under `demos/`) with what the run actually required:

- The exact prepare and run commands that worked
- Any prerequisites, config values, or accounts the learner needs
- Errors encountered and the fixes applied
- Expected output or the healthy startup line
- No AI reasoning, no em dashes

After editing any `readme.md` under `demos/`, discover and run the repo-local `brand-voice-*` skill to verify it.
