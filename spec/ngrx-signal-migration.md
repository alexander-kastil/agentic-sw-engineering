# NgRx → NgRx Signal Store Migration Plan — food-shop

## Prompt

examine src\food-app\food-shop ... currently it is using old ngrx -> create a migration plan to ngrx signal like defined in our angular skills like here D:\git-customers\bauer-sport\src\citythong-members-ui -> save your plan in spec\ngrx-signal-migration.md

## Migration Plan


Target: `src/food-app/food-shop`. Migrate classic NgRx (`@ngrx/store`, `@ngrx/effects`, `@ngrx/data`, `@ngrx/entity`) to NgRx Signal Store (`@ngrx/signals`), following `.github/skills/angular-conventions/references/angular-signal-store-design.md`. Reference implementation: `D:\git-customers\bauer-sport\src\citythong-members-ui`.

## Goal

Replace the classic NgRx `Store`/`Effects`/`Entity`/`Data` stack with a single composed signal store (`@ngrx/signals`) that serves the whole app. Components bind to the store's signals directly; async work moves from `@ngrx/effects` into `rxMethod` + `tapResponse` inside feature slices. MSAL plumbing (instance, interceptor, guard, broadcast service) stays; only the NgRx-wrapped auth *state* migrates.

## Current state inventory

Classic NgRx is used in four domains plus the auth slice, all wired through module-level `StoreModule`/`EffectsModule`/`EntityDataModule` registrations.

**Dependencies (`package.json`)**

- `@ngrx/data`, `@ngrx/entity`, `@ngrx/router-store`, `@ngrx/store` (dependencies)
- `@ngrx/schematics`, `@ngrx/store-devtools` (devDependencies)
- `@ngrx/effects` is imported in source but **not declared** — it resolves transitively via `@ngrx/data`. It disappears when `@ngrx/data` is removed.
- `@ngrx/router-store` is declared but **never imported** in source — dead weight, removed.

**Root state — `src/app/state/state.ts`**

- `ActionReducerMap` holding the `sidenav` reducer.
- `debug` metaReducer that logs every action to console + `AILoggerService` (ApplicationInsights), gated by `environment.features.logging` (currently `false` in both environments).

**Sidenav — `src/app/state/sidenav/`**

- `sidenav.actions.ts` (`createActionGroup`: toggleSideNav, setSideNavEnabled, setSideNavVisible, setSideNavPosition)
- `sidenav.state.ts` (`createFeature`/`createReducer`): `sideNavEnabled`, `sideNavVisible`, `sideNavPosition`
- `sidenav.facade.ts` (`SidenavFacade`): BreakpointObserver watch + Store selects/dispatches. The `watchScreen` subscription only `console.log`s and `adjustSidenavToScreen` is unused.
- Consumers: `app.component.ts`, `menus/navbar/navbar.component.ts`

**Cart — `src/app/food/state/cart/`**

- `cart.actions.ts` (`createActionGroup`: clear, updateCart, checkout, togglePersist, loadFromStorage, loadFromStorageSuccess, clearStorage, saveToStorage, storageActionSuccess, storageActionFailure)
- `cart.state.ts` (`createFeature`/`createReducer`): `items: CartItem[]`, `persist: boolean`; local `updateCart` upsert/remove reducer logic
- `cart.effects.ts` (`cartEffects`): `clearStorage$`, `loadFromStorage$`, `saveToStorage$` — wrap `StorageService` (localStorage)
- `cart.facade.ts` (`CartFacade`): clear, set, togglePersist, getPersist, getItems, getItemsCount, getOrder, getSumTotal, saveToStorage, loadFromStorage (Observables via `store.select`)
- `mock-data.ts` (plain data, not NgRx — keep)
- Consumers: `food-shop-container.component.ts`, `checkout.component.ts`, `menus/sidebar/sidebar.component.ts`

**Catalog — NgRx Data/Entity (`src/app/food/state/catalog/` + `custom-url-generator.ts`)**

