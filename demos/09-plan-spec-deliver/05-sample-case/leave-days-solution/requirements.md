# Feature Brief: Leave Days Preview

Written by the product owner of the HR self-service portal. This is the text handed to `/speckit-specify`.

## Request

Employees keep submitting leave requests and only learn afterwards how many days HR deducted from their annual allowance. Christmas week is the worst: public holidays, the company's half days and weekends all overlap, and the questions land in the HR inbox every January. Show the number before the employee submits.

Build a small library with a command line wrapper. It takes the first and last day of the leave and the holiday file HR already publishes for the office, and returns the working days the request deducts.

## User stories

- As an employee, I enter the first and last day of my leave, so I can see how many allowance days it costs before I submit.
- As an employee, I see that public holidays and weekends inside my leave cost me nothing, so I can plan around them.
- As an HR administrator, I maintain the office's holidays in one file, including 24 and 31 December, which are half working days at our company, so the portal and payroll agree.

## Acceptance criteria

- Monday 14 to Friday 18 December 2026 deducts 5 days.
- Monday 21 to Friday 25 December 2026 deducts 3.5 days: 24 December is a half day and 25 December is a holiday.
- A request that includes only a Saturday and a Sunday deducts 0 days.
- The command line wrapper prints the deducted days and exits with code 0 on success.
- Invalid input exits with a non-zero code and a message naming the offending field.

## Constraints

- Runs locally: no network calls, no database.
- Standard library only, apart from the test framework.
- HR's holiday file format stays as it is: one ISO date per line, followed by `half` for a half day.

## Edge cases to handle

- The last day is before the first day.
- A date that is not a real calendar date.
- A malformed or duplicated line in the holiday file.
