# MSAL Angular — Troubleshooting

Every failure mode of an MSAL Angular SPA in one place: what the symptom means, where the fault sits, and the fix. Read this when auth is wired but misbehaving.

---

## Popup Failure Mode (do not repeat)

Symptoms:

- Popup opens, user authenticates, popup stays open
- Main window stays at login screen
- Console in popup: `BrowserAuthError: no_token_request_cache_error`

Root cause: The popup window loads Angular, `APP_INITIALIZER` calls `handleRedirectObservable()`, MSAL tries to do a full redirect exchange but the original token request is in the **main window's session storage** (not the popup's). MSAL fails before sending `postMessage` back to opener.

Fix: switch to redirect flow (see `msal-angular.md`).

---

## Do NOT Enable Easy Auth Alongside MSAL Angular

**App Service Easy Auth and `Microsoft.Identity.Web` must never coexist.** Easy Auth intercepts requests at the infrastructure layer before .NET sees them. If `unauthenticatedClientAction` is not `AllowAnonymous`, it returns 401/redirect responses that override the app's own auth logic.

If Easy Auth was previously enabled on the App Service, delete and recreate the App Service — disabling it via CLI is unreliable when `configVersion: v2` is active.

---

## 401 Triage — Client Side

A 401 from `https://localhost:5001/api/...` can come from either side. Find which:

1. Open DevTools > Network > failed request > check **Request Headers** for `Authorization: Bearer ...`.
2. If header is **MISSING**, this is a client problem. Most common cause: `protectedResourceMap` key without `/*` wildcard (v5 strict matching). Work through the Troubleshooting table below.
3. If header is **PRESENT**, the server rejected the token. Most common cause: `Audience` config is `api://<guid>` while app issues v2 tokens (token `aud` is bare GUID), causing `IDX10214`. Consult the .NET MSAL reference.

---

## Anti-pattern: hand-rolled token interceptor → redirect loop

Do not write a custom interceptor that calls `acquireTokenRedirect` (or `loginRedirect`) on
failure. Combined with a missing/404 user-load call it produces an infinite loop: API call →
silent acquire fails → `acquireTokenRedirect` → Microsoft → back to app → user-load 404 →
clear user → guard → API call → … Use `MsalInterceptor` + `protectedResourceMap`, which only
acquires **silently** and never triggers interaction from inside the HTTP pipeline.

---

## Debug Auth Mode

`environment.development.ts` sets `authEnabled: false` to disable MSAL entirely during local development. The mechanic relies on three pieces working together:

| File | Role |
|---|---|
| `src/app/auth/auth.tokens.ts` | Declares `AUTH_ENABLED` injection token backed by `environment.authEnabled` |
| `src/app/auth/auth.service.ts` | `init()` checks `AUTH_ENABLED`; when false, calls `store.setUser({ email: 'claude@debug.local', isAdmin: true })` |
| `app.html` | Gates the authenticated shell components (e.g. `<app-{shell-nav}>`, `<app-{primary-feature}>`) on `@if (store.isAuthenticated())` |

`store.isAuthenticated()` is a computed signal that returns `user() !== null`. When `authEnabled` is false and `init()` seeds the debug user, the signal is true and the full shell renders. When auth is disabled WITHOUT seeding a user, `store.isAuthenticated()` stays false and the entire app shell (nav, primary feature surfaces, admin features) is hidden.

The `/login` route redirects to `/` when auth is off. The guard and MSAL interceptor are bypassed.

