# Leave Days Constitution

## Core Principles

### I. Separation of Concerns

Calculation logic MUST NOT import the command line layer, read files or print. The calculation is importable and testable on its own, so the portal can call it directly.

### II. No Hidden Dependencies

The runtime MUST use the Python standard library only; `pytest` is the single permitted development dependency. Any other package requires a written rationale in `plan.md`.

### III. Explicit Failure

Invalid input MUST raise a named error identifying the offending field. Nothing is silently coerced, defaulted or skipped.

### IV. Leave Is Counted in Exact Half Days

Day counts MUST use `decimal.Decimal`. Binary floating point and integer day counts are not acceptable, because a half day has to survive every sum exactly.

### V. Every Acceptance Criterion Has a Test

A criterion in `spec.md` without a corresponding test is an incomplete task.

### VI. Holidays Are Data

No holiday date may appear in source code. Holidays come only from the file HR supplies, so a new year or a new office is a data change, never a code change.

## Governance

`/speckit-plan` MUST verify every principle individually in its Constitution Check. A violation is fixed in the plan, or justified in writing; it is never left for implementation to discover.

**Version**: 1.0.0 | **Ratified**: 2026-09-24
