# Health Checks in ASP.NET Core

Reference for adding real `/health` endpoints — liveness, readiness, and dependency probes —
independent of hosting style (minimal hosting vs. `Startup.cs`) or endpoint style (minimal APIs
vs. MVC controllers). Health checks work identically across all four combinations.

## Package

`Microsoft.Extensions.Diagnostics.HealthChecks` — part of the shared framework since .NET 6, no
extra NuGet package needed for the basics.

## Basic probe

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();          // existing controllers, unaffected
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapControllers();
app.MapHealthChecks("/health");

app.Run();
```

Classic `Startup.cs` wiring is the same shape: `services.AddHealthChecks()` in
`ConfigureServices`, `endpoints.MapHealthChecks("/health")` inside `UseEndpoints` in `Configure`.

With no checks registered, the app is "healthy" if it can respond at all — this alone satisfies a
basic Docker `HEALTHCHECK`.

## `MapHealthChecks` vs. `UseHealthChecks`

| | `MapHealthChecks` (routing) | `UseHealthChecks` (middleware) |
|---|---|---|
| Where | Endpoint, evaluated with other routes | Anywhere in the pipeline, before routing |
| Auth | Composable — `app.MapHealthChecks("/health").RequireAuthorization()` | Not endpoint-aware |
| Multiple endpoints | Yes — call it once per path/tag combination | Awkward |
| Short-circuit | `app.MapHealthChecks("/health").ShortCircuit()` | Always terminates the pipeline on match |

Default to `MapHealthChecks` — it composes with `RequireAuthorization()` and other endpoint
metadata, and supports mapping multiple tagged endpoints cleanly. Only reach for `UseHealthChecks`
when a health check must run in front of routing (rare).

## Dependency checks (DB, downstream services)

A "the process is up" check is weaker than "the process can actually do its job":

```csharp
builder.Services.AddHealthChecks()
    .AddSqlServer(
        connectionString: builder.Configuration.GetConnectionString("DefaultConnection")!,
        name: "sql-server",
        tags: ["ready"])
    .AddUrlGroup(new Uri("https://api.example.com/ping"), name: "downstream-api", tags: ["ready"]);
```

`AddSqlServer` comes from the community `AspNetCore.HealthChecks.SqlServer` package (not
Microsoft-maintained) and runs `SELECT 1` — keep the probe query trivial; don't run anything that
could add load to the database.

For EF Core, prefer the first-party `Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore`
package instead — it calls `DbContext.CanConnectAsync()`:

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>(tags: ["ready"]);
```

`AspNetCore.HealthChecks.*` community packages exist for Postgres, MySQL, Redis, RabbitMQ, and
most common dependencies.

## Custom checks

```csharp
public class QueueDepthHealthCheck : IHealthCheck
{
    public Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, CancellationToken ct = default)
    {
        var depth = GetQueueDepth();
        return Task.FromResult(depth < 10_000
            ? HealthCheckResult.Healthy($"Queue depth: {depth}")
            : HealthCheckResult.Degraded($"Queue depth high: {depth}"));
    }
}

builder.Services.AddHealthChecks()
    .AddCheck<QueueDepthHealthCheck>("queue-depth", tags: ["ready"]);
```

`CheckHealthAsync` returns `Healthy`, `Degraded`, or `Unhealthy`. A check can also consume DI —
inject config or options into the `IHealthCheck` implementation's constructor when the probe needs
more than what a static delegate can capture.

## Liveness vs. readiness

Two different questions, worth separating once past a trivial app:

- **Liveness** — "is the process alive and not deadlocked?" Keep cheap and fast; a restart is the
  right response if this fails. Exclude all dependency checks.
- **Readiness** — "can it serve real traffic right now?" (DB reachable, migrations applied, caches
  warm.) A failing readiness check shouldn't trigger a restart — the process is fine, it's just not
  ready yet.

Tag dependency checks `"ready"` and filter by tag per endpoint:

```csharp
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false                              // exclude everything — liveness only
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")   // only dependency checks
});
```

Point Docker's `HEALTHCHECK` (and container-orchestrator restart policies) at `/health/live`. Point
a load balancer or readiness gate at `/health/ready`. Kubernetes readiness probe example:

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 80
  initialDelaySeconds: 30
  timeoutSeconds: 1
