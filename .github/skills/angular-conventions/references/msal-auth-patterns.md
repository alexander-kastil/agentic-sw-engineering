# MSAL Angular — AuthService, Guards, Logout

The application-level patterns that sit on top of the MSAL providers: a cached `AuthService`, functional guards in both directions, the two kinds of logout, and running the same build with auth off.

---

## Bootstrapping: AuthService + functional guard (recommended)

Prefer a small `AuthService` with a cached `ensureInitialized()` over `MsalGuard`'s
auto-login when you want a public login page and full control of post-login navigation.
**The critical rule: something must call `ensureInitialized()` at startup (the root
component) or the guard's observable never resolves and the app renders a blank page.**
This is the #1 cause of a "blank screen the moment auth is enabled" — it stays dormant
while `authEnabled=false` (the guard short-circuits) and only bites when you flip it on.

```typescript
// auth.service.ts
@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly msal = inject(MsalService, { optional: true });
  private cachedInit$?: Observable<void>;

  ensureInitialized(): Observable<void> {
    if (!this.msal) return of(undefined);                   // auth disabled / no MSAL providers
    this.cachedInit$ ??= this.msal.initialize().pipe(       // v5 REQUIRES initialize() first
      concatMap(() => this.msal!.handleRedirectObservable()),
      tap((r) => { if (r?.account) this.msal!.instance.setActiveAccount(r.account); }),
      map(() => undefined),
      shareReplay(1),                                        // run once; replay to guard + root
    );
    return this.cachedInit$;
  }

  login(): void {
    this.msal?.loginRedirect({ scopes: environment.azure.protectedScopes })
      .subscribe({ error: (e) => console.error('loginRedirect failed', e) });
  }
  logout(): void {
    this.msal?.logoutRedirect()
      .subscribe({ error: (e) => console.error('logoutRedirect failed', e) });
  }
}
```

**Subscribe to `loginRedirect()` / `logoutRedirect()`, always.** They return Observables. Dropping
them on the floor looks harmless because `msal-angular` wraps a promise chain that fires whether or
not anything subscribes, so a clean session still redirects and the code passes every test. The
failure is the unhappy path: any rejection becomes an unhandled promise rejection with nothing
attached to surface it, so the button visibly does nothing, prints no error a user would find, and
offers no retry. `BrowserAuthError: interaction_in_progress` is the common one, set by MSAL whenever
an earlier redirect did not complete (a closed Microsoft tab, a double click, a stale flag from a
previous session), and it survives in the cache until something clears it. Symptom to recognise:
"the Login button does nothing" on one machine while the same build works on a fresh profile.

```typescript
// app.ts — call it ONCE at startup; gate routing on completion
export class App {
  private readonly auth = inject(AuthService);
  protected readonly ready = signal(false);
  constructor() {
    this.auth.ensureInitialized().subscribe({ next: () => this.ready.set(true), error: () => this.ready.set(true) });
  }
}
// app.html:  @if (ready()) { <router-outlet /> } @else { <div class="auth-splash">…</div> }
```

```typescript
// auth.guard.ts — functional, reuses the cached init
export const authGuard: CanActivateFn = () => {
  if (!environment.authEnabled) return true;               // toggle: pass through when disabled
  const auth = inject(AuthService); const router = inject(Router);
  return auth.ensureInitialized().pipe(map(() => (auth.isAuthenticated() ? true : router.createUrlTree(['/login']))));
};
```

Read the signed-in user from the MSAL `AccountInfo` (`account.name` / `account.username`).
**Do NOT call a `/api/auth/me` endpoint unless one actually exists** — a 404 there will clear
the user right after a successful login and bounce the guard straight back to `/login`.

---

## Logout: server sign-out vs. local-only (v5)

`logoutRedirect()` always navigates the browser to the Entra end-session endpoint
(`login.microsoftonline.com/.../oauth2/v2.0/logout`), clearing the IdP session and — **if no
account is passed — showing a "pick an account to sign out" interstitial** before returning to
`postLogoutRedirectUri`. Choose the call by intent:

| Goal | Call |
|---|---|
| Full sign-out (terminate the Entra session too) | `msalService.logoutRedirect({ account })` — pass the active account to skip the account-picker |
| **Local-only** sign-out (clear tokens, stay on-site, **no** redirect to Microsoft) | `msalService.instance.clearCache({ account })` then `router.navigate(['/'])` |

```typescript
logout(): void {
  this._isLoggedIn.set(false);
  this._userName.set('');
  const account =
    this.msal?.instance.getActiveAccount() ?? this.msal?.instance.getAllAccounts()[0];
  if (account) {
    this.msal!.instance.clearCache({ account }); // local-only: wipes that account's tokens, zero network
  }
  this.router.navigate(['/']);                    // guard reads the now-false isLoggedIn() signal
}
```

**MSAL v5 gotcha:** the documented `logoutRedirect({ onRedirectNavigate: () => false })` "skip
server sign-out" snippet does **not compile** in msal-browser v5 — `onRedirectNavigate` was
removed from the per-request `EndSessionRequest` type (it now lives only on the global
`BrowserAuthOptions`). Use `instance.clearCache(request?: ClearCacheRequest)` with `{ account }`
instead (verified against `@azure/msal-browser` 5.15). **Trade-off:** a local-only logout leaves
the Entra **server session active**, so a later login can complete silently without re-prompting —
usually the desired SPA UX; use full `logoutRedirect({ account })` when the IdP session must end too.

---

## Guard pattern: redirect authenticated users away from public/landing routes

The inverse of `authGuard`. Put it on a public landing route (`path: ''`) so a signed-in user is
sent straight to the app shell (e.g. `/dashboard`) and never sees the marketing/login view:

```typescript
export const publicOnlyGuard: CanActivateFn = async () => {
  if (!environment.authEnabled) return true;
  const auth = inject(AuthService); const router = inject(Router);
  await auth.whenReady();                                   // or ensureInitialized()
  return auth.isLoggedIn() ? router.createUrlTree(['/dashboard']) : true;
};
```

Pair it with hiding the public nav links when `auth.isLoggedIn()` (`@if (!authEnabled || !auth.isLoggedIn())`)
so the logged-in shell stays clean.

---

## Toggle-able auth (one flag, both ends)

Gate the whole thing behind a single `environment.authEnabled` flag so the app runs open during
development and flips to protected for prod:
- Frontend: spread MSAL providers only when enabled — `...(environment.authEnabled ? msalProviders : [])`; guards return `true` early when disabled.
- Backend (.NET): read `Auth:Enabled`; when **true** register `AddMicrosoftIdentityWebApi("AzureAd")` and an `AdminOnly` policy = `RequireAuthenticatedUser()`; when **false** register `AdminOnly` = `RequireAssertion(_ => true)` (allow-all) and skip `UseAuthentication`. Annotate protected controllers with `[Authorize(Policy = "AdminOnly")]` — it then enforces when enabled and is a no-op when disabled, with no per-toggle edits. Keep genuinely public endpoints (e.g. a read-only content feed another site consumes) un-annotated / `[AllowAnonymous]`.

---


## See Also

- [`angular-msal-auth.md`](angular-msal-auth.md) - provider wiring the patterns here assume
- [`msal-troubleshooting.md`](msal-troubleshooting.md) - blank page, redirect loop, 401 triage
- [`msal-angular.md`](msal-angular.md) - `AuthStateService`, `MsalRedirectComponent`, bootstrap rules

