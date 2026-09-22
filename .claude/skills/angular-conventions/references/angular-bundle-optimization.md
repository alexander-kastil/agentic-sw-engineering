# Angular Bundle-Size Optimization (measure → cut the eager graph)

Reduce a failing production bundle budget by moving weight out of the **eager** `main.js`,
not by guessing and not by raising the budget. Proven on a real Angular 22 SPA: initial bundle
went from 2.20 MB (failing a 1.5 MB budget) to 1.13 MB across two safe cuts, without weakening
`angular.json` and without changing runtime behavior.

## Core discipline: measure before attributing a cause

The failure mode this reference exists to prevent: **naming a culprit from surface signals
(git status, "that big new feature") before running the build.** In the proven session, a large
new `plan-board/` feature was flagged as the "likely" budget driver — the production build then
showed `plan-board` is lazy-loaded and completely unrelated; the real cost was a non-ESM date
library. Always run the build and read the chunk table first.

Two facts that make eyeballing wrong:

- **Angular budgets measure RAW size, not gzip.** A bundle can be ~300 kB on the wire (gzip
  "estimated transfer size") yet fail a 1.5 MB raw budget. The `initial` budget in `angular.json`
  (`maximumWarning`/`maximumError`) is on raw bytes.
- **Only the EAGER graph counts against the `initial` budget.** Anything reached exclusively
  through a lazy `loadComponent`/`loadChildren` route sits in its own chunk and is irrelevant to
  the initial budget. A "big" feature that is lazy-loaded cannot be the cause.

## Step 1 — Read the chunk table

```bash
npx ng build --configuration production
```

The output separates **Initial chunk files** (the eager `main-*.js` + polyfills + styles) from
**Lazy chunk files**. The budget error is about the *Initial total*. Confirm which side your
suspect is on before touching anything.

## Step 2 — Rank what's actually in `main.js`

Get a ranked list of eager contributors from esbuild's metafile. Do **not** reach for
`source-map-explorer` first — it chokes on repos that emit a non-ESM warning (see below), which
are exactly the repos you most need to measure.

```bash
# Temporary build config that writes the esbuild metafile, then inspect it.
npx ng build --configuration production --stats-json
# → dist/<app>/stats.json ; rank the `inputs` bytes feeding the initial output.
```

Rank the byte contributions to the initial output. A single dependency dominating the list (in the
proven case one dep was **44% of the eager bundle**) is the cut to make first.

## Cut A — Replace non-ESM dependencies (they can't be tree-shaken)

The build warns:

```
Module 'X' used by 'src/.../foo.ts' is not ESM
```

A non-ESM (CommonJS/UMD) module is bundled **whole** — the bundler can't drop unused parts. Worse,
if the file that imports it is reachable from several lazy chunks, the bundler **hoists** the dep
into the shared eager `main.js`.

Proven hit: `date-fns-timezone` pulled in `timezone-support` — a **934 kB static IANA timezone
database** — hoisted into `main.js` because the importing `time-functions.ts` was reachable from
8 lazy chunks. Fix: swap to the ESM equivalent (`date-fns-tz`), which tree-shakes to only the zone
data used. Preserve exact behavior (timezone math is correctness-sensitive) — keep wrapper function
signatures identical and add a DST + non-DST regression test proving parity with the old library
before deleting the old import.

Generalize: audit every "not ESM" warning; each is a tree-shaking hole. Prefer an ESM replacement;
if none exists, confine the import to a single lazy feature so it can't hoist into `main.js`.

## Cut B — Lazy-init a heavy eager library via dynamic `import()`

Heavy libs that a root-level service/component imports statically (App Insights, charting, editors,
PDF/Excel) land in `main.js` even when they aren't needed at first paint. Convert to lazy init:

1. Change the top-level value import to a **type-only** import so it's erased at build time:
   ```ts
   import type { ApplicationInsights } from '@microsoft/applicationinsights-web';
   ```
2. Keep the constructor synchronous; fire an async initializer without awaiting:
   ```ts
   constructor() { void this.init(); }

   private async init() {
     const { ApplicationInsights } = await import('@microsoft/applicationinsights-web');
     this.instance = new ApplicationInsights({ /* same config */ });
     this.instance.loadAppInsights();
     this.flushPending();
   }
   ```
3. **Queue-and-flush** every public method so calls made before init resolves are never dropped or
   thrown — route them through a helper that calls straight through once `this.instance` exists,
   else pushes a thunk onto a `pendingCalls` array flushed (in order) at the end of `init()`.

Result: the package moves into its own lazy async chunk (`applicationinsights-web-*.js`), off the
initial budget. Proven cut: ~170 kB off `main.js`. Verify with `--stats-json` that `main.js` now
contains only the `await import('./chunk-*.js')` call site, not the SDK's class code.

Which eager libs are safe to defer: anything whose first use is after first paint. Libs that must
run before route guards resolve (e.g. **MSAL** auth) are legitimately eager — don't defer those.

## Step 3 — Re-measure, don't relax the budget

Re-run `ng build --configuration production` and confirm the `initial` ERROR is gone; report the
new initial total (raw + gzip) and which chunk the moved code landed in. **Never** fix a budget
failure by raising `maximumError` in `angular.json` — that hides the regression instead of removing
it. Run only the specs for files you changed (`ng test --include=...`), plus the parity test for any
library swap.

## Checklist

- [ ] Ran the prod build and read the Initial-vs-Lazy chunk table before naming a cause.
- [ ] Confirmed the suspect is actually in the eager graph (lazy features are exonerated).
- [ ] Ranked eager contributors from the esbuild metafile (`--stats-json`), not by guessing.
- [ ] Replaced non-ESM deps with ESM equivalents (or confined them to a lazy feature).
- [ ] Lazy-init'd heavy after-first-paint libs via `import type` + dynamic `import()` + queue/flush.
- [ ] Left genuinely-eager libs (MSAL/auth) alone.
- [ ] Preserved behavior; added a parity/regression test for any library swap.
- [ ] Re-measured; did NOT raise the `angular.json` budget.