```

For startup work that must finish before an app is ready (e.g. a slow config download), register a
singleton `IHealthCheck` that a `BackgroundService` flips to healthy on completion, tagged `"ready"`
— don't restart the process while it's still starting up. There's no separate Kubernetes-style
"startup probe" concept in ASP.NET Core health checks — model it as a readiness check instead.

Filtering by multiple tags is OR logic — a check runs if it matches any tag in the predicate:

```csharp
Predicate = check => check.Tags.Contains("foo_tag") || check.Tags.Contains("baz_tag")
```

## Health check options

```csharp
app.MapHealthChecks("/health", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("sample"),   // filter which checks run
    ResultStatusCodes =
    {
        [HealthStatus.Healthy] = StatusCodes.Status200OK,
        [HealthStatus.Degraded] = StatusCodes.Status200OK,
        [HealthStatus.Unhealthy] = StatusCodes.Status503ServiceUnavailable
    },
    AllowCachingResponses = false   // default: sets Cache-Control/Expires/Pragma to prevent caching
});
```

## Custom JSON response

By default `/health` returns a plain `Healthy`/`Unhealthy`/`Degraded` string. For a richer response
(useful if a dashboard consumes it directly):

```csharp
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        var payload = new
        {
            status = report.Status.ToString(),
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString(),
                description = e.Value.Description,
                duration = e.Value.Duration
            })
        };
        await context.Response.WriteAsync(JsonSerializer.Serialize(payload));
    }
});
```

## Push-based publishing (`IHealthCheckPublisher`)

For monitoring systems that expect the app to push status rather than being polled, register an
`IHealthCheckPublisher` — the health check system runs it on a timer and calls `PublishAsync` with
the aggregated report:

```csharp
public class SampleHealthCheckPublisher : IHealthCheckPublisher
{
    public Task PublishAsync(HealthReport report, CancellationToken cancellationToken)
    {
        // push report.Status / report.Entries to an external monitoring system
        return Task.CompletedTask;
    }
}

builder.Services.Configure<HealthCheckPublisherOptions>(options =>
{
    options.Delay = TimeSpan.FromSeconds(2);      // initial delay after startup (default: 5s)
    options.Period = TimeSpan.FromSeconds(30);    // execution interval (default: 30s)
    options.Predicate = check => check.Tags.Contains("sample");
});

builder.Services.AddSingleton<IHealthCheckPublisher, SampleHealthCheckPublisher>();
```

The community `AspNetCore.HealthChecks.UI` package builds on this pattern to provide a dashboard
that polls multiple services' health endpoints and a `HealthCheckPublisher` for pushing results —
not Microsoft-maintained, evaluate before adopting.

## Security

A health endpoint can leak internal details (dependency names, exception messages via a custom
`ResponseWriter`). For anything beyond a bare liveness check, either restrict `/health/ready` to
internal network access or gate it behind auth:

```csharp
app.MapHealthChecks("/health/ready", readinessOptions).RequireAuthorization();
```

Keep `/health/live` anonymous and cheap — orchestrators need to reach it without a token.

`RequireHost` alone isn't a security boundary — `HttpRequest.Host` is client-supplied and can be
spoofed. If restricting a health endpoint to a specific port, chain `RequireAuthorization()` after
it rather than relying on the host/port match alone:

```csharp
app.MapHealthChecks("/healthz")
    .RequireHost("*:5001")
    .RequireAuthorization();
```

## Adding `/health` to an MCP server (or anything auth-gated)

An MCP server has no controllers to hang a health route off: the whole surface is one transport
endpoint carrying the auth policy. Map health as its own endpoint beside it:

```csharp
builder.Services.AddHealthChecks();

app.UseAuthentication();
app.UseAuthorization();

app.MapMcp("/mcp").RequireAuthorization("Mcp");
app.MapHealthChecks("/health").AllowAnonymous();
```

**`AllowAnonymous()` is endpoint metadata, and only the authorization middleware reads it.** It
correctly bypasses `RequireAuthorization("...")`, a `FallbackPolicy`, and an
`AuthenticationHandler` such as an API-key scheme. It does **nothing** against a hand-rolled
`app.Use(async (ctx, next) => ...)` that checks a header on every request: that middleware runs
before routing has selected an endpoint and never sees the metadata. Read the pipeline before
claiming the endpoint is reachable unauthenticated, and prove it with an unauthenticated request
rather than by reading the `.AllowAnonymous()` call.

Verify: `curl -i http://127.0.0.1:<port>/health` with no credentials returns `200 Healthy`, while
the same call to the MCP route returns `401`.

## Wiring into a Docker `HEALTHCHECK`

