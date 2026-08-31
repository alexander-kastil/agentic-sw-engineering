# Angular Signal Store Design (`@ngrx/signals`)

How to design application state so a **single composed signal store fully serves the app** — state *and* data access — with components binding to it directly or through a container/presenter split. The only things that stay outside the store are auth (MSAL), cross-cutting utility services, and deliberately backend-less caches.

Reference implementations: `src/ui/src/app/store/app.store.ts` (this repo), `citythong-members/.../store/members.store.ts`, `vouchers-ai/.../store/vouchers.store.ts`.

## Core shape

One `signalStoreFeature()` per domain, composed into a single root `signalStore({ providedIn: 'root' })`.

```ts
// store/app.store.ts
export const AppStore = signalStore(
  { providedIn: 'root', protectedState: false },
  withState(initialAppState),   // base shell state (testing, invited, …)
  withMethods(/* base methods */),
  withActivity(),               // cross-cutting slices first (see angular-activity-indicator)
  withSidenav(),
  withTasks(),                  // task authoring AND the task planner live in ONE slice
  withPlanning(),               // scheduling grid, mailing AND timesheet — one planning domain
  withResources(),
  // …one with<Domain>() per feature area
);
```

Rules:
- **One file per domain:** `store/features/with-<domain>.feature.ts`, colocated `with-<domain>.spec.ts`.
- Each feature = `withState` (+ `withComputed` for derived signals) + `withMethods`.
- State mutations go through `patchState(store, { … })` — never assign signals directly.
- Compose everything into ONE root store. Do **not** create parallel `providedIn: 'root'` domain stores or services-with-`BehaviorSubject`.

### Getting the granularity right — one slice per DOMAIN, not per screen

A "domain" is a cohesive area of the app, not an individual view. Over-splitting is as wrong as under-binding:

- **Don't split one domain across several slices.** The task *planner* is part of the *tasks* domain → it belongs in `withTasks`, not a separate `withTaskPlanner`. The *timesheet* is part of *planning* → it belongs in `withPlanning`, not a separate `withTimesheet`. If two slices only ever change together or one wraps a subset of the other's service, they are one domain — merge them. (Merging is a pure internal move: because every method lives on the single composed `AppStore`, moving definitions between feature functions does **not** change the public API, so component consumers need no changes — the build proves it.)
- **Don't split a domain across a feature slice AND a companion service.** State that belongs in the store must not live in a `providedIn: 'root'` service that mutates the store from the outside. The sidenav was state (`sideNavVisible/Position/Collapsed`) sitting inline in base state with a separate `SideNavService` doing the responsive bootstrap — the correct shape is a single `withSidenav()` slice that owns both the state and the bootstrap (see `withHooks` below). Once the slice owns it, the service is dead code — delete it.

### Lifecycle/bootstrap logic → `withHooks(onInit)`, not a service constructor

Bootstrap side-effects a slice needs (responsive layout, a one-time seed, a subscription) go in the slice's `withHooks({ onInit })`, which runs when the store is first constructed — you can `inject()` inside it:

```ts
withHooks({
  onInit(store) {
    const destroyRef = inject(DestroyRef);
    const mq = window.matchMedia('(max-width: 959.98px)');
    const apply = (mobile: boolean) => patchState(store, {
      sideNavVisible: !mobile, sideNavPosition: mobile ? 'over' : 'side',
    });
    apply(mq.matches);
    const listener = (e: MediaQueryListEvent) => apply(e.matches);
    mq.addEventListener('change', listener);
    destroyRef.onDestroy(() => mq.removeEventListener('change', listener));
  },
})
```

**jsdom test gotcha:** once a root slice's `onInit` touches `window.matchMedia`, that runs on **every** `AppStore` construction across the whole spec suite, and jsdom has no `matchMedia` — add a guarded polyfill to `src/test-setup.ts` (specs that assert responsive behavior override it with `vi.stubGlobal`).

## Feature slice template

```ts
// Generic illustration of slice shape (a made-up "reports" domain).
export interface ReportsState {
  reports: Report[];
  reportsLoading: boolean;
  selected: Report | null;
}

export function withReports() {
  return signalStoreFeature(
    withState<ReportsState>({ reports: [], reportsLoading: false, selected: null }),

    withComputed((store) => ({
      hasReports: computed(() => store.reports().length > 0),
    })),

    // Repo convention: inject the existing feature SERVICE and wrap it.
    withMethods((store, svc = inject(ReportsService)) => ({
      loadReports: rxMethod<ReportsParam>(
        pipe(
          switchMap((param) => {
            patchState(store, { reportsLoading: true });
            return svc.getReports(param).pipe(
              tapResponse({
                next: (reports) => patchState(store, { reports, reportsLoading: false }),
                error: () => patchState(store, { reportsLoading: false }),
              }),
            );
          }),
        ),
      ),
    })),
  );
}
```

## Two HTTP variants — pick per repo convention

**(a) Inject `HttpClient` directly in the feature** (citythong `with-members.feature.ts`). Feature owns the endpoint URLs. Good for greenfield / no existing service.

**(b) Wrap an existing feature service** (this repo — `with-planning.feature.ts` wraps `PlanningService`). Keep the service as the HTTP layer (it owns base URL + endpoints); the slice only manages state and wraps the service methods in `rxMethod`s. **New maintenance-planner slices use (b).**

Both use `rxMethod` + `tapResponse` (`@ngrx/operators`) for async; choose the flattening operator deliberately — `switchMap` (cancel prior), `exhaustMap` (ignore while in-flight, e.g. saves — see `with-planning.feature.ts`), `concatMap` (queue).

### Circular dependency gotcha (variant b)

