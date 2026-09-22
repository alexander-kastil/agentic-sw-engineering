# Angular Activity Indicator (store-driven, request-counted + explicit activity)

A global activity indicator driven by the **signal store**: an HTTP request counter *plus* an explicit `aiActive` flag, combined into one `isBusy` signal. Any in-flight request **or** any long-running non-HTTP work (e.g. an AI agent streaming/thinking) shows the bar. No per-component `loading` booleans for global chrome.

> Formerly "loading indicator" (`withLoading`/`isLoading`). Generalized to `withActivity`/`isBusy` so the same bar can signal AI activity, not just HTTP loading.

Reference: `src/ui/src/app/store/features/with-activity.feature.ts` + `src/ui/src/app/store/activity.interceptor.ts`.

## 1. The `withActivity` feature slice

```ts
// store/features/with-activity.feature.ts
type ActivityState = { pendingRequests: number; aiActive: boolean };

export function withActivity() {
  return signalStoreFeature(
    withState<ActivityState>({ pendingRequests: 0, aiActive: false }),
    withComputed((store) => ({
      // busy when any HTTP request is in flight OR explicit activity is set
      isBusy: computed(() => store.pendingRequests() > 0 || store.aiActive()),
    })),
    withMethods((store) => ({
      requestStarted(): void {
        patchState(store, { pendingRequests: store.pendingRequests() + 1 });
      },
      requestFinished(): void {
        patchState(store, { pendingRequests: Math.max(0, store.pendingRequests() - 1) });
      },
      // explicit, non-HTTP activity (AI agent run, long compute, etc.)
      setAiActive(active: boolean): void {
        patchState(store, { aiActive: active });
      },
    })),
  );
}
```

Compose it into the root store early (before domain slices):

```ts
export const AppStore = signalStore(
  { providedIn: 'root', protectedState: false },
  withState(initialAppState),
  withActivity(),
  // …domain slices
);
```

## 2. The functional interceptor (HTTP side)

```ts
// store/activity.interceptor.ts
export const activityInterceptor: HttpInterceptorFn = (req, next) => {
  const store = inject(AppStore);
  store.requestStarted();
  return next(req).pipe(finalize(() => store.requestFinished()));
};
```

`finalize` fires on success, error, **and** cancellation, so the counter never leaks.

## 3. Registration — the `withInterceptorsFromDi` coexistence gotcha

This app already registers MSAL's interceptor via **DI** (`withInterceptorsFromDi()`). Add the functional activity interceptor with `withInterceptors([...])` **alongside** it — do not replace the DI form or MSAL bearer-token injection breaks:

```ts
// app.config.ts
provideHttpClient(
  withInterceptorsFromDi(),           // keep — MSAL
  withInterceptors([activityInterceptor]),
  withFetch(),
),
```

## 4. Drive the AI/activity side explicitly

For work the interceptor can't see (an AI agent run, a long client-side compute), wrap it:

```ts
store.setAiActive(true);
try {
  await runAgent();
} finally {
  store.setAiActive(false);   // always clear, even on error
}
```

## 5. Bind the indicator in the shell

Bind global chrome to `store.isBusy()`. Zoneless + OnPush safe — it's a signal read.

This app's indicator is `app-gen-loader` (`src/ui/src/app/shared/gen-loader/`), a
"dot-wave" component ported from `rahimi-carpets`' carpet-visualizer, living in
the top-nav's right cluster (not the app shell root) so it sits directly next
to other status affordances (e.g. the cost entry point in
`shared/top-nav/top-nav.component.html`):

```html
<!-- shared/top-nav/top-nav.component.html -->
<app-gen-loader [active]="isBusy()" />
```

```ts
// shared/top-nav/top-nav.component.ts
isBusy = this.appStore.isBusy;
```

`app-gen-loader` is purely presentational (`active = input(false)`) — it
doesn't inject `AppStore` itself, so any host can drive it from whatever
signal represents "busy" for that surface. It stays mounted in the DOM at a
constant intrinsic width whether `active` is true or false (dim + paused when
idle, animating when active), so neighboring icons never jump when the busy
state toggles. Colors come from the brand tokens (`--color-brand` /
`--color-brand-deep`) per `bico-brand`, so it reads gold on the charcoal
top-nav (`bg-ink`).

The former `.app-loading-bar` (a thin fixed sweep bar pinned to the viewport
top, rendered from `app.component.html`) has been retired in favor of this —
do not reintroduce it; the dot-wave in the top-nav is now the single global
busy indicator.

## Notes / pitfalls

- **Global, not per-view.** For a *specific* long operation you still want a local `xLoading` flag in the owning slice (e.g. `membersLoading`); `withActivity` is only for the app-wide bar.
- **Always clear `aiActive`** in a `finally` — a thrown error mid-run must not leave the bar stuck on.
- **Excludes.** If polling / telemetry requests should not trip the bar, branch in the interceptor on `req.url` / a custom `req.context` token before `requestStarted()`.
- **Constant footprint (no jump).** The indicator must occupy identical layout idle vs. active or neighbors shift when busy toggles. Two traps hit `gen-loader` and were fixed: (1) an a11y text node inserted only while active (`@if (active()) { <span class="sr-only">…</span> }`) — this app has **no** global `.sr-only`, so it rendered in-flow and its removal on deactivate jumped the wallet/badges left; keep the node always-present, component-scoped-hidden, and toggle only its text. (2) `animation-play-state: paused` for the idle state froze the dots on a random bright frame; use `animation: none` idle and attach the animation only under `--active`. See `angular-antipatterns` → "Visually-hidden text & CSS animation". Verify by sampling a neighbor's `getBoundingClientRect().left` across idle→active→idle.
- **Test:** drive `requestStarted()` × n then `requestFinished()` × n and assert `isBusy()` flips true→false only at zero; separately assert `isBusy()` is true when `aiActive` is set with zero pending requests (reference: `with-activity.spec.ts`).
