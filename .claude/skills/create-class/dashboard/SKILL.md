---
name: dashboard
description: Scaffold, evaluate, render, update, show, test, and publish the class progress dashboard for a course repo. A static web app plus Python evaluators plus a GitHub Pages workflow that report per-module completeness (theory, demos, labs, slides). Optional per class. Peer skill the create-class master delegates to; also invocable directly. Trigger phrases: class dashboard, module status, whats missing, setup dashboard, show status, update class status, test dashboard, publish class dashboard, github pages dashboard, class progress.
---

# Dashboard

Self-contained skill for the class progress dashboard. It is optional per class: some courses use it, some do not. It ships everything it needs in its own subfolders so it travels as one unit.

The `create-class` master skill delegates here, and it is independently invocable. It collapses seven sub-verbs into one document, each self-contained: `setup`, `evaluate`, `render`, `update`, `show`, `test`, and `publish`. Pick the sub-verb that matches the request.

## What it produces

- A static web app (`index.html`, `styles.css`, `app.js`) that renders per-module status without a server.
- Two Python evaluators: `evaluate.py` inspects the repo and writes status fields, `render-dashboard.py` injects the data inline into `index.html`.
- A GitHub Pages workflow that re-evaluates, renders, commits, and deploys on every relevant push.

## Bundled assets

Everything lives inside this skill folder:

| Path | Purpose |
|------|---------|
| `templates/dashboard.json` | Config plus generated state: assignee, issue numbers, project meta (hand-maintained) plus `theory`, `demos`, `labs`, `slides` status fields written by `evaluate.py`. |
| `templates/evaluate.py` | Inspects the repo and writes status fields into `dashboard.json`. Automated via GitHub Actions; also runnable locally. |
| `templates/render-dashboard.py` | Reads `dashboard.json`, injects data inline into `index.html` between `<!-- DATA:START -->` and `<!-- DATA:END -->`. |
| `templates/index.html`, `templates/styles.css`, `templates/app.js` | The static web app. Self-contained; opens directly from disk. |
| `templates/test_evaluate.py` | Unit tests for the evaluator. |
| `templates/collect_contributors.py`, `templates/contributors-override.json` | Contributor collection helper and override list. |
| `templates/update-class-dashboard.yml` | The GitHub Pages deployment workflow. |
| `references/class-module-evaluation.md` | Discovery rules the evaluator applies per component. |

When installed into a course repo, all runtime files live in `dashboard/` at the repo root: source data, scripts, and the static web app. `index.html` is self-contained; the rendered JSON is injected inline so it opens directly from disk without a server.

## States

- **planned**: nothing exists yet for this component
- **doing**: partial progress, below target
- **done**: meets or exceeds target

A module's overall status is the worst state across its components. See `references/class-module-evaluation.md` for the discovery rules the evaluator applies per component (theory, code demos, labs, slides).

## Sub-verb: setup

Scaffold `dashboard/` with everything needed to evaluate module status and render a live progress dashboard. Run this once when setting up a new course repo. Populate modules first, then use the `publish` sub-verb to install the GitHub Pages workflow.

### Steps

1. Locate the repo root.

2. Create `dashboard/` at the repo root if it does not exist.

3. For each file in `templates/` (relative to this skill root), except `update-class-dashboard.yml`:
   - `index.html`, `styles.css`, `app.js`
   - `evaluate.py`, `render-dashboard.py`, `test_evaluate.py`
   - `collect_contributors.py`, `contributors-override.json`
   - `dashboard.json` (only if `dashboard/dashboard.json` does not already exist)

   Copy the file to `dashboard/<file>`. If the target file already exists, skip it and report "skipped (already exists)".

4. Print a summary table of created vs. skipped files.

5. Print next steps:

   ```text
   Next steps:
   1. Edit dashboard/dashboard.json. Set project.title, project.repo, project.projectUrl, and the modules list.
   2. Run: python dashboard/evaluate.py && python dashboard/render-dashboard.py
   3. Open dashboard/index.html in a browser to verify the data renders.
   4. Run the publish sub-verb to install the deployment workflow.
   5. Commit dashboard/ and push to master.
   ```

## Sub-verb: evaluate and render

Two paired operations: **evaluate** (inspect the repo and write status fields into `dashboard/dashboard.json`) and **render** (regenerate the local web dashboard via `dashboard/render-dashboard.py`). Always evaluate before rendering.

### Evaluate

**Always run a full evaluation. Never use cached status, delta comparisons, or assumptions from prior context.**

1. Run the evaluator. This discovers all module paths and names from the filesystem and overwrites every status field:

   ```bash
   python dashboard/evaluate.py
   ```

2. Run the renderer to keep `dashboard/index.html` in sync:

   ```bash
   python dashboard/render-dashboard.py
   ```

3. Read the updated `dashboard/dashboard.json` and report the full status table: all modules, all fields. Never summarise from memory.

The evaluator overwrites `name`, `path`, `theory`, `demos`, `labs`, and `slides` on every run from the actual filesystem. Never read prior state from `dashboard.json` before running, it is stale by definition.

### Render

1. Ensure `dashboard.json` status fields are current (run evaluate first if anything in the repo has changed).
2. Run the renderer:

   ```bash
   python dashboard/render-dashboard.py
   ```

3. Output: `dashboard/index.html` with data injected inline, ready to open in a browser.
4. Open `dashboard/index.html` directly (no server needed) or on GitHub Pages.

