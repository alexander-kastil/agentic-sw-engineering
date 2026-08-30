# Runtime configuration injection (one bundle, many environments)

Angular's default answer to per-environment config is `fileReplacements` in `angular.json`: a
`environment.<slot>.ts` swapped in at build time. That works, but it bakes the API host into the
bundle, which means **every environment needs its own build**. If the app ships as a container, that
also means the image you tested is never the image you promote.

Runtime injection removes that: the bundle reads its config from a `config.js` written at container
start, so one build serves every environment.

## When to use which

| Situation | Approach |
| --- | --- |
| Values differ per environment and the app is containerized | Runtime injection (this file) |
| Values differ only between local dev and everything else | `fileReplacements` is fine; keep `environment.development.ts` |
| A value is a secret | Neither. Anything in the bundle or in `config.js` is public; it reaches the browser |

`config.js` is served to the browser, so it may hold only what is already public: API base URLs, a
public MSAL client id, a tenant authority, a telemetry instrumentation key. Never a client secret,
never a connection string.

## The environment module

Read the injected object, fall back to sane defaults. The fallbacks are what keep `ng serve` and
Vitest working, since neither serves a `config.js`:

```ts
interface AppRuntimeConfig {
  apiBase?: string;
  siteBase?: string;
  msalClientId?: string;
  msalAuthority?: string;
}

declare global {
  // eslint-disable-next-line no-var
  var __APP_CONFIG__: AppRuntimeConfig | undefined;
}

const runtimeConfig = globalThis.__APP_CONFIG__ ?? {};

const msalClientId = runtimeConfig.msalClientId ?? '00000000-0000-0000-0000-000000000000';

export const environment = {
  production: true,
  apiBase: runtimeConfig.apiBase ?? 'https://api.example.com',
  authEnabled: true,
  siteBase: runtimeConfig.siteBase ?? 'https://www.example.com',
  msal: {
    clientId: msalClientId,
    authority: runtimeConfig.msalAuthority ?? 'https://login.microsoftonline.com/<tenant-id>/',
    redirectUri: '/',
    postLogoutRedirectUri: '/',
    scope: `api://${msalClientId}/access_as_user`,
  },
};
```

Rules that matter here:

- **Keep the exported object's shape identical** to what it was before the conversion. Every consumer
  imports `environment`; if the shape holds, the conversion touches nothing else in the app.
- **Derive, do not repeat.** `msal.scope` is built from `msalClientId` rather than injected
  separately, so the client id cannot be updated in one place and stale in the other.
- **Type the injected object.** `declare global` with an interface, never `any`.
- Do not turn `environment` into a service or a signal. It is read at module init, before the
  injector exists (MSAL config in `app.config.ts` needs it at bootstrap).

## index.html

```html
<head>
  <meta charset="utf-8">
  <title>…</title>
  <base href="/">
  <script src="config.js"></script>
```

After `<meta charset>` (so the charset stays in the first bytes) and before anything Angular injects.
A plain relative `src`, so a strict `script-src 'self'` CSP is satisfied without a nonce. Under `ng
serve` this 404s harmlessly and the fallbacks take over.

## Removing the old machinery

The conversion is only half-done until these are gone, and a leftover slot build configuration is the
usual way it half-lands:

1. Delete `src/environments/environment.<slot>.ts`.
2. Remove that slot's build **and** serve configuration from `angular.json`, including its
   `fileReplacements`. Also remove any per-slot configuration that is now a byte-for-byte duplicate of
   `production`; it no longer means anything and implies a slot-specific build still exists.
3. Drop the slot build ARG from the Dockerfile and build with a plain `npm run build`. Confirm
   `defaultConfiguration` is `production` first, or the plain build silently produces a dev bundle.
4. Keep `environment.development.ts` and the `development` configuration. Local dev is not a slot.

Verify with a grep, not by eye:

```bash
grep -rn "blue-api.example.com\|blue.example.com" src/ angular.json     # must be empty
grep -o "__APP_CONFIG__[^;]\{0,180\}" dist/*/browser/main-*.js          # must show the ?? fallbacks
```

The second grep is the decisive one: it proves the *shipped* bundle reads the global. Since `??`
short-circuits on a defined value, an injected config always wins over the fallback.

## Container side

The `config.template.js` + `envsubst` entrypoint, the unprivileged-nginx `chown` trap, the CRLF
`.gitattributes` trap, the no-cache rules for `config.js`/`index.html`, and the one-image-two-slots
acceptance test are deployment concerns. They are documented in the `deploy-init` skill's
`references/slot-agnostic-images.md`. Read that before touching the Dockerfile.

One rule belongs on both sides: **the entrypoint must refuse to start when a required variable is
missing.** An SPA that boots with `apiBase` empty looks perfectly healthy and silently talks to
nothing, which is far harder to diagnose than a container that will not start.

## Scope check before converting

Only convert apps that actually have per-environment values. A SPA whose MSAL `redirectUri` is
relative and which calls its API on a same-origin path has nothing to inject, and adding the
machinery to it is pure overhead. Check first, then convert the ones that need it.
