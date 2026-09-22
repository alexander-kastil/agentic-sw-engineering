## When to use

Downloading a file the API generates (CSV, PDF, xlsx, a zip) from an Angular app, when the request
must carry auth. Triggers: "download a file", "export button", "save a blob", "responseType blob",
"Content-Disposition", "filename is always the fallback", "download opens a login page", "downloaded
file is 401 HTML".

The upload direction lives in [`angular-http.md`](angular-http.md) under File Upload.

## Never point an `<a href>` at the endpoint

The shortest version is a link or `window.open` straight at the API url. It works in dev with auth
off and fails the moment auth is on: a browser navigation carries cookies, never the `Authorization`
header your MSAL or JWT interceptor adds, so the response is a 401 page saved to disk as a file with
the right name and the wrong content. `fetch` has the same problem for the opposite reason: it
bypasses `HttpClient`, so no interceptor runs at all.

Go through `HttpClient`. That is the whole point: it is the only path the app's interceptors see.

```ts
exportAll(): Observable<HttpResponse<Blob>> {
  return this.http.get(`${environment.apiUrl}/secrets/export`, {
    responseType: 'blob',
    observe: 'response',
  });
}
```

`observe: 'response'` is what makes the headers reachable; with the default you get the body only.

## Saving the blob

```ts
private readonly exporting = signal(false);

exportAll(): void {
  this.exporting.set(true);
  this.secrets.exportAll().subscribe({
    next: res => {
      const url = URL.createObjectURL(res.body!);
      const a = document.createElement('a');
      a.href = url;
      a.download = filenameFrom(res.headers.get('Content-Disposition')) ?? 'export.csv';
      a.click();
      URL.revokeObjectURL(url);
      this.exporting.set(false);
    },
    error: () => this.exporting.set(false),
  });
}
```

Three things that are easy to get wrong here:

- **Revoke the object URL.** An un-revoked blob url pins its buffer for the life of the document, so
  a page that exports repeatedly leaks the full file each time.
- **Reset the in-flight signal on the error path too**, or a single failure leaves the button disabled
  until reload. That is not defensive extra scope, it is the difference between a disabled button and
  a broken one.
- **Bind `[disabled]` to the signal** rather than tracking it imperatively, so a double click cannot
  fire two downloads.

## The header the browser will not give you

`Content-Disposition` is not a CORS-safelisted response header. Cross-origin, `res.headers.get(...)`
returns `null` however correct the server's header is, so the filename silently falls back forever and
the bug never appears in a same-origin build. The server has to opt in:

```csharp
policy.WithOrigins(allowedOrigins)
      .AllowAnyHeader()
      .AllowAnyMethod()
      .WithExposedHeaders("Content-Disposition");
```

Same for any other custom header the client reads (`X-Total-Count`, a pagination cursor). Note the
asymmetry that makes this confusing: `AllowAnyHeader()` governs the **request**, and does nothing for
what the client may **read** back.

## Verifying it

Not from the code, and not from a screenshot of a saved file. Run this in the page's own console
(or via chrome-devtools) and read the four facts at once:

```js
const res = await fetch('http://localhost:5099/api/secrets/export');
const blob = await res.blob();
const buf = new Uint8Array(await blob.arrayBuffer());
({ status: res.status,
   disposition: res.headers.get('content-disposition'),   // null => CORS is not exposing it
   type: blob.type,
   bom: buf[0] === 0xEF && buf[1] === 0xBB && buf[2] === 0xBF });
```

To prove the button rather than the endpoint, wrap `URL.createObjectURL`, `URL.revokeObjectURL` and
`HTMLAnchorElement.prototype.click` before clicking it, then assert one blob created, one url revoked,
and the anchor's `download` value. That is the only way to see the filename the user actually gets.

**Read the BOM from bytes, never from text.** `blob.text()` decodes UTF-8 per the Encoding standard,
which strips a leading BOM, so a correct file reports `bom: false` and sends you chasing a server bug
that is not there. Read `arrayBuffer()`.

**Check `disabled` after a frame, not synchronously.** With signals and `OnPush` the DOM updates on
the next change detection pass, so reading `btn.disabled` immediately after `click()` returns the old
value and looks like the guard is missing. Await one `requestAnimationFrame` first.