A HEALTHCHECK is two dependencies, the endpoint and the probe binary, and only one of them is
visible in the app's code: `mcr.microsoft.com/dotnet/aspnet:*` ships with neither `curl` nor
`wget`, so the probe fails on the missing binary and the container reads `unhealthy` while serving
traffic perfectly. Install it in the runtime stage per
[docker-dotnet](../../docker-images/references/docker-dotnet.md), and verify with
`docker inspect --format '{{.State.Health.Status}}'` rather than by reading the Dockerfile.

Once `/health` exists and the runtime image has `curl` (or `wget` on Alpine-based images):

```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --retries=5 --start-period=15s \
  CMD curl -f http://localhost:8080/health || exit 1
```

Or the equivalent in `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 15s
```

## Detecting an existing health endpoint without writing code

Useful for tooling (like an onboarding pipeline) that wants to *use* a health endpoint if one
exists, without injecting code into someone else's repo. A safe, read-only signal check:

- Search source for `MapHealthChecks(` or `UseHealthChecks(` (minimal hosting or `Startup.cs`).
- Search for a controller route matching `health` (`[Route("health")]`, `[HttpGet("health")]`).
- Search `.csproj` files for an `AspNetCore.HealthChecks.*` or
  `Microsoft.Extensions.Diagnostics.HealthChecks*` package reference as a corroborating signal.

If none of these match, treat the endpoint as absent and fall back to a TCP-level check
(e.g. `bash -c '</dev/tcp/127.0.0.1/<port>'`) rather than guessing at a path that may 404.

## `/api/about`: exposing build identity alongside health

A health probe answers "is it up". An about endpoint answers "*which build* is up", which is what a
fleet or ops dashboard actually needs. Keep both, anonymous, and give them one shape across every API
in a portfolio so a single client can consume all of them:

```json
{
  "slot": "blue", "imageTag": "ghcr.io/org/app:blue", "container": "86944018cf85",
  "environment": "Production", "runtime": ".NET 10.0.10", "version": "a1b2c3d",
  "gitTag": "main", "gitSha": "a1b2c3d4e5f6",
  "startedAtUtc": "2026-07-31T17:56:02Z", "uptimeSeconds": 323,
  "status": "healthy", "checks": { "database": "healthy" }
}
```

Values flow `docker build --build-arg` -> `ARG` -> `ENV Deployment__*` -> config binding -> DTO.

### The `"unknown"` sentinel trap

The Dockerfile `ARG`s default to the literal string `"unknown"`. If the CI workflow never passes
`build-args:`, the endpoint returns **HTTP 200 with every build field reading `"unknown"`**. The
feature looks shipped, the probe looks green, and the data is worthless. This survives review easily
because nothing errors.

- **Verify the values, never just the status code.** `curl` the deployed endpoint and read the payload.
  A 200 is not evidence the wiring works.
- **Never render the sentinel.** A client must treat `""`, whitespace, and `"unknown"` as absent
  (one shared `isUnknown()` helper) and omit the element or show a neutral placeholder. Printing the
  word "unknown" to a customer is worse than printing nothing.
- Where no workflow computes a real git tag, `GIT_TAG` honestly degrades to the branch name. Say so
  rather than inventing a tagging scheme; `gitSha` is the real build identity.

### Consuming it cross-origin: probe states are not HTTP statuses

A browser dashboard on a different origin cannot map HTTP status to UI state naively:

- The endpoint must list the dashboard origin in `Cors:AllowedOrigins`. Keep that in the checked-in
  `appsettings.json` so the fix ships **inside the image**, with no hand-managed box env change.
- A redirecting hostname (`www` -> apex) is useless as an allowed origin: a redirect never carries the
  preflight. Allow the canonical host.
- **A 404 without CORS headers is indistinguishable from a network failure**, so a client cannot tell
  "endpoint absent" from "host unreachable". Design the state machine for that, not against it.

Map outcomes to intent, and pick tone by *who reported the fault*:

| Outcome | State | Tone |
| --- | --- | --- |
| 200, `status`/`checks` all healthy | `ok` | success |
| 200 or 503 with any `unhealthy` value | `degraded` | **danger** (the service reported a real fault) |
| 404 | `absent` | neutral |
| network error, CORS failure, timeout | `unreachable` | **neutral, never danger** |

The rule: **red means the service told us something is wrong; muted means we could not ask it.**
A slot running an older image, or one merely blocked by CORS, is usually serving production traffic
perfectly. Painting it red says "this app is down" and is simply false.
