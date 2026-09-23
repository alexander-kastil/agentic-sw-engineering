# Test Results

Run on Windows 11, PowerShell 7, Python 3.12.10. Every command was run from a copy of `labs/07-copilot-app/food-shop-py` in a fresh folder standing in for the session worktree, with this folder's `shop.html` and `test_shop.py` applied on top. The starter in the repository was never modified.

## Baseline (unmodified starter)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

```text
tests\test_shop.py ..                                                    [100%]
============================== 2 passed in 0.18s ==============================
```

Installed: fastapi 0.141.1, starlette 1.7.0, uvicorn 0.53.0, Jinja2 3.1.6, httpx2 2.13.1, pytest 9.1.1.

## Step 5, with the heading change applied

```powershell
cd labs/07-copilot-app/food-shop-py
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

```text
rootdir: C:\wt-lab07\labs\07-copilot-app\food-shop-py
configfile: pyproject.toml
testpaths: tests
collected 3 items

tests\test_shop.py ...                                                   [100%]

============================== 3 passed in 0.36s ==============================
```

```powershell
python -m uvicorn app.main:app --reload
```

```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [75636] using StatReload
INFO:     Application startup complete.
```

`GET http://127.0.0.1:8000/` returned the page with `<h1>Fresh Food, Fast</h1>` above the three food items, and `/static/styles.css` returned 200.

## Step 7, the review comment applied

Changing the heading and its test to `Fresh Food, Delivered Fast` while uvicorn was running: the reloader picked up the template change, the page served `<h1>Fresh Food, Delivered Fast</h1>`, and `python -m pytest -q` reported `3 passed`.

## Defects found by running, fixed in the guide and the starter

| Defect | Evidence | Fix |
|---|---|---|
| `pip install` fails in a deep worktree path on Windows | `OSError: [Errno 2] No such file or directory: '...\.venv\Lib\site-packages\pydantic_core-2.46.5.dist-info\sboms\pydantic-core.cyclonedx.json'` with a Windows Long Path hint, when the copy sat under `%LOCALAPPDATA%\Temp\...`; the same install at `C:\wt-lab07` succeeded | Step 1 now asks for a short worktree location such as `C:\wt`, and the Troubleshooting table carries the symptom |
| An older FastAPI against a current Starlette breaks test collection | fastapi 0.111.1 in a global environment: `TypeError: Router.__init__() got an unexpected keyword argument` | `requirements.txt` pins `fastapi>=0.141`, and Step 5 installs into a fresh `.venv` |
| `TestClient` warns on `httpx` | `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead.` | `requirements.txt` lists `httpx2` |
| The original review comment could leave the line unchanged | "Use title case here" asked for a change to `Fresh Food, Fast`, which is already title case, so the line might not move and the **Outdated** badge would never appear | Step 7 now asks for `Fresh Food, Delivered Fast`, which always moves the line |

## Steps that could not be executed

Steps 1 to 4 and 6 to 10 are driven inside the GitHub Copilot desktop app (Customize, `/permissions`, the Plan tab, `/btw`, the Files and diff views, the in-app browser screenshot, Agent Merge, repository MCP sync, scheduled automations) or in VS Code's external session list, and have no command-line equivalent.
