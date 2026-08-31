# User & Permission Admin UI (RBAC + mixed auth)

A reusable Angular pattern for a **user/role/permission administration UI** backed by **mixed auth**
(Entra ID/MSAL for humans + a local username/password JWT for a service/debug account). Pairs with the
global **`add-mixed-auth`** skill (the full-stack auth design) — this file is the **Angular client** half.

**Use when** building or extending: an admin users screen, a permission matrix, role management, a
dual-auth client (local token + MSAL), a token interceptor, or an admin route guard. Triggers:
"user admin UI", "permission admin", "roles screen", "RBAC UI", "mixed auth client", "local login form",
"admin guard", "adminEmails".

## Shape

- **Two store slices** (`@ngrx/signals` `signalStoreFeature`, composed into the app store):
  - `withAuth()` — current user + permission checks. State `{ user, authEnabled, authType:'entra'|'local'|null,
    authResolved }`; seeds a `DEV_SUPERUSER` (`permissions:['*']`) when `!authEnabled`. Computeds:
    `isAuthenticated`, `hasPermission` (a computed **returning a function** → call `store.hasPermission()('x')`),
    `isAdmin`. Methods `setUser(user, authType)`, `clearUser()`, `markAuthResolved()`.
  - `withAdmin()` — data access (`rxMethod` + `tapResponse`): `loadUsers`, `saveUser`, `saveUserCredentials`,
    `setUserRoles`, `deleteUser`, `loadRoles`, `createRole`/`updateRole`/`deleteRole`, `loadPermissions`,
    `savePermissions({roleId,entries})`, `loadAdminEmails`.
- **Dual-auth client:** a functional `HttpInterceptorFn` that (a) passes through when auth is disabled,
  (b) only decorates API-base calls, (c) skips any public/unauthenticated API paths, (d) attaches the
  **local token first** (with a 401 → clear-session + redirect-to-login handler), and (e) falls back to MSAL
  `acquireTokenSilent`. A local-session helper stores `{token, expiresAt}` in a per-app localStorage key. A
  two-path auth service does `init()`/restore (local token → `GET /auth/me`; else MSAL restore),
  `loginLocal(user,pwd)` (`POST /auth/login` → save session → `GET /auth/me`), MSAL `login()`, `logout()`,
  and a `whenReady()` gate.
- **Screens** (build with the host app's component toolkit — Material, Tailwind, or a custom `ux` library —
  do NOT assume Material): `admin-users` (table + name/role filter + a read-only "Entra admins" section from
  `adminEmails`, add/edit dialog, delete-confirm, password reset), `admin-permissions` (role selector +
  Lesen/Bearbeiten checkbox matrix over the app's routes, cascade rules, dirty-track + save), plus `user-dialog`
  and `roles-dialog`. An `adminGuard` protects the admin routes; an unguarded `/login` route hosts the local
  form + Entra button.

## API surface wrapped

`GET/POST/PUT/DELETE /users` (+ `/{id}/roles`, `/{id}/credentials`), `GET/POST/PUT/DELETE /roles`,
`GET /permissions` + `PUT /permissions/{roleId}` (replace-all, persist only `canRead||canEdit`),
`GET /auth/{me,admins}`, `POST /auth/login`. See `add-mixed-auth` for the server contracts.

## Gotchas (load-bearing)

1. **The guard MUST honor a local session before deferring to `MsalGuard`.** `MsalGuard` only checks
   `msalService.instance.getAllAccounts().length`, which is **always 0 for a local (LocalJwt) login** — so a
   guard that blindly defers to `MsalGuard` when auth is enabled calls `loginRedirect()` and bounces a
   locally-authenticated admin out to Entra, breaking every gated route for local accounts. The guard must
   `await whenReady()` and allow when the store reports an authenticated user (local OR Entra), falling
   through to `MsalGuard` only when there is **no** session. This is the correctness crux of client-side
   mixed auth — cover it with an E2E "login as the local account → reach an admin route" test.
2. **Duplicate store member names are silently dropped.** If a `withAuth` member (e.g. a `permissions`
   computed) collides with a `withAdmin` member (e.g. `permissions` state) on the composed store,
   `@ngrx/signals` keeps only one (console warning, no compile error), silently breaking permission checks.
   Give every member a unique name across composed features (e.g. `userPermissions`).
3. **Entra admins are an allow-list, not DB rows.** List the server's admin-email allow-list (`GET
   /auth/admins`) as read-only "Entra Administrator" rows, separate from managed DB users; grant/revoke Entra
   admins by editing that config (server restart reloads it), not the users table. Local users get roles from
   the DB.
4. **Dev bypass:** with auth disabled, seed a `DEV_SUPERUSER` (`['*']`) so guards pass and the admin UI is
   reachable without login; the server's `/auth/me` should mirror this (return an admin identity).
5. **Replacing `MsalInterceptor`:** the official `MsalInterceptor` unconditionally attaches an Entra token to
   matched URLs, which fights local-token auth. Replace it with the custom local-first interceptor above;
   keep the MSAL providers (`MSAL_INSTANCE`, `MSAL_GUARD_CONFIG`, `MsalService`, `MsalGuard`,
   `MsalBroadcastService`).

## Store slices (composed into `AppStore`, `store/app.store.ts`)

**`withAuth()`** — current user + permission checks. State `{ user: UserDto|null, authEnabled, authType:
'entra'|'local'|null, authResolved }`; seeds `DEV_SUPERUSER` (`permissions: ['*']`) when
`!environment.authEnabled`. Computeds: `isAuthenticated` (`!authEnabled || user!==null`),
`currentUserName`, **`userPermissions`**, `hasPermission`, `isAdmin`. Methods `setUser(user, authType)`,
`clearUser()`, `markAuthResolved()`.

**`withAdmin()`** — data access for the screens (all `rxMethod` + `tapResponse`, base
`environment.webApiUrl`): `loadUsers({text?,roleId?})`, `saveUser`, `saveUserCredentials`, `setUserRoles`,
`deleteUser`, `loadRoles`, `createRole`, `updateRole`, `deleteRole`, `loadPermissions`,
`savePermissions({roleId,entries})`, `loadAdminEmails`. State `{ users, usersTotalCount, roles,
permissions, adminEmails, *Loading }`.

API surface wrapped: `GET/POST/PUT/DELETE /api/users` (+ `/{id}/roles`, `/{id}/credentials`),
`GET/POST/PUT/DELETE /api/roles`, `GET /api/permissions` + `PUT /api/permissions/{roleId}` (replace-all,
only rows where `canRead||canEdit`), `GET /api/auth/{me,admins}`, `POST /api/auth/login`.

