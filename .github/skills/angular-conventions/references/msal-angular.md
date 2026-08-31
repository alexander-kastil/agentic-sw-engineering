# Angular MSAL — Standalone Setup Reference

> Angular 22 standalone + `@azure/msal-angular ^6.x` + `@azure/msal-browser ^5.x`

---

## Provider Setup (`msal.auth.ts`)

```typescript
import { APP_INITIALIZER } from '@angular/core';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import {
  MsalInterceptorConfiguration, MsalGuardConfiguration, MsalInterceptor,
  MSAL_INSTANCE, MSAL_GUARD_CONFIG, MSAL_INTERCEPTOR_CONFIG,
  MsalService, MsalGuard, MsalBroadcastService,
} from '@azure/msal-angular';
import {
  LogLevel, IPublicClientApplication, PublicClientApplication,
  BrowserCacheLocation, InteractionType,
} from '@azure/msal-browser';
import { firstValueFrom } from 'rxjs';

export function MSALInstanceFactory(): IPublicClientApplication {
  return new PublicClientApplication({
    auth: {
      clientId: environment.azure.msalConfig.auth.clientId,
      authority: environment.azure.msalConfig.auth.authority,
      redirectUri: environment.azure.msalConfig.auth.redirectUri, // e.g. '/'
      postLogoutRedirectUri: environment.azure.msalConfig.auth.redirectUri,
      // DO NOT add navigateToLoginRequestUrl here: removed from config in v5.
      // It moved onto the call: handleRedirectObservable({ navigateToLoginRequestUrl: false })
    },
    cache: { cacheLocation: BrowserCacheLocation.LocalStorage },
    system: {
      allowPlatformBroker: false, // REQUIRED on Windows — disables WAM broker
      loggerOptions: { ... },
    },
  });
}

export function MSALInterceptorConfigFactory(): MsalInterceptorConfiguration {
  const protectedResourceMap = new Map<string, Array<string>>();
  protectedResourceMap.set(`${environment.apiUrl}/api/*`, environment.azure.protectedScopes);
  return {
    interactionType: InteractionType.Redirect, // match the guard
    protectedResourceMap,
  };
}

export function MSALGuardConfigFactory(): MsalGuardConfiguration {
  return {
    interactionType: InteractionType.Redirect, // match the interceptor
    authRequest: { scopes: environment.azure.protectedScopes },
    loginFailedRoute: '/login-failed',
  };
}

function msalInitializerFactory(msalService: MsalService) {
  return () => firstValueFrom(msalService.handleRedirectObservable(), { defaultValue: null });
}

export const msalServiceProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: MsalInterceptor, multi: true },
  { provide: MSAL_INSTANCE, useFactory: MSALInstanceFactory },
  { provide: MSAL_GUARD_CONFIG, useFactory: MSALGuardConfigFactory },
  { provide: MSAL_INTERCEPTOR_CONFIG, useFactory: MSALInterceptorConfigFactory },
  MsalService,
  MsalGuard,
  MsalBroadcastService,
  {
    provide: APP_INITIALIZER,
    useFactory: msalInitializerFactory,
    deps: [MsalService],
    multi: true,
  },
];
```

**Why `APP_INITIALIZER`?** It ensures MSAL is fully initialized (via `handleRedirectObservable()`) before Angular routes activate. Without it, the `MsalGuard` may run against an uninitialized `PublicClientApplication`, or a redirect response (`#code=...`) can be stripped by the router before MSAL reads it.

**Do NOT also call `handleRedirectObservable()` in `AuthStateService`** — `APP_INITIALIZER` is the single owner.

---

## `MsalRedirectComponent` — NOT for Standalone

The docs are explicit:

> "This approach is not compatible with Angular standalone components."

Do **not** do:

```typescript
// WRONG for standalone
bootstrapApplication(MsalRedirectComponent, appConfig);
```

```html
<!-- WRONG — remove if present -->
<app-redirect></app-redirect>
```

The `APP_INITIALIZER` pattern above replaces `MsalRedirectComponent` for standalone apps.

---

## `AuthStateService` — Auth State Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class AuthStateService {
  private readonly msalGuardConfig = inject<MsalGuardConfiguration>(MSAL_GUARD_CONFIG);
  private readonly authService = inject(MsalService);
  private readonly msalBroadcastService = inject(MsalBroadcastService);
  private readonly router = inject(Router);

  loggedInUserEMail = signal('');

  constructor() {
    // Listen for login/logout events
    this.msalBroadcastService.msalSubject$.pipe(
      filter((msg: EventMessage) =>
        msg.eventType === EventType.LOGIN_SUCCESS ||   // was ACCOUNT_ADDED in v4
        msg.eventType === EventType.LOGOUT_SUCCESS,    // was ACCOUNT_REMOVED in v4
      ),
    ).subscribe(() => {
      if (this.authService.instance.getAllAccounts().length === 0) {
        window.location.pathname = '/';
      }
    });

    // Set active account when interaction completes
    this.msalBroadcastService.inProgress$.pipe(
      filter((status: InteractionStatus) => status === InteractionStatus.None),
    ).subscribe(() => {
      const account =
        this.authService.instance.getActiveAccount() ??
        this.authService.instance.getAllAccounts()[0];
      if (account) {
        this.authService.instance.setActiveAccount(account);
        this.loggedInUserEMail.set(account.username);
        if (this.router.url === '/') this.router.navigate(['/vouchers']);
      } else {
        this.loggedInUserEMail.set('');
      }
    });
  }

  login() {
    // Use loginRedirect — loginPopup has cross-window session storage issues
    if (this.msalGuardConfig.authRequest) {
      this.authService.loginRedirect({ ...this.msalGuardConfig.authRequest } as RedirectRequest);
    } else {
      this.authService.loginRedirect();
    }
  }

  logout() {
    this.authService.logoutRedirect(); // logout() removed in MSAL Angular v5
    this.loggedInUserEMail.set('');
  }
}
```

> **Local-only logout (no Microsoft round-trip).** `logoutRedirect()` always navigates to the
> Entra end-session endpoint (and, with no account, shows a "pick an account to sign out" page).
> For a purely local sign-out — clear tokens and stay on-site — call
> `msalService.instance.clearCache({ account })` then navigate in-app. The documented
> `logoutRedirect({ onRedirectNavigate: () => false })` "skip server sign-out" pattern does **not
> compile in v5** (`onRedirectNavigate` moved off the per-request type onto global
> `BrowserAuthOptions`); use `clearCache({ account })` instead. Trade-off: the Entra server session
> persists, so a later login can complete silently.

---

## `main.ts` — Single Bootstrap Only

```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

bootstrapApplication(App, appConfig).catch(err => console.error(err));
// No second bootstrapApplication(MsalRedirectComponent) — not for standalone
```

---

## Checklist for MSAL v4 to v5 Migration

- [ ] Remove `enableAccountStorageEvents()` call
- [ ] Replace `EventType.ACCOUNT_ADDED` with `LOGIN_SUCCESS`, `ACCOUNT_REMOVED` with `LOGOUT_SUCCESS`
- [ ] Replace `authService.logout()` with `logoutRedirect()` or `logoutPopup()`
- [ ] Move `navigateToLoginRequestUrl` out of `BrowserAuthOptions` and into the `handleRedirectObservable({ navigateToLoginRequestUrl: false })` call
- [ ] Add `allowPlatformBroker: false` to `system` config
- [ ] Add `APP_INITIALIZER` with `handleRedirectObservable()`
- [ ] Remove `MsalRedirectComponent` bootstrap and `<app-redirect>` from index.html
- [ ] Remove any `handleRedirectObservable()` call from service constructors
- [ ] Set `InteractionType.Redirect` consistently (guard + interceptor + login method)
- [ ] Update `protectedResourceMap` keys to use `path/*` wildcards (strictMatching is now default)
- [ ] Replace `loginPopup()` with `loginRedirect()` in login method
- [ ] Replace any `PopupRequest` type with `RedirectRequest`

---

## `app.config.ts` Pattern

```typescript
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptorsFromDi(), withFetch()),
    AppStore,
    ...(environment.authEnabled ? msalServiceProviders : []),
  ],
};
```

Conditionally loading providers via `authEnabled` flag is fine — MSAL tokens and interceptors are only registered when auth is enabled.

---

## `environment.ts` — Project MSAL Config

```typescript
export const environment = {
  production: false,
  apiUrl: 'https://localhost:5001',
  authEnabled: true,
  azure: {
    msalConfig: {
      auth: {
        clientId: '54f03c51-f41a-4f1f-97ca-d219ee28ee50',
        authority: 'https://login.microsoftonline.com/d92b247e-90e0-4469-a129-6a32866c0d0a/',
        redirectUri: '/',                 // resolves to http://localhost:4200/ — must match SPA redirect URI in Azure AD
      },
    },
    protectedScopes: ['api://54f03c51-f41a-4f1f-97ca-d219ee28ee50/access_as_user'],
  },
};
```

Key values:

| Property | Value |
|---|---|
| `clientId` | `54f03c51-f41a-4f1f-97ca-d219ee28ee50` |
| `authority` | `https://login.microsoftonline.com/d92b247e-90e0-4469-a129-6a32866c0d0a/` |
| `redirectUri` | `/` (resolves to `http://localhost:4200/` in dev) |
| `protectedScopes` | `api://54f03c51-f41a-4f1f-97ca-d219ee28ee50/access_as_user` |

The `protectedScopes` value is also the `access_as_user` scope exposed in **Expose an API** in the app registration — see `msal-angular-appreg.md`.

---


## See Also

- [`msal-version-changes.md`](msal-version-changes.md) - which major to run, v4 to v6 upgrade
- [`angular-msal-auth.md`](angular-msal-auth.md) - provider wiring, `protectedResourceMap`, `app.config.ts`
- [`msal-auth-patterns.md`](msal-auth-patterns.md) - `AuthService`, guards, logout
- [`msal-troubleshooting.md`](msal-troubleshooting.md) - 401 triage and every other failure mode

