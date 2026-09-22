# Implementation Plan: Meeting Cost Calculator

**Spec**: [spec.md](./spec.md)
**Constitution**: [constitution.md](./constitution.md)

## Technical Context

| Decision | Choice | Rationale |
| --- | --- | --- |
| Language | Python 3.11 or later | `decimal.Decimal` and `argparse` are in the standard library, so the whole feature ships without a runtime dependency. 3.11 is the floor because the code uses builtin generic types in annotations and frozen dataclasses without a compatibility shim. |
| Monetary type | `decimal.Decimal` | Principle IV forbids binary floating point for money. `Decimal` gives exact decimal arithmetic and an explicit rounding mode, so the rounding rule in `spec.md` is applied deterministically instead of depending on binary representation. |
| CLI parsing | `argparse` | Standard library, gives positional arguments, a generated usage message and a variadic attendee list with no extra package. Principle II rules out a third-party CLI framework. |
| Tests | `pytest` | The single permitted dependency under principle II. Parameter-free assertions and `capsys` cover both the logic and the command line surface. |
| Packaging | `pyproject.toml` with `[tool.pytest.ini_options]` only | The project is run from its own directory with `python -m meeting_cost`, so no build backend, console script or install step is needed. The file exists solely to put the project root on `sys.path` for pytest and to point it at `tests/`. |
| Storage and network | none | Principle VI. The tool reads its arguments and writes to standard output. |

## Structure

```text
meeting-cost-solution/
├── meeting_cost/
│   ├── __init__.py
│   ├── calculator.py
│   ├── cli.py
│   └── __main__.py
├── tests/
│   ├── test_calculator.py
│   └── test_cli.py
└── pyproject.toml
```

## Modules and Their Boundary

### `meeting_cost.calculator` (calculation logic)

Owns the domain: parsing a value into a `Decimal`, validating it, computing per attendee cost, summing the total and applying the rounding rule.

Public surface:

```python
class InvalidInputError(ValueError): field: str
@dataclass(frozen=True) class AttendeeCost: hourly_rate: Decimal; cost: Decimal
@dataclass(frozen=True) class MeetingCost: duration_minutes: Decimal; breakdown: tuple[AttendeeCost, ...]; total: Decimal
def parse_duration(value) -> Decimal
def parse_rate(value, position) -> Decimal
def round_total(amount: Decimal) -> Decimal
def calculate(duration_minutes, hourly_rates) -> MeetingCost
```

It imports `dataclasses` and `decimal` and nothing else. It never imports `meeting_cost.cli`, never reads `sys.argv`, never prints and never calls `sys.exit`.

### `meeting_cost.cli` (command line wrapper)

Owns everything about being a program: argument parsing, formatting and the exit code.

```python
def build_parser() -> argparse.ArgumentParser
def format_report(result: MeetingCost) -> str
def main(argv=None) -> int
```

`main` returns an exit code rather than calling `sys.exit`, so tests drive it as a function. `meeting_cost/__main__.py` is the only place that turns that return value into a process exit, which is what makes `python -m meeting_cost` work.

### The boundary

The boundary is one call and one exception. The CLI hands `calculate` the raw argument strings and receives a `MeetingCost` or an `InvalidInputError`. Validation lives in the calculation module, not in argparse types, so that an importing caller gets the same named errors a command line user gets. The dependency points one way: `cli` imports `calculator`.

## Constitution Check

| Principle | Verification |
| --- | --- |
| I. Separation of concerns | `calculator.py` imports `dataclasses` and `decimal` only. `tests/test_calculator.py` exercises the full calculation with no reference to the CLI, and `tests/test_cli.py` asserts in a subprocess that importing `meeting_cost.calculator` leaves `meeting_cost.cli` out of `sys.modules`. PASS |
| II. No hidden dependencies | Runtime imports are `argparse`, `dataclasses`, `decimal` and `sys`, all standard library. `pytest` is the only development dependency, which the principle permits. No further package is proposed, so no rationale is owed. PASS |
| III. Explicit failure | Every invalid value raises `InvalidInputError` carrying a `field` attribute, `duration` or `rate N`, and the message repeats that name. No branch substitutes a default, clamps a negative to zero or falls back to `0`. A non-finite value such as `nan` parses as a `Decimal` but is rejected explicitly. PASS |
| IV. Money is never a float | Rates, per attendee costs and the total are `Decimal` end to end. `float` appears nowhere in the runtime code, no value passes through `float()`, and rounding is `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` rather than the builtin `round`. `tests/test_calculator.py` asserts the reported types. PASS |
| V. Every acceptance criterion has a test | AC-1 through AC-5 each map to at least one test, and each edge case in `spec.md` maps to at least one test. The mapping is recorded in [tasks.md](./tasks.md). PASS |
| VI. Offline by default | No socket, no HTTP client, no file is opened. Output goes to standard output and errors to standard error. PASS |

## Rounding and Currency in the Implementation

The spec fixes the rule: the total is rounded half up to two decimal places, breakdown values stay unrounded. The plan puts that in one place, `round_total`, called once by `calculate` on the summed total. `AttendeeCost.cost` keeps the full `Decimal` division result. Amounts are currency-agnostic, so no symbol, code or locale formatting is applied on output.
