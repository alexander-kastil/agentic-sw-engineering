# .NET MSAL Authentication (Microsoft.Identity.Web)

How to wire `Microsoft.Identity.Web` in an ASP.NET Core 10 API for JWT Bearer authentication against Entra ID.

> **Package version.** Stay on the latest `Microsoft.Identity.Web` 4.x (current stable **4.11.0**, 2026-06).
> Minor bumps across the 4.x line are non-breaking — no public-API or config changes to `AddMicrosoftIdentityWebApi` —
> so a straight `<PackageReference Version="…">` bump + `dotnet restore`/`build` is safe. No companion
> `Microsoft.Identity.Client` / `Microsoft.Identity.Web.UI` references are needed for a bearer-token API.

## App Registration Requirements

| Setting | Required value | Why |
|---|---|---|
| `api.requestedAccessTokenVersion` | `2` | Default (null) issues v1 tokens with issuer `https://sts.windows.net/{tenantId}/`; `Microsoft.Identity.Web` validates the v2 issuer, causing 401 |

Check and fix:

```bash
az ad app show --id <clientId> --query "api.requestedAccessTokenVersion" -o tsv
# Must return 2. If null:
az ad app update --id <clientId> --set "api={'requestedAccessTokenVersion': 2}"
```

## Do NOT Enable Easy Auth Alongside Microsoft.Identity.Web

App Service Easy Auth and `Microsoft.Identity.Web` must never coexist. Easy Auth intercepts all requests before ASP.NET Core sees them. Even setting `unauthenticatedClientAction` to `AllowAnonymous` is not enough when the config is in a broken state.

If Easy Auth is stuck enabled and cannot be disabled via CLI, delete and recreate the App Service.

## AppBuilder — Service Registration

```csharp
public static void AddMsalAuth(this WebApplicationBuilder builder)
{
    var cfg = builder.Configuration.Get<AppConfig>();
    if (!cfg.AuthEnabled) return;

    builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
        .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));
    builder.Services.AddAuthorization();
    // Do NOT add AuthorizeFilter via AddControllers here — use MapControllers().RequireAuthorization() instead
}
```

`AddMicrosoftIdentityWebApi` reads the `AzureAd` section and wires the full JWT Bearer pipeline including JWKS retrieval, signature validation, issuer/audience checks, and `Microsoft.Identity.Web` claim mapping.

**Critical: Never call `AddControllers()` twice.** If `AddMsalAuth` calls `AddControllers(options => options.Filters.Add(AuthorizeFilter))` and `Program.cs` calls `AddControllers()` again for JSON options, the filter from the first call is silently discarded.

Correct pattern — call `AddControllers` once in `Program.cs`:

```csharp
builder.AddMsalAuth();
builder.Services.AddControllers()
    .AddJsonOptions(options => options.JsonSerializerOptions.PropertyNamingPolicy = null);
```

## Program.cs — Middleware Order

The correct middleware order when using `Microsoft.Identity.Web`:

```csharp
app.UseStaticFiles();
app.UseRouting();        // 1. Routing first
app.UseCors("AllowAll"); // 2. CORS after routing
if (cfg.AuthEnabled)
{
    app.UseAuthentication(); // 3. Authentication
    app.UseAuthorization();  // 4. Authorization (MUST follow Authentication)
}

// 5. Endpoint-level authorization — never omit RequireAuthorization in production
if (cfg.AuthEnabled)
    app.MapControllers().RequireAuthorization();
else
    app.MapControllers();
```

`UseCors` must come AFTER `UseRouting` — placing it before breaks CORS policy matching.

`UseAuthorization` must always follow `UseAuthentication` — if it is absent, the authorization middleware never runs and all requests pass through unchallenged.

## AzureAd Config Section

Must be in `appsettings.json` (not only in `appsettings.Development.json`) so the production App Service can read it:

```json
"AzureAd": {
  "Instance": "https://login.microsoftonline.com/",
  "TenantId": "<tenantId>",
  "ClientId": "<clientId>",
  "Audience": "<clientId>"
}
```

`AddMicrosoftIdentityWebApi` reads `GetSection("AzureAd")`. The section name must match exactly.

### Audience — v1 vs v2 Tokens

**`Audience` must match the token's `aud` claim EXACTLY** (string comparison). Which value to use depends on the app registration's `accessTokenAcceptedVersion`:

| Manifest `accessTokenAcceptedVersion` | Token `aud` claim | API `Audience` config |
|---|---|---|
| `null` or `1` (v1 tokens) | `api://<clientId>` | `api://<clientId>` |
| `2` (v2 tokens) | bare `<clientId>` GUID | `<clientId>` (no `api://` prefix) |

Setting `Audience` to `api://<guid>` when the token is v2 produces `IDX10214: Audience validation failed`.

To accept both token versions (version-agnostic), configure `ValidAudiences` explicitly:

