# File Import / Ingest Endpoint (ASP.NET Core)

Server side of the **file → AI-draft → review → commit** import pattern: a controller accepts an
uploaded spreadsheet/PDF, an AI call maps its columns onto domain fields, the caller reviews a
draft, and only then does the server commit rows through EF Core. The client half (drop zone +
wizard) lives in `angular-conventions` → [`angular-file-dropzone`](../../angular-conventions/references/angular-file-dropzone.md) and [`file-import-wiz`](../../angular-conventions/references/file-import-wiz.md).

## When to use

- A controller must accept an uploaded Excel/PDF and turn it into editable domain rows (e.g. an
  uploaded roster spreadsheet → `Customer`/`Product` rows) — column headers vary per source file, so
  a fixed parser breaks on every new source.
- You want the AI/parsing to live in ONE place (the server) so the client only ships `FormData` and
  renders/commits a draft.

## The shape (9 pieces)

```
POST /import/{kind}/ingest  (IFormFile, ?review=bool)   → extract → AI draft → return draft (un-persisted)
POST /import/assist         ({ Draft, Messages })        → chat over draft → { Reply, PatchJson, Refs }
POST /import/{kind}/confirm ({ reviewed draft })         → regenerate ids → EF insert
POST /documents/categorize  (IFormFile)                  → { Category, Confidence }  (seam, may start as a stub)
```

### 1. Upload endpoint — buffer `IFormFile`, share one pipeline

```csharp
[ApiController]
[Route("import")]
public class ImportController(ImportIngestionService ingestion) : ControllerBase
{
    [HttpPost("{kind}/ingest")]
    public async Task<IngestionResult> Ingest(string kind, IFormFile file, [FromQuery] bool review)
    {
        using var stream = new MemoryStream();
        await file.CopyToAsync(stream);
        var src = new IngestionSource(stream.ToArray(), file.FileName, file.ContentType, IngestionOrigin.Upload);
        return await ingestion.IngestAsync(kind, src, review);
    }
}
```

- Receive as `IFormFile`, buffer to `byte[]` via `MemoryStream`.
- Wrap in a small record so upload and any future origin (email inbox, MCP tool) share the pipeline: `public record IngestionSource(byte[] Bytes, string FileName, string ContentType, IngestionOrigin Origin);`
- **Validate** size and content-type/extension explicitly — don't skip this. Reject anything but `.xlsx`/`.pdf`/`image/*`; cap size via `[RequestSizeLimit]` or Kestrel limits.
- `kind` selects the target mapping (e.g. `customers` → `Customer`, `products` → `Product`).

### 2. Extraction — content-type fork (Excel / text-PDF / image)

Uploaded files come in three physical shapes; branch on content type:

| Input | Extraction |
|---|---|
| `.xlsx` | Read cells server-side (**EPPlus**) into a row/column grid. |
| text-layer PDF | **UglyToad.PdfPig** — `PdfDocument.Open`, bucket words into rows by rounded `BoundingBox.Bottom`, emit `\t` when the x-gap exceeds a threshold to preserve columns. |
| image / scanned PDF | Pass raw bytes to a **vision model** (`image_url` data-URI content part). Files with no text layer need OCR via the vision model, not PdfPig. |

Then hand the reconstructed text (or image) to the AI with a **strict JSON-schema system prompt** and `response_format = { type: "json_object" }`, and deserialize case-insensitively into a POCO:

```csharp
var json = await ai.CompleteAsync(messages, json: true, image: imageBytes, preferVision: isImage);
var doc  = JsonSerializer.Deserialize<ExtractedSheet>(json,
              new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
           ?? throw new InvalidOperationException("Empty extraction response");
```

> **Why AI mapping, not a fixed parser:** every source spreadsheet uses different headers — the
> same "customer name" column might be called `Name`, `Full Name`, or `Kunde` across files. The
> system prompt describes the *target* fields and lets the model map whatever columns arrive. Bake
> locale rules (date formats, phone formats, honorifics) into the prompt where the domain needs them.

### 3. Reuse the app's existing AI client — do NOT add a new SDK

If the app already talks to an OpenAI-compatible chat model, reuse that client/abstraction for the
extraction and assist calls rather than adding a second SDK:

- Provider-agnostic `/chat/completions` over `IHttpClientFactory` (model catalog + keys resolved at runtime, not hardcoded in `appsettings`).
- `json` switch → `response_format=json_object`; `image`/`preferVision` switches for vision.
- Keep the AI-call methods `virtual` and `InternalsVisibleTo` the test project so they mock cleanly.
- Read all config through a strongly-typed config class, never raw `IConfiguration`.

### 4. Draft assembly + history grounding

Map the extracted DTO to domain entities and pre-fill fields from existing data with a tiered fuzzy match (exact → contains → token-overlap) — e.g. resolve the target parent record from the sheet's header row, suggest related rows from prior imports of the same source:

```csharp
var draft = new ImportDraft {
    Kind = kind,
    ParentId = ResolveParent(doc.Header),                // fuzzy match against existing records
    Rows = doc.Rows.Select(MapRow).ToList(),
};
```

