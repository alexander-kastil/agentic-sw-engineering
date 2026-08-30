# Running an Angular Vitest suite, and reading the run

How to invoke the suite, how to scope it, and how to tell a broken runner from a broken test.
Writing the specs themselves: [`angular-testing`](angular-testing.md).

## Run tests through the Angular builder, never raw Vitest

Use `ng test` (or `npm test`). Do **not** run `npx vitest run` directly, even though the specs import
from `vitest` and a `vitest` binary is present in `node_modules`.

```bash
ng test --watch=false     # correct
npx vitest run            # wrong, fails before a single test executes
```

Raw Vitest skips Angular's build step, so the partially-compiled Angular packages are never processed
by the Angular Linker and the first Angular injectable that is touched throws:

```
Error: The injectable 'PlatformLocation' needs to be compiled using the JIT compiler,
but '@angular/compiler' is not available.
```

This is a **harness error, not a test failure**: it reports `Test Files 1 failed`, `Tests no tests`,
and the stack points into `node_modules/@angular/common`, not into any spec. Read those three signals
together before concluding the code is broken. A suite that fails with zero tests executed and a stack
inside `@angular/*` means the runner was invoked wrongly. `ng test` builds first (`Application bundle
generation complete`) and then hands the bundle to Vitest, which is why the same specs pass under it.

The message varies with which part of the bundle is missing; the shape does not. On a workspace on the
`@angular/build:unit-test` builder, `npx vitest run` produced ~111 identical failures reading
`Need to call TestBed.initTestEnvironment() first`, one per spec file, because the builder is what
loads the test-environment setup and the raw runner never ran it. **Read the uniformity, not the
message: every file failing, and all in the same way, is a runner problem.** A real defect fails a
few files with different errors.

## Scoping a run: `--include`, never `--filter`

`@angular/build:unit-test` accepts `--filter`, but it matches **test names, not file paths**. Passing a
path fragment therefore selects whichever unrelated tests happen to have that word in their `it(...)`
title, and reports every other file skipped rather than erroring:

```
npx ng test --no-watch --filter="employee-edit"
  ->  Test Files  120 skipped (120)      # looks green, ran nothing

npx ng test --no-watch --filter="sort"
  ->  Test Files  4 passed | 116 skipped # WORSE: a partial match that looks like it worked
```

That second shape is the trap. A few tests really do run, so the output has green in it and reads as
confirmation that the flag works, while the suite you meant to scope to never executed. A glob is no
better (`--filter="**/x/**"` -> `SyntaxError: Invalid regular expression: Nothing to repeat`), because
the value is a regex over names. Use `--include`, which does take paths:

```bash
npx ng test --no-watch --include "src/app/<feature>/<name>.component.spec.ts"
npx ng test --no-watch          # whole suite
```

**A skipped-everything run reads as a pass, and a partly-skipped run reads as a scoped pass.**
`120 skipped (120)`, `4 passed | 116 skipped`, and `38 passed` all show no red. Always read the
executed test COUNT against the number of specs you expected to run, and when reporting a scoped run,
state how many tests actually ran, otherwise "tests pass" can mean "almost nothing executed".

**Verify the flag before building a plan on it.** A single probe whose output merely lacks red is not
evidence the scoping worked; this exact `--filter` mistake was propagated into six parallel agent
prompts on the strength of one green-looking run, in a repo whose own skill already documented it.

## `ng test` type-checks the whole spec program

The builder type-checks every spec in `tsconfig.spec.json` before running anything, so **one broken
spec anywhere fails everybody's run**, including runs scoped to unrelated folders. `--exclude` does
not remove a file from the type-check, so it cannot be used to route around a broken file.

The escape hatch is a temporary tsconfig whose `include` is narrowed to your specs, passed via
`--ts-config`. Delete it and its `out-tsc` output when done.

This matters most with parallel agents: a compile error one agent introduces blocks every other
agent's verification until fixed. When a run fails in files outside your scope, check whether the
error is even yours before "fixing" it.

## "Scope tests to what changed" does not survive a shared-type change

Running only the specs for files you edited assumes the blast radius equals the diff. Widening a
shared model (adding a field to a DTO, entity, or interface used across features) breaks that
assumption: every spec that constructs a literal of that type is now in scope, and those live in
unrelated features that never appear in your diff.

After changing a shared type, run the FULL suite once before declaring done. A subagent that reports
green "across the files I touched" has told you nothing about the suite.

## Fix the file whose teardown fails first, not the file with the most red

One spec whose `afterEach` throws (typically `httpMock.verify()` reporting an unmatched request) can
cascade into dozens of failures in other files, because the leaked state outlives the file that
created it: a single broken `msal.auth.spec.ts` produced roughly 40 downstream failures across the
suite. Sort the failures by file, find the one failing in teardown rather than in an assertion, fix
that, and re-run before triaging anything else. The unmatched-request diagnosis itself is in
[`angular-test-doubles`](angular-test-doubles.md).
