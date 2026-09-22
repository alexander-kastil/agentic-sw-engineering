# Storing a file IN the SQL database (varbinary(max) through EF Core)

Keep an uploaded file's bytes in the relational database next to the row that owns it, and serve
them back as a download, without letting the blob leak into every query that never reads it.

## When to use

- One file belongs to one row, the file is small (single-digit MB), and you want it to back up,
  restore, replicate and delete with the row rather than needing a second system kept in sync.
- The deployment has no object store, or adding one buys nothing: an internal tool, a single box, a
  blue/green pair sharing one SQL Server.

Use [`azure-blob-storage`](azure-blob-storage.md) instead when files are large, numerous, streamed,
or served directly to browsers via a signed URL. The upload half of a multi-row import pipeline
(spreadsheet, PDF, OCR) is [`file-import-ingest`](file-import-ingest.md); this leaf is only about
where the bytes come to rest.

## The blob lives in its own table, keyed on the owner's id

```sql
CREATE TABLE dbo.ItemFiles (
    ItemId      uniqueidentifier NOT NULL,
    FileName    nvarchar(260)    NOT NULL,
    ContentType nvarchar(100)    NOT NULL,
    FileSize    int              NOT NULL,
    Content     varbinary(max)   NOT NULL,
    CONSTRAINT PK_ItemFiles PRIMARY KEY (ItemId),
    CONSTRAINT FK_ItemFiles_Items FOREIGN KEY (ItemId)
        REFERENCES dbo.Items(Id) ON DELETE CASCADE
);
```

Four decisions, none of them cosmetic:

- **A separate table, not a column on `Items`.** `varbinary(max)` on the owning table is what makes
  every `SELECT *`, every list endpoint and every EF entity load drag megabytes it never reads. The
  side table means the blob is only ever touched by a query that names it.
- **The id is simultaneously the primary key and the foreign key.** One file per row is expressed by
  the schema rather than by a unique index bolted on afterwards, and there is no surrogate `FileId`
  for anyone to pass around.
- **`ON DELETE CASCADE`.** Deleting the owner disposes the bytes. Without it the file outlives the
  row and nothing ever collects it.
- **`FileSize` is stored, not derived.** A list needs the size; computing it from `DATALENGTH` in the
  projection is fine in raw SQL but is one more thing EF has to be persuaded not to materialise.

In a project that ships schema as hand-written deltas rather than EF migrations, this table arrives
as a delta script: see [`sql-delta-scripts`](sql-delta-scripts.md).

## EF configuration: `WithOne` plus `HasForeignKey<TDependent>`

```csharp
public class ItemFile
{
    public Guid ItemId { get; set; }
    public string FileName { get; set; } = string.Empty;
    public string ContentType { get; set; } = string.Empty;
    public int FileSize { get; set; }
    public byte[] Content { get; set; } = [];
}

public class ItemFileConfiguration : IEntityTypeConfiguration<ItemFile>
{
    public void Configure(EntityTypeBuilder<ItemFile> builder)
    {
        builder.ToTable("ItemFiles");
        builder.HasKey(f => f.ItemId);
        builder.Property(f => f.FileName).IsRequired().HasMaxLength(260);
        builder.Property(f => f.ContentType).IsRequired().HasMaxLength(100);
        builder.Property(f => f.Content).IsRequired();

        builder.HasOne<Item>()
               .WithOne()
               .HasForeignKey<ItemFile>(f => f.ItemId)
               .OnDelete(DeleteBehavior.Cascade);
    }
}
```

**This is where a copied sibling configuration goes wrong.** Every ordinary FK in the model reads
`HasOne<Parent>().WithMany().HasForeignKey(e => e.ParentId)`, and copying that shape here is the
natural mistake: `WithMany` makes it one-to-many, EF then wants a key of its own for the dependent,
and you get a shadow column beside the PK instead of the shared key you designed. A shared-PK
one-to-one needs both halves changed: `WithOne()`, and `HasForeignKey<TDependent>(...)` with the
**dependent** type as the generic argument.

Declaring no navigation property in either direction is deliberate. There is no `item.File` for an
`Include` to pull in, so the blob cannot be dragged into a query by habit or by a later refactor.

## The bytes are never selected into a DTO

The DTO carries the metadata and nothing else, so a list of a thousand rows costs a few kilobytes:

