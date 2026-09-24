# Tasks: Leave Days Preview

**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Phase 1: Setup

- [x] T001 Create `leave_days/`, `tests/` and `pyproject.toml` with `pythonpath = ["."]` and `testpaths = ["tests"]`
- [x] T002 [P] Add `holidays-2026.txt` and `holidays-2026-2027.txt` in HR's format

## Phase 2: Foundational

- [x] T003 Define `InvalidInputError`, `HolidayCalendar`, `YearCharge` and `LeaveCharge` in `leave_days/calculator.py`
- [x] T004 Implement `parse_holidays(lines)`: full and `half` entries, blank lines ignored, malformed or repeated lines rejected as `holidays line N`

## Phase 3: User Stories 1 and 2 (P1)

- [x] T005 [P] [US1] Test SC-001 and the single-day edge case in `tests/test_calculator.py`
- [x] T006 [P] [US2] Test SC-002, SC-003 and the holiday-on-a-weekend edge case in `tests/test_calculator.py`
- [x] T007 [US1] Test SC-006: the per-year split and that the years sum to the total
- [x] T008 [US1] Test the `end` before `start` and malformed date edge cases, and the missing-year rejection
- [x] T009 [US1] Implement `charge_leave` in `leave_days/calculator.py` until T005 to T008 pass

## Phase 4: User Story 3 (P2)

- [x] T010 [US3] Test malformed and duplicated holiday lines name their line number
- [x] T011 [US3] Test that no holiday date literal appears in `calculator.py`

## Phase 5: Command line wrapper

- [x] T012 Test in `tests/test_cli.py`: per-year and total output with exit 0 (SC-004); invalid input on standard error with exit 1 (SC-005); unreadable holiday file names `holidays`
- [x] T013 Implement `build_parser`, `format_report` and `main` in `leave_days/cli.py`, and `leave_days/__main__.py`
- [x] T014 Test through a subprocess that `python -m leave_days` runs and that importing the calculator does not load the CLI

## Coverage

| Criterion or edge case | Tasks |
| --- | --- |
| SC-001 plain week | T005, T009 |
| SC-002 Christmas week | T006, T009 |
| SC-003 weekend only | T006, T009 |
| SC-004 wrapper success | T012, T013, T014 |
| SC-005 wrapper failure | T012, T013 |
| SC-006 across New Year | T007, T009 |
| End before start, malformed date | T008 |
| Year not covered by the file | T008 |
| Malformed or duplicated holiday line | T004, T010 |
