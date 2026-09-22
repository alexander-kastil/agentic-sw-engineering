# Angular MSAL Authentication — Overview

How to wire MSAL Angular with `@azure/msal-angular ^5.x` and `@azure/msal-browser ^5.x` for an Angular 22 standalone SPA talking to a protected .NET API.

---

## Interaction Type — Critical Rule

**Never mix popup and redirect in the same app.** Pick one and use it everywhere:

| Concern | Popup | Redirect |
|---|---|---|
| `MsalGuard interactionType` | `Popup` | `Redirect` |
| `MsalInterceptor interactionType` | `Popup` | `Redirect` |
| `login()` method | `loginPopup()` | `loginRedirect()` |

**Recommended: use Redirect.** Popup flow has a cross-window session storage problem in Angular standalone — the popup loads the full Angular app, `APP_INITIALIZER` runs `handleRedirectObservable()` in the popup context, but the cached token request lives in the main window's session storage only. Result: `no_token_request_cache_error` in the popup, login hangs indefinitely.

---

## Environment Configuration

```typescript
// environment.ts / environment.prod.ts
export const environment = {
  apiUrl: 'https://your-api.azurewebsites.net',
  authEnabled: true,
  azure: {
    msalConfig: {
      auth: {
        clientId: '<SPA clientId>',
        authority: 'https://login.microsoftonline.com/<tenantId>/',
        redirectUri: '/',
      },
    },
    protectedScopes: ['api://<clientId>/access_as_user'],
  },
};
```

---

## MSAL Providers Factory

```typescript
// msal.auth.ts
import { APP_INITIALIZER } from '@angular/core';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import {
  MsalInterceptorConfiguration,
  MsalGuardConfiguration,
  MsalInterceptor,
  MSAL_INSTANCE,
  MSAL_GUARD_CONFIG,
  MSAL_INTERCEPTOR_CONFIG,
  MsalService,
  MsalGuard,
  MsalBroadcastService,
} from '@azure/msal-angular';
import {
  PublicClientApplication,
  BrowserCacheLocation,
  InteractionType,
} from '@azure/msal-browser';
import { firstValueFrom } from 'rxjs';
import { environment } from '../../environments/environment';

export function MSALInstanceFactory() {
  return new PublicClientApplication({
    auth: {
      clientId: environment.azure.msalConfig.auth.clientId,
      authority: environment.azure.msalConfig.auth.authority,
      redirectUri: environment.azure.msalConfig.auth.redirectUri,
      postLogoutRedirectUri: environment.azure.msalConfig.auth.redirectUri,
      // DO NOT add navigateToLoginRequestUrl here — in msal-browser/angular v5 it is
      // NOT set here, it moved to handleRedirectObservable() options. Set it false there
      // when login can start from the same URL as redirectUri (e.g. a landing page
      // with redirectUri '/'), or the redirect return hangs on `/?state=...`.
    },
    cache: { cacheLocation: BrowserCacheLocation.LocalStorage },
    system: {
      allowPlatformBroker: false, // REQUIRED on Windows — disables WAM broker
    },
  });
}

export function MSALInterceptorConfigFactory(): MsalInterceptorConfiguration {
  const protectedResourceMap = new Map<string, Array<string>>();
  // Key MUST end with /api/* — the trailing wildcard is required. MSAL v5 has
  // strictMatching ON by default, so `${apiUrl}/api/` (no wildcard) matches ONLY
  // the exact URL `/api/`, never `/api/inventory` → no token attached → 401.
  protectedResourceMap.set(`${environment.apiUrl}/api/*`, environment.azure.protectedScopes);
  return {
    interactionType: InteractionType.Redirect,
    protectedResourceMap,
  };
}

export function MSALGuardConfigFactory(): MsalGuardConfiguration {
  return {
    interactionType: InteractionType.Redirect,
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

---

## `protectedResourceMap` Key Rules

Under MSAL v5 `strictMatching` (the default), the key is a **glob pattern**, not a plain prefix. To cover every path under `/api`, the key MUST end with `/api/*`. The trailing `*` is the whole game.

| Key | Result |
|---|---|
| `https://api.example.com/api/*` | ✅ Correct — attaches token to all `/api/<path>` requests |
| `https://api.example.com/api/` | ❌ No wildcard — strict matching treats this as an exact URL, not a prefix, so real calls like `/api/inventory` get NO token → 401 |
| `https://api.example.com/api` | ❌ Missing trailing slash and wildcard — will not match sub-paths |
| `https://api.example.com` | ❌ Too broad — attaches token to every request including static files |

The `/*` suffix is a special wildcard marker the v5 matcher recognizes. It is not shell glob expansion.

The failure is silent and confusing: the request still goes out (to the correct absolute URL) but with no `Authorization` header, so the API returns 401 and the browser may surface it as a CORS-flavoured error. The server logs show no token-validation failure because no token ever arrived. If you see a 401 with the right URL and no `IDX*` audience/signature error server-side, suspect a missing `*` here first.

### Interceptor ordering when combined with a base-URL rewrite interceptor

If you issue relative URLs (`http.get('/api/inventory')`) and rely on a functional interceptor to prefix `environment.apiUrl`, that rewrite MUST run before `MsalInterceptor` sees the request — otherwise MSAL matches the relative URL against `window.location.origin` (the SPA host, not the API host) and never matches the map. With `provideHttpClient(withInterceptors([apiBaseInterceptor]), withInterceptorsFromDi())` the functional interceptor is registered first, so it runs first — correct. The robust alternative (used by the vouchers-ai reference app) is to issue absolute `${environment.apiUrl}/api/...` URLs at the call site so MSAL always sees the final URL regardless of interceptor order.

---

## `app.config.ts` Registration

```typescript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptorsFromDi, withFetch } from '@angular/common/http';
import { msalServiceProviders } from './auth/msal.auth';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptorsFromDi(), withFetch()), // withInterceptorsFromDi() required for MsalInterceptor
    ...(environment.authEnabled ? msalServiceProviders : []),
  ],
};
```

`withInterceptorsFromDi()` is **required** because `MsalInterceptor` is registered via the class-based `HTTP_INTERCEPTORS` token. Without it, the interceptor is silently dropped and no bearer token is attached.

---


## See Also

- [`msal-auth-patterns.md`](msal-auth-patterns.md) - `AuthService`, functional guards, logout, the auth toggle
- [`msal-troubleshooting.md`](msal-troubleshooting.md) - blank page, redirect loop, missing `Authorization` header, 401 triage
- [`msal-version-changes.md`](msal-version-changes.md) - which major to run and what each one broke
- [`msal-angular.md`](msal-angular.md) - client wiring deep-dive: full provider setup, `APP_INITIALIZER`, `AuthStateService`
- [`msal-angular-appreg.md`](msal-angular-appreg.md) - Entra app registration via Azure CLI

