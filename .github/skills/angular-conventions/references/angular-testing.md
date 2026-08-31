# Writing Angular specs with Vitest

Author unit tests for Angular components, services, guards and signals with Vitest and `TestBed`.

This leaf answers "how do I write a spec for this thing". Three siblings answer the other questions:

| Arrival question | Leaf |
| --- | --- |
| How do I run the suite, and why does the run look wrong? | [`angular-test-execution`](angular-test-execution.md) |
| Where are the coverage gaps and how do I close them? | [`angular-test-coverage`](angular-test-coverage.md) |
| The spec fails for a reason that is not the code under test | [`angular-test-doubles`](angular-test-doubles.md) |

## File Structure

Create `.spec.ts` files adjacent to source files. Use `describe`/`it` blocks with names that describe behavior, not implementation.

```
user-list.component.ts
user-list.component.spec.ts
user.service.ts
user.service.spec.ts
```

A spec is routinely named for the *concept* rather than the file: `with-tasks.feature.ts` is covered by
`with-tasks.spec.ts`. Never read a missing same-stem spec as missing coverage; see
[`angular-test-coverage`](angular-test-coverage.md).

## Component Testing

Test signal inputs, outputs, and user interactions. Mock services via `TestBed.configureTestingModule`.

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { UserListComponent } from './user-list.component';
import { UserService } from './user.service';
import { describe, it, expect, beforeEach } from 'vitest';
import { of } from 'rxjs';

describe('UserListComponent', () => {
  let component: UserListComponent;
  let fixture: ComponentFixture<UserListComponent>;
  let userService: { getUsers: ReturnType<typeof vi.fn> };

  beforeEach(async () => {
    userService = { getUsers: vi.fn().mockReturnValue(of([])) };

    await TestBed.configureTestingModule({
      imports: [UserListComponent],
      providers: [{ provide: UserService, useValue: userService }],
    }).compileComponents();

    fixture = TestBed.createComponent(UserListComponent);
    component = fixture.componentInstance;
  });

  it('renders users when input is provided', () => {
    const users = [{ id: 1, name: 'Alice' }];
    fixture.componentRef.setInput('users', users);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Alice');
  });

  it('emits selected user on card click', () => {
    const user = { id: 1, name: 'Alice' };
    fixture.componentRef.setInput('users', [user]);
    fixture.detectChanges();

    const emitted: unknown[] = [];
    component.selected.subscribe((v) => emitted.push(v));

    fixture.nativeElement.querySelector('app-user-card').click();
    expect(emitted).toEqual([user]);
  });
});
```

Drive real events rather than calling handlers: `querySelector(...).click()` covers the template's
listener closures, `component.onSave()` does not. In a zoneless app the dispatched event is also the
only thing that repaints a plain (non-signal) field.

## `provideRouter` for `routerLink` templates

`TestBed.createComponent` instantiates the component's template directives. A template using
`routerLink`/`routerLinkActive` fails with `NG0201: No provider found for ActivatedRoute` unless the
router is provided. Add `provideRouter([])`:

```typescript
import { provideRouter } from '@angular/router';

TestBed.configureTestingModule({
  providers: [
    provideRouter([]),
    { provide: SomeStore, useValue: storeMock },
  ],
});
```

For pure logic checks (method delegation, signal wiring), read `createComponent(X).componentInstance`
directly without `detectChanges()`: the constructor and field initializers still run.

## Service Testing

The `provideHttpClient()` + `provideHttpClientTesting()` setup and the request/flush examples live in
[`angular-http`](angular-http.md) under "Testing HTTP". Two rules that section does not state:

- Call `httpMock.verify()` in `afterEach` of **every** HTTP spec, not just the first one.
- Match requests that carry query parameters with the predicate overload, never a bare path string.
  Both the failure it produces and the fix are in [`angular-test-doubles`](angular-test-doubles.md).

## Functional Guard / Resolver Testing

Functional guards (`CanActivateFn`, `CanMatchFn`) call `inject()`, so run them inside `TestBed.runInInjectionContext`. Mock `MsalService` via its `instance` shape and `Router` via `parseUrl`, then assert the boolean or the returned `UrlTree`.

```typescript
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { MsalService } from '@azure/msal-angular';
import { describe, it, expect, afterEach, vi } from 'vitest';
import { canMatchAuth } from './msal-auth.guard';

function configure(activeAccount: unknown, accounts: unknown[]) {
  const msalMock = { instance: { getActiveAccount: () => activeAccount, getAllAccounts: () => accounts } };
  const urlTree = { redirectTo: '/' };
  const routerMock = { parseUrl: vi.fn(() => urlTree) };
  TestBed.configureTestingModule({
    providers: [
      { provide: MsalService, useValue: msalMock },
      { provide: Router, useValue: routerMock },
    ],
  });
  return { routerMock, urlTree };
}

const run = () => TestBed.runInInjectionContext(() => canMatchAuth({} as never, [] as never));

describe('canMatchAuth', () => {
  afterEach(() => TestBed.resetTestingModule());

  it('allows access when an account exists', () => {
    configure({ username: 'a@b.at' }, []);
    expect(run()).toBe(true);
  });

  it('redirects a logged-out user to /', () => {
    const { routerMock, urlTree } = configure(null, []);
    expect(run()).toBe(urlTree);
    expect(routerMock.parseUrl).toHaveBeenCalledWith('/');
  });
});
```

If the guard reads `isAuthEnabled()` (which checks `environment.authEnabled` and a `localStorage` flag), set/clear that `localStorage` key per-test in `afterEach` to exercise both the enabled and disabled branches.

## Signal Testing

Test computed values and effects directly, no TestBed needed.

```typescript
import { signal, computed } from '@angular/core';
import { describe, it, expect } from 'vitest';

describe('signal computation', () => {
  it('updates computed value when source changes', () => {
    const count = signal(0);
    const doubled = computed(() => count() * 2);

    expect(doubled()).toBe(0);
    count.set(5);
    expect(doubled()).toBe(10);
  });
});
```

## Async Testing

Use `fakeAsync` + `tick` for synchronous time control. Use the `done` callback for observable-based assertions.

```typescript
import { fakeAsync, tick } from '@angular/core/testing';

it('loads data after delay', fakeAsync(() => {
  component.load();
  tick(200);
  expect(component.data()).toBeDefined();
}));

it('subscribes to observable', (done) => {
  service.getData().subscribe((v) => {
    expect(v).toBeTruthy();
    done();
  });
});
```
