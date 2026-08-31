# run-foundry-demo

**This skill is always a /goal.** State the goal before doing anything:

> Goal: Prepare and guide the run of `<demo-folder>` against `<PROJECT_ENDPOINT>` using model `<MODEL_DEPLOYMENT_NAME>`.

## Guiding principle

The demo script is interactive; it runs in the user's terminal, not a background process. This skill prepares everything and hands off clear commands. **If errors arise, discuss them with the user and solve together.** Do not try to fully automate the run.

## Step 0: Check for provision script

Look for `provision.azcli` in the demo's folder or its parent (for example `src/<demo>/provision.azcli`). If present, run it in Bash before doing anything else. It creates all required Azure resources and updates `.claude/deploy.config`.

If the provision script needs Azure resources not yet created, run it. If resources already exist, the script is idempotent and safe to re-run.

## Step 1: Locate the demo

Identify the target Foundry Python demo folder (a `*-py/` project) under `src/`. If not clear from context, ask.

## Step 2: Load deploy config

Read `.claude/deploy.config`:

- `PROJECT_ENDPOINT`
- `MODEL_DEPLOYMENT_NAME`
- Any service-specific keys added by provision scripts

## Step 3: Collect missing variables

Read the demo's `.env.example` (or existing `.env`) to find required variables. Cross-reference with `deploy.config`. Ask for any variable not covered; do not invent values.

## Step 4: Write .env

Write `.env` in the demo folder with all resolved values. Never commit this file.

## Step 5: Create .gitignore

Write a `.gitignore` in the demo folder if one does not exist:

```gitignore
.env
.venv/
__pycache__/
*.pyc
report_*.txt
```

## Step 6: Create venv and install dependencies

Run these (they do not require an interactive terminal):

```bash
cd <demo-folder>
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows
```

Pin versions after successful install:

```bash
.venv/Scripts/pip freeze > requirements.txt
```

## Step 7: Code quality checks before handoff

Before giving the user any run commands, verify and fix two things in the demo script(s):

**A. Graceful Ctrl+C handling:** every demo must exit cleanly without a traceback. Apply the appropriate pattern:

- Synchronous scripts: wrap the top-level call in `try/except KeyboardInterrupt: print("\nInterrupted.")`
- Async scripts (`asyncio.run`): also catch `asyncio.CancelledError` inside the async `main()`, and suppress errors from cleanup (`exit_stack.aclose()` etc.) with `try/except (asyncio.CancelledError, Exception): pass`

Do not hand off until this is in place.

**B. Default prompts from the lab guide:** read `readme.md` for any suggested user prompts. For each `input()` call in an interactive loop:
- Show the default in the prompt string: `[default: <prompt text>]`
- If the user presses Enter without typing, use the default: `if not user_input: user_input = "<prompt text>"`

## Step 8: Hand off terminal commands

The demo script is interactive. Give the user these commands to run in their VS Code terminal (`Ctrl+\``):

```powershell
cd <demo-folder>
.venv\Scripts\Activate.ps1
python <script>.py
```

Do not attempt to run the script yourself.

## Step 9: Errors: discuss and guide

When the user pastes an error:

