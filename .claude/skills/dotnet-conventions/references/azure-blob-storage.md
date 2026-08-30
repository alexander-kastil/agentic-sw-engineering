# Azure Blob Storage (passwordless retention)

Server-side pattern for retaining an uploaded file in Azure Blob Storage with **no connection
strings or account keys** — `DefaultAzureCredential` (RBAC data-plane role) only. Built on top of
the ingest pipeline in [`file-import-ingest.md`](file-import-ingest.md).

## When to use

- A pipeline needs to **keep the original uploaded file** (not just the rows extracted from it) —
  e.g. an import service retaining the source `.xlsx`/`.pdf` against the parent record it populated.
- You want passwordless Azure Storage access (`BlobServiceClient` + `DefaultAzureCredential`) instead
  of a connection string, and a stage-then-promote (temp → permanent) blob lifecycle tied to a
  draft-review-confirm flow.
- Not for arbitrary blob CRUD outside this "stage on ingest, promote on confirm" shape — for that,
  use `Azure.Storage.Blobs` directly rather than bending this skill's `BlobStorageService`.

## The pattern

**One container, prefix folders — not one container per kind.** Use exactly one container
(`AppConfig.Storage.Container`) and use blob-name **prefixes** as the "folder per import type":
`staging/` (uploaded, not yet confirmed) → `{kind}/` (confirmed, permanent). `BlobStorageService.MoveAsync`
takes **one** container plus a source/destination name within it:

```csharp
// src/my-api/Services/BlobStorageService.cs
public virtual async Task MoveAsync(string container, string srcName, string dstName, string contentType)
{
    if (!IsEnabled) throw new BlobStorageDisabledException();
    var (content, ct) = await DownloadAsync(container, srcName);
    using var ms = new MemoryStream();
    await content.CopyToAsync(ms);
    ms.Position = 0;
    await UploadAsync(container, dstName, ms, ct ?? contentType);
    await DeleteAsync(container, srcName);
}
```

Move is still download+reupload+delete (not a server-side rename/copy) — the SDK/passwordless RBAC
setup doesn't guarantee an atomic rename primitive.

**Six methods, all `virtual`, all guarded by an `IsEnabled` check:**

```csharp
// src/my-api/Services/BlobStorageService.cs
public class BlobStorageService(BlobServiceClient client)
{
    // The DI registration (see below) provides a null BlobServiceClient when
    // Storage:AccountName is blank (e.g. local dev without Azure) so the app still boots;
    // every method below no-ops/throws predictably instead of NullReferenceException, and
    // callers that wrap this service stay non-fatal too.
    private bool IsEnabled => client != null;

    public virtual async Task EnsureContainerAsync(string container) { ... }   // no-op when disabled
    public virtual async Task UploadAsync(string container, string name, Stream content, string contentType) { ... } // throws when disabled
    public virtual async Task<bool> ExistsAsync(string container, string name) { ... }  // false when disabled
    public virtual async Task<(Stream Content, string ContentType)> DownloadAsync(string container, string name) { ... } // throws when disabled
    public virtual async Task DeleteAsync(string container, string name) { ... }  // no-op when disabled
    public virtual async Task MoveAsync(string container, string srcName, string dstName, string contentType) { ... } // throws when disabled
}
```

