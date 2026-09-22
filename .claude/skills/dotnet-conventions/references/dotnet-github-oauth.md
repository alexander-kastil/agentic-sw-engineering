# .NET GitHub OAuth (Device Flow)

How to let a self-hosted ASP.NET Core service authenticate as a GitHub user — to clone private
repos and list the user's repositories — with **one click, no client secret, and no callback URL**.
Use the **OAuth device flow** (RFC 8628), not the web/redirect flow.

> **Validate against sources.** Cross-check the protocol against **GitHub docs** (Authorizing OAuth
> apps → Device flow) and **Microsoft Learn** (`microsoft-learn` MCP → "OAuth 2.0 device authorization
> grant", RFC 8628). Both agree on the rules below; the `slow_down` rule is the one implementations
> most often get wrong.

## When to use device flow vs web flow

- **Device flow** — the operator registers **one** OAuth App once, ticks **Enable Device Flow**, and
  puts only its **public Client ID** in config. End users click "Sign in with GitHub", type a short
  code at `github.com/login/device`, and the server receives a token. No secret, no callback URL, no
  per-user or per-repo setup. This is the right default for a single-service / admin console.
- Web (redirect) flow needs a client **secret** and a registered **callback URL** — avoid it when a
  device flow will do; it pushes secret + redirect config onto every deployment.

## Configuration — Client ID in `appsettings.json`, never `.env`

The device-flow Client ID is a **public identifier**, not a secret. It belongs in `appsettings.json`
(or the DB config registry) — not in `.env` and not in a compose env var:

```json
"GitHub": { "ClientId": "Ov23li..." }
```

```csharp
public string? ClientId => config["GitHub:ClientId"] is { Length: > 0 } id ? id : null;
public bool IsConfigured => !string.IsNullOrWhiteSpace(ClientId);
```

Rationale: device flow uses **no client secret**, so there is nothing secret to protect. `.env` is
Docker Compose's mechanism for infra values Compose itself consumes (SQL passwords, ports, Caddy
hostnames) — application config that the .NET app reads at runtime goes in appsettings.json/DB. The
standard .NET env override (`GitHub__ClientId`) still works if a deployment ever needs it.

## The two calls

**Start** — `POST https://github.com/login/device/code`, body `{ client_id, scope }`, header
`Accept: application/json`. Response: `device_code` (40 chars), `user_code` (8 chars w/ hyphen),
`verification_uri`, `expires_in` (~900s), `interval` (~5s). Scope example: `repo read:org`.

**Poll** — `POST https://github.com/login/oauth/access_token`, body
`{ client_id, device_code, grant_type }`, header `Accept: application/json`.
`grant_type` **must** be `urn:ietf:params:oauth:grant-type:device_code`. **No `client_secret`.**

```csharp
private const string GrantType = "urn:ietf:params:oauth:grant-type:device_code";

var req = new HttpRequestMessage(HttpMethod.Post, TokenUrl)
{
    Content = JsonContent.Create(new { client_id = ClientId, device_code = deviceCode, grant_type = GrantType }),
};
req.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
```

- `Accept: application/json` matters: GitHub's token endpoint returns **form-encoded** by default;
  with this header it returns JSON (`{ "access_token": ... }` or `{ "error": ... }`). GitHub accepts a
  JSON request body too (verified empirically) even though RFC/Entra examples use form-encoding.

## Carry the device_code in the request body, NOT a cookie

Do **not** stash the `device_code` in an HttpOnly cookie between `start` and `poll`. Behind a reverse
proxy (Caddy/nginx), cookie `Secure`/`SameSite`/scheme handling makes the cookie go stale or mismatch
across attempts — the classic symptom is polling a code the user never authorized, so it "waits
forever". Instead **return `device_code` from `start` to the SPA and have the SPA send it back on each
`poll`.** The access token is exchanged and stored **server-side** and never reaches the SPA, so this
is safe. It is also deterministic and debuggable.

## The `slow_down` back-off is mandatory (the #1 bug)

Map GitHub's poll errors and **honor `slow_down`**:

| GitHub `error` | Client action |
|---|---|
| `authorization_pending` | Keep polling, do not exceed `interval` |
| `slow_down` | **Increase the interval by 5s** and keep polling (RFC 8628 §3.5) |
| `access_denied` | Stop — user declined |
| `expired_token` | Stop — request a new device code |

If you ignore `slow_down` and keep polling at the original rate, GitHub returns `slow_down` on **every**
subsequent request and **never processes the authorization** — the UI hangs on "waiting" even though
the user authorized. Return the interval to the client so it can back off; poll at `interval + 1s`
initially to avoid tripping it at all.

```csharp
public sealed record PollResult(string? Token, string? Pending, int Interval);
// ... on non-token response: return new PollResult(null, body?.Error, body?.Interval);
```

## Controller shape

- `device/start` → returns `{ deviceCode, userCode, verificationUri, expiresIn, interval }`.
- `device/poll` → `[FromBody]` `{ deviceCode }`; on token, resolve login + persist, return `connected`;
  otherwise return a status (`pending` / `slow_down` (+interval) / `denied` / `expired`).
- `repos` → list `GET /user/repos?per_page=100&sort=updated&affiliation=owner,collaborator,organization_member`;
  include `owner.login` so the UI can distinguish the user's own repos from shared/org repos.
- All endpoints stay behind the app's normal authorization (MSAL/admin) — the SPA attaches its bearer.

## Using the token

Store the token once (single service identity, e.g. a `GitHubAuth` singleton row). Reuse it to clone
private repos by rewriting the URL to `https://x-access-token:<token>@github.com/owner/repo`, and to
list repos. The token is never exposed to the browser.

## Gotchas checklist

- OAuth App must have **Enable Device Flow** ticked, or `start` returns `device_flow_disabled`.
- No `client_secret` anywhere — device flow does not use one.
- `Accept: application/json` on both GitHub calls.
- Honor `slow_down` (+5s) — otherwise infinite "waiting".
- `device_code` travels in the request body, not a cookie.
- Client ID lives in `appsettings.json` (public), not `.env`.