Edit `dashboard/dashboard.json` when assignees change, when new GitHub issue numbers need to be linked, or when the project meta (title, repo, projectUrl) changes. Never edit the `theory`, `demos`, `labs`, or `slides` fields by hand, they are overwritten by `evaluate.py`.

### Rules

- Always run `evaluate.py` before reporting any status.
- Never use status values from prior context, memory, or a previous run of `dashboard.json`.
- Always run the renderer after evaluating, `dashboard/index.html` must stay in sync with `dashboard/dashboard.json`.
- Never hand-edit the status fields in `dashboard.json`. They are generated.
- When a new component is added to the model (e.g. a fifth column beyond Theory, Demos, Labs, Slides), update `references/class-module-evaluation.md`.

## Sub-verb: update

Re-evaluate every module in `demos/` and `labs/` and refresh the dashboard, with no browser.

1. Run the evaluator and renderer from the repo root:

   ```bash
   python dashboard/evaluate.py && python dashboard/render-dashboard.py
   ```

2. Report a one-line summary: number of modules evaluated and the overall completion percentage from the updated payload.

The command is complete when both scripts exit without error. Do not open a browser or commit any files.

## Sub-verb: show

Refresh the dashboard data and open it in the browser with live-server.

1. Run the two dashboard scripts to evaluate all modules and render the output:

   ```bash
   python dashboard/evaluate.py && python dashboard/render-dashboard.py
   ```

2. Report the one-line summary (modules evaluated + completion percentage).

3. Launch live-server pointed at the `dashboard/` folder, opening the browser automatically:

   ```bash
   npx live-server dashboard --open=/index.html --port=5500
   ```

The command is complete once the browser tab is open. Do not commit any files.

## Sub-verb: test

Four phases: unit tests, pipeline, live server, browser check. All four must pass.

### Phase 1: Unit Tests

```bash
python -m pytest dashboard/test_evaluate.py -v
```

All 33 tests must pass. Stop and report immediately if any fail.

### Phase 2: Pipeline

Run evaluate then render in sequence:

```bash
python dashboard/evaluate.py
python dashboard/render-dashboard.py
```

Verify evaluate prints "Evaluated 13 modules". Verify render exits with no output (success) or no error output.

### Phase 3: Live Server

Start a Python HTTP server serving `dashboard/` on port 8765:

```bash
nohup python -m http.server 8765 --directory dashboard > /tmp/dashboard-server.log 2>&1 &
echo $! > /tmp/dashboard-server.pid
sleep 2
```

Verify it started:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
```

Must return `200`.

### Phase 4: Browser Check

Use Chrome DevTools MCP to verify the rendered dashboard:

1. `mcp__chrome-devtools__new_page`: open a new browser tab
2. `mcp__chrome-devtools__navigate_page`: go to `http://localhost:8765`
3. `mcp__chrome-devtools__take_screenshot`: capture the dashboard
4. `mcp__chrome-devtools__evaluate_script`: run this check:

   ```js
   const d = window.DASHBOARD_DATA;
   JSON.stringify({
     loaded:      !!d,
     moduleCount: d?.modules?.length,
     firstModule: d?.modules?.[0]?.name,
     lastModule:  d?.modules?.[12]?.name,
     overallPct:  d?.summary?.percent,
   })
   ```

   Expected: `loaded: true`, `moduleCount: 13`, first module "Fundamentals", last "Agentic DevOps & Deployment".

5. `mcp__chrome-devtools__list_console_messages`: verify no JS errors.

### Cleanup

```bash
kill $(cat /tmp/dashboard-server.pid) 2>/dev/null || true
rm -f /tmp/dashboard-server.pid /tmp/dashboard-server.log
```

### Report

Print the result as a table:

```text
============================================================
PHASE            RESULT    DETAIL
------------------------------------------------------------
Unit tests       PASS      33/33
Evaluate         PASS      13 modules
Render           PASS      index.html updated
HTTP server      PASS      200 on localhost:8765
Browser load     PASS      window.DASHBOARD_DATA present
Module count     PASS      13 modules
Console errors   PASS      none
============================================================
OVERALL: PASS
```

Mark any failed step FAIL with the error detail inline. Screenshot is saved automatically by the Chrome DevTools MCP call.

## Sub-verb: publish

Install the GitHub Actions workflow that evaluates module status, renders the dashboard, commits the refresh, and deploys to GitHub Pages whenever `demos/`, `labs/`, or `dashboard/dashboard.json` change on `master`.

### Steps

1. Read `templates/update-class-dashboard.yml` (relative to this skill root).

2. Create `.github/workflows/` at the repo root if it does not exist.

3. Write the workflow content to `.github/workflows/update-class-dashboard.yml`.
   - If the file already exists, report it and ask the user to confirm before overwriting.

4. Ask the user for their GitHub owner and repo name (e.g. `alexander-kastil/masterclass-claude-code`).

5. Open `dashboard/dashboard.json` and set:
   - `project.pagesUrl` to `https://<owner>.github.io/<repo>/`

6. Report the files written.

7. Print next steps:

   ```text
   Next steps:
   1. Commit .github/workflows/update-class-dashboard.yml and dashboard/dashboard.json, then push to master
   2. Go to repo Settings, Pages, Source: GitHub Actions
   3. The workflow triggers on the next push to demos/, labs/, or dashboard/dashboard.json, or via Actions, workflow_dispatch
   4. Live URL: https://<owner>.github.io/<repo>/
   ```