Compute any totals/derived fields server-side.

### 5. Review toggle

`review=true` → persist immediately with a `Review` flag set (skip the client round-trip). `review=false` → return the draft **un-persisted** so the wizard can edit it; it comes back through `confirm`.

### 6. (Optional) stage the raw file in blob storage

A pipeline that must keep the source document stages the upload in a *temporary* blob container
under a `{guid}-{filename}` name **before** AI work, carries that name on the draft, and on confirm
**promotes** it to a permanent location keyed by business id. See
[`azure-blob-storage`](azure-blob-storage.md) for the passwordless `DefaultAzureCredential` pattern
and the stage→confirm lifecycle, or [`sql-stored-files`](sql-stored-files.md) to keep the bytes in
the database itself. If you only need the extracted rows, skip storage entirely.

### 7. Assist (chat-over-draft)

```csharp
[HttpPost("assist")]
public async Task<AssistResult> Assist([FromBody] AssistRequest req)
{
    var messages = new List<AiChatMessage> {
        new() { Role = "system", Content = """
            You help correct an imported draft. When you suggest concrete changes,
            return them in PatchJson as a JSON object of draft fields to merge; else null.
            Return ONLY: { "Reply": "string", "PatchJson": "json string or null", "ReferenceIds": [] }
            """ },
        new() { Role = "user", Content = $"Draft:\n{JsonSerializer.Serialize(req.Draft)}" },
    };
    messages.AddRange((req.Messages ?? []).Select(m => new AiChatMessage { Role = m.Role, Content = m.Content }));
    var json = await ai.CompleteAsync(messages, json: true);
    return JsonSerializer.Deserialize<AssistResult>(json, CaseInsensitive)!;
}
```

`PatchJson` is deliberately a **string** holding a partial JSON object the client merges into the draft — the model returns `null` when it has no concrete change.

### 8. Confirm / commit — insert-only, regenerate ids

```csharp
public async Task<ImportResult> ConfirmAsync(ImportDraft draft)
{
    // regenerate keys so it is always a fresh insert (EMPTY_GUID → new)
    foreach (var row in draft.Rows) { row.Id = Guid.NewGuid(); row.ParentId = draft.ParentId; }
    ctx.Rows.AddRange(draft.Rows);
    await ctx.SaveChangesAsync();
    return new ImportResult { ImportedCount = draft.Rows.Count, ParentId = draft.ParentId };
}
```

Persist through `AppDbContext` (see [`dotnet-efcore`](dotnet-efcore.md)). Decide **insert vs update** per domain: some imports *replace* a parent's rows entirely — dedup by a natural key and update-or-insert rather than blind add.

### 9. Categorize seam

Keep an `IDocumentCategorizer` returning `(Category, Confidence)` in front of the pipeline so a stub can grow into an AI/rules classifier without touching callers. Fine to ship a stub first (`Category = ..., Confidence = 1.0`), but wire the interface now.

## DI wiring (`Program.cs`)

```csharp
builder.Services.AddScoped<ImportIngestionService>();
builder.Services.AddScoped<IDocumentCategorizer, DocumentCategorizationService>();
// reuse the existing AI client registration used elsewhere in the app; add BlobStorageService only if staging files
```

## Testing (xUnit + NSubstitute + FluentAssertions — see [`dotnet-testing`](dotnet-testing.md))

- Mock the AI client (`virtual CompleteAsync`) to return a canned JSON draft — assert the extractor maps varied header sets to the same target fields.
- Assert `review=false` does NOT hit the DB; `confirm` inserts with fresh GUIDs.
- Assert dedup/update logic for re-imported source files.
- Feed a real converted sample as the extractor's input fixture.

## Checklist

- [ ] `IFormFile` buffered to `byte[]`; size + content-type validated (don't skip this).
- [ ] Content-type fork: EPPlus (xlsx) / PdfPig (text PDF) / vision model (image + scanned PDF).
- [ ] Strict JSON-schema prompt + `json_object`; case-insensitive deserialize; AI-mapped columns (not a fixed parser).
- [ ] Reuse the existing app AI client; config via a strongly-typed config class; keys resolved at runtime, not hardcoded.
- [ ] `review` toggle; draft un-persisted when false.
- [ ] Blob staging only if the source doc must be retained.
- [ ] Confirm = insert-only with regenerated ids; deliberate update-vs-insert for the domain.
- [ ] `IDocumentCategorizer` seam in place (stub OK).
- [ ] xUnit coverage with a mocked AI client and real sample fixtures.

## Related

- [`dotnet-controllers`](dotnet-controllers.md) / [`dotnet-efcore`](dotnet-efcore.md) — controller + EF patterns.
- [`dotnet-mcp-tool-design`](dotnet-mcp-tool-design.md) — expose ingest as an MCP tool so external Claude can import too.
- `angular-conventions` → [`file-import-wiz`](../../angular-conventions/references/file-import-wiz.md) / [`angular-file-dropzone`](../../angular-conventions/references/angular-file-dropzone.md) — the client half.
