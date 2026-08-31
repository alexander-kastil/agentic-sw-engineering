# A2UI Message Types and Validation

When to use: you are defining or validating the C# types that cross the A2UI wire.
Setup and wiring live in [`dotnet-a2ui`](dotnet-a2ui.md); the endpoint itself in
[`dotnet-a2ui-endpoint`](dotnet-a2ui-endpoint.md); SSE in [`dotnet-a2ui-streaming`](dotnet-a2ui-streaming.md).

## C# Message Types

### Envelope and Payloads

All server-to-client A2UI v0.9 messages share `"version": "v0.9"` and carry exactly one payload property.

```csharp
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Serialization;

namespace MyApp.A2Ui;

public record A2UiEnvelope
{
    [JsonPropertyName("version")]
    public string Version { get; init; } = "v0.9";

    [JsonPropertyName("createSurface")]
    public CreateSurfacePayload? CreateSurface { get; init; }

    [JsonPropertyName("updateComponents")]
    public UpdateComponentsPayload? UpdateComponents { get; init; }

    [JsonPropertyName("updateDataModel")]
    public UpdateDataModelPayload? UpdateDataModel { get; init; }

    [JsonPropertyName("deleteSurface")]
    public DeleteSurfacePayload? DeleteSurface { get; init; }
}

public record CreateSurfacePayload(
    [property: JsonPropertyName("surfaceId")] string SurfaceId,
    [property: JsonPropertyName("catalogId")] string CatalogId,
    [property: JsonPropertyName("theme")] A2UiTheme? Theme = null,
    [property: JsonPropertyName("sendDataModel")] bool? SendDataModel = null);

public record A2UiTheme(
    [property: JsonPropertyName("primaryColor")] string? PrimaryColor = null,
    [property: JsonPropertyName("agentDisplayName")] string? AgentDisplayName = null);

public record UpdateComponentsPayload(
    [property: JsonPropertyName("surfaceId")] string SurfaceId,
    [property: JsonPropertyName("components")] A2UiComponentNode[] Components);

public record UpdateDataModelPayload(
    [property: JsonPropertyName("surfaceId")] string SurfaceId,
    [property: JsonPropertyName("path")] string? Path = null,
    [property: JsonPropertyName("value")] JsonNode? Value = null);

public record DeleteSurfacePayload(
    [property: JsonPropertyName("surfaceId")] string SurfaceId);
```

### Component Nodes

A2UI v0.9 uses a flat adjacency-list model. Every entry in `updateComponents.components` has:

- `id`: unique string within the surface
- `component`: catalog type name (`"Text"`, `"Button"`, `"Column"`, etc.)
- Exactly one component per message must carry `"id": "root"` to anchor the tree
- Component-specific properties (`text`, `children`, `action`, `value`, ...) sit at the same JSON level as `id` and `component`

Use `[JsonExtensionData]` to carry the variable per-type properties without defining per-component records:

```csharp
public record A2UiComponentNode
{
    [JsonPropertyName("id")]
    public required string Id { get; init; }

    [JsonPropertyName("component")]
    public required string Component { get; init; }

    [JsonExtensionData]
    public Dictionary<string, JsonElement>? Properties { get; init; }
}
```

### Component Factory

Build component nodes via static factory methods:

```csharp
public static class A2UiComponent
{
    private static readonly JsonSerializerOptions s_opts = new(JsonSerializerDefaults.Web);
    private static JsonElement E<T>(T value) => JsonSerializer.SerializeToElement(value, s_opts);

    public static A2UiComponentNode Column(string id, params string[] childIds) =>
        new() { Id = id, Component = "Column", Properties = new() { ["children"] = E(childIds) } };

    public static A2UiComponentNode Row(string id, params string[] childIds) =>
        new() { Id = id, Component = "Row", Properties = new() { ["children"] = E(childIds) } };

    public static A2UiComponentNode Card(string id, params string[] childIds) =>
        new() { Id = id, Component = "Card", Properties = new() { ["children"] = E(childIds) } };

    public static A2UiComponentNode Text(string id, object textBinding, string? usageHint = null)
    {
        var props = new Dictionary<string, JsonElement> { ["text"] = E(textBinding) };
        if (usageHint is not null) props["usageHint"] = E(usageHint);
        return new() { Id = id, Component = "Text", Properties = props };
    }

    public static A2UiComponentNode Button(string id, string childId, string actionName,
        object? context = null) =>
        new()
        {
            Id = id,
            Component = "Button",
            Properties = new()
            {
                ["child"] = E(childId),
                ["action"] = E(new { @event = new { name = actionName, context = context ?? (object)new { } } })
            }
        };

    public static A2UiComponentNode TextField(string id, string dataPath, string? placeholder = null)
    {
        var props = new Dictionary<string, JsonElement> { ["value"] = E(new { path = dataPath }) };
        if (placeholder is not null) props["placeholder"] = E(placeholder);
        return new() { Id = id, Component = "TextField", Properties = props };
    }

    public static A2UiComponentNode DateTimeInput(string id, string dataPath,
        bool enableDate = true, bool enableTime = false) =>
        new()
        {
            Id = id,
            Component = "DateTimeInput",
            Properties = new()
            {
                ["value"] = E(new { path = dataPath }),
                ["enableDate"] = E(enableDate),
                ["enableTime"] = E(enableTime)
            }
        };
}
```

