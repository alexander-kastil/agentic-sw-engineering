# Feature Specification: Leave Days Preview

**Status**: accepted at the specify checkpoint
**Input**: [requirements.md](./requirements.md)

## User Scenarios & Testing

### User Story 1: See the cost before submitting (Priority: P1)

As an employee, I enter the first and last day of my leave, so I can see how many allowance days it costs before I submit.

**Independent test**: a request for Monday 14 to Friday 18 December 2026 reports 5 days.

### User Story 2: Holidays and weekends cost nothing (Priority: P1)

As an employee, I see that public holidays and weekends inside my leave cost me nothing, so I can plan around them.

**Independent test**: a request for Monday 21 to Friday 25 December 2026 reports 3.5 days.

### User Story 3: One holiday file (Priority: P2)

As an HR administrator, I maintain the office's holidays in one file, including the company's half days, so the portal and payroll agree.

**Independent test**: changing the file changes the result with no code change.

### Edge Cases

| Case | Behavior |
| --- | --- |
| Last day before first day | Invalid. Error names `end`. |
| A date that is not a real calendar date | Invalid. Error names `start` or `end`. |
| Malformed or duplicated holiday line | Invalid. Error names `holidays line N`. |
| Request containing only weekend days | Valid. Deducts 0. |
| Holiday falling on a weekend | Valid. The day already costs 0; it is not deducted twice. |
| First day equals last day | Valid. The single day is counted. |

## Requirements

### Functional Requirements

- **FR-001**: The request is the first and last day of leave; both days are included.
- **FR-002**: Saturdays and Sundays deduct 0.
- **FR-003**: A full holiday deducts 0; a half day deducts 0.5; every other weekday deducts 1.
- **FR-004**: Holidays are read from HR's file: one ISO date per line, optionally followed by `half`; blank lines are ignored.
- **FR-005**: The result reports the days deducted per calendar year and the total.
- **FR-006**: A request touching a calendar year for which the holiday file has no entry is rejected, naming `holidays`.
- **FR-007**: Invalid input is rejected with an error naming the offending field; nothing is coerced or skipped.
- **FR-008**: The calculation is available without the command line wrapper.

## Success Criteria

| ID | Criterion |
| --- | --- |
| SC-001 | Monday 14 to Friday 18 December 2026 deducts 5. |
| SC-002 | Monday 21 to Friday 25 December 2026 deducts 3.5. |
| SC-003 | A Saturday and Sunday only deducts 0. |
| SC-004 | The wrapper prints the deducted days and exits 0 on success. |
| SC-005 | Invalid input exits non-zero with a message naming the field. |
| SC-006 | Monday 28 December 2026 to Friday 8 January 2027 deducts 3.5 from 2026 and 4 from 2027, 7.5 in total. |

## Resolved Gaps

The brief left two decisions open. Both are decided here, in writing, before any plan exists.

### A request across New Year

Allowances are per calendar year, and the brief did not say which year a request spanning New Year is charged to. Decision: each day is charged to its own calendar year, and the result reports the split (FR-005, SC-006).

### A year the holiday file does not cover

HR publishes the file one year at a time. Counted against a file that ends in December, 1 and 6 January would become working days and the preview would overcharge by two days without any error. Decision: a request touching a year with no entries is rejected (FR-006).

## Assumptions

- The office works Monday to Friday.
- Half days exist only where HR's file marks them.

## Out of Scope

- The remaining allowance balance, approval workflow and payroll export.
- Part-time schedules.
