# MSAL Angular — Version Choice and Breaking Changes

Which `@azure/msal-angular` major to run against which Angular, and exactly what changed at each hop. Read before an upgrade and when an API that used to exist no longer compiles.

---

## MSAL Browser v5 — Breaking API Changes

| What changed | Before (v4) | After (v5) |
|---|---|---|
| Account storage events | `instance.enableAccountStorageEvents()` | Remove — always enabled |
| Account added/removed events | `EventType.ACCOUNT_ADDED / REMOVED` | `EventType.LOGIN_SUCCESS / LOGOUT_SUCCESS` |
| Logout | `authService.logout()` | `authService.logoutRedirect()` or `logoutPopup()` |
| Navigate after redirect | `auth.navigateToLoginRequestUrl: true` in config | Pass to `handleRedirectObservable({ navigateToLoginRequestUrl })` |
| Popup redirect handler | `handleRedirectObservable()` anywhere | `APP_INITIALIZER` (see msal-angular.md) |
| Platform broker (Windows) | Default off | **Default on** — must set `allowPlatformBroker: false` |

### `BrowserAuthOptions` — removed properties

`navigateToLoginRequestUrl` is **no longer a valid key** in the `auth` config block. Remove it from `MSALInstanceFactory`. Pass it to `handleRedirectObservable()` if needed — set it `false` there when login can start from the same URL as `redirectUri` (e.g. a landing page with `redirectUri: '/'`), or the redirect return hangs on `/?state=...`.

---

## MSAL Angular v5 — Breaking Changes

| What changed | Before (v4) | After (v5) |
|---|---|---|
| `MsalService.logout()` | Available | Removed — use `logoutRedirect()` / `logoutPopup()` |
| `protectedResourceMap` matching | Loose by default | **Strict by default** — use `path/*` wildcards |
| `handleRedirectObservable(hash)` | Accepts hash string | Deprecated — pass `{ hash: '...' }` options object |
| Token injection to `inject(TOKEN)` | String-based | Type-based — TypeScript errors without explicit types |

---

## Pick the right major first

`npm outdated` cannot see this and neither can the peer range: msal-angular publishes its supported Angular versions as a table in its README. Read it from the installed package before deciding anything:

```bash
sed -n '/## Version Support/,/## Prerequisites/p' node_modules/@azure/msal-angular/README.md
```

| MSAL Angular version | Supported Angular versions |
| --- | --- |
| v6 (active development) | 22 |
| v5 (maintenance) | 19, 20, 21 |
| v4 (maintenance) | 15, 16, 17, 18, 19, 20 |

**On Angular 22, only msal-angular v6 is supported**, and v6 requires `@azure/msal-browser ^5.18.0`, so the two move together. A v4 app on Angular 22 installs, typechecks, builds and passes its tests while being formally unsupported; that exact combination was found in `dashboard.integrations.at` on 2026-08-10 with nothing flagging it. Verify the pairing with `npm ls @azure/msal-angular @azure/msal-browser` plus the table above, not with `npm outdated`.

---

## v4 to v6 upgrade: what actually changes

Going 4 to 6 crosses both the v4 to v5 and v5 to v6 guides. In practice the code delta is small; the audit is the work.

Bump both packages in one install, because v6 peers on msal-browser `^5.18.0` and a partial bump leaves an unresolvable tree:

```bash
npm install --legacy-peer-deps @azure/msal-angular@^6.0.3 @azure/msal-browser@^5.18.0
```

`npm install` writes the new caret floors into `package.json` itself. Confirm it did, because a Dockerfile that copies only `package.json` and runs `npm install` (no lockfile) would otherwise rebuild the image on v4 regardless of a green lockfile. See `angular-update.md`, "Caret floors are the deployed version".

### The one required code change: `navigateToLoginRequestUrl` moved

It did not disappear in v5, it **relocated** from the `PublicClientApplication` config into the `handleRedirectPromise()` / `handleRedirectObservable()` call:

```typescript
// v4: in BrowserAuthOptions (no longer valid)
new PublicClientApplication({ auth: { ..., navigateToLoginRequestUrl: false } });

// v5+: an option on the call
provideAppInitializer(() => {
  const msal = inject(MsalService);
  return firstValueFrom(
    msal.initialize().pipe(
      concatMap(() => msal.handleRedirectObservable({ navigateToLoginRequestUrl: false })),
    ),
    { defaultValue: null },
  );
});
```

Passing a bare hash string to `handleRedirectObservable()` is deprecated; use the options object.

### Removed-API audit checklist

Run these greps over `src/` before bumping. Each maps to a documented v5/v6 break:

