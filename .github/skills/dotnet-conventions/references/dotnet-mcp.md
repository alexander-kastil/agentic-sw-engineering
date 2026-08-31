# .NET MCP Server Reference

General-purpose reference for building a .NET MCP (Model Context Protocol) server using `ModelContextProtocol` and `ModelContextProtocol.AspNetCore`. Use this file when creating or extending any .NET MCP server project.

## NuGet Packages

Core MCP packages:

```xml
<PackageReference Include="ModelContextProtocol" Version="2.2.0" />
<PackageReference Include="ModelContextProtocol.AspNetCore" Version="2.2.0" />
```

`dotnet package search ModelContextProtocol --exact-match` is not a reliable way to
pick a version. It has been observed returning only the oldest `0.1.0-preview.*`
entries; on 2026-08-28 it returned `1.0.0` through `2.2.0` ascending, with the current
version as the last row. Either way it is a truncated, ordering-dependent view and
`--take N` does not mean "the newest N". Read the flat index instead, which lists every
published version in order:

```bash
curl -s https://api.nuget.org/v3-flatcontainer/modelcontextprotocol/index.json
```

Confirm what actually resolved after `dotnet restore --force`, since a stale
`obj/project.assets.json` lets a build succeed against the old package:

```bash
grep -oE '"ModelContextProtocol(\.AspNetCore)?/[0-9][^"]*"' obj/project.assets.json | sort -u
```

**2.x is a silent behaviour change, not just a version bump.** The 1.x -> 2.0
breaking-change list touches nothing in the shape below (attributes, registration and
`Task<string>` tools all compile unchanged), so the upgrade looks free — but
`HttpServerTransportOptions.Stateless` now defaults to **true**. A single POST to
`/mcp` now answers `tools/list` with no session, and any curl recipe or doc that walks
`initialize` -> `Mcp-Session-Id` -> `notifications/initialized` is stale. Verify by
calling `tools/list` directly and counting the tools.

## Program.cs — HTTP Transport

```csharp
using ModelContextProtocol.Server;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<MyDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("MyDb")));
builder.Services.AddScoped<IMyService, MyService>();

builder.Services.AddMcpServer()
    .WithHttpTransport()
    .WithToolsFromAssembly();

var app = builder.Build();

app.MapMcp();

app.Run();
```

- `AddMcpServer()` registers MCP protocol infrastructure.
- `.WithHttpTransport()` uses ASP.NET Core Kestrel as the transport — no stdio.
- `.WithToolsFromAssembly()` auto-discovers every class marked `[McpServerToolType]`.
- `app.MapMcp()` mounts the MCP routes onto the HTTP pipeline at `/mcp`.

## Tool Class Structure

```csharp
using System.ComponentModel;
using ModelContextProtocol.Server;

[McpServerToolType]
internal class MyTools
{
    private readonly IMyService _service;
    private readonly ILogger<MyTools> _logger;

    public MyTools(IMyService service, ILogger<MyTools> logger)
    {
        _service = service;
        _logger = logger;
    }

    [McpServerTool]
    [Description("Short description of what this tool does")]
    public async Task<string> DoSomething(
        [Description("What this parameter controls")] string input,
        [Description("Optional flag with a default")] bool flag = false)
    {
        var result = await _service.ProcessAsync(input, flag);
        return result;
    }
}
```

- One `[McpServerToolType]` per class; one `[McpServerTool]` per method.
- Every parameter must have a `[Description("...")]` attribute — MCP clients use this for introspection.
- Return `string` for simple text results; return a typed DTO for structured data.
- Optional parameters use default values (`= false`, `= 8`, etc.).
- Nullable parameters (`string?`) accept absent values from the MCP client.
- All tools should be `async Task<T>` unless computation is truly synchronous.

## The tool catalog is built at startup, so every surface change needs a restart

`WithToolsFromAssembly()` enumerates `[McpServerTool]` methods and generates their JSON schemas
**once, at boot**. Under `dotnet watch` the code hot-reloads but the catalog does not: a new tool, a
renamed tool, a changed description, or a parameter that just became optional stays invisible.

The symptom is misleading, because everything else works. Plain controller endpoints answer with the
new behaviour, so the process looks current while `tools/list` still serves the old catalog and the
new tool appears "missing".

```bash
curl -s -X POST http://127.0.0.1:5000/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | tr ',' '\n' | grep '"name"'
```

Rules:

- Check `tools/list` for the tool name **before** debugging why the tool misbehaves. Absent from the
  catalog means restart, not a bug.
- Batch tool-surface changes: each one costs a restart, and you cannot kill a watch you did not
  start. Ask for `Ctrl+R` and state what you will verify once it is back.
- A failed rebuild keeps the previous catalog **and** the previous code with no visible error. See
  [`app-lifecycle-and-watch.md`](app-lifecycle-and-watch.md).

## Explicit StreamableHttp skips the discovery probe

`HttpClientTransportOptions.TransportMode = HttpTransportMode.StreamableHttp` makes the 2.x client
go straight to `POST initialize`. Leave the mode unset and it probes `GET /mcp` first, which is the
source of the "MCP calls got slower after the upgrade" report: a server that does not answer that
GET can leave the client waiting on a timeout.

Measured on a server that rejects the GET outright (405 in 65ms, no hang): a client constructed
**per call** costs roughly 65-70ms over a plain REST call to the same host, which is one extra
round trip for the handshake. That is worth caching only if the path is hot. Measure before caching:
the per-call construction is visible in a profiler and invisible in a stopwatch at low volume.

## Kestrel Port Configuration

```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": { "Url": "http://*:47000" }
    }
  }
}
```

Choose an unused port (e.g., 47001, 47002, 3001) that does not conflict with other services running on the host.

## Stdio Transport

Use a console host when targeting Claude Desktop or GitHub Copilot instead of an HTTP client:

```csharp
var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();

builder.Services.AddScoped<IMyService, MyService>();

await builder.Build().RunAsync();
```

Client config in `.vscode/mcp.json` or `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "dotnet",
      "args": ["run", "--project", "src/my-mcp-server"]
    }
  }
}
```

## MCP Client Configuration for HTTP Transport

```json
{
  "mcpServers": {
    "my-server": {
      "url": "http://localhost:47000/mcp"
    }
  }
}
```

The `/mcp` path is the default mount point set by `app.MapMcp()`.
