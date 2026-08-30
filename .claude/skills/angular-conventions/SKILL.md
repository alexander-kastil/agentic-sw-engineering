---
name: angular-conventions
description: Consolidated Angular conventions for components, dependency injection, forms, HTTP, routing, signals, directives, overlays/dialogs, collapsible panels, MSAL authentication, and A2UI generative UI. Use when working on Angular applications and you need modern Angular guidance or routing into a specific Angular concern. Triggers on component creation, inject(), signal forms, httpResource(), guards, route configuration, computed(), linkedSignal(), attribute directives, modal/dialog/popup ESC handling, color-scheme dark, expandable/collapsible panel, accordion, disclosure, show more, equal-height cards, card grid same height, panel will not expand, MSAL, Azure Entra, login button does nothing, loginRedirect does nothing, interaction_in_progress, unhandled promise rejection on login, blank page when auth is enabled, redirect loop through Microsoft, which msal-angular version, A2UI, agent-driven / generative UI, Angular architecture, load-once data loading, ensureLoaded guards, duplicate HTTP requests, refetch-after-CRUD elimination, production bundle-size optimization (initial budget exceeded, main.js too big, tree-shaking, lazy-init), evaluating whether to adopt a third-party library (is library X worth it, which markdown or rich-text editor, npmjs.com returns 403, registry.npmjs.org, last publish date, ngx wrapper is dead, use the library directly, measure gzip with esbuild, WYSIWYG mangles shortcodes or raw HTML or front matter), shared page chrome (page hero, KPI band, routed tab nav, double headline, two headlines stacked, tab label repeated as heading, prose to KPIs, unify headlines, type scale ladder), runtime DI/signal graph inspection in the browser (angular:di_graph, angular:signal_graph, which providers actually resolved, is the interceptor registered, why does this effect re-run), CSS that will not apply (css change has no effect, style not applied, container query not working, @container not matching, container-type on the same element, stale ng serve bundle, hard reload does not help, verify CSS via the CSSOM, deployed app is completely unstyled, app renders unstyled in production only, inlineCritical, CSP blocks the stylesheet onload, media print never flips, font-weight has no effect, faux light, is this font variable, fvar, woff2 table directory, measure advance widths), static data an SPA ships without protection (public/data json readable without login, route guard does not protect the file, json fetchable by URL, basic auth breaks the SPA, Sec-Fetch-Dest, block direct access to a static file, noindex a data file), and data-table column geometry (columns jump when sorting, table shifts sideways on sort or filter, layout jumps on infinite scroll, table-fixed vs table-auto, column widths recompute per page, columns overflow the container, last column pushed off-screen, unwanted horizontal scrollbar on a table, resizable columns, drag column border, column resize handle, drag accidentally triggers sort, flexible column collapses to a few pixels, persist column widths, stale stored widths override new defaults, column picker, show/hide columns, hidden by default, explicit visibility choice vs responsive breakpoint, cannot hide the last column, collapsible nav rail changes the row width at the same viewport, layout differs with the sidebar expanded vs collapsed, no breakpoint value is right for both rail states, container query instead of media query for column geometry, deriving container thresholds from old viewport breakpoints, iPad Pro 13 inch 1032x1376, iPad 12.9 inch 1024 lands on the breakpoint), empty live regions costing layout space (too much space at the bottom, wasted height, unexplained gap in a flex column, empty aria-live wrapper, status region eats a gap, empty:absolute vs empty:hidden), and runtime configuration injection (one bundle many environments, runtime config injection, config.js, __APP_CONFIG__, apiBase baked into the bundle, environment.blue.ts, fileReplacements per slot, slot-agnostic image, promote by retag), and drag-and-drop reordering without the CDK (drag and drop, reorder cards, reorder rows, sortable list, drag handle, grip handle, dragstart never fires, drag does not work, draggable button does nothing, insertion line, drop indicator invisible, persist the order, reset the order, edit mode toggle for reordering), file download from an API (download a file, export button, responseType blob, Content-Disposition, filename is always the fallback, downloaded file is 401 HTML, download opens a login page, revoke object url), unit testing with Vitest and the Angular builder (write a spec, TestBed, fakeAsync, testing a functional guard, NG0201 no provider for ActivatedRoute), running and scoping a suite (ng test vs npx vitest run, needs to be compiled using the JIT compiler, Need to call TestBed.initTestEnvironment() first, --include vs --filter, 120 skipped looks green, one broken spec fails everybody's run), coverage (coverage requires @vitest/coverage-v8, coverage-summary.json MODULE_NOT_FOUND, html file at 0% functions, missing spec file is not missing coverage), a spec failing for a reason that is not the code (vi.mock, vi.hoisted, __spreadValues is not a function, mock is undefined, is not a constructor, arrow function mockImplementation, expectOne found none, urlWithParams, expectOne with query params, flush a Blob, httpMock.verify cascade, 40 failures in other files), and a plain-bound native select showing nothing selected (select value empty, dropdown does not prefill, edit prefill missing, [value] on select ignored, [selected] on option, no ngModel no formField).
---

# Angular Conventions

Group reusable Angular guidance under one entry skill.

## When to Use This Skill

- The task is Angular-specific but not yet narrowed to one Angular topic.
- You need a single entry point for Angular components, DI, forms, HTTP, routing, or signals.
- The repository has its own Angular rules in `docs/` and you want to pair those with general Angular conventions.

## Defaults

| Topic                       | Current rule                                                                               |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| Angular version             | Angular `22.x` or later                                                                    |
| Architecture                | Standalone components — do NOT set `standalone: true` (default since v20)                 |
| Change detection            | `ChangeDetectionStrategy.OnPush` on every component                                       |
| Dependency injection        | `inject()` function only — never constructor parameters                                    |
| Inputs / Outputs            | `input()` / `output()` signals — never `@Input()` / `@Output()` decorators                |
| Host bindings               | `host` object in `@Component` / `@Directive` — never `@HostBinding` / `@HostListener`    |
| Template control flow       | `@if` / `@for` / `@switch` — never `*ngIf` / `*ngFor` / `*ngSwitch`                      |
| Class and style bindings    | `[class.x]` / `[style.x]` — never `ngClass` / `ngStyle`                                  |
| Local state                 | `signal()` — never `BehaviorSubject`                                                       |
| State management            | **NgRx Signal Store (`@ngrx/signals`) is required** for shared/server state — `signalStoreFeature()` slices with `withState`/`withComputed`/`withMethods`, async via `rxMethod` + `tapResponse` + `patchState`. `signal()` is for component-local UI state only; never `BehaviorSubject` stores or class-based `@ngrx/store` reducers. |
| HTTP reads                  | `httpResource()` for reactive reads; `HttpClient` for mutations                            |
| Forms                       | Signal Forms (`form()` + `[formField]`) — never Reactive Forms or `ngModel`               |
| Scaffolding                 | Angular CLI for components, services, directives, and pipes                                |
| Project structure           | Feature-based folder organization; flat feature folders for smaller apps                   |
| Routing                     | `app.routes.ts` with functional guards and lazy-loaded feature routes                     |
| Component file layout       | Separate `.ts`, `.html`, `.css` files; kebab-case names; one folder per component         |
| Component organization      | Functional hierarchy: feature folder → component sub-folder                                |

## Usage Note

- This skill captures shared Angular 22 conventions. Always check the target repository's own `docs/` or `CLAUDE.md` for repo-specific overrides (API base URLs, store architecture, auth provider, money conventions, etc.) before applying these defaults.

## Component File Organization

Angular projects use a functional storage hierarchy:

```
app/
  <feature>/              ← domain/feature folder (auth, person, cart, …)
    <component-name>/     ← one folder per component
      <component-name>.ts
      <component-name>.html  (if separate template)
      <component-name>.spec.ts
    <service>.ts          ← services live at feature level, not in a sub-folder
  shared/                 ← cross-cutting UI components used across features
    <shared-component>/
  store/                  ← global state (NgRx store, signal stores)
```

Rules:

- Each component gets its own folder named after the component.
- Files inside the folder share the component's name (e.g., `user-card/user-card.ts`).
- Services are placed at the feature level, not inside a component sub-folder.
- `shared/` contains components reused across multiple features.
- `store/` contains global state artifacts.

## Delegate Map

| Request type                                          | Reference to use                                                   |
| ----------------------------------------------------- | ------------------------------------------------------------------ |
| Build or refactor standalone components               | [`angular-component`](references/angular-component.md)             |
| Component folder layout and file organization         | [`angular-component`](references/angular-component.md)             |
| Configure dependency injection or providers           | [`angular-di`](references/angular-di.md)                           |
| Build forms and validation flows                      | [`angular-forms`](references/angular-forms.md)                     |
| Implement API calls and data loading                  | [`angular-http`](references/angular-http.md)                       |
| Download a file the API generates, with auth          | [`angular-file-download`](references/angular-file-download.md)     |
| Configure navigation and route behavior               | [`angular-routing`](references/angular-routing.md)                 |
| Model reactive state with signals                     | [`angular-signals`](references/angular-signals.md)                 |
| Design app state so one composed signal store fully serves the app (feature-per-domain, container/presenter binding) | [`angular-signal-store-design`](references/angular-signal-store-design.md) |
| Add a global store-driven activity indicator (HTTP request-counter + explicit AI-activity flag + interceptor + progress bar) | [`angular-activity-indicator`](references/angular-activity-indicator.md) |
| Load-once data loading with local CRUD sync (ensure*Loaded guards, in-flight dedupe/shareReplay, resolvers scoped to what a route reads, mutations patch the store instead of refetching, sessionStorage TTL cache, duplicate-request elimination) | [`angular-load-once-store`](references/angular-load-once-store.md) |
| Write a spec for a component, service, guard or signal with Vitest and `TestBed` | [`angular-testing`](references/angular-testing.md)                 |
| Run or scope a Vitest suite and read the result (`ng test` vs raw `npx vitest`, `--include` vs `--filter`, a run that skipped everything but shows no red, one broken spec failing the whole type-check, which failing file to fix first) | [`angular-test-execution`](references/angular-test-execution.md) |
| Measure coverage and rank the gaps (`@vitest/coverage-v8` not installed, where `coverage-summary.json` actually lands, a `.html` file at ~0% functions, missing `<name>.spec.ts` is not missing coverage) | [`angular-test-coverage`](references/angular-test-coverage.md) |
| The spec fails for a reason that is not the code under test: `vi.mock` factory traps (`__spreadValues is not a function`, mock is `undefined`, `is not a constructor`, `vi.hoisted`), `expectOne` finding no matching request when the URL has query params, flushing the wrong body type for a blob request, one leaked request cascading into dozens of failures | [`angular-test-doubles`](references/angular-test-doubles.md) |
| A plain-bound native `<select>` renders with nothing selected (no `ngModel`/`formField`): `[value]` on the select loses to the options' own bindings, put `[selected]` on the options | [`angular-select-binding`](references/angular-select-binding.md) |
| Build modals/dialogs/popups, ESC-to-close, dark native controls | [`angular-overlays`](references/angular-overlays.md)     |
| Build a draggable/resizable two-pane splitter (`ux-splitter`) | [`angular-draggable-splitter`](references/angular-draggable-splitter.md) |
| Stable data-table column geometry (columns jump when sorting, table shifts on sort/filter, `table-fixed` vs `table-auto`, columns overflow the container, last column pushed off-screen, unwanted horizontal scrollbar, server-side sort with infinite scroll, collapsible nav rail changes available width at a fixed viewport, container query instead of media query, sidebar expanded vs collapsed, iPad Pro 13 inch) | [`angular-table-column-layout`](references/angular-table-column-layout.md) |
| User-resizable table columns (drag column border, resize column width, column resize handle, drag fires the sort by mistake, flexible column collapses to a few px, persist column widths, stale stored widths override new defaults) | [`angular-table-column-resize`](references/angular-table-column-resize.md) |
| Show/hide table columns (column picker, "Spalten" dropdown, hide a column, hidden by default, column visibility, explicit choice vs responsive breakpoint, checkbox stays checked below breakpoint, cannot hide last column) | [`angular-table-column-visibility`](references/angular-table-column-visibility.md) |
| Drag and drop for grids or reorderable lists without a library (cdkDrag alternative, reorder rows, draggable grid, drop target, not-allowed drop) | [`angular-drag-drop`](references/angular-drag-drop.md) |
| Build a bottom sheet with no Angular Material/CDK (native `<dialog>`, viewport-anchored, slide-up, imperative open()/close()) | [`angular-bottom-sheet`](references/angular-bottom-sheet.md) |
| Build a file drop zone / drag-and-drop file upload (dragover state, hidden input, single vs multi, `filesSelected` output, store-event variant) | [`angular-file-dropzone`](references/angular-file-dropzone.md) |
| Build a multi-step file-import wizard (upload → review/column-map → AI-assist → commit; draft in the store, no client-side parsing) | [`file-import-wiz`](references/file-import-wiz.md) |
| Blob download or a retained-documents list (blob download, document list, file download, object URL, retained documents, import documents; `HttpClient` blob → `createObjectURL` → anchor click) | [`blob-document-list`](references/blob-document-list.md) |
| Build a user & permission admin UI (RBAC: admin-users, admin-permissions, user/roles dialogs) backed by mixed auth (Entra MSAL + local JWT), with `withAuth`/`withAdmin` signal-store slices, a local-first token interceptor, and an `adminGuard` — admin UI, permission matrix, roles screen, RBAC UI, local login form, adminEmails | [`angular-users-permissions-admin`](references/angular-users-permissions-admin.md) |
| Build a collapsible/expandable disclosure panel or accordion, especially inside an equal-height card grid (collapsed by default, show more, panel will not expand, cards same height, `0fr`/`1fr` row animation) | [`angular-disclosure-panels`](references/angular-disclosure-panels.md) |
| Give a set of pages one shared chrome: eyebrow + H1 hero, KPI band, routed tab nav; fix two stacked headlines ("double headline"), convert stacked sections into routed tabs, replace explanatory prose with KPI tiles, share CSS primitives without leaking through global `styles.css` | [`angular-page-chrome`](references/angular-page-chrome.md) |
| A CSS edit has no visible effect: diagnose via the CSSOM, a stale `ng serve` bundle, a `@container` rule that cannot match its own container, an unlayered global beating a Tailwind utility, a class living in another component's stylesheet, or a `font-weight` the loaded font file cannot honour (prove the face is variable via `fvar` before declaring a weight), or a production build whose inlined critical CSS is blocked by the app's own CSP so the deployed page ships completely unstyled; choose `flex-wrap` over a container query for "sits beside, else wraps below" | [`angular-css-not-applying`](references/angular-css-not-applying.md) |
| Data the SPA ships as static files under `public/` is readable without login (the route guard protects the route, not the file): how to check, why basic auth breaks the app's own `fetch()`, why the edge cannot validate an MSAL token, the `Sec-Fetch-Dest`/`Sec-Fetch-Site` nginx and Caddy mitigation, and its honest obscurity-grade limits | [`spa-static-data-exposure`](references/spa-static-data-exposure.md) |
| Unexplained vertical space in a `gap`-spaced column: an always-rendered but currently empty `aria-live` wrapper (or any conditionally-empty child) still eats a full gap — `empty:absolute` vs `empty:hidden`, and why `:empty` still matches through an `@if` anchor | [`angular-live-region-layout`](references/angular-live-region-layout.md) |
| Inspect the RUNNING app's DI graph or signal graph from the browser (which providers actually resolved, is the interceptor registered once, did MSAL_INSTANCE resolve, is zoneless really on, why does this effect re-run, `angular:di_graph`, `angular:signal_graph`, `devtoolstooldiscovery`, `list_3p_developer_tools`, `categoryExperimentalThirdParty`, converting circular structure to JSON) | [`angular-runtime-graph-inspection`](references/angular-runtime-graph-inspection.md) |
| Spot or fix anti-patterns / legacy code               | [`angular-antipatterns`](references/angular-antipatterns.md)       |
| Wire MSAL providers: interaction-type rule, `environment` config, the providers factory, `protectedResourceMap` keys, `app.config.ts` registration | [`angular-msal-auth`](references/angular-msal-auth.md) |
| MSAL application patterns: a cached `AuthService`, functional guards in both directions, local-only vs full logout, one `authEnabled` flag across SPA and API | [`msal-auth-patterns`](references/msal-auth-patterns.md) |
| MSAL is wired but misbehaving: blank page when auth is enabled, redirect loop through Microsoft, missing `Authorization` header, 401 triage, popup failure, Easy Auth conflict, the Login button that silently does nothing (an unsubscribed `loginRedirect()` swallowing `interaction_in_progress`) | [`msal-troubleshooting`](references/msal-troubleshooting.md) |
| Which `@azure/msal-angular` major to run and what each hop broke: v4/v5/v6 API changes, where `navigateToLoginRequestUrl` moved, the removed-API grep checklist | [`msal-version-changes`](references/msal-version-changes.md) |
| MSAL client wiring deep-dive: provider setup, `APP_INITIALIZER`, `AuthStateService`, single-bootstrap rules, the migration checklist, and whether the COOP redirect-bridge page is needed at all | [`msal-angular`](references/msal-angular.md) |
| Entra app registration via Azure CLI: create from scratch, redirect URIs, platform types, `requestedAccessTokenVersion` and the pre-authorization chicken-and-egg | [`msal-angular-appreg`](references/msal-angular-appreg.md) |
| Upgrade or update an Angular app to the latest version, and the compatibility gate for deciding what NOT to bump (TypeScript peer range off `@angular/compiler-cli`, stable-with-unmet-peer vs an RC, README support matrices no tool can see, test-env majors, the Node engine floor and where it is actually pinned, why caret floors are the deployed version when the Dockerfile has no lockfile). Run the gate first with `node <this-skill>/scripts/angular-update-preflight.mjs --root <dir>` | [`angular-update`](references/angular-update.md) |
| Fix a failing production bundle-size budget: measure eager vs lazy chunks, non-ESM tree-shaking traps, raw-vs-gzip budgets, lazy-init a heavy lib via dynamic `import()` (reduce bundle, main.js too big, initial budget exceeded, tree-shaking, lazy load) | [`angular-bundle-optimization`](references/angular-bundle-optimization.md) |
| Decide whether to adopt a third-party library at all: is it maintained, is the Angular wrapper dead, how many kB does it really cost against the current budget, and will it round-trip our content (is library X worth it, which markdown/rich-text/chart/date library, npmjs.com returns 403, registry.npmjs.org, weekly downloads, last publish, ngx wrapper unmaintained, use the library directly, measure gzip with esbuild, WYSIWYG mangles shortcodes or raw HTML or front matter) | [`angular-dependency-evaluation`](references/angular-dependency-evaluation.md) |
| Move per-environment values out of the bundle so one build serves every environment: read `globalThis.__APP_CONFIG__` in `environment.ts` with `??` fallbacks, load `config.js` from `index.html`, and retire the per-slot `environment.<slot>.ts` + `fileReplacements` (runtime config injection, config.js, `__APP_CONFIG__`, apiBase baked into the bundle, one bundle many environments, environment.blue.ts, fileReplacements per slot, slot-agnostic image, promote by retag) | [`angular-runtime-config`](references/angular-runtime-config.md) |
| Migrate markdown-renderer into a split demo-container layout | [`angular-migrate-markdown`](references/angular-migrate-markdown.md) |
| Render agent-driven generative UI with the A2UI protocol (catalogs, surfaces, actions, theming) | [`angular-a2ui`](references/angular-a2ui.md) |
| Build a multi-step wizard / setup flow: full-width step-rail shell, phase-driven active/done states, two-column step body, copy-to-clipboard, real-data chip filters | [`angular-wizard`](references/angular-wizard.md) |

## Example Prompts

- "Use angular-conventions to choose the right pattern for a new Angular form."
- "Route this Angular data-loading task to the right conventions reference."
- "Use angular-conventions for a component and signals refactor."
- "Use angular-conventions to design a feature-per-domain signal store that fully serves the app."
- "Use angular-conventions to add a global store-driven activity indicator (HTTP + AI activity) with an interceptor."
- "Use angular-conventions to scaffold a standalone Angular component and confirm the right CLI command."
- "Use angular-conventions to upgrade this workspace to the latest Angular version."
- "Use angular-conventions to migrate markdown-renderer into the split demo-container layout."
- "Use angular-conventions to wire an A2UI renderer and custom catalog into an Angular client."
- "Use angular-conventions to add a drag-and-drop file drop zone that emits selected files to the store."
- "Use angular-conventions to build a file-import wizard (upload → review → commit) for Mieterlisten."
- "Use angular-conventions to add a retained-documents list with a blob download button."

## Layout Rules

| Rule | Detail |
| ---- | ------ |
| Button alignment | All button groups (`.actions`, `.section-actions`, `.hero-actions`) must use `justify-content: flex-end` so buttons sit at the right edge |
| Default button style | Orange fill (`var(--accent)`) with black text (`#0a0c10`), `font-weight: 700`. This is the global default — no extra class needed |
| Destructive buttons | Stop, Delete, Remove, Drop — use `.btn-danger`: solid red fill (`var(--danger)`) with black text (`#0a0c10`) |
| Exceptions | Icon/utility buttons (`.btn-close`, `.tree-btn`, `.template-card`) keep their own component-scoped overrides |


## Project-Specific Rule

- Use this skill for reusable Angular guidance.
- Check the repository's `docs/` for project-specific architecture, folder layout, naming, and build rules before applying these conventions.


## Code Generation

Use Angular CLI rather than hand-writing the initial file structure.

```bash
ng generate component my-component
ng generate service my-service
ng generate directive my-directive
ng generate pipe my-pipe
```


## Development Commands

| Command            | Use                                        |
| ------------------ | ------------------------------------------ |
| `ng serve`         | Start the local Angular development server |
| `ng build`         | Create a production build                  |
| `ng build --watch` | Rebuild continuously during development    |


## Deployment Note

Angular projects in this repository are typically deployed to Azure Static Web Apps or Azure Container Apps. Use the project-specific deployment scripts and documentation instead of inventing a new deployment path.

## NDJSON Streaming into Signal Store

When a store feature must consume a server-sent NDJSON stream:

1. Use `fetch` (not `HttpClient`) to POST and obtain `response.body.getReader()`.
2. Decode chunks with `new TextDecoder()` in streaming mode; split on `\n`; parse each non-empty line as JSON.
3. Drive `patchState` for each event type (`stage`, `cost`, `result`) as lines arrive.
4. Fall back to an `HttpClient` call on any `fetch` rejection, non-200 response, or absent body.
5. Put the fallback in a separate async function and call it from both the `catch` block and the non-ok guard.
6. Revoke any object-URL (`URL.revokeObjectURL`) in both success and error paths.

Reference implementation: `src/inventory-ui/src/app/store/features/with-scan.feature.ts` (`resolvePhotoStream`).
