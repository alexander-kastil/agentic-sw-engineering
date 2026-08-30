# A2UI Catalog and Agent Endpoint

When to use: you are serving the component catalog or implementing the agent endpoint.
Setup and wiring live in [`dotnet-a2ui`](dotnet-a2ui.md); message types in
[`dotnet-a2ui-messages`](dotnet-a2ui-messages.md); SSE in [`dotnet-a2ui-streaming`](dotnet-a2ui-streaming.md).

## Serving the Catalog

The client renderer needs the catalog to know which components exist. Serve the same catalog file the system prompt embeds so agent and client always stay in sync.

Embed the catalog JSON Schema in the assembly:

```xml
<!-- .csproj -->
<ItemGroup>
  <EmbeddedResource Include="A2Ui/catalog.json" />
</ItemGroup>
```

Singleton catalog loader:

```csharp
public class A2UiCatalogService
{
    private readonly byte[] _bytes;

    public A2UiCatalogService()
    {
        var asm = typeof(A2UiCatalogService).Assembly;
        using var stream = asm.GetManifestResourceStream("MyApp.A2Ui.catalog.json")
            ?? throw new InvalidOperationException("Embedded resource 'A2Ui/catalog.json' not found.");
        using var ms = new MemoryStream();
        stream.CopyTo(ms);
        _bytes = ms.ToArray();
    }

    public Stream OpenStream() => new MemoryStream(_bytes, writable: false);
    public string Json => System.Text.Encoding.UTF8.GetString(_bytes);
}
```

Controller:

```csharp
[ApiController]
[Route("api/a2ui/catalog")]
public class A2UiCatalogController(A2UiCatalogService catalog) : ControllerBase
{
    [HttpGet]
    [Produces("application/json")]
    public IActionResult Get() => File(catalog.OpenStream(), "application/json");
}
```

To proxy the upstream basic catalog at `https://a2ui.org/specification/v0_9/basic_catalog.json` instead, fetch it once at startup with a hosted service and cache it in memory. The hosted-service pattern avoids embedding a file and always tracks the upstream version, at the cost of an outbound request.

## Agent Endpoint

### Service

The agent service calls an OpenAI-compatible chat completion endpoint, parses the LLM output, validates it, and returns the typed envelope list.

