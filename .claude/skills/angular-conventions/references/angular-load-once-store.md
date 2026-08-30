# angular-load-once-store — Load-once data loading with local CRUD sync

The data-loading contract for a signal-store-served app: **every collection loads at most once per
app session, and mutations update the store locally from the API response instead of refetching
collections.** Proven by a measured optimization pass (−38% duplicate requests, −36% list-fetch
traffic); pair with the `kpi-driven-optimization` skill for the measurement method, and check the
target repo's own docs for its concrete instance.

## The ensure*Loaded guard pattern

Per collection slice, keep two flags and one guard method:

```ts
withState({ housesLoaded: false, housesLoading: false, houses: [] as House[] }),
withMethods((store) => ({
  ensureHouses(): Observable<boolean> {
    if (store.housesLoaded()) return of(true);          // cache hit — zero HTTP
    if (inFlight) return inFlight;                      // join the in-flight request
    patchState(store, { housesLoading: true });         // set SYNCHRONOUSLY, before subscribe
    inFlight = service.getHouses().pipe(
      tap((houses) => patchState(store, { houses, housesLoaded: true, housesLoading: false })),
      map(() => true),
      finalize(() => (inFlight = null)),
      shareReplay(1),                                    // same-tick callers share ONE request
    );
    return inFlight;
  },
}))
```

Rules that make it race-proof (each one was a real bug):

- **Set the loading flag synchronously** before the HTTP subscribe. An rxMethod that patches the
  flag inside its pipe leaves a same-tick window where two `ensure*` calls both pass the guard.
- **Share the in-flight observable** (`shareReplay(1)` + a closure ref) so concurrent callers
  (resolver racing a warm-up, two components' `ngOnInit`) join one request instead of double-firing.
- **Every slice gets the same treatment.** The one slice that skipped the loading flag
  (`adminEmails`) was the one that double-fired.

## Callers: resolvers and components use `ensure*`, never raw `load*`

- Route resolvers call the `ensure*` guards for **exactly the slices that route's components
  read** (verify by grep, not by assumption — over-fetching hides here). No "load everything"
  resolver: it made 5 GETs per navigation of which 2–3 were never read.
- Components never call an unguarded `load*` from `ngOnInit`. If a call site genuinely needs
  server truth (e.g. a refresh button), it calls the raw `load*`/`{force: true}` variant and says
  why inline.
- Remove warm-up calls that fire right before a redirect unloads the page — they never complete.

## Mutations patch the store locally

After a successful POST/PUT/DELETE, upsert/remove the entity in the store from the API response —
do not refetch the collection, and do not leave it to the caller to reload the list:

```ts
saveHouse: rxMethod<...>(pipe(exhaustMap((req) => service.save(req).pipe(
  tap((saved) => store.upsertHouse(saved)),   // list stays correct without a refetch
))))
```

- If the API returns void, patch from the request payload + returned id.
- Parameterized queries (filtered lists) keep fetch-on-filter-change but dedupe identical
  consecutive queries and patch rows through the **current filter** (a mutation may move a row
  out of the filtered set).
- Document the justified exceptions in code: a mutation whose final state the server computes
  (e.g. a move with server-side placement) may force-refetch — with a comment saying why.
- Keyed request dedupe also applies to detail fetches: a hover-preview and a click that build the
  identical request should share one in-flight call (param-keyed `shareReplay(1)` cache that
  clears on settle).

## Session-static data: storage-backed cache

Data that is static per session (a model catalog, a config blob) can additionally cache in
`sessionStorage` with a TTL so full page reloads skip the fetch too:

- `ensure*` reads the cache first (fresh hit → patch state synchronously, zero HTTP).
- **Every write path invalidates/rewrites the cache** (invalidate before the PUT, rewrite from the
  server response on success, leave cleared on failure) — an admin edit must never be masked.
- Wrap all storage access in try/catch and fall back to in-memory behavior (quota/private mode).
- Unit tests: jsdom's `sessionStorage` persists across `it()` blocks in one spec file — add a
  global `afterEach(() => sessionStorage.clear())` to the test setup or caches leak between tests
  and silently suppress HTTP mocks.

## Verifying the contract

- Vitest: two same-tick `ensure*` calls → exactly one HTTP request (HttpTestingController).
- Empirically: log requests per view (interceptor → file), diff before/after E2E runs. Measure
  duplicate counts **single-worker** — parallel test workers boot separate app instances whose
  interleaved requests masquerade as same-app double-fires (three "residual bugs" here were
  exonerated this way). Each E2E test boots the SPA fresh, so per-boot first loads are the floor;
  only in-session navigation traffic can improve.

## Splitting components without changing the UI

When extracting a child component from a large one during optimization work, use an **attribute
selector** hosted on the existing element (`selector: '[appCreditsPanel]'`) — zero new DOM
elements, so CSS child selectors, flex layouts, and E2E locators all keep working. Keep
destroy-sensitive content (a modal that must survive a layout toggle) in the parent.