- `entity-metadata.ts` (`EntityMetadataMap` for `Food`, `sortComparer` by name)
- `food-data.service.ts` (`FoodDataService extends DefaultDataService<CatalogItem>`), custom `update` that PUTs `{ ...changes }` to `${environment.catalogApi}/food`
- `food-entity.service.ts` (`FoodEntityService extends EntityCollectionServiceBase<CatalogItem>`)
- `custom-url-generator.ts` (`CustomUrlHttpGenerator extends DefaultHttpUrlGenerator`) registering the `Food` collection/entity URL
- Registered in `food.module.ts` constructor via `EntityDefinitionService.registerMetadataMap` + `EntityDataService.registerService`
- Consumers: `food-container.component.ts` (entities$, loaded$, getAll, add, update, delete), `food-shop-container.component.ts` (entities$, loaded$, getAll)

**Auth — MSAL via NgRx (`src/app/auth/state/`)**

- `auth.actions.ts`, `auth.reducer.ts` (`authFeatureKey`, `authResponse`, `authEnabled`), `auth.effects.ts` (`tryLoginSilent$`, `logout$`), `auth.selectors.ts` (getAuthEnabled, getLoggedIn, getUser, getToken), `auth.facade.ts` (`MsalAuthFacade` + MSAL factory functions), `auth.interceptor.ts`
- `auth.interceptor.ts` is dead code (`//TODO: Not used here`, `providedIn: 'root'` but never registered)
- Registered via `auth/msal-auth-util.module.ts` (`StoreModule.forFeature` + `EffectsModule.forFeature`)
- Consumers: `app.component.ts` (`isAuthenticated`), `sidebar.component.ts` (`getUser`, `getAuthEnabled`, `logout`), `current-user.component.ts` (`getUser`)
- The MSAL factory functions (`MSALInstanceFactory`, `MSALInterceptorConfigFactory`, `MSALGuardConfigFactory`, `isIE`, `loggerCallback`) live in `auth.facade.ts` and must survive.

**Wiring**

- `app.config.ts`: `StoreModule.forRoot(reducers, metaReducers)`, `EffectsModule.forRoot([])`, `EntityDataModule.forRoot({})`, `StoreDevtoolsModule.instrument`
- `food.module.ts`: `StoreModule.forFeature(cartFeature)`, `EffectsModule.forFeature([cartEffects])`, `HttpUrlGenerator` provider, `FoodEntityService`/`FoodDataService` providers, constructor entity registration
- `auth/msal-auth-util.module.ts`: `StoreModule.forFeature(authFeatureKey, authReducer)`, `EffectsModule.forFeature([AuthEffects])`

**Specs that reference classic NgRx**

- `food/shop/shop-container/food-shop-container.component.spec.ts` (`provideStore`, `provideEffects`, `provideEntityData`)
- `auth/components/current-user/current-user.component.spec.ts` (`provideMockStore`)
- `menus/navbar/navbar.component.spec.ts` (`provideMockStore`)

## Target architecture

One root signal store composed of one feature slice per domain, under a new `src/app/store/` folder.

```ts
// src/app/store/app.store.ts
export const AppStore = signalStore(
  { providedIn: 'root', protectedState: false },
  withSidenav(),
  withCart(),
  withCatalog(),
  withAuth(),
);
```

**Feature slices (`src/app/store/features/`)** — each `signalStoreFeature()` with `withState` (+ `withComputed`) + `withMethods`, async via `rxMethod` + `tapResponse`.

- `with-sidenav.feature.ts` — state `sideNavEnabled`/`sideNavVisible`/`sideNavPosition`; methods `toggleSideNav`, `setSideNavEnabled`, `setSideNavVisible`, `setSideNavPosition`. Breakpoint bootstrap moves into `withHooks({ onInit })` using `window.matchMedia` (per the signal-store-design sidenav example), replacing the dead `watchScreen` + `adjustSidenavToScreen`.
- `with-cart.feature.ts` — state `items`, `persist`; methods `clear`, `set(item)` (ports the `updateCart` upsert/remove reducer logic into a method), `togglePersist`, `loadFromStorage`, `saveToStorage`, `clearStorage` (wrap `StorageService`); `withComputed` for `itemsCount`, `sumTotal`, `order`. The persist/subscribe orchestration currently in `food-shop-container` and `sidebar` (`ensureStorageFeature`) moves into the slice (`withHooks` + methods) so components stop subscribing.
- `with-catalog.feature.ts` — state `foods: CatalogItem[]`, `catalogLoading`, `selected`; methods `loadFoods` (getAll, idempotent), `addFood`, `updateFood` (custom PUT to `${environment.catalogApi}/food`), `deleteFood`, `selectFood`. Inject `HttpClient` directly (variant **a** — there is no clean HTTP service today; `FoodDataService` is a NgRx-Data class). `sortByName` becomes a `computed` or is applied after load. Replaces the entire entity-metadata/data-service/url-generator trio.
- `with-auth.feature.ts` — state `user`/`authResponse`, `authEnabled`, `authResolved`; `withComputed` `isAuthenticated`, `currentUserName`; methods `setUser`, `clearUser`, `logout` (call `MsalService` directly), mirroring the reference `with-auth.feature.ts`. MSAL instance/interceptor/guard providers stay out of the store.

