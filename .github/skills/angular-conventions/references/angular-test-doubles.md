# When the spec fails for a reason that is not the code under test

Mocks, spies and the HTTP testing backend have failure modes of their own, and they report as
assertion failures, missing constructors or "found none" errors that point at healthy code.
Writing specs: [`angular-testing`](angular-testing.md). Reading a whole run:
[`angular-test-execution`](angular-test-execution.md).

## Mocking strategy

Mock external dependencies (services, HTTP). Test in isolation. Verify calls with spies.

```typescript
// Mock the service, not internal implementation
const mockService = { getUsers: vi.fn().mockReturnValue(of([{ id: 1, name: 'Test' }])) };

// Never test private methods
// expect(component['privateMethod']).toHaveBeenCalled(); // wrong
```

## A `vi.mock` factory runs before every `const` in the file

`vi.mock` is hoisted above the imports, so its factory executes at the first import of the mocked
module: earlier than the module body, therefore earlier than every `const` you wrote below it. Three
distinct traps follow from that one fact, and **each one masks the next**, so a single mocked class
can fail three times in a row with three unrelated-looking errors. Apply all three at once.

### 1. No object spread inside the factory

```typescript
vi.mock('@azure/msal-browser', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@azure/msal-browser')>();
  return { ...actual, PublicClientApplication: appMock };   // TypeError: __spreadValues is not a function
});
```

esbuild rewrites the spread into a `__spreadValues` helper that it emits into the module scope, which
the hoisted factory runs before. Use `Object.assign`, which needs no helper:

```typescript
return Object.assign({}, actual, { PublicClientApplication: appMock });
```

### 2. Declare the mock with `vi.hoisted`, not `const`

With the spread fixed, the mock resolves to `undefined` and the code under test throws
`TypeError: PublicClientApplication is not a constructor`. A `const appMock = vi.fn()` below the
`vi.mock` call is still in its temporal dead zone when the factory fires. Hoist the declaration too:

```typescript
const { appMock } = vi.hoisted(() => ({ appMock: vi.fn() }));
```

### 3. A mock that gets `new`-ed needs a `function`, not an arrow

With hoisting fixed it fails again, this time
`TypeError: (config) => ({ config }) is not a constructor`. Arrow functions have no `[[Construct]]`
slot, so `vi.fn().mockImplementation(arrowFn)` cannot be called with `new`:

```typescript
const { appMock } = vi.hoisted(() => ({
  appMock: vi.fn().mockImplementation(function (config: unknown) {
    return { config, getActiveAccount: () => null };
  }),
}));
```

**The rule: when the code under test does `new Mocked(...)`, all three apply.** Write the factory with
`Object.assign`, the double with `vi.hoisted`, and the implementation as a `function` expression, in
one pass. Fixing them one at a time costs three runs, because each error only appears once the
previous one is gone. The correct shape, all three together:

```typescript
import { vi } from 'vitest';

const { appMock } = vi.hoisted(() => ({
  appMock: vi.fn().mockImplementation(function (config: unknown) {
    return { config, getActiveAccount: () => null };
  }),
}));

vi.mock('@azure/msal-browser', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@azure/msal-browser')>();
  return Object.assign({}, actual, { PublicClientApplication: appMock });
});
```

A spec broken this way does not fail an assertion, it fails to **load**, and the runner reports it as
one failed file rather than as a broken mock. That is how such a file stays latent from the day it was
committed: it only surfaces when someone runs the suite to green. Verified end state after the three
fixes: `Test Files 29 passed (29)`, `Tests 311 passed (311)`.

## `expectOne(string)` matches `urlWithParams`, not the path

The string overload of `HttpTestingController.expectOne` compares against the request's
`urlWithParams`. The moment the call carries query parameters, a path-only assertion fails with
"Expected one matching request, found none" while the request is plainly in flight:

```typescript
httpMock.expectOne('/api/secrets/name');   // fails: actual is /api/secrets/name?listId=42
```

Use the predicate overload and assert the parameters explicitly, which is a stronger test anyway:

```typescript
const req = httpMock.expectOne(
  (r) => r.url === '/api/secrets/name' && r.params.get('listId') === listId,
);
```

## Flush the body type the request asked for

A request issued with `responseType: 'blob'` must be flushed with a `Blob`, in the error path as well
as the success path. Flushing a plain string as the error body throws inside the testing backend
itself, so the failure looks like a bug in `HttpClient` rather than in the spec:

```typescript
req.flush(new Blob(['nope']), { status: 404, statusText: 'Not Found' });
```

## An unmatched request fails the file that leaked it, and dozens more

`httpMock.verify()` in `afterEach` throws when a request was issued and never flushed. That failure
happens in teardown, so it can cascade into unrelated files: one leaking spec produced roughly 40
downstream failures across the suite. Triage by teardown, not by volume; see
[`angular-test-execution`](angular-test-execution.md).