**Rule:** never set `authEnabled: false` without verifying that `auth.service.ts init()` seeds a fallback user. Prod `environment.ts` stays `authEnabled: true` and must not be changed.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| **Blank page the moment auth is enabled, no console error** | Nothing calls `ensureInitialized()` at startup, so the guard's observable never resolves | Call it once from the root component constructor and gate `<router-outlet>` on a `ready` signal |
| **Redirect loop bouncing through Microsoft** | A custom interceptor calls `acquireTokenRedirect` on failure, and/or the bootstrap hits a non-existent `/api/auth/me` (404) that clears the user | Use `MsalInterceptor` + `protectedResourceMap` (silent acquire only); read the user from `AccountInfo`, not `/me` |
| `Authorization` header missing | `protectedResourceMap` key does not match request URL | Add `/*` wildcard suffix to the key |
| `Authorization` header missing | `withInterceptorsFromDi()` absent from `provideHttpClient` | Add it to `app.config.ts` |
| 401 even with valid login | `requestedAccessTokenVersion` is null (v1 token) | Set to 2 on app registration |
| 401 with `"You do not have permission to view this directory or page."` | Easy Auth is blocking the request | Disable / remove Easy Auth from App Service |
| Token not attached to requests | `protectedResourceMap` key doesn't match request URL (most often a missing `*` wildcard under strictMatching) | Verify key ends with `/api/*` and matches `environment.apiUrl` exactly |
| First request 401s, subsequent succeed | HTTP call fires before MSAL settles | Gate calls behind `inProgress$` reaching `InteractionStatus.None` |
| `redirect_uri` mismatch (AADSTS50011) | `redirectUri: '/'` resolves to `origin + '/'` (trailing slash) but the registration has no trailing slash (or vice-versa) | Make `environment.msal.redirectUri` an explicit absolute URL that matches the registered SPA redirect URI exactly |
| Redirect loop on login | `redirectUri` not registered as SPA redirect URI | Add to app registration under SPA platform |
| Stuck on `/?state=...` after login | Login started from the same URL as `redirectUri` with `navigateToLoginRequestUrl` defaulting to `true` | Pass `{ navigateToLoginRequestUrl: false }` to `handleRedirectObservable()` and let the app handle post-login navigation |
| Logout redirects to `login.microsoftonline.com` / shows "pick an account to sign out" | `logoutRedirect()` always hits the Entra end-session endpoint; with no account it adds the account-picker | For local-only sign-out use `instance.clearCache({ account })` + in-app navigate; for full sign-out pass `{ account }` to skip the picker (see Logout section) |

---

## 401 Troubleshooting

If `https://localhost:5001/api/...` returns 401, work through these in order. (For server-side validation failures, see the .NET MSAL reference.)

### 1. Is the `Authorization` header actually being sent?

Open DevTools > Network > the failing request > Request Headers. If `Authorization: Bearer ...` is **missing**, the interceptor did not match the request URL. Continue to step 2.

If the header is **present**, the problem is server-side — token rejected. Consult the .NET reference's IDX error table.

### 2. `protectedResourceMap` key — strict matching trap

msal-angular v5 enables `strictMatching` by default. Under strict matching, a key without a wildcard suffix only matches that exact URL, not subpaths. The `/*` suffix is a special marker the matcher recognizes as "match this prefix and anything under it".

```typescript
// WRONG — only matches the literal URL "https://localhost:5001/api/" (zero real requests hit this)
protectedResourceMap.set(`${environment.apiUrl}/api/`, scopes);

// CORRECT — matches /api/anything/anything
protectedResourceMap.set(`${environment.apiUrl}/api/*`, scopes);
```

If the interceptor finds no matching key, it silently skips the request and no token is attached, resulting in 401 with `Authorization` header absent.

**Counter-intuitive note:** the `/*` is NOT shell glob expansion — it is parsed by the matcher. The literal `*` character is the documented v5 wildcard form.

### 3. Is the user signed in?

In DevTools > Application > Local Storage, look for keys like `msal.<clientId>.account.keys` and `msal.<clientId>-login.<tenant>-accesstoken-...`. If absent, the login redirect never completed; verify `redirectUri` matches the SPA registration in Azure AD.

### 4. Is the interceptor in the HttpClient chain?

`provideHttpClient(withInterceptorsFromDi(), withFetch())` — the `withInterceptorsFromDi()` is **required** because `MsalInterceptor` is registered via the class-based `HTTP_INTERCEPTORS` token. Without it, the interceptor is silently dropped.

### 5. Did the first HTTP call fire before MSAL settled?

If a store or component fires an HTTP request from its constructor or `APP_INITIALIZER`-adjacent code, it may run before `inProgress$` reaches `InteractionStatus.None` and the active account is set. Symptom: first request 401s, subsequent requests succeed.

Fix: gate HTTP calls behind `msalBroadcastService.inProgress$.pipe(filter(s => s === InteractionStatus.None))` or behind a "ready" signal in `AuthStateService`.

---


## See Also

- [`angular-msal-auth.md`](angular-msal-auth.md) - provider wiring, `protectedResourceMap`, `app.config.ts`
- [`msal-auth-patterns.md`](msal-auth-patterns.md) - `AuthService`, guards, logout, the auth toggle
- [`msal-angular-appreg.md`](msal-angular-appreg.md) - Entra app registration via Azure CLI
- [`msal-version-changes.md`](msal-version-changes.md) - which major to run, and what each one broke

