# .NET A2UI Streaming

SSE/NDJSON streaming for an A2UI agent endpoint, the full wire example, and the gotchas that break a
renderer silently. For the message types, catalog, validation, and endpoint registration this builds
on, see [`dotnet-a2ui`](dotnet-a2ui.md).

## SSE Streaming

ASP.NET Core 10 serializes `IAsyncEnumerable<T>` as NDJSON (one JSON object per line) when `Accept: application/x-ndjson` is set. The Angular A2UI renderer can consume this as a progressive stream:

```csharp
[HttpPost("stream")]
public async IAsyncEnumerable<A2UiEnvelope> Stream(
    [FromBody] A2UiQueryRequest request,
    [EnumeratorCancellation] CancellationToken ct)
{
    var messages = await agent.QueryAsync(request.Query, ct);
    foreach (var msg in messages)
        yield return msg;
}
```

For true token-by-token streaming from the LLM, enable `"stream": true` on the chat completions request, accumulate the SSE delta tokens, and yield each complete A2UI message as soon as the JSON is parseable (the flat adjacency-list structure of v0.9 makes partial parsing straightforward because each message object is independent).

## Full Wire Example

A valid A2UI v0.9 response body for a reservation form:

```json
[
  {
    "version": "v0.9",
    "createSurface": {
      "surfaceId": "main",
      "catalogId": "https://a2ui.org/specification/v0_9/basic_catalog.json",
      "sendDataModel": true
    }
  },
  {
    "version": "v0.9",
    "updateComponents": {
      "surfaceId": "main",
      "components": [
        {
          "id": "root",
          "component": "Column",
          "children": ["title", "date-input", "size-input", "lbl-confirm", "submit-btn"]
        },
        {
          "id": "title",
          "component": "Text",
          "text": "Reserve a Table",
          "usageHint": "h1"
        },
        {
          "id": "date-input",
          "component": "DateTimeInput",
          "value": { "path": "/reservation/date" },
          "enableDate": true
        },
        {
          "id": "size-input",
          "component": "TextField",
          "value": { "path": "/reservation/partySize" },
          "placeholder": "Party size"
        },
        {
          "id": "lbl-confirm",
          "component": "Text",
          "text": "Confirm"
        },
        {
          "id": "submit-btn",
          "component": "Button",
          "child": "lbl-confirm",
          "action": {
            "event": {
              "name": "submit_booking",
              "context": {
                "date": { "path": "/reservation/date" },
                "partySize": { "path": "/reservation/partySize" }
              }
            }
          }
        }
      ]
    }
  },
  {
    "version": "v0.9",
    "updateDataModel": {
      "surfaceId": "main",
      "path": "/reservation",
      "value": { "date": "", "partySize": 2 }
    }
  }
]
```

## Gotchas / Anti-Patterns

| Pattern | Why it breaks |
|---|---|
| Catalog in the system prompt diverges from the catalog served to the Angular client | The renderer rejects components it does not recognize; the agent produces valid-looking JSON that silently renders nothing. Serve the catalog from the API (`GET /api/a2ui/catalog`) and embed the identical bytes in the system prompt. |
| Returning LLM output without validation | Hallucinated component names and malformed data bindings go undetected in production; the result is a blank surface with no error signal. Always call `ValidateOrThrow` before responding. |
| Omitting `createSurface` from the first response in a session | The renderer has no surface to render into; all subsequent `updateComponents` messages are silently dropped. `createSurface` must be the first message. |
| Using v0.8 message keys (`surfaceUpdate`, `beginRendering`, `dataModelUpdate`, `userAction`) | v0.9 renamed every key. An Angular renderer targeting v0.9 rejects the messages entirely. |
| Missing `"id": "root"` in `updateComponents` | The renderer cannot locate a tree root and renders nothing. |
| Missing `"version"` on any message | Clients reject version-less messages per the protocol spec. |
| Embedding business logic in `MapActionToQuery` arms | The switch arm must produce a natural-language string and nothing else. DB calls, state mutations, and branching rules in switch arms bypass the LLM and make the surface brittle. |
| Hardcoding the basic catalog URI in client code instead of fetching from the API | If upstream changes the catalog schema, client and agent diverge without any signal. Always serve the catalog from your own API and version it alongside your code. |
| Generating deeply nested component JSON for the LLM | A2UI v0.9 is deliberately flat (adjacency list). The LLM must produce sibling component objects with ID references, not nested trees. A nesting-oriented few-shot example in the system prompt will cause the LLM to hallucinate invalid structure. |
