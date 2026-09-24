# Solution: Leave Days Preview

The worked sample case from [the topic page](../readme.md): a feature brief, the four artifacts that came out of the checkpoints, the code they describe and the tests that hold the code to them. The artifacts follow the Spec Kit 1.0.9 templates; the commands and output below were executed on 2026-09-24.

Environment: Windows 11, Python 3.12.10, pytest 9.0.3.

## Contents

| File | Phase |
| --- | --- |
| [requirements.md](./requirements.md) | The product owner's brief, input to `/speckit-specify` |
| [constitution.md](./constitution.md) | `/speckit-constitution`, six principles |
| [spec.md](./spec.md) | `/speckit-specify`, with both gaps closed under `Resolved Gaps` |
| [plan.md](./plan.md) | `/speckit-plan`, with a per-principle Constitution Check |
| [tasks.md](./tasks.md) | `/speckit-tasks`, T001 to T014 plus a coverage table |
| `leave_days/`, `tests/`, `holidays-*.txt` | `/speckit-implement` |

## Run it

From this folder, with nothing to install:

```bash
python -m pytest -q
```

```text
.....................                                                    [100%]
21 passed in 0.12s
```

```bash
python -m leave_days 2026-12-21 2026-12-25 --holidays holidays-2026-2027.txt
```

```text
Leave: 2026-12-21 to 2026-12-25
2026: 3.5 days
Total: 3.5 days
```

```bash
python -m leave_days 2026-12-28 2027-01-08 --holidays holidays-2026-2027.txt
```

```text
Leave: 2026-12-28 to 2027-01-08
2026: 3.5 days
2027: 4.0 days
Total: 7.5 days
```

The same request against the file HR published in September, which stops at December, is rejected instead of quietly counting 1 and 6 January as working days:

```bash
python -m leave_days 2026-12-28 2027-01-08 --holidays holidays-2026.txt
```

```text
error: holidays has no entries for 2027
```

```bash
python -m leave_days 2026-12-22 2026-12-21 --holidays holidays-2026-2027.txt
```

```text
error: end must not be before start: 2026-12-21
```

Both error runs exit with code 1 and print nothing on standard output.

[← Back to Sample Case: Implement a Product Feature](../readme.md)
