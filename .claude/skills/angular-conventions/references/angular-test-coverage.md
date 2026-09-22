# Angular test coverage: measuring it and reading the gaps

Where the untested code actually is, and which coverage signals mean something.
Running the suite: [`angular-test-execution`](angular-test-execution.md).

## Coverage goals

Target 80%+ coverage. Prioritize:

1. Happy path scenarios
2. Error handling and edge cases
3. User interactions and emitted outputs
4. Service integration points
5. State transitions

## Measuring coverage

The provider is not installed by default; `--coverage` fails with "Code coverage requires either
`@vitest/coverage-v8` or `@vitest/coverage-istanbul` to be installed". Install the provider at the
**same version as the resolved `vitest`** (check `npm ls vitest`, which may resolve through
`@angular/build`):

```bash
npm i -D @vitest/coverage-v8@<vitest version>
npx ng test --watch=false --coverage --coverage-reporters=text-summary --coverage-reporters=json-summary
```

The JSON lands in `coverage/<angular-project-name>/coverage-summary.json`, **not** `coverage/`.
Requiring `./coverage/coverage-summary.json` fails with MODULE_NOT_FOUND; locate it before parsing.

Rank gaps by uncovered-statement COUNT (`statements.total - statements.covered`), not by percentage.
A 40%-covered 8-line file is noise; a 74%-covered template with 178 uncovered statements is the
single biggest win in the codebase.

### Never infer "untested" from a missing `<name>.spec.ts`

Listing source files with no adjacent same-stem spec massively over-reports gaps, because specs are
routinely named for the *concept* rather than the file: `with-tasks.feature.ts` is covered by
`with-tasks.spec.ts`, not `with-tasks.feature.spec.ts`. That heuristic flagged a dozen thoroughly
tested store features as having zero coverage. Measure, then rank; do not infer from filenames.

Skip files with no executable logic: interfaces, DTOs, enums, type-only modules, directives whose
whole body is static `host` metadata. A spec there restates the type and buys no coverage.

## A `.html` file at ~0% functions means the tests never touched the DOM

Angular compiles a template into a module with a function per event-listener closure, so coverage
reports the `.html` file separately. A template showing decent statement coverage but near-zero
function coverage is a precise, mechanical signal:

```
74.6% stmts /  1.81% functions   <- every (click), (change), (keydown) handler never fired
```

The tests are calling component methods directly (`component.onSave()`), which covers the `.ts` and
leaves every listener closure cold. The fix is to drive real events and assert rendered output:

```typescript
fixture.nativeElement.querySelector('[data-testid="save"]').click();
fixture.detectChanges();
expect(store.save).toHaveBeenCalled();
```

This one shift moved function coverage across an app from 71% to 87%. Also drive the template's
control-flow branches (`@if` / `@for` / `@empty` / `@switch`) by setting state and asserting the DOM.
Untriggered blocks are where the missing statement coverage lives.

**In a zoneless app you must dispatch the real event, not call the handler.** Component state held in
a plain field (not a signal) repaints only because the writer was a template listener that marked the
view dirty. Calling that same method programmatically does not repaint, even after
`fixture.detectChanges()`, so template-branch tests have to go through dispatched events.