```csharp
builder.Services.Configure<JwtBearerOptions>(
    JwtBearerDefaults.AuthenticationScheme,
    options =>
    {
        options.TokenValidationParameters.ValidAudiences =
            [clientId, $"api://{clientId}"];
    });
```

## AppConfig Mapping

```csharp
public class AppConfig
{
    public bool AuthEnabled { get; set; }
    public AzureAdConfig AzureAd { get; set; }
    // ...
}

public class AzureAdConfig
{
    public string Instance { get; set; }
    public string TenantId { get; set; }
    public string ClientId { get; set; }
    public string Audience { get; set; }
}
```

## App Service Settings

When deploying to Azure App Service, set the `AzureAd__*` settings (double underscore = nested config path):

```bash
az webapp config appsettings set -g <rg> -n <app> --settings \
  "AzureAd__Instance=https://login.microsoftonline.com/" \
  "AzureAd__TenantId=<tenantId>" \
  "AzureAd__ClientId=<clientId>" \
  "AzureAd__Audience=<clientId>"
```

These override `appsettings.json` values at runtime. They are not required if `appsettings.json`
already carries the correct values, but setting both does no harm.

## Diagnostic JwtBearerEvents (dev only)

When 401 reasons are opaque, wire this block AFTER `AddMicrosoftIdentityWebApi`. It preserves the library's handlers and adds logging on top:

```csharp
using System;
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Logging;

if (builder.Environment.IsDevelopment())
    IdentityModelEventSource.ShowPII = true;   // reveals actual aud/iss values in IDX errors

builder.Services.Configure<JwtBearerOptions>(
    JwtBearerDefaults.AuthenticationScheme,
    options =>
    {
        var existing = options.Events ?? new JwtBearerEvents();
        options.Events = new JwtBearerEvents
        {
            OnMessageReceived = async ctx =>
            {
                if (existing.OnMessageReceived is not null) await existing.OnMessageReceived(ctx);
                var auth = ctx.Request.Headers.Authorization.ToString();
                var preview = string.IsNullOrEmpty(auth) ? "<MISSING>" : auth[..Math.Min(40, auth.Length)] + "...";
                Console.WriteLine($"[JwtBearer] OnMessageReceived path={ctx.Request.Path} authHeader={preview}");
            },
            OnTokenValidated = async ctx =>
            {
                if (existing.OnTokenValidated is not null) await existing.OnTokenValidated(ctx);
                Console.WriteLine($"[JwtBearer] OnTokenValidated aud={ctx.Principal?.FindFirst("aud")?.Value} iss={ctx.Principal?.FindFirst("iss")?.Value} scp={ctx.Principal?.FindFirst("scp")?.Value}");
            },
            OnAuthenticationFailed = async ctx =>
            {
                if (existing.OnAuthenticationFailed is not null) await existing.OnAuthenticationFailed(ctx);
                var sb = new StringBuilder();
                var ex = ctx.Exception;
                while (ex is not null) { sb.AppendLine(ex.GetType().FullName + ": " + ex.Message); ex = ex.InnerException; }
                Console.WriteLine($"[JwtBearer] OnAuthenticationFailed\n{sb}");
            },
            OnChallenge = async ctx =>
            {
                if (existing.OnChallenge is not null) await existing.OnChallenge(ctx);
                Console.WriteLine($"[JwtBearer] OnChallenge error={ctx.Error} description={ctx.ErrorDescription} failure={ctx.AuthenticateFailure?.Message}");
            }
        };
    });
```

Remove or gate behind `IsDevelopment()` before shipping. `IdentityModelEventSource.ShowPII = true` must only be set in development — it prints actual claim values (email, tenant, object ID) to the console.

## IDX Error Reference

| Code | Meaning | Fix |
|---|---|---|
| `IDX10214` | Audience validation failed | Make `Audience` match the token's `aud` claim. See the v1/v2 table above. Most common cause: `api://<guid>` config with v2 tokens (bare GUID `aud`). |
| `IDX10205` | Issuer validation failed | Check `TenantId`; v1 tokens come from `https://sts.windows.net/<tid>/`, v2 from `https://login.microsoftonline.com/<tid>/v2.0`. Both should be accepted by `Microsoft.Identity.Web` defaults. |
| `IDX10223` | Token expired | Clock skew or stale token. Check `exp` claim at jwt.ms. |
| `IDX10500` | Signature validation failed | Wrong signing key — usually means token is for a different tenant. |
| `IDX10501` | Signing key not found | Authority/TenantId mismatch — JWKS lookup hit wrong endpoint. |

If `OnAuthenticationFailed` never fires but you still get 401, the request arrived without an `Authorization` header. That is an Angular interceptor problem: check that the `protectedResourceMap` entry uses a `/*` wildcard (MSAL Angular v5 uses strict matching by default).

## 401 Triage Flow

A 401 from the API can come from either the client side (token not attached) or the server side (token rejected). Find which:

1. Open DevTools, Network, select the failed request, check Request Headers for `Authorization: Bearer ...`.
2. If the header is **MISSING**: client problem. Most common cause is the `protectedResourceMap` key missing the `/*` wildcard.
3. If the header is **PRESENT**: server rejected the token. Add the diagnostic block above, restart the API, and retry.

