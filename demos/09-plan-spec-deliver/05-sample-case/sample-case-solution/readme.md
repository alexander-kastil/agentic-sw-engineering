# Solution: The Sample Case, Run

[The topic page](../readme.md) describes the run without doing it. The run itself is checked in at [labs/09-plan-spec-deliver/02-plan-spec-deliver/meeting-cost-solution/](../../../../labs/09-plan-spec-deliver/02-plan-spec-deliver/meeting-cost-solution/readme.md): the four artifacts, the code, the tests and their real output. This folder records the two claims on the topic page that are worth checking before you teach them.

Environment: Windows 11, Python 3.12.10, pytest 9.0.3, executed 2026-09-21.

## The two totals

```bash
python -m meeting_cost 60 100 80 60
python -m meeting_cost 30 90
```

```text
Total: 240.00
Total: 45.00
```

Both are exact. `240` and `45` are what the lab's table asks for; the two decimal places come from the rounding rule the student writes into `spec.md` at the specify checkpoint, which is the whole point of closing that gap in writing.

## The float constraint, and why its tell is the plan

The topic page says the agent tends to violate principle 4. It does. What it does not do is produce a visibly wrong number on this feature's inputs:

```bash
python -c "h=60/60.0; print(repr(sum(r*h for r in (100.0,80.0,60.0))))"
python -c "print(repr(90.0*(30/60.0)))"
```

```text
240.0
45.0
```

Every figure in the brief is exactly representable in binary, so a `float` implementation passes the lab's own verification table and the test suite. The violation is invisible in the output and visible only in `plan.md`, where a type is named. That is why the plan checkpoint is where this one gets caught, and why the topic page describes the tell as a plan naming `float` rather than a total coming back wrong.

## The 25 tests

```bash
python -m pytest -q
```

```text
.........................                                                [100%]
25 passed in 0.16s
```

Run from [meeting-cost-solution/](../../../../labs/09-plan-spec-deliver/02-plan-spec-deliver/meeting-cost-solution/readme.md). Five acceptance criteria and four edge cases, each with a test behind it, which is principle 5 holding.

[← Back to Sample Case: Implement a Product Feature](../readme.md)