| Error type | Resolution |
|---|---|
| Dependency / import error | Look up in `mcp__microsoft-learn__microsoft_docs_search` before changing anything |
| MCP server import error (`mcp.server.fastmcp`) | `mcp` v2 removed fastmcp. Add `--with mcp>=1.0,<2.0` to the uvx args in `.mcp.json` |
| MCP server secrets in `.mcp.json` | Never put API keys inline. Use `--envFile <path>` and store secrets in `.claude/deploy.config` (git-excluded via `.git/info/exclude`) |
| Foundry API / auth / permissions error | Use `mcp__azure-deploy__foundry` to investigate; check role assignments via `az role assignment list` |
| Missing RBAC role | Give the exact `az role assignment create` command with `--scope` (full resource ID). Run via PowerShell if Bash fails |
| Agent not found on startup | The agent must be pre-created in Foundry portal or via `mcp__microsoft-foundry__*` tools. Check `state.md` for status |
| Workflow runs but routing/branches never execute, OR portal canvas is empty | Portal declarative workflow published with the wrong CSDL dialect. **Verify the portal canvas first** (chrome-devtools then `.../build/workflows/<name>/build`) before any code surgery. Foundry uses `kind: ConditionGroup` (`conditions`/`elseActions`) + `Foreach` (`items`/`value`), NOT `kind: If`/`then`/`else`. Build in the portal, export the YAML, publish that. See `microsoft-agent-framework/references/foundry-workflow-declarative.md` |
| Power Fx error `'.' operator cannot be used on Text values` | Dotting a Text scalar (e.g. a Foreach loop var over a `["..."]` array). Use the var directly, or bind agent JSON to `responseObject` and dot into that. See `microsoft-agent-framework/references/foundry-workflow-powerfx.md` |
| Portal-built nodes vanish after edit | Portal does not autosave. Click **Save**; never reload the page (or navigate away) with unsaved changes |
| `UnicodeEncodeError: 'charmap' codec ... '\U0001f680'` (emoji) at startup | Windows stdout defaults to `cp1252`. Call `sys.stdout.reconfigure(encoding="utf-8")` in the launcher + client; spawn child servers with `encoding="utf-8"`, `errors="replace"`, `PYTHONIOENCODING=utf-8`. See `microsoft-agent-framework/references/agent-framework-run-troubleshooting.md` |
| Multi-server demo exits non-zero, no `Goodbye!` / shutdown lines | `CTRL_BREAK_EVENT` hit the launcher's own process group. Spawn servers with `creationflags=subprocess.CREATE_NEW_PROCESS_GROUP` on Windows. See `agent-framework-run-troubleshooting.md` |
| `address already in use` on a server port | A prior run left a listener (A2A: 10007/10008/10009). Re-use the healthy instance or stop the stale PID before re-running |
| Routing/host agent errors only when using a `FunctionTool` | The model lacks Function-tool support (e.g. `gpt-5.4`). Point that agent at a Function-capable deployment (e.g. `gpt-5.2` via `ROUTING_MODEL_DEPLOYMENT_NAME`) |

For any local-run failure (encoding, server lifecycle, ports, model tool support), the symptom-first guide is `.claude/skills/microsoft-agent-framework/references/agent-framework-run-troubleshooting.md`.

Discuss the error with the user before making any fix. Do not guess.

## Step 10: Pin on success

After the user confirms a successful run, freeze versions:

```bash
.venv/Scripts/pip freeze > requirements.txt
```

## Step 11: Update the demo readme

After resolving any issues, update the `readme.md` in the parent folder of the demo with:
- A "Demo resources" table listing all pre-created Azure resources (names, endpoints)
- Permissions required
- Errors encountered and fixes applied
- No AI reasoning, no em dashes

## MCP server configuration rules

When configuring stdio MCP servers in `.mcp.json`:
- Never embed API keys or passwords in the `env` block; `.mcp.json` is tracked by git
- Use `--envFile <absolute-path>` in `args` to point to `.claude/deploy.config` (git-excluded)
- When using `uvx --prerelease=allow`, always add `--with mcp>=1.0,<2.0` to pin the MCP library to v1.x

## Model suitability check

Before proceeding, confirm the target model fits the demo. Ask the user and propose alternatives via `mcp__azure-deploy__foundry` if the demo needs vision, audio, embeddings, or a fine-tuned model.

## Azure resource management

For demos that require Azure resources (AI Search, Storage, etc.):
- Free tier is always preferred unless the demo feature explicitly requires Basic+ (e.g., managed identity outbound from AI Search)
- Provision scripts go in the demo's parent folder, not the `*-py/` subfolder
- Use `--sku free` for AI Search; use `Standard_LRS` for Storage
- Assign RBAC with PowerShell if Bash fails with "MissingSubscription"