If the service you wrap **itself injects `AppStore`** (e.g. `ResourcesService` calls `patchState` on the store), the usual eager default-parameter shape `withMethods((store, svc = inject(ResourcesService)) => …)` throws at bootstrap:

```
NG0200: Circular dependency: AppStore -> ResourcesService -> AppStore
```

Resolve the service **lazily** so it isn't constructed until the first method call, which breaks the cycle:

```ts
withMethods((store) => {
  const injector = inject(Injector);
  return {
    saveHouse: rxMethod<{ house: House; onSuccess?: () => void }>(
      pipe(exhaustMap(({ house, onSuccess }) =>
        injector.get(ResourcesService).saveHouse(house).pipe(
          tapResponse({
            next: (saved) => { patchState(store, /* upsert */); onSuccess?.(); },
            error: () => {},
          }),
        ),
      )),
    ),
  };
})
```

Reference: `store/features/with-mail-templates.feature.ts` and `with-resources.feature.ts`. Prefer moving the save→upsert step into the slice (as above) over leaving a `service.save().subscribe(saved => store.upsertX(saved))` in each edit component.

## Component binding

Components consume the store; they do not own domain state.

- **Direct bind:** `private store = inject(AppStore);` then read `store.entries()` / call `store.loadTimesheet(param)`.
- **Container/presenter:** a container `inject`s the store and passes signals down via `input()` to presentational children (reference: `schedule-container` → `scheduler.component` → `scheduler-row`). Presentational children take `input()/output()` only and never inject the store.
- **Resolvers** may patch the store before a route activates (reference: `resources/resolvers/resource.resolvers.ts`).

Anti-patterns this replaces (see `references/angular-antipatterns.md`): plain non-signal class fields for domain data, bare `.subscribe()` in components, manual `ChangeDetectorRef.markForCheck()`, per-component `BehaviorSubject` services, duplicate fetches of the same endpoint from two components (share one slice instead).

## Resets never live in a parallel request's handler

Two `rxMethod`s dispatched together are a race decided by payload size, not by call order. A reset
written into one response handler will stomp state the other has already loaded.

```ts
// WRONG — details is the fatter payload, so it always lands last and wipes the loaded rule
loadDetails: rxMethod<string>(pipe(switchMap(id => service.getDetails(id).pipe(tapResponse({
  next: d => patchState(store, { current: d, currentRule: null, pendingRule: null }),
})))))

// RIGHT — clear synchronously before dispatching, in the one entry path that needs it
onNew() { this.store.clearEdit(); this.store.loadDetails(id); }
```

Symptom: a saved value is present in the network tab and absent on screen, reproducibly, and
"works" whenever the other endpoint is slow. Rules:

- A response handler patches what its own response carries, nothing else.
- A reset that exists to protect one entry path is fixed at that entry path, not on every response.
- Pin it with a spec that flushes the two responses in **both** orders; only the real-world order
  fails, so a single-order test passes against the bug.

## A store method must not read store signals in its `patchState` arguments

A component that loads on an input change writes `effect(() => this.store.load(this.id()))`. Every
signal the method reads **synchronously** becomes a dependency of that effect, so a method that reads
the state it is about to write turns the effect into an infinite request loop.

```ts
// WRONG — store.versionsOf() and store.versions() are read inside the effect's reactive context,
// and the same call writes both. Each response re-runs the effect and fires the next request.
loadVersions(name: string) {
  patchState(store, {
    versions: store.versionsOf() === name ? store.versions() : [],
    versionsOf: name,
    versionsLoading: true
  });
  return service.getVersions(name).pipe(tap(v => patchState(store, { versions: v, versionsLoading: false })), ...);
}

// RIGHT — the updater's `state` is a plain object, not a tracked read
patchState(store, (state) => ({
  versions: state.versionsOf === name ? state.versions : [],
  versionsOf: name,
  versionsLoading: true
}));
```

```ts
// AND at the call site: the effect depends on its inputs only
effect(() => {
  const name = this.secretName();
  untracked(() => this.store.loadVersions(name).subscribe());
});
```

Both halves. The updater form fixes this method; `untracked` at the call site stops the next method
that forgets. Symptom: the page renders correctly and nothing errors — the only evidence is the
network panel filling with the same GET, so check it after wiring any load-on-input effect.

## What stays OUT of the store

- **Auth** — MSAL / `AuthStateService` (the sanctioned exception).
- **Cross-cutting utility services** — download/blob export (`download.service.ts`), telemetry (`app-insights.service.ts`), client-IP utility (`ip-service`). These are stateless helpers, not domain state.
- **Deliberately backend-less caches** — e.g. `home-chat-history.service.ts` (localStorage only, no API). Document each such exception explicitly.

A stateless HTTP proxy service that the store's `rxMethod`s call (e.g. `PlanningService`, `ResourcesService`, `task-chat.service.ts`) is correct — it is the HTTP layer *for* the store, not a competitor to it.

## Testing

Colocate `with-<domain>.spec.ts` next to each feature (reference: `store/features/with-planning.spec.ts`, `with-resources.spec.ts`). Instantiate the feature in a store, mock the injected service, drive methods, assert on the resulting signals.

## Checklist

- [ ] One `with-<domain>.feature.ts` per domain, composed into the single root store.
- [ ] State via `withState` + `patchState`; derived via `withComputed`.
- [ ] Async via `rxMethod` + `tapResponse`, correct flattening operator.
- [ ] New slices wrap the existing feature service (variant b).
- [ ] Components bind to the store (direct or container/presenter); presentational children stay `input()/output()`-only.
- [ ] No domain state in plain class fields, no bare `.subscribe()`, no manual `markForCheck()`.
- [ ] Colocated `*.spec.ts`.
- [ ] Only auth / utility services / documented localStorage caches remain outside the store.
