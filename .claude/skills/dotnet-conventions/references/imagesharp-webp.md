# Converting an uploaded image to WebP server-side (ImageSharp)

Shrink a JPEG or PNG the moment it arrives, before it is stored, and never damage anything else that
arrives with it. A real 351 KB PNG came back as a 71 KB WebP through exactly this code.

## When to use

- An API accepts image uploads and you want one canonical, small format on disk or in the database.
- The conversion has to be safe for arbitrary input: the same endpoint also receives PDFs, SVGs,
  zero-byte files and JPEGs that are secretly something else.

Build-time conversion of a folder of site assets is a different job with different tools; that is
the `optimize-images` skill. This leaf is the in-process, per-request conversion.

## Package

```bash
dotnet add package SixLabors.ImageSharp
```

Pin the version already used elsewhere in the solution rather than taking whatever is newest.
ImageSharp has moved namespaces and licence terms between majors, and a second version in one
solution is a diamond waiting to happen.

## The converter: encode both ways, keep the smaller

```csharp
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Formats.Webp;

public static class WebpConverter
{
    public static (byte[] Bytes, string FileName, string ContentType) Convert(
        byte[] bytes, string fileName, string contentType)
    {
        if (!IsConvertible(fileName, contentType)) return (bytes, fileName, contentType);

        try
        {
            using var image = Image.Load(bytes);

            var lossy = Encode(image, new WebpEncoder { FileFormat = WebpFileFormatType.Lossy, Quality = 82 });
            var lossless = Encode(image, new WebpEncoder { FileFormat = WebpFileFormatType.Lossless });
            var best = lossless.Length < lossy.Length ? lossless : lossy;

            if (best.Length >= bytes.Length) return (bytes, fileName, contentType);

            return (best, Path.ChangeExtension(fileName, ".webp"), "image/webp");
        }
        catch (ImageFormatException)
        {
            return (bytes, fileName, contentType);
        }
    }

    private static byte[] Encode(Image image, WebpEncoder encoder)
    {
        using var ms = new MemoryStream();
        image.Save(ms, encoder);
        return ms.ToArray();
    }

    private static readonly HashSet<string> ConvertibleTypes =
        new(StringComparer.OrdinalIgnoreCase) { "image/jpeg", "image/jpg", "image/png" };

    private static bool IsConvertible(string fileName, string? contentType)
    {
        if (contentType is not null && ConvertibleTypes.Contains(contentType)) return true;
        return Path.GetExtension(fileName).ToLowerInvariant() is ".jpg" or ".jpeg" or ".png";
    }
}
```

**"Optimal" means encoding twice and measuring, not picking a mode.** Which one wins is a property
of the picture, not of the format: photographic noise favours lossy, flat colour art and screenshots
favour lossless. The verified case here, a real screenshot-like PNG, came back **lossless** at
roughly a fifth of its original size, which is the opposite of what a lossy-by-default converter
would have produced. Encoding both costs milliseconds on an upload path that is already doing IO.

**A converter that can grow the file is a bug.** Lossy WebP regularly exceeds the source on
flat-colour art, so the size comparison against the original bytes is not an optimisation, it is the
guard that stops the endpoint from making uploads worse. When it fires, return the original bytes,
name and content type untouched.

## The API names, because guessing costs a compile cycle

| What you want | The actual name |
|---|---|
| The encoder | `WebpEncoder`, in `SixLabors.ImageSharp.Formats.Webp` |
| Lossy vs lossless | `WebpFileFormatType.Lossy` / `.Lossless` |
| The encoder property | `WebpEncoder.FileFormat`, typed `WebpFileFormatType?` |
| Decode failure | `ImageFormatException` |

`WebpFileFormat` does not exist. It is the obvious guess, it reads correctly in a sentence, and it
does not compile. Verify a library's enum and property names against the assembly (F12 in the IDE,
or `dotnet build` on a one-line probe) rather than from memory: a plausible name is exactly the kind
of detail a model reconstructs confidently and wrongly.

`ImageFormatException` is the base of both `UnknownImageFormatException` (nothing recognised the
bytes) and `InvalidImageContentException` (the format was recognised and the content is corrupt), so
catching the base covers both. Do not catch `Exception` here: an `OutOfMemoryException` from a
decompression bomb is not a "pass it through" case.

## What must pass through untouched

- **Anything that is not JPEG or PNG.** Same bytes, same name, same content type. A PDF that comes
  back renamed `.webp` is a data-loss bug that only surfaces at download time.
- **Anything that fails to decode.** Callers upload broken files; the endpoint's job is to store what
  it was given, not to reject it on the converter's behalf.
- **Detection accepts either signal, case-insensitively.** Clients post `image/jpg`, `IMAGE/PNG`, or
  `application/octet-stream` with a `.PNG` filename, and a browser drag-and-drop can send no content
  type at all. Requiring both signals to agree rejects normal traffic.

## Testing without committing binary fixtures

Generate the input in the test with ImageSharp itself. A repo that accumulates `.png` fixtures for
image tests gets one per case and reviews none of them.

```csharp
private static byte[] PngOf(int w, int h, Color fill)
{
    using var image = new Image<Rgba32>(w, h);
    image.Mutate(ctx => ctx.Fill(fill));
    using var ms = new MemoryStream();
    image.SaveAsPng(ms);
    return ms.ToArray();
}
```

Cover the four outcomes: a PNG converts, a PDF's bytes come back identical, garbage bytes come back
identical, and a file whose WebP would be larger comes back identical.

## Proof it still holds

A WebP file is a RIFF container: bytes 0..3 are `RIFF` and bytes 8..11 are `WEBP`. Assert that on the
converter's output rather than trusting the returned content type, and assert it again on a file
pulled back out of storage:

```csharp
Encoding.ASCII.GetString(result.Bytes, 0, 4).Should().Be("RIFF");
Encoding.ASCII.GetString(result.Bytes, 8, 4).Should().Be("WEBP");
result.Bytes.Length.Should().BeLessThan(original.Length);
```

On the wire, `file downloaded.webp` reporting `RIFF (little-endian) data, Web/P image` is the same
check from outside the process.

## Related

- [`sql-stored-files`](sql-stored-files.md) - where the converted bytes come to rest, and the endpoint that serves them back.
- [`file-import-ingest`](file-import-ingest.md) - the upload endpoint shape and `IFormFile` buffering.
- `optimize-images` (global skill) - build-time conversion of a folder of site assets, and the same encode-both-and-keep-the-smaller rule applied there.
