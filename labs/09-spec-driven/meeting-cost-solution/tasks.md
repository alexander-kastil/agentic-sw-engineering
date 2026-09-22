# Tasks: Meeting Cost Calculator

**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

Tasks are ordered. The data types and the calculation module come before the command line wrapper, and the wrapper comes before its tests.

## Phase 1: Project skeleton

- [x] **T001** Create `meeting_cost/` and `tests/`, and a `pyproject.toml` whose only content is `[tool.pytest.ini_options]` with `pythonpath = ["."]` and `testpaths = ["tests"]`, so that `python -m pytest -q` collects `tests/` and imports `meeting_cost` from the project root.

## Phase 2: Data types

- [x] **T002** In `meeting_cost/calculator.py`, define `InvalidInputError(ValueError)` carrying a `field` attribute and a message that repeats the field name.
- [x] **T003** In `meeting_cost/calculator.py`, define the frozen dataclasses `AttendeeCost(hourly_rate: Decimal, cost: Decimal)` and `MeetingCost(duration_minutes: Decimal, breakdown: tuple[AttendeeCost, ...], total: Decimal)`, and the constants `MINUTES_PER_HOUR = Decimal(60)` and `TOTAL_EXPONENT = Decimal("0.01")`.

## Phase 3: Calculation logic

- [x] **T004** Implement `parse_duration(value)`: convert to `Decimal`, raise `InvalidInputError("duration", ...)` when the value is not a finite number, and raise it again when the value is negative.
- [x] **T005** Implement `parse_rate(value, position)`: same conversion, with the field name `rate <position>` so the message names which attendee's rate was rejected.
- [x] **T006** Implement `round_total(amount)` as `amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`.
- [x] **T007** Implement `calculate(duration_minutes, hourly_rates)`: validate the duration, validate each rate in order, compute `hours = duration / 60`, build one unrounded `AttendeeCost` per rate, sum the costs and return a `MeetingCost` whose `total` is the rounded sum.
- [x] **T008** Export the public surface from `meeting_cost/__init__.py` without importing `meeting_cost.cli`.

## Phase 4: Calculation tests

- [x] **T009** In `tests/test_calculator.py`, assert `calculate("60", ["100", "80", "60"]).total == Decimal("240.00")`.
- [x] **T010** Assert `calculate("30", ["90"]).total == Decimal("45.00")`.
- [x] **T011** Assert the rounded sum of the breakdown costs equals the reported total, on a duration that does not divide the hour evenly.
- [x] **T012** Assert the breakdown reports one entry per attendee carrying that attendee's rate and its cost.
- [x] **T013** Assert the rounding rule: a total of `0.125` reports `0.13`, and a breakdown value keeps its full unrounded precision.
- [x] **T014** Assert `total`, every `cost` and every `hourly_rate` is a `Decimal`.
- [x] **T015** Assert zero attendees gives an empty breakdown and a total of `0.00`, and a duration of zero gives a cost of `0` per attendee and a total of `0.00`.
- [x] **T016** Assert a negative duration raises `InvalidInputError` with `field == "duration"`, and a negative rate raises it with the field naming that rate's position.
- [x] **T017** Assert a non-numeric duration, a non-numeric rate, a `nan` rate and an empty rate each raise `InvalidInputError` naming the offending field rather than being coerced.

## Phase 5: Command line wrapper

- [x] **T018** In `meeting_cost/cli.py`, implement `build_parser()` with a positional `duration` and a variadic positional `rates`, so that the zero attendee case is expressible on the command line.
- [x] **T019** Implement `format_report(result)`: the duration, the attendee count, one line per attendee showing the rate and the unrounded cost, and a final `Total:` line showing the rounded total with no currency symbol.
- [x] **T020** Implement `main(argv=None)`: parse, call `calculate`, print the report and return `0`; on `InvalidInputError` print `error: <message>` to standard error, print nothing to standard output and return `1`.
- [x] **T021** Add `meeting_cost/__main__.py` that calls `sys.exit(main())`, so `python -m meeting_cost 60 100 80 60` runs.

## Phase 6: Command line tests

- [x] **T022** In `tests/test_cli.py`, assert `main(["60", "100", "80", "60"])` returns `0` and prints all three attendee lines and `Total: 240.00`, and that `main(["30", "90"])` returns `0` and prints `Total: 45.00`.
- [x] **T023** Assert `main(["60"])` returns `0` and prints `Attendees: 0` and `Total: 0.00`, and that `main(["0", "100", "80"])` returns `0` and prints `Total: 0.00`.
- [x] **T024** Assert `main(["-30", "100"])` returns a non-zero code, writes `duration` to standard error and writes nothing to standard output.
- [x] **T025** Assert `main(["30", "100", "-80"])` and `main(["30", "eighty"])` each return a non-zero code and name the offending rate on standard error.
- [x] **T026** Assert through a subprocess that `python -m meeting_cost 60 100 80 60` exits `0` printing `Total: 240.00`, and that `python -m meeting_cost -30 100` exits non-zero naming `duration`.
- [x] **T027** Assert through a subprocess that importing `meeting_cost.calculator` leaves `meeting_cost.cli` absent from `sys.modules`.

## Acceptance criteria coverage

| Criterion | Tasks |
| --- | --- |
| AC-1: 60 minutes at 100, 80 and 60 totals 240 | T007, T009, T022, T026 |
| AC-2: 30 minutes at 90 totals 45 | T007, T010, T022 |
| AC-3: the breakdown sums to the total | T007, T011, T012 |
| AC-4: the wrapper prints total and breakdown and exits 0 | T019, T020, T021, T022, T023, T026 |
| AC-5: invalid input exits non-zero naming the field | T004, T005, T016, T017, T020, T024, T025, T026 |

## Edge case coverage

| Edge case | Tasks |
| --- | --- |
| Zero attendees | T018, T015, T023 |
| Duration of zero minutes | T015, T023 |
| Negative duration or negative hourly rate | T004, T005, T016, T024, T025 |
| Non-numeric hourly rate | T005, T017, T025 |
