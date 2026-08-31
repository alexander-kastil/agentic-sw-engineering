# Spec: Migrate QR Server from Python to .NET

## Goal

Rewrite `src/qr-server/` from Python (FastMCP + uvicorn) to a .NET 9 MCP server that exposes identical tool/resource contracts and supports the same two transport modes (stdio and HTTP).

## Source App Summary

| Aspect | Python |
|---|---|
| Framework | FastMCP (`mcp>=1.26.0`) |
| QR generation | `qrcode[pil]>=8.0` |
| HTTP server | uvicorn + Starlette |
| Transport modes | `--stdio` flag or HTTP on port 3001 |
| Tool | `generate_qr(text, box_size, border, error_correction, fill_color, back_color) → base64 PNG` |
| Resource | `ui://qr-server/view.html` — embedded HTML viewer |
| Config | `HOST` and `PORT` env vars |

---

## Target: .NET Implementation

### Location

`src/qr-server-dotnet/` (new directory, Python original untouched)

### Tech Stack

| Concern | Package |
|---|---|
| MCP server | `ModelContextProtocol` SDK (official C# SDK) |
| QR generation | `QRCoder` NuGet package |
| HTTP transport | ASP.NET Core minimal API (built-in) |
| Stdio transport | `ModelContextProtocol` stdio transport |

---

## Files to Create

| File | Purpose |
|---|---|
| `qr-server-dotnet.csproj` | Project file — .NET 9, console app |
| `Program.cs` | Entry point — wires up MCP server, selects transport |
| `Tools/QrTool.cs` | `generate_qr` tool implementation |
| `Resources/ViewResource.cs` | `ui://qr-server/view.html` resource |
| `Resources/view.html` | Embedded HTML viewer (same as Python) |
| `readme.md` | Setup and usage instructions |
| `.gitignore` | Standard .NET gitignore |

---

## Tool Contract (must match Python exactly)

```csharp
[McpServerTool(Name = "generate_qr")]
public static ImageContent GenerateQr(
    string text,
    int boxSize = 5,
    int border = 4,
    string errorCorrection = "M",
    string fillColor = "black",
    string backColor = "white"
)
```

**Returns:** `ImageContent` with `Type = "image"`, `MimeType = "image/png"`, base64-encoded PNG data.

**Error correction mapping:**

| Input | QRCoder enum |
|---|---|
| `L` | `QRCodeGenerator.ECCLevel.L` |
| `M` | `QRCodeGenerator.ECCLevel.M` |
| `Q` | `QRCodeGenerator.ECCLevel.Q` |
| `H` | `QRCodeGenerator.ECCLevel.H` |

---

## Resource Contract (must match Python exactly)

```csharp
[McpServerResource(Uri = "ui://qr-server/view.html", MimeType = "text/html;profile=mcp-app")]
public static string View()
```

Returns the same embedded HTML string from `view.html` (copied verbatim from Python).

---

## Transport Modes

`Program.cs` checks for `--stdio` arg, matching the Python pattern:

```csharp
if (args.Contains("--stdio"))
    // run stdio transport
else
    // run HTTP on HOST:PORT via ASP.NET Core
```

`HOST` and `PORT` env vars default to `0.0.0.0` / `3001`.

HTTP endpoint: `http://<HOST>:<PORT>/mcp`

---

## Conventions

- Use .NET 9 primary constructors where applicable
- `PascalCase` for classes/methods/properties; `camelCase` for locals
- Use `dotnet cli` for all package operations
- No background process — block on `await app.RunAsync()`

---

## Out of Scope

- Docker / nginx config (can be added later)
- Removing or modifying the Python original
- Any new tool parameters beyond what the Python server exposes
