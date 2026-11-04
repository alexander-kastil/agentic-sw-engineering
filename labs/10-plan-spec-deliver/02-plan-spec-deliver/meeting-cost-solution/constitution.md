# Meeting Cost Calculator Constitution

Ratified at the constitution checkpoint of the lab. These are non-negotiables. Every plan, task list and change is checked against them, and a violation blocks the work rather than producing a follow-up item.

## Core Principles

### I. Separation of Concerns

Calculation logic MUST NOT import the command line layer. The logic module MUST be importable and testable without invoking the CLI. A test that exercises the calculation MUST be able to run without touching argument parsing, process exit codes or standard streams.

### II. No Hidden Dependencies

The runtime MUST use the standard library only. The test framework is the single permitted exception. Any further package MUST carry a written rationale in `plan.md` before it is added, and a package added without that rationale MUST be removed.

### III. Explicit Failure

Invalid input MUST produce a named error identifying the offending field. Nothing is silently coerced, defaulted or clamped. A value that cannot be interpreted MUST stop the operation, and the error MUST reach the caller carrying the field name.

### IV. Money Is Never a Float

Currency amounts MUST use a decimal or integer minor-unit type. Binary floating point MUST NOT be used for a monetary result, an intermediate monetary value or a rate. A monetary value that reaches an interface as a binary float is a defect regardless of how it prints.

### V. Every Acceptance Criterion Has a Test

Every acceptance criterion in `spec.md` MUST have at least one corresponding automated test. A criterion without a test is an incomplete task, not a passing one. A task list that leaves a criterion untested MUST be corrected before implementation starts.

### VI. Offline by Default

The tool MUST make no network calls. It MUST NOT write to the filesystem outside the project directory. There is no database, no cache directory and no external service.

## Governance

This constitution supersedes any convenience argument raised during planning or implementation. `plan.md` MUST carry a Constitution Check section that states, principle by principle, how the proposal complies. An implementation step that would violate a principle stops and the plan is amended first.

**Version**: 1.0.0 | **Ratified**: 2026-09-21 | **Last Amended**: 2026-09-21