Usage:

```csharp
var components = new[]
{
    A2UiComponent.Column("root", "title", "date-input", "lbl-confirm", "submit-btn"),
    A2UiComponent.Text("title", "Reserve a Table", usageHint: "h1"),
    A2UiComponent.DateTimeInput("date-input", "/reservation/date"),
    A2UiComponent.Text("lbl-confirm", "Confirm"),
    A2UiComponent.Button("submit-btn", "lbl-confirm", "submit_booking",
        context: new { date = A2UiBind.Path("/reservation/date"), partySize = A2UiBind.Path("/reservation/partySize") })
};
```

### Data Binding Helpers

A2UI v0.9 data bindings are plain JSON objects. Provide helpers to avoid magic anonymous-type literals at call sites:

```csharp
public static class A2UiBind
{
    public static object Path(string jsonPointer) => new { path = jsonPointer };

    public static object FormatString(string template) =>
        new { call = "formatString", args = new { value = template } };
}
```

Binding patterns:

| Source | C# | Serialized JSON |
|---|---|---|
| Literal string | `"Hello"` | `"Hello"` |
| Data model path | `A2UiBind.Path("/user/name")` | `{"path":"/user/name"}` |
| Interpolated | `A2UiBind.FormatString("Hi, ${/user/name}!")` | `{"call":"formatString","args":{"value":"Hi, ${/user/name}!"}}` |

Paths starting with `/` resolve from the data model root. Paths without a leading `/` resolve relative to the current collection item (inside templated `children`).

### Client-to-Server Action

The Angular client POSTs an action event when the user interacts with a component. Deserialize it:

```csharp
public record A2UiActionMessage(
    [property: JsonPropertyName("version")] string Version,
    [property: JsonPropertyName("action")] A2UiActionPayload Action);

public record A2UiActionPayload(
    [property: JsonPropertyName("name")] string Name,
    [property: JsonPropertyName("surfaceId")] string SurfaceId,
    [property: JsonPropertyName("sourceComponentId")] string SourceComponentId,
    [property: JsonPropertyName("timestamp")] string Timestamp,
    [property: JsonPropertyName("context")] JsonElement Context);
```

Wire format the client sends:

```json
{
  "version": "v0.9",
  "action": {
    "name": "submit_booking",
    "surfaceId": "main",
    "sourceComponentId": "submit-btn",
    "timestamp": "2026-07-01T18:30:00Z",
    "context": {
      "date": "2026-07-15",
      "partySize": 4
    }
  }
}
```

The context values are fully resolved by the renderer before dispatch: all `{"path":"..."}` references in the component's action definition are replaced with their current data model values.


## Validation

Validate the LLM output against the catalog schema before sending it to the client. This catches hallucinated component names and malformed bindings at the server boundary.

```csharp
using Json.Schema;

public class A2UiValidator(A2UiCatalogService catalog)
{
    private readonly JsonSchema _schema = JsonSchema.FromText(catalog.Json);

    public void ValidateOrThrow(string json)
    {
        var node = JsonNode.Parse(json);
        var result = _schema.Evaluate(node, new EvaluationOptions
        {
            OutputFormat = OutputFormat.Basic
        });

        if (result.IsValid) return;

        var errors = string.Join("; ", result.Details
            .Where(d => !d.IsValid && d.HasErrors)
            .SelectMany(d => d.Errors ?? [])
            .Select(e => e.Value));

        throw new InvalidOperationException($"A2UI schema validation failed: {errors}");
    }
}
```

Scope note: the A2UI catalog (`catalog.json`) defines component schemas. The message envelope schema lives in a separate file (`server_to_client.json`) in the specification repository. For full envelope validation, load `server_to_client.json` as a second schema and run a second pass. Deserializing through `JsonSerializer.Deserialize<List<A2UiEnvelope>>` already catches envelope structural errors, so envelope schema validation is optional.

