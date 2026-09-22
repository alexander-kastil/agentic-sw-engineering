# .NET A2UI

Implement an A2UI (Agent-to-UI) v0.9-compatible agent endpoint in ASP.NET Core 10 at the protocol level.

**No official or community .NET SDK for A2UI exists as of June 2026.** The reference implementations are Python (Google ADK) and TypeScript. Because A2UI is a declarative JSON-over-HTTP protocol, an ASP.NET Core controller can serve a fully conformant agent endpoint without a dedicated library.

> For SSE streaming, the full wire example, and gotchas/anti-patterns, see [`dotnet-a2ui-streaming`](dotnet-a2ui-streaming.md).

## What A2UI Is

A2UI (Apache 2.0, Google, v0.9.1 stable) lets AI agents drive UI by emitting structured JSON messages. The agent server produces a list of typed messages: it initializes a surface, declares components in a flat adjacency-list tree, and populates a data model. The Angular (or Flutter/Lit/React) client maps those messages to native components from a pre-approved **catalog**. Agents can only reference components defined in the catalog; no executable code is transmitted.

The .NET agent server's job: receive a natural-language query, call an LLM constrained to emit catalog-valid JSON, validate the output, and return the A2UI message list. The transport is negotiable (A2A, SSE, WebSockets, plain REST). This reference uses plain JSON-array responses as the primary pattern, with a note on SSE streaming.

## Protocol Version

Pin `"version": "v0.9"` on every outgoing message. v1.0 is release-candidate and its message keys may still change before GA. Monitor [a2ui.org](https://a2ui.org) for the stable v1.0 promotion date.

## NuGet Packages

No A2UI package exists. Add JSON Schema validation only:

```xml
<PackageReference Include="JsonSchema.Net" Version="9.*" />
```

Verify the current version at [NuGet: JsonSchema.Net](https://www.nuget.org/packages/JsonSchema.Net/). This package is built on `System.Text.Json`. If the project already uses Newtonsoft.Json, [NJsonSchema](https://www.nuget.org/packages/NJsonSchema) (v11.x) is the alternative.


## Configuration

```csharp
public class A2UiOptions
{
    [Required]
    public string LlmEndpoint { get; set; } = string.Empty;

    [Required]
    public string LlmApiKey { get; set; } = string.Empty;

    public string LlmModel { get; set; } = "gpt-4o-mini";

    public string CatalogUri { get; set; } =
        "https://a2ui.org/specification/v0_9/basic_catalog.json";

    public string SurfaceId { get; set; } = "main";
}
```

`appsettings.json`:

```json
{
  "A2Ui": {
    "LlmEndpoint": "https://api.openai.com/v1",
    "LlmApiKey": "...",
    "LlmModel": "gpt-4o",
    "CatalogUri": "https://a2ui.org/specification/v0_9/basic_catalog.json",
    "SurfaceId": "main"
  }
}
```


## Program.cs Registration

```csharp
builder.Services.Configure<A2UiOptions>(builder.Configuration.GetSection("A2Ui"));

builder.Services.AddSingleton<A2UiCatalogService>();
builder.Services.AddSingleton<A2UiValidator>();
builder.Services.AddHttpClient<A2UiAgentService>();
```

`A2UiCatalogService` and `A2UiValidator` are singletons: they load the catalog once and are thereafter read-only. `A2UiAgentService` is registered via `AddHttpClient` for a properly managed `HttpClient` lifetime (transient with pooled handler).


## Where the rest lives

| You want to... | Read |
|---|---|
| Define or validate the C# message types crossing the wire | [`dotnet-a2ui-messages`](dotnet-a2ui-messages.md) |
| Serve the component catalog / implement the agent endpoint | [`dotnet-a2ui-endpoint`](dotnet-a2ui-endpoint.md) |
| Stream responses over SSE | [`dotnet-a2ui-streaming`](dotnet-a2ui-streaming.md) |

## Sources

- A2UI site and spec: <https://a2ui.org/> , <https://a2ui.org/specification/v0.9-a2ui/>
- A2UI catalogs and actions concepts: <https://a2ui.org/concepts/catalogs/> , <https://a2ui.org/concepts/actions/>
- Google Developers Blog: <https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/> , <https://developers.googleblog.com/a2ui-v0-9-generative-ui/>
- GitHub (no C# in repo): <https://github.com/google/A2UI>
- ADK integration: <https://adk.dev/integrations/a2ui/>
- NuGet validators: <https://www.nuget.org/packages/JsonSchema.Net/> , <https://www.nuget.org/packages/NJsonSchema>