```csharp
public record ItemDto(Guid Id, string Name, string? FileName, string? ContentType, int? FileSize);

var rows = await db.Items.AsNoTracking()
    .Select(i => new ItemDto(
        i.Id,
        i.Name,
        db.ItemFiles.Where(f => f.ItemId == i.Id).Select(f => f.FileName).FirstOrDefault(),
        db.ItemFiles.Where(f => f.ItemId == i.Id).Select(f => f.ContentType).FirstOrDefault(),
        db.ItemFiles.Where(f => f.ItemId == i.Id).Select(f => (int?)f.FileSize).FirstOrDefault()))
    .ToListAsync();
```

Those subqueries translate to one `LEFT JOIN`. With no navigation property this is the only shape
available, which is the point: the projection lists the columns it wants and `Content` is not one of
them. The single-row read that does want the bytes is its own method, called by one endpoint:

```csharp
public Task<ItemFile?> GetFileAsync(Guid itemId) =>
    db.ItemFiles.AsNoTracking().FirstOrDefaultAsync(f => f.ItemId == itemId);
```

The write side is an upsert, because the key is the owner's id and a second upload for the same item
is a replacement, not a new row. `Add` on an existing key throws at `SaveChangesAsync`:

```csharp
public async Task SaveFileAsync(Guid itemId, byte[] content, string fileName, string contentType)
{
    var file = await db.ItemFiles.FirstOrDefaultAsync(f => f.ItemId == itemId);
    if (file is null)
    {
        file = new ItemFile { ItemId = itemId };
        db.ItemFiles.Add(file);
    }

    file.Content = content;
    file.FileName = fileName;
    file.ContentType = contentType;
    file.FileSize = content.Length;
    await db.SaveChangesAsync();
}
```

The lookup is tracked, so no `AsNoTracking()` here, and it does load the old bytes in order to
overwrite them. Where that matters, `ExecuteUpdateAsync` replaces the columns without materialising
the entity.

## Upload endpoint: multipart, buffered, size-capped

```csharp
[HttpPost("{id:guid}/file")]
[RequestSizeLimit(10 * 1024 * 1024)]
public async Task<IActionResult> UploadFile(Guid id, IFormFile file, [FromForm] string? caption)
{
    using var buffer = new MemoryStream();
    await file.CopyToAsync(buffer);
    await service.SaveFileAsync(id, buffer.ToArray(), file.FileName, file.ContentType, caption);
    return NoContent();
}
```

- `IFormFile` plus `[FromForm]` scalars makes the endpoint `multipart/form-data` only. It cannot
  also accept a JSON body, so a client that was posting JSON has to change, and any `.http` file or
  test modelling the request has to send parts rather than a body.
- `[RequestSizeLimit]` is explicit and per-endpoint. Relying on the host default means the cap moves
  when the hosting does, and a reverse proxy in front of it has its own limit that must agree.
- Buffer to `byte[]` rather than handing the request stream to EF: the stream is not seekable and is
  gone by the time `SaveChangesAsync` runs.
- To shrink an uploaded image before it is stored, convert here: [`imagesharp-webp`](imagesharp-webp.md).

## Download endpoint: return a `FileResult`

```csharp
[HttpGet("{id:guid}/file")]
public async Task<IActionResult> GetFile(Guid id)
{
    var file = await service.GetFileAsync(id);
    return file is null ? NotFound() : File(file.Content, file.ContentType, file.FileName);
}
```

`File(bytes, contentType, fileName)` is what produces a correct `Content-Disposition`. Writing the
bytes to the response by hand, or returning the entity as JSON and decoding base64 in the client,
both lose the filename and the type the browser needs in order to save the file with the right
extension.

## Proof it still holds

Round-trip one real file through the running server and check the headers and the bytes:

```bash
curl -s -F "file=@sample.png" http://localhost:5000/items/$ID/file
curl -sD - -o out.bin http://localhost:5000/items/$ID/file | grep -i content-disposition
file out.bin && stat -c %s out.bin
```

The header must name the stored filename twice (a plain `filename=` and an RFC 5987 `filename*=`),
`file` must report the real format rather than "data", and the byte count must equal the `FileSize`
the list endpoint reports. In the test suite, assert that the list DTO type has no `byte[]` member:
that is the invariant which silently rots when someone adds a field.

## Related

- [`dotnet-efcore`](dotnet-efcore.md) - entity configuration and query patterns.
- [`dotnet-controllers`](dotnet-controllers.md) - controller and CRUD endpoint shape.
- [`sql-delta-scripts`](sql-delta-scripts.md) - shipping the table where migrations are prohibited.
- [`azure-blob-storage`](azure-blob-storage.md) - the alternative when the file does not belong in the DB.