**MSAL factories** move from `auth.facade.ts` into a small `auth/auth.factories.ts` (or stay in the facade file with the store-facing class removed). The NgRx `auth.reducer`/`auth.effects`/`auth.selectors`/`auth.interceptor` are deleted; `MsalAuthFacade` is replaced by direct `inject(AppStore)` reads in the three consumers.

**Logging** — the `debug` metaReducer has no signal-store equivalent (no actions) and is disabled everywhere (`features.logging: false`). Delete it with `state.ts`; if per-event telemetry is still wanted, add explicit `AILoggerService.logEvent` calls at the mutation sites (key events are already logged in components).

## Dependency changes

Remove from `package.json`:

- `@ngrx/data`, `@ngrx/entity`, `@ngrx/router-store`, `@ngrx/store`
- devDependencies: `@ngrx/schematics`, `@ngrx/store-devtools`

Add:

- `@ngrx/signals` `^22.0.1`
- `@ngrx/operators` `^22.0.1` (for `tapResponse`)

## Migration steps

Phased so the app compiles after each step.

**Phase 1 — deps.** Add `@ngrx/signals` + `@ngrx/operators`; do not remove classic deps yet (keeps partial builds green).

**Phase 2 — sidenav.** Create `with-sidenav.feature.ts` + `with-sidenav.spec.ts`. Rewire `app.component.ts` and `navbar.component.ts` to `inject(AppStore)` (sidenav signals + `toggleSideNav`). Delete `state/sidenav/*` and `SidenavFacade`.

**Phase 3 — cart.** Create `with-cart.feature.ts` + spec, porting `updateCart` logic and `StorageService` orchestration into the slice. Rewire `sidebar`, `food-shop-container`, `checkout` to store signals/methods; drop `AsyncPipe`-based facade Observables. Delete `cart.actions.ts`, `cart.state.ts`, `cart.effects.ts`, `cart.facade.ts` (keep `mock-data.ts`).

**Phase 4 — catalog.** Create `with-catalog.feature.ts` + spec with direct `HttpClient` and the custom PUT. Rewire `food-container` and `food-shop-container` to `store.foods()` / `store.loadFoods()` / `store.addFood()` / `store.updateFood()` / `store.deleteFood()` (replace the `loaded$`+`getAll` bootstrap with a store `loadIfEmpty`/`withHooks`). Delete `entity-metadata.ts`, `food-data.service.ts`, `food-entity.service.ts`, `custom-url-generator.ts`.

**Phase 5 — auth.** Create `with-auth.feature.ts` + spec. Extract MSAL factories out of `auth.facade.ts`. Rewire `app.component`, `sidebar`, `current-user` to `inject(AppStore)` auth signals/methods. Delete `auth.reducer.ts`, `auth.actions.ts`, `auth.effects.ts`, `auth.selectors.ts`, `auth.interceptor.ts` and the store-facing `MsalAuthFacade` class. Remove `StoreModule`/`EffectsModule` from `msal-auth-util.module.ts` (keep MSAL providers).

**Phase 6 — wiring.** Compose `app.store.ts`. Remove `StoreModule.forRoot`, `EffectsModule.forRoot`, `EntityDataModule.forRoot`, `StoreDevtoolsModule` from `app.config.ts`; remove `StoreModule.forFeature`/`EffectsModule.forFeature`/`HttpUrlGenerator`/entity providers + constructor registration from `food.module.ts`; delete `state/state.ts`.

