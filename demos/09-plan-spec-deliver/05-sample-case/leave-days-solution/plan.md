# Implementation Plan: Leave Days Preview

**Spec**: [spec.md](./spec.md)
**Constitution**: [constitution.md](./constitution.md)

## Technical Context

| Decision | Choice | Rationale |
| --- | --- | --- |
| Language | Python 3.11 or later | `datetime`, `decimal` and `argparse` cover the feature with no runtime dependency. |
| Day count type | `decimal.Decimal` | Principle IV. `Decimal("0.5")` sums exactly; `int` cannot hold a half day and `float` is ruled out. |
| Holidays | Parsed from HR's file into a `date` to `Decimal` map | Principle VI and FR-004. The file is the only source of holiday dates. |
| CLI parsing | `argparse` | Standard library; positional `start` and `end`, required `--holidays`. |
| Tests | `pytest` | The single permitted development dependency. |

## Structure

```text
leave-days-solution/
├── leave_days/
│   ├── __init__.py
│   ├── __main__.py
│   ├── calculator.py
│   └── cli.py
├── tests/
│   ├── test_calculator.py
│   └── test_cli.py
├── holidays-2026.txt
├── holidays-2026-2027.txt
└── pyproject.toml
```

## Modules and Their Boundary

`leave_days.calculator` owns the domain and takes the holiday file's lines, not its path:

```python
class InvalidInputError(ValueError): field: str
@dataclass(frozen=True) class HolidayCalendar: days_off: dict[date, Decimal]; years: frozenset[int]
@dataclass(frozen=True) class YearCharge: year: int; days: Decimal
@dataclass(frozen=True) class LeaveCharge: start: date; end: date; per_year: tuple[YearCharge, ...]; total: Decimal
def parse_holidays(lines) -> HolidayCalendar
def charge_leave(start: str, end: str, calendar: HolidayCalendar) -> LeaveCharge
```

`leave_days.cli` owns reading the file, printing and the exit code. `main(argv)` returns an exit code; `__main__.py` is the only place that calls `sys.exit`. The dependency points one way: `cli` imports `calculator`.

## Constitution Check

| Principle | Verification |
| --- | --- |
| I. Separation of concerns | `calculator.py` imports `dataclasses`, `datetime` and `decimal` only; it never opens a file or prints. A test asserts importing it leaves `leave_days.cli` unloaded. PASS |
| II. No hidden dependencies | Runtime imports are all standard library. A third-party holiday package was considered and rejected: it would violate this principle and principle VI. PASS |
| III. Explicit failure | Every rejection raises `InvalidInputError` with `field` set to `start`, `end`, `holidays` or `holidays line N`. An unknown year is rejected, not counted as all working days. PASS |
| IV. Exact half days | Every count is `Decimal`; the only fractional constant is `Decimal("0.5")`. A test asserts the types. PASS |
| V. Every criterion has a test | SC-001 to SC-006 and each edge case map to tests in [tasks.md](./tasks.md). PASS |
| VI. Holidays are data | No date literal for a holiday appears in `leave_days/`. A test scans `calculator.py` for one. PASS |