| API console shows | Cause | Next step |
|---|---|---|
| `authHeader=<MISSING>` | Token not attached on the client | Fix MSAL Angular interceptor |
| `OnAuthenticationFailed ... IDX10214` | Audience mismatch | Match `Audience` config to token's `aud` (most likely flip to bare GUID for v2) |
| `OnAuthenticationFailed ... IDX10205` | Issuer mismatch | Verify `TenantId` in config |
| `OnAuthenticationFailed ... IDX10223` | Expired | Re-acquire on the client |
| `OnTokenValidated ...` then 403 | Token valid, scope/role check failed | Check `[RequiredScope]` / policy attributes |
| `OnTokenValidated ...` then 200 | Working — remove diagnostics |  |

## CORS Note

`AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader()` does NOT strip the `Authorization` header — that header is not considered a CORS "credential". `AllowCredentials()` is not needed for bearer-token auth. (CORS credentials apply to cookies and `XHR.withCredentials`.)

## `AuthEnabled: false` plus `[Authorize]` locks you out of your own dev box

`if (!cfg.AuthEnabled) return;` means "no auth locally" only while no endpoint asks for it. Add
`[Authorize]` to a controller later and local development breaks in a way that reads like a bug in the
controller: every mutation returns 401 and no token can fix it, because the bare
`AddAuthentication().AddJwtBearer()` registered on that path has no authority configured, so nothing
validates. The endpoints are not open, they are unreachable.

Relax the policy, not the attribute, and gate it on the environment rather than on the flag alone:

```csharp
if (!cfg.AuthEnabled)
{
    builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer();

    if (builder.Environment.IsDevelopment())
        builder.Services.AddAuthorizationBuilder()
            .SetFallbackPolicy(null)
            .SetDefaultPolicy(new AuthorizationPolicyBuilder().RequireAssertion(_ => true).Build());
    else
        builder.Services.AddAuthorization();

    return;
}
```

Outside Development the endpoints stay locked, so an instance shipped with `AuthEnabled: false` by
mistake answers 401 rather than serving mutations anonymously. That is strictly safer than both the
early-return version and a plain `AddAuthorization()`.

**The trap this sets for tests.** `WebApplicationFactory` inherits the host environment, so an
integration test suite runs as Development, the permissive policy applies, and every `[Authorize]`
passes unconditionally. A test asserting "unauthenticated calls are rejected" then passes while
proving nothing. Pin the test host to a non-Development environment and let the suite's own auth
handler satisfy the real policy:

```csharp
builder.UseEnvironment("Test");
```

Verify by running the negative case: an unauthenticated request must return 401 in the test suite. If
it returns 200 or 201, the host is still Development. See `false-green-checks`, shape 6.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Every authenticated endpoint 401s on localhost with `AuthEnabled: false` | `[Authorize]` is enforced but the fallback `AddJwtBearer()` has no authority, so no token validates | Permissive default policy gated on `IsDevelopment()`, per the section above |
| Integration test asserting 401 passes trivially, and so does everything else | `WebApplicationFactory` inherited the Development environment and its permissive policy | `builder.UseEnvironment("Test")` on the factory |
| 401 from Azure with `"You do not have permission to view this directory"` | Easy Auth is intercepting requests | Delete and recreate the App Service without Easy Auth |
| 401 even with valid Bearer token | `requestedAccessTokenVersion` is null, issuing v1 tokens with wrong issuer | Set to `2` on app registration |
| 401 even after adding `UseAuthorization()` | `AddControllers()` called twice — second call silently replaces the filter | Consolidate to one `AddControllers()` call; use `MapControllers().RequireAuthorization()` |
| CORS error in browser before auth | `UseCors` placed before `UseRouting` | Move `UseCors` after `UseRouting` |
| Authorization not enforced at all | `UseAuthorization()` absent from pipeline | Add after `UseAuthentication()` |
| Audience set to `api://<guid>`, token `aud` is bare GUID | `accessTokenAcceptedVersion: 2` issues bare GUID tokens | Switch `Audience` to bare GUID, or configure `ValidAudiences` with both |

## Common Pitfalls

- **`Audience` set to `api://<guid>` while app issues v2 tokens** — IDX10214. The single most common 401 cause on this stack. Fix by switching to the bare GUID or by configuring `ValidAudiences` with both.
- **No `[Authorize]` attribute anywhere, but 401 still fires.** Look for `MapControllers().RequireAuthorization()` in `Program.cs` — it applies a fallback policy to every controller globally.
- **`UseCors` called AFTER `UseAuthentication`.** Correct order is CORS first; otherwise preflight `OPTIONS` requests may be rejected before CORS headers are written.
- **Secrets in committed `appsettings*.json`.** `Microsoft.Identity.Web` reads `AzureAd:ClientCredentials` from config; rotate any committed secret and move to user-secrets or Key Vault.
