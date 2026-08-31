# .NET MCP Server: auth, trust levels and the reverse proxy

## Behind a reverse proxy: honour X-Forwarded-Proto or OAuth discovery breaks

An MCP server's 401 challenge carries the absolute URL of its protected-resource
metadata, and ASP.NET Core builds that from **its own** scheme. Kestrel behind Caddy /
nginx / App Gateway sees plain HTTP, so it advertises
`resource_metadata="http://host/.well-known/oauth-protected-resource"` while the site
is https. Clients follow that URL, discovery dead-ends, and Claude reports *"Automatic
client registration isn't supported"* — an auth-shaped message with a transport cause.

```csharp
var forwarded = new ForwardedHeadersOptions
{
    ForwardedHeaders = ForwardedHeaders.XForwardedProto | ForwardedHeaders.XForwardedHost | ForwardedHeaders.XForwardedFor
};
forwarded.KnownNetworks.Clear();   // the proxy is the only hop in front of Kestrel
forwarded.KnownProxies.Clear();
app.UseForwardedHeaders(forwarded);   // before UseRouting and any auth middleware
```

Check it from outside, not from the container:

```bash
curl -sD - -o /dev/null -X POST https://<host>/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"p","version":"1"}}}' \
  | grep -i www-authenticate
```

Optional — add when the server needs a database:

```xml
<PackageReference Include="Microsoft.EntityFrameworkCore" Version="10.0.x" />
<PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="10.0.x" />
<PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="10.0.x" />
```

## Two trust levels on one server: `[Authorize]` per tool, from 2.2

Before `ModelContextProtocol.AspNetCore` 2.2 this was a hard split: `AddMcpServer()` is a single DI
registration and `MapMcp` takes only a route pattern, so `/mcp` and `/mcp/admin` in one process
served **the same tools twice** with two auth decisions in front of identical capability, and the
remedy was two projects.

2.2 removes the constraint. `IMcpServerBuilder.AddAuthorizationFilters()` honours
`[Authorize]` and `[AllowAnonymous]` on individual tools, prompts and resources, and its
`FilterAuthorizedItemsAsync` filters **list** operations too, so a protected tool is invisible to a
caller who may not call it. Tool authorization runs before background dispatch, so a refused call
never executes.

```csharp
builder.Services.AddMcpServer()
    .WithHttpTransport()
    .AddAuthorizationFilters()
    .WithTools<PublicTools>()
    .WithTools<AdminTools>();

app.MapMcp("/mcp").AllowAnonymous();   // the endpoint stays open; each tool decides
```

```csharp
[McpServerTool]
[Authorize(Policy = "McpAdmin")]
[Description("...")]
public async Task<InquiryListResult> list_inquiries(...) => ...
```

Three things this gets wrong if you skip them:

- **The attribute belongs on the method.** Verify a class-level `[Authorize]` on the
  `[McpServerToolType]` before relying on it; the per-method attribute is what was proven to work.
- **An anonymous endpoint never runs a custom auth handler.** With `.AllowAnonymous()` on `MapMcp`,
  ASP.NET Core authenticates only the default scheme, so an `X-API-Key` handler registered as a
  second scheme is never invoked and the key-bearing caller reads as anonymous. Naming the scheme in
  the policy does not fix it: a policy evaluated inside the filter checks the *current* principal.
  Authenticate it explicitly before `UseAuthorization`:

  ```csharp
  app.Use(async (ctx, next) =>
  {
      if (ctx.User.Identity?.IsAuthenticated != true && ctx.Request.Headers.ContainsKey("X-API-Key"))
      {
          var result = await ctx.AuthenticateAsync("ApiKey");
          if (result.Succeeded) ctx.User = result.Principal!;
      }
      await next();
  });
  ```

- **An always-authenticated test handler hides the whole feature.** A `WebApplicationFactory` that
  replaces the default scheme with a handler returning `AuthenticateResult.Success` makes every
  request authenticated, so the tool list is complete for "anonymous" callers and the guard test
  passes while measuring nothing. Give the MCP tests a factory that leaves authentication alone.

Rules that survive the change:

- **Pin the surface with a guard test**, now three assertions rather than one: the anonymous
  `tools/list` equals an explicit array, the authenticated list adds exactly the private names, and
  an anonymous `tools/call` on a private tool is refused without returning data.
- **Prove the guard by watching it fail.** Remove one `[Authorize]`, run, see red, restore, see
  green. Without that, a filter that silently is not wired reads as a pass.
- The trust boundary is the **data**, not the transport. An anonymous `/mcp` serving exactly what an
  already-anonymous REST endpoint serves adds no exposure.
- Split into two projects only for a reason 2.2 does not solve: separate deployment, separate
  scaling, or a network boundary the data actually needs.

## Securing the /mcp endpoint (dual auth)

`app.MapMcp("/mcp")` returns an endpoint you gate explicitly — it sits **outside** `MapControllers()`, so a blanket `MapControllers().RequireAuthorization()` does **not** cover it. To accept both an Entra ID JWT (for OAuth clients like Claude.ai) **and** a static API key (for header-capable clients like Claude Desktop/Code via `mcp-remote`), combine two schemes under one policy:

```csharp
var mcp = app.MapMcp("/mcp");
if (cfg.App.AuthEnabled) mcp.RequireAuthorization("Mcp");   // leave open in dev
```

```csharp
// JWT: accept both the API's own audience and the MCP resource URI
builder.Services.Configure<JwtBearerOptions>(JwtBearerDefaults.AuthenticationScheme, o =>
{
    o.TokenValidationParameters.ValidAudiences = [ $"api://{cfg.EntraId.ClientId}", cfg.Mcp.ResourceUri ];
    o.Events = new JwtBearerEvents { OnChallenge = ctx => { /* emit WWW-Authenticate below */ } };
});
// API key: a custom handler that DEFERS (NoResult) when its header is absent, so JWT can still run
builder.Services.AddAuthentication().AddScheme<AuthenticationSchemeOptions, McpApiKeyAuthHandler>("ApiKey", _ => { });
builder.Services.AddAuthorization(o => o.AddPolicy("Mcp", p =>
    p.AddAuthenticationSchemes(JwtBearerDefaults.AuthenticationScheme, "ApiKey").RequireAuthenticatedUser()));
```

- The key handler **must return `AuthenticateResult.NoResult()` when its header is missing** (not `Fail()`), or the two schemes can't coexist — `Fail()` short-circuits the whole policy. Return `Fail()` only when a key is present but wrong.
- Expose an **anonymous** RFC 9728 discovery endpoint so OAuth clients can find the auth server:
  `GET /.well-known/oauth-protected-resource` → `{ resource, authorization_servers, scopes_supported, bearer_methods_supported: ["header"] }`.
- On a 401 for `/mcp`, emit `WWW-Authenticate: Bearer resource_metadata="{scheme}://{host}/.well-known/oauth-protected-resource", error="invalid_token"` so clients auto-discover it.
- For the OAuth `resource`/scope byte-match gotcha (AADSTS9010010), custom-domain requirement, and which clients support header auth vs. OAuth-only, see the `mcp-keybased-auth` / `mcp-claude` skills — those own the client side.