`virtual` on every method exists for exactly one reason: `Substitute.ForPartsOf<BlobStorageService>`
in tests (see [Testing](#testing) below) — same reason the AI chat client's `CompleteAsync` is
`virtual` in `file-import-ingest.md`.

`BlobStorageDisabledException` is a small dedicated exception (not a generic one) so the "storage
isn't configured" case reads clearly in logs, distinct from a genuine Azure outage:

```csharp
// src/my-api/Services/BlobStorageService.cs
public class BlobStorageDisabledException() : System.Exception("Blob storage is not configured (Storage:AccountName is blank).");
```

## DI wiring

`AppConfig.Storage` — read via a strongly-typed config class, never raw `IConfiguration`:

```csharp
public class StorageConfig
{
    public string AccountName { get; set; }
    public string Container { get; set; } = "import-documents";
}

public class AppConfig
{
    ...
    public StorageConfig Storage { get; set; }
}
```

`appsettings.json` / `appsettings.Development.json`:

```json
"Storage": {
  "AccountName": "mystorageaccount",
  "Container": "import-documents"
}
```

`AddBlobStorage` (`Common/AppBuilder.cs`) — the **null-client guard** so a blank
`Storage:AccountName` (e.g. before the account/RBAC is provisioned, or a stripped-down local dev
config) never crashes startup: register a `null` `BlobServiceClient` rather than skip registration
entirely, so `BlobStorageService`'s constructor (and any service that depends on it) still resolves
through DI:

```csharp
// src/my-api/Common/AppBuilder.cs
public static void AddBlobStorage(this WebApplicationBuilder builder)
{
    var cfg = builder.Configuration.Get<AppConfig>();
    var accountName = cfg?.Storage?.AccountName;

    builder.Services.AddSingleton(_ => string.IsNullOrWhiteSpace(accountName)
        ? null
        : new BlobServiceClient(new Uri($"https://{accountName}.blob.core.windows.net"), new DefaultAzureCredential()));
    builder.Services.AddScoped<BlobStorageService>();
}
```

`Program.cs` — call this **before** registering the service(s) that depend on `BlobStorageService`:

```csharp
// src/my-api/Program.cs
builder.AddBlobStorage();

builder.Services.AddScoped<IDocumentCategorizer, DocumentCategorizationService>();
builder.Services.AddScoped<ImportIngestionService>();
```

No connection strings, no `SharedKeyCredential`, no SAS tokens anywhere in this path — the only
identity primitive is `DefaultAzureCredential()`.

## Retention hook

The pipeline this backs (`ImportIngestionService`, see `file-import-ingest.md` for the surrounding
ingest/confirm shape) stages the original upload **before** the AI/extraction work, then promotes it
**only if/when the row data itself is actually persisted**:

1. **Stage on ingest** — upload the raw bytes to `staging/{guid}-{safeFileName}`, before deciding
   whether this is a review draft or an auto-persist:

   ```csharp
   // src/my-api/Services/ImportIngestionService.cs
   private async Task<SourceDocument> StageDocumentAsync(IngestionSource source)
   {
       try
       {
           var blobName = $"{StagingPrefix}/{Guid.NewGuid()}-{SafeBlobFileName(source.FileName)}";
           await using var stream = new MemoryStream(source.Bytes);
           await blob.UploadAsync(StorageContainer, blobName, stream, source.ContentType);

           return new SourceDocument { BlobName = blobName, FileName = source.FileName, ContentType = source.ContentType, SizeBytes = source.Bytes.LongLength };
       }
       catch (Exception ex)
       {
           logger.LogEvent("ImportIngestionService-StageDocument-Error", ex);
           return null; // draft round-trips with no SourceDocument -- confirm simply skips retention
       }
   }
   ```

   The resulting `SourceDocument { BlobName, FileName, ContentType, SizeBytes }` is set on the draft
   so it round-trips through the review wizard untouched.

2. **Persist on confirm** — move `staging/...` → `{kind}/{guid}-{safeFileName}` and insert an
   `ImportDocument` row, **only** once the row upsert has actually happened:

   ```csharp
   // src/my-api/Services/ImportIngestionService.cs
   private async Task PersistSourceDocumentAsync(SourceDocument sourceDocument, string kind, Guid? parentId)
   {
       if (sourceDocument is null) return;
       try
       {
           var permanentName = $"{kind}/{Guid.NewGuid()}-{SafeBlobFileName(sourceDocument.FileName)}";
           await blob.MoveAsync(StorageContainer, sourceDocument.BlobName, permanentName, sourceDocument.ContentType);

           dc.ImportDocuments.Add(new ImportDocument { Id = Guid.NewGuid(), Kind = kind, FileName = sourceDocument.FileName, ContentType = sourceDocument.ContentType, SizeBytes = sourceDocument.SizeBytes, BlobName = permanentName, UploadedUtc = DateTime.UtcNow, ParentId = parentId });
           await dc.SaveChangesAsync();
       }
       catch (Exception ex)
       {
           logger.LogEvent("ImportIngestionService-PersistSourceDocument-Error", ex);
           // Non-fatal: the row import above already succeeded and is not rolled back --
           // retention just didn't happen this time (blob left in staging/ or move failed).
       }
   }
   ```

   Call this from **every** code path that actually writes the row data — the explicit `confirm`
   action for each `kind`, *and* the `review=true` auto-persist branch inside `ingest`. Miss the
   auto-persist branch and you leak an orphaned blob in `staging/` forever (rows imported, file
   never promoted, no `ImportDocument` row pointing at it) — wire retention to "did the data get
   written", not to "which HTTP action was called."

3. **Blob failure is never fatal to the data import.** Both helpers above wrap every blob call in
   `try/catch` and only `log + return`/`return null` — a storage outage, RBAC misconfiguration, or
   the null-client "disabled" case from the DI guard must never roll back or block the row
   upsert. This is the same non-fatal posture the file-import-ingest skill uses for AI failures.

4. **`ImportDocument` is a new, EF-migration-managed table** — it sits alongside (not instead of)
   the rest of the schema:

   ```csharp
   // src/my-api/Models/ImportDocument.cs
   public class ImportDocument
   {
       public Guid Id { get; set; }
       public string Kind { get; set; }           // e.g. "customers" | "products"
       public string FileName { get; set; }
       public string ContentType { get; set; }
       public long SizeBytes { get; set; }
       public string BlobName { get; set; }        // permanent blob name, e.g. "customers/{guid}-roster.xlsx"
       public DateTime UploadedUtc { get; set; }
       public Guid? ParentId { get; set; }          // the draft's resolved parent record, if any
   }
   ```

   Fluent config lives in an `IEntityTypeConfiguration<ImportDocument>` next to the other entity
   configurations (`entity.ToTable("ImportDocuments")`, `IsRequired()`/`HasMaxLength` on the string
   columns, indexes on `ParentId` and `Kind`) and the table is created by an EF Core migration (see
   [`dotnet-efcore`](dotnet-efcore.md)). Apply that migration against a Release build/output
   (`dotnet ef database update -c <DbContext> --configuration Release`), never against the
   `bin/Debug` output the running API holds locked. In a project that ships schema as SQL delta
   scripts rather than migrations, create the table with a delta instead (see the router's SQL delta
   row) and keep everything else in this section unchanged.

**Read/download surface** — a controller can expose `GET api/import/documents?parentId={guid?}`
(→ `List<ImportDocumentDto>`) and `GET api/import/documents/{id:guid}/download` (→
`FileStreamResult`, `Content-Disposition: attachment` via `File(content, contentType, fileName)`),
both backed by the service's `GetDocumentsAsync`/`DownloadDocumentAsync`.

### The RBAC gotcha worth remembering

**Subscription `Owner`/`Contributor` are control-plane roles only — `dataActions: []`.** They let you
create/list/delete the storage *account* and manage its ARM resource, but grant **zero** permission
to read/write blob *data*. `DefaultAzureCredential` calling `BlobClient.UploadAsync`/`DownloadAsync`
etc. needs an explicit **data-plane** role — `Storage Blob Data Contributor` (or `...Data Reader` for
read-only) assigned at the storage account (or container) scope, separately from any
Owner/Contributor grant. This trips people up because "I'm Owner on the subscription, why is this
403ing" is the natural first reaction — Owner/Contributor and Storage Blob Data Contributor are
orthogonal role families (control-plane ARM vs. data-plane Storage).

Provision both required assignments (the dev identity via `az login` locally, and the compute's
managed identity in the deployed environment) with `az role assignment create --role "Storage Blob
Data Contributor" --scope <storage-account-resource-id>`, guarded so it's idempotent to re-run. Every
new environment needs the identical treatment before this pattern works end-to-end there — it is not
automatic.

## Testing

Mock `BlobStorageService` the same way the AI chat client is mocked in `file-import-ingest.md` —
`Substitute.ForPartsOf`, since every member is `virtual` on a concrete class, not an interface:

```csharp
// src/my-api.Tests/ImportDocumentTests.cs
var blob = Substitute.ForPartsOf<BlobStorageService>((Azure.Storage.Blobs.BlobServiceClient)null!);
```

**Important gotcha**: `ForPartsOf` calls the *real* method body for anything you haven't explicitly
stubbed with `.Returns(...)`. Since the substitute's `client` is `null` ("disabled"), an unstubbed
call runs the real guarded body and throws `BlobStorageDisabledException` — correct for the
"storage unavailable" tests, but happy-path tests must stub success explicitly first:

```csharp
// src/my-api.Tests/ImportDocumentTests.cs
private static void StubBlobSuccess(BlobStorageService blob)
{
    blob.UploadAsync(Arg.Any<string>(), Arg.Any<string>(), Arg.Any<Stream>(), Arg.Any<string>()).Returns(Task.CompletedTask);
    blob.MoveAsync(Arg.Any<string>(), Arg.Any<string>(), Arg.Any<string>(), Arg.Any<string>()).Returns(Task.CompletedTask);
}
```

What to assert:

- **Stage on ingest**: `await blob.Received(1).UploadAsync("import-documents", Arg.Is<string>(n => n.StartsWith("staging/") && n.Contains(originalFileName)), Arg.Any<Stream>(), contentType);` and `draft.SourceDocument` is populated.
- **Persist on confirm**: `await blob.Received(1).MoveAsync("import-documents", stagingBlobName, Arg.Is<string>(n => n.StartsWith($"{kind}/")), contentType);` and exactly one `ImportDocument` row exists with the expected `Kind`/`FileName`/`ParentId`.
- **Non-fatal blob failure**: `blob.MoveAsync(...).Throws(new InvalidOperationException(...));` then confirm — the row upsert result is unaffected and no `ImportDocument` row was inserted.
- **No `SourceDocument`** (staging never happened, e.g. it failed on ingest): confirm skips retention entirely — `blob.DidNotReceive().MoveAsync(...)`, no `ImportDocument` row.
- **Download endpoint**: stub `blob.DownloadAsync(container, blobName).Returns((stream, contentType))`, seed the `ImportDocument` row directly, call the controller action, assert the returned `FileStreamResult.FileStream`/`ContentType`/`FileDownloadName`.

Never hit real Azure Storage in tests — there is no integration-test tier for this unless the project has explicitly added one.

## Blob metadata: make the file self-describing

Stamping the parent row's identity onto the blob means a lost or corrupted database row can be
rebuilt from the container alone. It is cheap, and it is the difference between an orphaned PDF and
a recoverable document. Three things break quietly.

**1. Metadata travels as HTTP headers, so values must be ASCII.** `Internetgebühren`, a newline, or
any accented supplier name will throw or corrupt. Encode on write, decode on read, and keep the
decode on the server so consumers never see the escaped form:

```csharp
metadata[key] = Uri.EscapeDataString(value);   // write
value = Uri.UnescapeDataString(metadata[key]); // read
```

Test it with a real umlaut. An ASCII placeholder proves nothing.

**2. Numbers must be invariant.** `ToString("F2", CultureInfo.InvariantCulture)`. A German-locale
server emits `50,45` otherwise, and the value is unparseable by anything downstream.

**3. Listing returns no metadata unless you ask for it.** `GetBlobsAsync()` omits it by default, so
every row comes back with an empty map while single-blob fetches look perfectly correct — a bug that
only ever surfaces in the UI:

```csharp
await foreach (var item in containerClient.GetBlobsAsync(new GetBlobsOptions { Traits = BlobTraits.Metadata }))
```

(The overload shape moves between SDK majors; on `Azure.Storage.Blobs` 12.28 it is `GetBlobsOptions`,
not the `(traits, states, prefix, ct)` positional form. A wrong guess here is a compile error, which
under `dotnet watch` means the app silently keeps serving the previous build.)

**4. Every copy/move/promote drops metadata unless it carries it.** A helper that re-uploads through
`UploadAsync` starts the destination blob with nothing, and the stage-then-promote path above is
exactly such a helper. Fetch the source metadata and pass it to the destination, and cover it with
its own test.

Keep the key set small and named by whoever owns the data. Identity keys (row id, document number,
date, original file name before any prefixing, ingestion origin) are what make matching possible;
everything else is convenience.

## Checklist

- [ ] One shared container (`AppConfig.Storage.Container`) with prefix folders per stage/kind — not
      a new container per kind.
- [ ] Retained blobs carry the parent row's identity as metadata, encoded for ASCII, with numbers
      invariant, and every move/promote carries it across.
- [ ] Listing requests `BlobTraits.Metadata`, and a test asserts a non-empty map from `ListAsync`.
- [ ] `BlobStorageService` methods are all `virtual`; constructor takes `BlobServiceClient` only (no
      connection string/key parameter anywhere).
- [ ] `AddBlobStorage` registers a **null** `BlobServiceClient` (not a skipped registration) when
      `Storage:AccountName` is blank, so DI still resolves and the app boots.
- [ ] `AppConfig.Storage` bound and read through a strongly-typed config class — never `IConfiguration` directly.
- [ ] Stage on ingest, persist (move + insert) on confirm **and** on any auto-persist path that
      writes the same row data — not just the literal "confirm" action.
- [ ] Every blob call from the ingestion service is wrapped in try/catch; a storage failure never
      blocks or rolls back the row import.
- [ ] New retained-document entity is EF-migration-managed, not bolted onto an existing table by hand.
- [ ] Data-plane RBAC (`Storage Blob Data Contributor`) is assigned separately from any
      Owner/Contributor control-plane role, for both the local dev identity and the target
      compute's managed identity.
- [ ] Tests mock `BlobStorageService` via `Substitute.ForPartsOf` and explicitly stub success on
      happy-path tests (unstubbed calls hit the real "disabled" guard).

## Related

- [`file-import-ingest`](file-import-ingest.md) — the ingest/draft/review/confirm pipeline this
  retention hook plugs into (`ImportIngestionService`, `ImportController`).
- [`dotnet-efcore`](dotnet-efcore.md) — EF Core model/migration conventions (`ImportDocument` follows
  the same migration-managed pattern as any other new table).
- [`dotnet-testing`](dotnet-testing.md) — xUnit/FluentAssertions/NSubstitute conventions.
