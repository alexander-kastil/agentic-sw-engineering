# Reference Solution: Meeting Cost Calculator

This folder holds what a student holds at the end of [the lab](../readme.md): the four spec-driven artifacts, the code they describe, and the tests that hold the code to them. Everything here was produced by running the loop, not by describing it, and the output in [Test results](#test-results) is the real output of the commands shown.

Use it to check your own run. The wording will differ, because the agent generates it. The structure and the coverage should not.

## Contents

| File | Lab step |
| --- | --- |
| [constitution.md](./constitution.md) | Step 2, the generated `.specify/memory/constitution.md` after the checkpoint |
| [spec.md](./spec.md) | Step 3, the generated `specs/001-*/spec.md` after the checkpoint |
| [plan.md](./plan.md) | Step 4, `plan.md` after the constitution check was read |
| [tasks.md](./tasks.md) | Step 5, `tasks.md` after vague tasks were merged out |
| `meeting_cost/`, `tests/`, `pyproject.toml` | Step 6, what `/speckit-implement` works through |

## How it maps to the seven steps

| Step | What the lab asks | What is here |
| --- | --- | --- |
| 1. Initialize | Create the Spec Kit project | Not reproduced. The generated `.specify/` scaffolding is tool output, and this folder holds the artifacts the loop produces inside it. |
| 2. Constitution | All six principles survive, none softened | `constitution.md` states all six as MUST, including principle 4, and adds a governance clause that makes the plan's constitution check mandatory. |
| 3. Specify | Three stories, five criteria, four edge cases, the two gaps closed, no implementation detail | `spec.md`. The gaps are closed under `Resolved Gaps`: the total is rounded half up to two decimal places with breakdown values unrounded, and amounts are currency-agnostic decimals. No class name, file name or library name appears in it. |
| 4. Plan | Names the modules and their boundary, a rationale per technology choice, an explicit constitution check | `plan.md`. The boundary is one call and one exception, and the constitution check covers all six principles individually. |
| 5. Tasks | Data types and logic before the CLI, the CLI before its tests, every criterion mapped | `tasks.md`, six phases, T001 to T027, with an acceptance criteria coverage table and an edge case coverage table. |
| 6. Implement | Work inside the two modules and their tests | `meeting_cost/calculator.py`, `meeting_cost/cli.py`, `meeting_cost/__main__.py`, `tests/test_calculator.py`, `tests/test_cli.py`. |
| 7. Verify | Run the tests and check the criteria by hand | The commands and their real output below. |

## Design in one paragraph

`meeting_cost.calculator` imports `dataclasses` and `decimal` and nothing else. It parses and validates the raw values, so an importing caller gets the same named errors a command line user gets, and it returns a `MeetingCost` holding unrounded per attendee costs and a total rounded half up to two decimal places. `meeting_cost.cli` owns argument parsing, formatting and the exit code; `main` returns an exit code instead of calling `sys.exit`, so tests drive it as a plain function, and `meeting_cost/__main__.py` is the one place that turns that return value into a process exit.

## How to run it

From this folder:

```bash
python -m pytest -q
python -m meeting_cost 60 100 80 60
python -m meeting_cost 30 90
```

`pyproject.toml` carries only `[tool.pytest.ini_options]` with `pythonpath = ["."]` and `testpaths = ["tests"]`. There is nothing to install and no build step. That `pythonpath` line is what lets bare `pytest` work here; drop it and bare `pytest` fails collection with `ModuleNotFoundError: No module named 'meeting_cost'` while `python -m pytest` still passes, which is why the lab's step 7 uses `python -m pytest`.

## Test results

Run on Python 3.12.10, pytest 9.0.3, Windows 11.

```text
> python -m pytest -q
.........................                                                [100%]
25 passed in 0.17s
```

```text
> python -m meeting_cost 60 100 80 60
Duration: 60 minutes
Attendees: 3
Attendee 1 at 100 per hour: 100
Attendee 2 at 80 per hour: 80
Attendee 3 at 60 per hour: 60
Total: 240.00
exit code 0
```

```text
> python -m meeting_cost 30 90
Duration: 30 minutes
Attendees: 1
Attendee 1 at 90 per hour: 45.0
Total: 45.00
exit code 0
```

```text
> python -m meeting_cost 60
Duration: 60 minutes
Attendees: 0
Total: 0.00
exit code 0
```

```text
> python -m meeting_cost 0 100 80
Duration: 0 minutes
Attendees: 2
Attendee 1 at 100 per hour: 0
Attendee 2 at 80 per hour: 0
Total: 0.00
exit code 0
```

```text
> python -m meeting_cost -30 100
error: duration must not be negative: -30
exit code 1
```

```text
> python -m meeting_cost 30 100 -80
error: rate 2 must not be negative: -80
exit code 1
```

```text
> python -m meeting_cost 30 eighty
error: rate 1 is not a number: 'eighty'
exit code 1
```

The two totals the lab checks by hand print as `240.00` and `45.00`, which is the two decimal place rounding rule from `spec.md` applied to 240 and 45. The error lines go to standard error, which is why the invalid runs print nothing on standard output.
