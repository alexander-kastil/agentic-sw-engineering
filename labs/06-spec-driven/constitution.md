# Constitution Input

Paste this into `/speckit.constitution` in step 2 of the lab. It is deliberately short: a constitution states the non-negotiables, not every preference. Everything here is checkable, so you can hold the plan and the generated code against it later.

## Principles

1. **Separation of concerns.** Calculation logic never imports the command line layer. The logic module is importable and testable without invoking the CLI.
2. **No hidden dependencies.** Standard library only, apart from the test framework. Adding any other package requires a written rationale in `plan.md`.
3. **Explicit failure.** Invalid input produces a named error identifying the offending field. Nothing is silently coerced, defaulted, or clamped.
4. **Money is never a float.** Currency amounts use a decimal or integer minor-unit type. Binary floating point is not acceptable for a monetary result.
5. **Every acceptance criterion has a test.** A criterion in `spec.md` without a corresponding test is an incomplete task.
6. **Offline by default.** No network calls, no filesystem writes outside the project directory.

## How the agent uses this

Once the constitution is in place, `/speckit.plan` verifies its proposal against these principles and states the verification explicitly. If the plan proposes a float for the total, or a package outside the standard library with no rationale, that is a constitution violation you should catch at the plan checkpoint rather than after the code is written.
