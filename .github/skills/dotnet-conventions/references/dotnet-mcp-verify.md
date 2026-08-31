# .NET MCP Server: verifying it and logging what it did

## Verifying an HTTP MCP server (dev)

The transport is **streamable HTTP** — a session handshake, and responses come back as SSE (`data: {json}` lines), not plain JSON. Verify by hand with `curl` (more reliable than the Inspector for a quick check):

```bash
MCP=https://127.0.0.1:5001/mcp
# 1. initialize — grab the session id from the RESPONSE HEADER
SID=$(curl -sk -D - -o /dev/null -X POST $MCP \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"c","version":"1"}}}' \
  | grep -i "mcp-session-id" | tr -d '\r' | awk '{print $2}')
H=(-H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -H "Mcp-Session-Id: $SID")
# 2. required notification, THEN list/call (every call carries the session header)
curl -sk -o /dev/null -X POST $MCP "${H[@]}" -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
curl -sk -X POST $MCP "${H[@]}" -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'          | sed -n 's/^data: //p'
curl -sk -X POST $MCP "${H[@]}" -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"my_tool","arguments":{}}}' | sed -n 's/^data: //p'
```

Gotchas that waste time:

- **`/mcp` may be HTTPS-only.** If `UseHttpsRedirection()` is active (often when a `Testing`/prod flag is set even in the dev profile), `http://…:5000/mcp` returns a **307 redirect** to `https://…:5001/mcp`. Hit the HTTPS URL directly with `-k` (self-signed dev cert).
- **The MCP Inspector's node `fetch` fails on that redirect** (`Failed to connect: fetch failed`) and rejects the self-signed cert. Use the HTTPS URL and `NODE_TLS_REJECT_UNAUTHORIZED=0`, or just use the `curl` handshake above.
- A missing `Accept: application/json, text/event-stream` header, or forgetting the `Mcp-Session-Id` on follow-ups, yields opaque 400/406s — both are mandatory.
- **`/mcp` is authorized even in dev.** With `RequireAuthorization("Mcp")` the handshake above 401s until every request carries auth. For the API-key path that is one extra header, `-H "X-Api-Key: <Mcp:ApiKey from appsettings.Development.json>"`, on the initialize call *and* on each follow-up.
- **`tools/list` proves registration, not behaviour.** `WithToolsFromAssembly()` picking up a new `[McpServerTool]` says nothing about whether its query returns anything. Call each new tool and read the payload; an empty result set is a question, not a pass. If the rows needed to exercise a branch do not exist locally, set the field on an obviously-fake fixture row, call the tool, then revert and re-count to confirm the revert landed.

## Logging every tool call with a request filter

`McpServerOptions.Filters` (`ModelContextProtocol.Server.McpRequestFilters`) gives middleware-style
composition over the handler pipeline: `CallToolFilters` for the ordinary tool pipeline,
`CallToolWithAlternateFilters` composing outside it, and `McpRequestInvocationFilter<TParams,TResult>`
receiving `(context, next, cancellationToken)`. First registered is outermost. Primitive matching
happens before either family runs, so calls that resolved to a registered `[McpServerTool]` still
pass through. This is one registration, not a wrapper per tool:

```csharp
builder.Services.AddMcpServer()
    .WithHttpTransport()
    .WithToolsFromAssembly()
    .WithRequestFilters(filters => filters.AddCallToolFilter(next => async (context, ct) =>
    {
        var sw = Stopwatch.StartNew();
        try
        {
            var result = await next(context, ct);
            await LogAsync(context, sw.ElapsedMilliseconds, IsRefused(result) ? "Refused" : "Ok");
            return result;
        }
        catch (Exception ex) { await LogAsync(context, sw.ElapsedMilliseconds, "Error", ex.Message); throw; }
    }));
```

What the filter must guarantee:

- **Best effort.** Wrap the write in its own try/catch. A logging failure must not change or fail the
  tool call, and the result must be byte-identical with logging on and off. Pin that with a test
  whose context throws only on the log entity's insert.
- **Classify from what the tool returned.** `CallToolResult.IsError` is often never set: tools
  returning `Task<string>` express refusals as a payload with a top-level `Error` property, so an
  `IsError`-only rule records every refusal as a success. Refusals are the rows worth having.
- **Redact by shape, not just by name.** Redacting an argument called `attachmentBase64` is not
  enough once a tool takes an array of bookings: recurse into arrays and objects and re-apply the
  name and length rules per field, or the one tool that writes logs nothing at all about what it
  wrote.
- **Bound it.** Index the timestamp, and prune on a schedule or at startup. A row per `tools/call`
  includes every read-only query the model makes while answering a question.

Verify the choice of filter family empirically: drive a real client over the transport
(`McpClient.CreateAsync` against `WithStreamServerTransport`) and assert a row appears. Reasoning
from the XML docs about which family sees a matched tool is not proof.
