# Lab 05 Solution: Agent Sessions (Python)

The artifacts the [Python variant of Lab 05](../readme-py.md) asks you to end up with, in the state they should reach by Step 10. In the lab they live in `src/scratch/session-lab/` and the Cleanup section deletes them; here they are kept so you can compare.

| File | Produced by | What it is |
|------|-------------|------------|
| `research.md` | Step 2 | The cited scoping report from the read-only research session: how `src/` organizes its sample projects and which manifest each project type carries |
| `slugify.py` | Step 3, hardened in Step 8 | The single `slugify(input)` function the writing session builds in its worktree |
| `test_slugify.py` | Step 3, extended in Step 8 | Nine pytest tests (fourteen cases once parametrized): the ordinary case and the empty string from Step 3, plus the three edge cases Step 8 predicts the reviewer raises |
| `pyproject.toml` | Step 7 | The minimal manifest whose absence makes the Step 7 run fail, with a `[tool.pytest.ini_options]` table and no dependencies |
| `handover.md` | Step 10 | The five-section assembly of all four surfaces |
| `test-results.md` | This run | Every command run verbatim, its output, and the steps that could not be executed outside the Agents window |

Run the tests with Python 3.10 or later and pytest installed:

```bash
python -m pytest
```
