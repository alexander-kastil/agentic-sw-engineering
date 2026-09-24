# Feature Specification: Meeting Cost Calculator

**Status**: accepted at the specify checkpoint
**Input**: the feature brief in [../requirements.md](../requirements.md)

## Overview

An organizer supplies a meeting length and the hourly rate of each attendee. The tool reports what the meeting costs in salary time: a total and a per attendee breakdown. It runs locally, makes no network calls and keeps no data between runs.

## User Scenarios

### US-1: See the total before scheduling

As a meeting organizer, I enter a duration and a list of attendee hourly rates, so I can see the total salary cost of the meeting before scheduling it.

### US-2: See who the cost comes from

As a meeting organizer, I see the cost contributed by each attendee, so I can tell whether the expensive people actually need to be in the room.

### US-3: Judge a recurring meeting

As a team lead, I run the tool for a recurring meeting and multiply by the occurrences per year, so I can decide whether to cancel it.

## Functional Requirements

- **FR-1**: The tool accepts a meeting duration in minutes and zero or more attendee hourly rates.
- **FR-2**: The cost of one attendee is that attendee's hourly rate multiplied by the meeting duration expressed in hours.
- **FR-3**: The total is the sum of the attendee costs.
- **FR-4**: The tool reports the total and the per attendee breakdown together.
- **FR-5**: The tool rejects input it cannot interpret and names the field it rejected.
- **FR-6**: The calculation is available on its own, independently of the way a user invokes the tool.
- **FR-7**: The tool performs no network access, keeps no database and holds no state between runs.

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| AC-1 | A meeting of 60 minutes with three attendees at 100, 80 and 60 per hour returns a total of 240. |
| AC-2 | A meeting of 30 minutes with one attendee at 90 per hour returns a total of 45. |
| AC-3 | The per attendee breakdown sums to the total. |
| AC-4 | The command line wrapper prints the total and the breakdown, and exits with code 0 on success. |
| AC-5 | Invalid input exits with a non-zero code and a message naming the offending field. |

## Edge Cases

| Case | Behaviour |
| --- | --- |
| Zero attendees | Valid input. The breakdown is empty, the total is 0 and the run succeeds with exit code 0. |
| Duration of zero minutes | Valid input. Every attendee contributes 0, the total is 0 and the run succeeds with exit code 0. |
| Negative duration or negative hourly rate | Invalid input. The run stops and exits with a non-zero code, reporting an error that names `duration` or names the offending rate by its position in the attendee list. |
| Non-numeric hourly rate | Invalid input. The run stops, reports an error naming the offending rate by its position in the attendee list, and exits with a non-zero code. |

No invalid value is coerced, defaulted or clamped. The first invalid field encountered stops the run.

## Resolved Gaps

The brief left two decisions open. They are decided here so that nothing is settled silently during implementation.

### Rounding

The total is rounded half up to two decimal places. Breakdown values are kept unrounded and are reported at full precision, so that the reported breakdown sums to the unrounded total and the rounding happens once, on the figure the organizer acts on.

### Currency

Amounts are currency-agnostic decimals. The tool neither accepts nor prints a currency symbol or code, and it applies no conversion. Every rate in one run is assumed to be in the same unit, and the output carries the same unit as the input.

## Out of Scope

- Recurrence arithmetic. US-3 is served by the organizer multiplying a single meeting's total by the occurrences, not by a recurrence input.
- Currency conversion, tax, overheads and non-salary meeting cost.
- Persistence, reporting history and calendar integration.