**Phase 7 — specs.** Migrate `food-shop-container.component.spec.ts` (drop `provideStore`/`provideEffects`/`provideEntityData`, use `provideHttpClient` + `provideHttpClientTesting` and the real `AppStore` or a test store), `current-user.component.spec.ts` and `navbar.component.spec.ts` (drop `provideMockStore`, provide `AppStore`). Add colocated `with-*.spec.ts` per feature.

**Phase 8 — cleanup + verify.** Remove classic NgRx deps from `package.json`, run `npm install`, then `ng build` and `ng test`, and a `ng serve` smoke test of the catalog/cart/checkout flows.

## Files created / deleted / modified

**Created**

- `src/app/store/app.store.ts`
- `src/app/store/features/with-sidenav.feature.ts` (+ `.spec.ts`)
- `src/app/store/features/with-cart.feature.ts` (+ `.spec.ts`)
- `src/app/store/features/with-catalog.feature.ts` (+ `.spec.ts`)
- `src/app/store/features/with-auth.feature.ts` (+ `.spec.ts`)
- `src/app/auth/auth.factories.ts` (MSAL factory functions extracted from `auth.facade.ts`)

**Deleted**

- `src/app/state/state.ts`
- `src/app/state/sidenav/sidenav.actions.ts`, `sidenav.state.ts`, `sidenav.facade.ts`
- `src/app/food/state/cart/cart.actions.ts`, `cart.state.ts`, `cart.effects.ts`, `cart.facade.ts`
- `src/app/food/state/catalog/entity-metadata.ts`, `food-data.service.ts`, `food-entity.service.ts`
- `src/app/food/state/custom-url-generator.ts`
- `src/app/auth/state/auth.actions.ts`, `auth.reducer.ts`, `auth.effects.ts`, `auth.selectors.ts`, `auth.interceptor.ts`

**Modified**

- `src/app/app.config.ts`
- `src/app/food/food.module.ts`
- `src/app/auth/msal-auth-util.module.ts`
- `src/app/app.component.ts` (+ `.html` if AsyncPipe is removed)
- `src/app/menus/navbar/navbar.component.ts`
- `src/app/menus/sidebar/sidebar.component.ts` (+ `.html`)
- `src/app/food/catalog/catalog-container/food-container.component.ts`
- `src/app/food/shop/shop-container/food-shop-container.component.ts` (+ `.spec.ts`)
- `src/app/food/shop/checkout/checkout.component.ts`
- `src/app/auth/components/current-user/current-user.component.ts` (+ `.spec.ts`)
- `src/app/auth/state/auth.facade.ts` (retain factories only, or delete in favor of `auth.factories.ts`)

## Testing & verification

- Colocate `with-<domain>.spec.ts` and drive methods, asserting on resulting signals (per the signal-store-design testing rules).
- `ng build` — proves the single-store composition and that no classic NgRx import survives.
- `ng test` — proves the migrated specs.
- `ng serve` smoke test: catalog loads, add/edit/delete a food item, cart add/remove/persist, checkout posts to `ordersApi`, sidenav toggles, auth (if enabled) still resolves.

## Risks & notes

- **`@ngrx/effects` is undeclared.** It currently compiles only because `@ngrx/data` depends on it. All effects usage is removed in this migration, so no declaration is needed.
- **The `debug` metaReducer telemetry is silently dropped** — it is already disabled (`features.logging: false`). Flag before removal if action-level AI logging was ever enabled in a deployed slot.
- **`AuthInterceptor` is dead code** and can be deleted regardless of the auth decision.
- **`ChangeDetectionStrategy.Eager`** is used on every component; converting to `OnPush` is a natural companion to signal binding but is out of scope for this NgRx migration (separate, optional follow-up).
- **`labs/07-copilot-app/copilot-app-solution/src/food-app/food-shop/`** is a duplicate copy of this app. It is out of scope here; leave it unless separately requested.
- **jsdom `matchMedia`** — once `withSidenav` runs `withHooks(onInit)` with `window.matchMedia`, add a guarded `matchMedia` polyfill to the test setup, mirroring the signal-store-design note.