| Check | Command | Why |
| --- | --- | --- |
| `protectedResourceMap` strict matching | `grep -rn "protectedResourceMap" src/` | v5 makes `strictMatching` the default. Bare base URLs stop matching subpaths, and the symptom is a 401 with **no** `Authorization` header. Keys need an explicit `/*` suffix. An app with no `MsalInterceptor` at all is unaffected. |
| Removed `logout()` | `grep -rn "\.logout(" src/` | Removed entirely; use `logoutRedirect()` / `logoutPopup()`. A local-only `instance.clearCache({ account })` sign-out is unaffected, it is a different API. |
| Removed config keys | `grep -rn "temporaryCacheLocation\|claimsBasedCachingEnabled\|storeAuthStateInCookie\|secureCookies\|cacheMigrationEnabled\|skipAuthorityMetadataCache\|supportsNestedAppAuth\|encodeExtraQueryParams" src/` | All dropped from `BrowserAuthOptions` / `CacheOptions` in v5. |
| Renamed system options | `grep -rn "asyncPopups\|iframeHashTimeout\|windowHashTimeout" src/` | `asyncPopups` became `navigatePopups` with **reversed** logic; the hash timeouts became `iframeBridgeTimeout` / `popupBridgeTimeout`. |
| Removed account getters | `grep -rn "getAccountByHomeId\|getAccountByLocalId\|getAccountByUsername" src/` | Replaced by `getAccount()` with a parameter object. |
| Request param consolidation | `grep -rn "authorizePostBodyParams\|tokenBodyParameters\|tokenQueryParameters" src/` | All fold into `extraParameters`. |

Surviving untouched across v4 to v6: `new PublicClientApplication(...)`, `getActiveAccount`, `getAllAccounts`, `setActiveAccount`, `clearCache`, `loginRedirect`, `EventType.LOGIN_SUCCESS` / `LOGOUT_SUCCESS`, and the `auth.*` / `cache.cacheLocation` / `system.allowPlatformBroker` config keys.

### The v6 change-detection caveat, and why signals satisfy it

v6 auto-initializes the client inside `loginRedirect`, `acquireTokenSilent`, `ssoSilent` and friends, which removes most `uninitialized_public_client_application` errors. In exchange, **components subscribing to `inProgress$` or `msalSubject$` must trigger change detection themselves** after mutating state, via `cdr.detectChanges()` / `markForCheck()`.

A service that writes subscription results into **signals** already satisfies this: signal writes notify consumers on their own, and the upgrade guide names signals as the recommended alternative to manual CD. No change needed for the `AuthStateService` pattern below. A component that assigns to a plain field in a `subscribe()` callback does need the fix.

Still required in v6, unchanged: subscribe to `handleRedirectObservable()` once at startup, and gate interactive calls on `inProgress$ === InteractionStatus.None`.

### The redirect bridge is OPTIONAL, do not add one by reflex

v5 added COOP support via a redirect bridge page, exposed as the subpath export `@azure/msal-browser/redirect-bridge` (visible in the package's `exports` map, `dist/redirect_bridge/index.mjs`). Its own doc comment: "Processes the authentication response from the redirect URL. For SSO and popup scenarios broadcasts it to the main frame. For redirect scenario navigates to the home page."

**Decision rule:**

| Your app | Bridge needed? |
| --- | --- |
| Redirect-only (`InteractionType.Redirect`, `loginRedirect`), path-based routing | **No.** Add nothing. |
| Hash-based routing (`withHashLocation()`) | **Yes, recommended.** Without it the auth response lands in the URL and collides with the hash router. |
| Popup or `ssoSilent` under COOP headers | **Yes.** |
| `logoutRedirect` | Optional. If present on the `postLogoutRedirectUri` page it returns the user to the origin. |

Confirm the precedent before adding one: `admin.integrations.at` runs msal-browser 5.18.0 with **no** bridge page (its `public/` holds only `favicon.ico`), because it is redirect-only with path routing. If you do add one, remember it must be a built file rather than an inline script when the CSP is `script-src 'self'`.

### Verifying the bump landed, without signing in

You can prove v5 is really in the bundle without touching auth:

- **Bundle size drops.** v5 hashes error messages to shrink the bundle. The dashboard's initial total went 408.80 kB to 371.03 kB (main 404.94 to 367.17) purely from the major bump.
- **Failures look different at runtime.** Error messages and console logs are hashed, so a v5 failure surfaces as a short code plus a link rather than a sentence. That is expected, not corruption, and it needs the decode script to read.

What a build and a test run **cannot** tell you: anything about the redirect flow. When providers are registered conditionally (`...(environment.authEnabled ? msalProviders : [])`) and the local runtime config ships `authEnabled: false`, MSAL never initializes in dev or in tests. A green suite is silent on auth. The redirect path needs a human clicking through a deployed slot: expect a clean URL with no leftover `#code=`/`?code=` after sign-in, a deep link to survive the round trip, and a reload not to bounce to Microsoft again.

---


## See Also

- [`angular-msal-auth.md`](angular-msal-auth.md) - the wiring the new APIs go into
- [`msal-angular.md`](msal-angular.md) - provider setup, `AuthStateService`, migration checklist
- [`msal-troubleshooting.md`](msal-troubleshooting.md) - symptoms an unfinished upgrade produces

