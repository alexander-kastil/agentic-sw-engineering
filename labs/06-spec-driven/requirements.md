# Feature Brief: Meeting Cost Calculator

This is the raw feature request you hand to `/speckit.specify` in step 3 of the lab. It is written the way a product owner would write it: clear about intent, deliberately silent on a few details you will have to resolve.

## Request

Teams keep scheduling recurring meetings without knowing what they cost. Build a small library with a command line wrapper that calculates what a meeting costs in salary time, so an organizer can see the number before they hit send.

An organizer supplies the meeting length and the list of attendees with their hourly rates. The tool returns the total cost and a per attendee breakdown. It runs locally, takes no network calls, and has no database.

## User stories

- As a meeting organizer, I enter a duration and a list of attendee hourly rates, so I can see the total salary cost of the meeting before scheduling it.
- As a meeting organizer, I see the cost contributed by each attendee, so I can tell whether the expensive people actually need to be in the room.
- As a team lead, I run the tool for a recurring meeting and multiply by the occurrences per year, so I can decide whether to cancel it.

## Acceptance criteria

- A meeting of 60 minutes with three attendees at 100, 80 and 60 per hour returns a total of 240.
- A meeting of 30 minutes with one attendee at 90 per hour returns a total of 45.
- The per attendee breakdown sums to the total.
- The command line wrapper prints the total and the breakdown, and exits with code 0 on success.
- Invalid input exits with a non-zero code and a message naming the offending field.

## Constraints

- No network calls, no database, no external service.
- Standard library only, apart from the test framework.
- The calculation logic is importable on its own, separate from the command line wrapper.

## Edge cases to handle

- Zero attendees.
- A duration of zero minutes.
- A negative duration or a negative hourly rate.
- A non-numeric hourly rate.

## Deliberately unstated

The brief does not say how to round the result, and it does not say what currency the numbers are in. Both matter to the implementation. Resolve them in `spec.md` during step 3 rather than letting the agent decide silently during `/speckit.implement`. That decision, made in writing at the specify checkpoint, is the point of the lab.