```csharp
using System.Net.Http.Headers;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Options;

public class A2UiAgentService(
    HttpClient http,
    IOptions<A2UiOptions> opts,
    A2UiCatalogService catalog,
    A2UiValidator validator)
{
    private static readonly JsonSerializerOptions s_json = new(JsonSerializerDefaults.Web)
    {
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
    };

    private const string JsonDelimiter = "---a2ui_JSON---";

    public async Task<IReadOnlyList<A2UiEnvelope>> QueryAsync(
        string naturalLanguageQuery, CancellationToken ct = default)
    {
        var o = opts.Value;
        var body = new
        {
            model = o.LlmModel,
            messages = new[]
            {
                new { role = "system", content = BuildSystemPrompt(o) },
                new { role = "user", content = naturalLanguageQuery }
            }
        };

        using var req = new HttpRequestMessage(
            HttpMethod.Post, $"{o.LlmEndpoint.TrimEnd('/')}/chat/completions");
        req.Headers.Authorization = new AuthenticationHeaderValue("Bearer", o.LlmApiKey);
        req.Content = JsonContent.Create(body, options: s_json);

        using var resp = await http.SendAsync(req, ct);
        resp.EnsureSuccessStatusCode();

        var doc = await resp.Content.ReadFromJsonAsync<JsonElement>(cancellationToken: ct);
        var raw = doc.GetProperty("choices")[0]
                     .GetProperty("message")
                     .GetProperty("content")
                     .GetString() ?? string.Empty;

        return ParseAndValidate(raw);
    }

    private IReadOnlyList<A2UiEnvelope> ParseAndValidate(string llmOutput)
    {
        var json = llmOutput.Contains(JsonDelimiter)
            ? llmOutput[(llmOutput.IndexOf(JsonDelimiter) + JsonDelimiter.Length)..].Trim()
            : llmOutput.Trim();

        if (json.StartsWith("```json", StringComparison.OrdinalIgnoreCase))
            json = json[7..json.LastIndexOf("```")].Trim();
        else if (json.StartsWith("```"))
            json = json[3..json.LastIndexOf("```")].Trim();

        validator.ValidateOrThrow(json);

        return JsonSerializer.Deserialize<List<A2UiEnvelope>>(json, s_json)
            ?? throw new InvalidOperationException("LLM returned no parseable A2UI messages.");
    }

    private string BuildSystemPrompt(A2UiOptions o) => $"""
        You are an AI agent that generates A2UI v0.9 interface definitions.

        RESPONSE FORMAT:
        - Write a brief natural-language reply first.
        - Add one line containing exactly: {JsonDelimiter}
        - Follow it immediately with a JSON array of A2UI messages. No markdown fences.

        RULES:
        - Every message must include "version": "v0.9".
        - The first message in every response must be createSurface with surfaceId "{o.SurfaceId}".
        - Every updateComponents message must contain exactly one component with "id": "root".
        - Use only component types defined in the catalog below.
        - Data bindings use JSON Pointer paths: {{"path": "/field"}}.
        - Server-side button actions: {{"event": {{"name": "action_name", "context": {{"key": {{"path": "/value"}}}}}}}}.
        - Children of layout components are expressed as arrays of sibling IDs: "children": ["id1","id2"].
        - A button's single child: "child": "label-component-id".

        CATALOG URI (use this as catalogId in createSurface):
        {o.CatalogUri}

        CATALOG SCHEMA:
        {catalog.Json}

        EXAMPLE (reservation form):
        Here is a booking form.
        {JsonDelimiter}
        [
          {{"version":"v0.9","createSurface":{{"surfaceId":"{o.SurfaceId}","catalogId":"{o.CatalogUri}","sendDataModel":true}}}},
          {{"version":"v0.9","updateComponents":{{"surfaceId":"{o.SurfaceId}","components":[
            {{"id":"root","component":"Column","children":["title","date-in","size-in","lbl","btn"]}},
            {{"id":"title","component":"Text","text":"Reserve a Table","usageHint":"h1"}},
            {{"id":"date-in","component":"DateTimeInput","value":{{"path":"/reservation/date"}},"enableDate":true}},
            {{"id":"size-in","component":"TextField","value":{{"path":"/reservation/partySize"}},"placeholder":"Party size"}},
            {{"id":"lbl","component":"Text","text":"Confirm"}},
            {{"id":"btn","component":"Button","child":"lbl","action":{{"event":{{"name":"submit_booking","context":{{"date":{{"path":"/reservation/date"}},"partySize":{{"path":"/reservation/partySize"}}}}}}}}}}
          ]}}}},
          {{"version":"v0.9","updateDataModel":{{"surfaceId":"{o.SurfaceId}","path":"/reservation","value":{{"date":"","partySize":2}}}}}}
        ]
        """;
}
```

### Controller

```csharp
[ApiController]
[Route("api/a2ui")]
public class A2UiController(A2UiAgentService agent) : ControllerBase
{
    [HttpPost("query")]
    public async Task<IActionResult> Query(
        [FromBody] A2UiQueryRequest request, CancellationToken ct)
    {
        var messages = await agent.QueryAsync(request.Query, ct);
        return Ok(messages);
    }

    [HttpPost("action")]
    public async Task<IActionResult> HandleAction(
        [FromBody] A2UiActionMessage action, CancellationToken ct)
    {
        var query = MapActionToQuery(action.Action);
        var messages = await agent.QueryAsync(query, ct);
        return Ok(messages);
    }

    private static string MapActionToQuery(A2UiActionPayload action) =>
        action.Name switch
        {
            "submit_booking" => FormatBookingQuery(action.Context),
            "confirm_order"  => FormatConfirmQuery(action.Context),
            "cancel"         => "Reset the surface and return to the initial view.",
            _                => $"The user triggered the '{action.Name}' action. Continue the conversation."
        };

    private static string FormatBookingQuery(JsonElement ctx)
    {
        var date  = ctx.TryGetProperty("date",      out var d) ? d.GetString()    : "unspecified";
        var size  = ctx.TryGetProperty("partySize", out var p) ? p.GetRawText()   : "unspecified";
        return $"Confirm a reservation for {size} people on {date}.";
    }

    private static string FormatConfirmQuery(JsonElement ctx)
    {
        var id = ctx.TryGetProperty("orderId", out var o) ? o.GetString() : "unspecified";
        return $"Show the confirmation screen for order {id}.";
    }
}

public record A2UiQueryRequest(
    [property: JsonPropertyName("query")] string Query);
```

Keep `MapActionToQuery` purely declarative: each arm produces a natural-language query and nothing else. The LLM owns domain reasoning. Never embed DB calls, conditional state, or business rules in switch arms.

