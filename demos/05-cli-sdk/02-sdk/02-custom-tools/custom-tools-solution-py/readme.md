# Copilot SDK Demos: Worked Solution in Python

The Python port of [the Node.js solution](../custom-tools-solution-node/readme.md) for [the topic guide](../readme.md), verified end to end against `github-copilot-sdk` 1.0.14 on Python 3.12. Same tools, same prompts, same model, same session settings.

Work through the guide and build the files yourself. Come here when a step does not behave, or to compare your version against one that runs.

## What is here

| File | Guide step | What it does |
|------|------------|--------------|
| `weather_agent.py` | Steps 2 and 3 | Defines one `get_weather` tool and streams a single turn that calls it for two cities |
| `interactive_agent.py` | Step 4 | The same tool behind a multi-turn prompt loop that exits cleanly on `exit` or end of input |
| `security_analyzer.py` | Step 5 | Two tools, a system message, and a session scoped to custom tools only |

## Run it

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python weather_agent.py
python interactive_agent.py
python security_analyzer.py
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## Prerequisites

Python 3.11 or later, and a signed-in Copilot CLI. The SDK brings the CLI runtime but not your credentials.

```bash
python --version
copilot --version
```

Run `copilot` and then `/login` once if you have never authenticated.

## The pitfalls, as they show up in Python

Each of these was reproduced by running the code.

| Symptom | Cause | Fix |
|---------|-------|-----|
| The agent answers "I couldn't fetch live weather because the weather tool needs permission" | Every tool call goes through the session's permission gate, and a session with no handler denies it | `skip_permission=True` on a tool whose handler only computes, or `on_permission_request=` on `create_session` |
| The tool is offered to the model with no parameter schema | `define_tool` builds the JSON schema only from a Pydantic model; a handler typed `params: dict` or `city: str` gets `parameters=None` | Declare a `BaseModel` with `Field(description=...)` and type the handler's first parameter with it |
| The prompt loop dies with `EOFError: EOF when reading a line` and `client.stop()` never runs | `input()` raises at end of input, which is the first thing that happens when you pipe input instead of typing it | Read with `sys.stdin.readline`, which returns an empty string at end of input, and leave the loop on it |
| The analyzer says it could not read `app.js` due to a permission error and never calls your tool | The session still exposes the built-in file tools, and the model prefers them over a custom tool with a similar job | `available_tools=["custom:*"]` so only your own tools are reachable |
| `°F` prints as `�F` when output is piped on Windows | Python writes a redirected stdout in the ANSI code page, not UTF-8 | Set `PYTHONIOENCODING=utf-8` or `PYTHONUTF8=1` before running |

## Model names

`gpt-5-mini` is what these files use and what was verified. Run `/model` in the CLI, or `await client.list_models()` in code, to see what your account and organization policy allow.
