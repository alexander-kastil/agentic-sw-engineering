# Blob Document List & Download

A reusable pattern for **listing server-retained files and downloading them** — built for
automation A3 (Dokument-Ablage pro Objekt), which retains every imported Mieterliste/
Wartungsliste original in blob storage and exposes a list + download endpoint. Pattern
lives in `src/ui` (maintenance-planner): `shared/import/import.service.ts`,
`store/features/with-imports.feature.ts`, and `resources/components/house-edit/`.

## When to use

- Rendering a list of server-stored files (imports, exports, attachments, generated reports)
  against a single entity (a House, a Task run, a Reservation…).
- Any "click to download the original/generated file" button backed by an authenticated API
  route rather than a public static URL.
- You already have (or are adding) the [`file-import-wiz`](file-import-wiz.md) pipeline and
  want to surface the originals it retained.

## Core principles (why this shape)

1. **Never link an anchor straight at an authenticated API URL.** A plain
   `<a href="https://api/.../download">` performs a normal browser navigation with no
   `Authorization` header — MSAL's bearer token only rides requests made through
   `HttpClient` (intercepted by the app's auth interceptor). So the download must be a real
   `HttpClient` request; the browser-native "save this file" gesture is then faked with a
   **blob + transient object-URL anchor**, not a direct navigation.
2. **The list and the download are two independent concerns.** Listing is a `GET` returning
   JSON metadata (`ImportDocumentDto[]`); downloading is a second `GET` per file returning
   the binary as a blob. Don't conflate them into one call.
3. **Blob/anchor mechanics live in a service, never inline in a component** — this repo's
   hard rule (see `CLAUDE.md`: "keep download/blob handling in a service, never inline in
   components"). The component/store only calls `service.downloadDocument(id, fileName)`.
4. **The list has its own loading flag, independent of any "busy" flag an unrelated wizard
   flow uses.** Browsing retained documents must never disturb an in-progress import/upload
   (see `angular-signal-store-design` — one composed store, many independent slices).
5. **Download is not a create/save/delete action** — per the bico-brand two-color button
   rule, the download button is **black/neutral**, never gold.

## Reference implementation

### The DTO

`src/ui/src/app/shared/models/import.model.ts`

```typescript
/** A retained original import document. `Kind` mirrors `ImportKind` ('mieterliste' |
 * 'wartungsliste') as a plain string on the wire. `HouseId` is nullable — a Wartungsliste
 * upload can produce documents for several buildings, or none yet if nothing matched. */
export interface ImportDocumentDto {
  ID: string;
  Kind: string;
  FileName: string;
  ContentType: string;
  SizeBytes: number;
  UploadedUtc: string;
  HouseId: string | null;
}
```

### The service — list (JSON) + download (blob → anchor)

`src/ui/src/app/shared/import/import.service.ts`

```typescript
/** `GET /import/documents?houseId={guid}` — A3 Dokument-Ablage; omit `houseId` for the
 * full list. Consumed by the House edit page's "Dokumente" section. */
listDocuments(houseId?: string) {
  const url = houseId
    ? `${environment.webApiUrl}import/documents?houseId=${encodeURIComponent(houseId)}`
    : `${environment.webApiUrl}import/documents`;
  return this.http.get<ImportDocumentDto[]>(url);
}

/** `GET /import/documents/{id}/download` — fetches the retained original as a blob and
 * triggers a browser download via a transient object-URL anchor (mirrors
 * `with-tasks.feature.ts`'s `downloadTaskRunFiles`, this repo's existing blob-download
 * pattern). Blob/download handling stays in this service, never inline in a component. */
downloadDocument(id: string, fileName: string): void {
  this.http.get(`${environment.webApiUrl}import/documents/${id}/download`, { responseType: 'blob' }).subscribe((blob) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(url);
  });
}
```

This exact `get(..., { responseType: 'blob' })` → `createObjectURL` → `<a download>` click →
`revokeObjectURL` shape is not new to A3 — it's this repo's established blob-download
precedent, first written for the Automatisierungen run-file export in
`src/ui/src/app/store/features/with-tasks.feature.ts` (`downloadTaskRunFiles`). Reuse the
shape rather than inventing a second one.

### Rendering — list rows with a kind chip, size, date, and a neutral download button

`src/ui/src/app/resources/components/house-edit/house-edit.component.html` (excerpt):

```html
@if (isEditMode()) {
  <section class="form-section">
    <div class="section-bar">Dokumente</div>

    @if (importDocumentsLoading()) {
      <p class="py-2 text-sm text-muted" aria-live="polite">Lade Dokumente…</p>
    } @else {
      <table class="data-table w-full">
        <thead>
          <tr>
            <th>Datei</th>
            <th>Art</th>
            <th class="text-right">Größe</th>
            <th>Hochgeladen</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          @for (doc of importDocuments(); track doc.ID) {
            <tr>
              <td>{{ doc.FileName }}</td>
              <td><span class="chip">{{ documentKindLabel(doc.Kind) }}</span></td>
              <td class="text-right tabular-nums">{{ formatFileSize(doc.SizeBytes) }}</td>
              <td>{{ formatDocumentDate(doc.UploadedUtc) }}</td>
              <td class="text-right">
                <button
                  type="button"
                  class="rounded p-1 hover:bg-surface-alt"
                  aria-label="Herunterladen"
                  uxTooltip="Herunterladen"
                  (click)="downloadDocument(doc)"
                >
                  <span class="material-icons text-base" aria-hidden="true">download</span>
                </button>
              </td>
            </tr>
          } @empty {
            <tr><td colspan="5" class="py-4 text-center text-muted">Keine abgelegten Dokumente für dieses Objekt.</td></tr>
          }
        </tbody>
      </table>
    }
  </section>
}
```

Note the download button is a plain neutral icon button (`hover:bg-surface-alt`, no
`ux-button variant="gold"`) — downloading doesn't create, save, or delete anything, so it
never gets the gold treatment (see `bico-brand` → "Buttons — TWO colors, chosen by action").

`src/ui/src/app/resources/components/house-edit/house-edit.component.ts` (excerpt):

```typescript
protected readonly importDocuments = this.store.importDocuments;
protected readonly importDocumentsLoading = this.store.importDocumentsLoading;

ngOnInit(): void {
  const id = this.id();
  if (!id) return;
  // ...pre-populate the edit form from the store...
  this.store.loadDocuments(id);
}

protected downloadDocument(doc: ImportDocumentDto): void {
  this.store.downloadDocument(doc.ID, doc.FileName);
}
```

### Where it lives

The House edit page (`resources/components/house-edit`), **edit-mode only** (`isEditMode()`
gates the whole section — a not-yet-saved "new" House has no `id` to query documents for).
This was the natural fit here because the House edit component already had the `id` input,
the `AppStore` injection, and an `ngOnInit` to hook into — no new route or shell needed. If
your target entity doesn't have an existing detail/edit page to host it, a compact list on
whatever page originates the imports (e.g. an automations/tasks page) is the fallback.

### The `SourceDocument` pass-through (draft → wizard confirmation)

The [`file-import-wiz`](file-import-wiz.md) draft types carry an optional `SourceDocument`
set by the server on ingest — the client's job is only to **not lose it**:

`src/ui/src/app/shared/models/import.model.ts`

```typescript
/** A3 Dokument-Ablage — the original uploaded file, staged by the server into blob storage
 * on ingest and referenced from the draft it produced. Present once the server has staged
 * the file; `undefined` for older/in-flight drafts that predate A3. Both `applyDraftPatch`
 * and `applyWartungsPatch` spread the whole draft on every patch, so this rides along
 * untouched through the review step automatically — it only needs to exist on the type so
 * TS doesn't strip it. */
export interface SourceDocument {
  BlobName: string;
  FileName: string;
  ContentType: string;
  SizeBytes: number;
}

export interface ImportDraft {
  Kind: string;
  HouseId: string | null;
  Rows: HouseUnitRow[];
  SourceDocument?: SourceDocument;
}
```

Because `applyDraftPatch`/`applyWartungsPatch` always do `{ ...current, ...patch }` (see
`with-imports.feature.ts`), `SourceDocument` survives every row edit without either method
ever mentioning it by name. The wizard reads it once, right when a commit lands, to decide
whether to show the retention confirmation:

`src/ui/src/app/tasks/import-wizard/import-wizard.component.ts` (excerpt):

```typescript
// 3. when the commit result lands, show the "Import abgeschlossen" confirmation
effect(() => {
  const done = this.kind() === 'mieterliste' ? this.store.lastImportedId() : this.store.lastWartungsResult();
  if (this.accepting() && done) {
    this.accepting.set(false);
    const hadSourceDocument = !!(this.kind() === 'mieterliste' ? this.draft()?.SourceDocument : this.wartungsDraft()?.SourceDocument);
    this.sourceDocRetained.set(hadSourceDocument);
    this.committed.set(true);
    // ...
  }
});
```

```html
@if (sourceDocRetained()) {
  <p class="mt-1 text-sm text-muted">Originaldokument abgelegt ✓</p>
}
```

## Store wiring

`src/ui/src/app/store/features/with-imports.feature.ts` — the list gets its **own** loading
flag (`importDocumentsLoading`), deliberately separate from `importBusy` (the flag A1/A2
`ingestFile`/`ingestWartungsFile`/`commitDraft`/`commitWartungsDraft` use):

```typescript
export interface ImportsState {
  // ...A1/A2 draft state...
  importDocuments: ImportDocumentDto[];
  importDocumentsLoading: boolean;
  importBusy: boolean; // shared by A1/A2 ingest/commit only — NOT by loadDocuments
  // ...
}
```

```typescript
/** `GET /import/documents?houseId={guid}` — pass `undefined` for the full list.
 * Independent of the ingest/commit busy flags above so browsing retained documents
 * (e.g. on the House edit page) never disturbs an in-progress A1/A2 wizard flow. */
loadDocuments: rxMethod<string | undefined>(
  pipe(
    tap(() => patchState(store, { importDocumentsLoading: true })),
    switchMap((houseId) =>
      importService.listDocuments(houseId).pipe(
        tapResponse({
          next: (importDocuments) => patchState(store, { importDocuments }),
          error: (error: unknown) => console.error('loadDocuments error:', error),
          finalize: () => patchState(store, { importDocumentsLoading: false }),
        }),
      ),
    ),
  ),
),

/** `GET /import/documents/{id}/download` — delegates the blob/anchor-click download
 * mechanics to `ImportService` (kept out of components per project convention). */
downloadDocument(id: string, fileName: string): void {
  importService.downloadDocument(id, fileName);
},
```

Call `store.loadDocuments(houseId)` from the host page's `ngOnInit` (pass `undefined` for an
unfiltered list); call `store.downloadDocument(id, fileName)` from the row's click handler.

## Testing (Vitest)

Mock the service, not `HttpClient` directly, at both layers.

**Service layer** — assert the real URLs and the blob→anchor mechanics
(`src/ui/src/app/shared/import/import.service.spec.ts`):

```typescript
it('GETs /import/documents?houseId={id} when a houseId is given', () => {
  service.listDocuments('house-1').subscribe();
  const req = httpMock.expectOne(`${environment.webApiUrl}import/documents?houseId=house-1`);
  expect(req.request.method).toBe('GET');
  req.flush([]);
});

it('GETs /import/documents/{id}/download as a blob and triggers an anchor download', () => {
  const blob = new Blob(['file-bytes']);
  const anchors: HTMLAnchorElement[] = [];
  vi.spyOn(document, 'createElement').mockImplementation(() => {
    const a = { href: '', download: '', click: vi.fn() } as unknown as HTMLAnchorElement;
    anchors.push(a);
    return a;
  });
  globalThis.URL.createObjectURL = vi.fn().mockReturnValue('blob:url');
  globalThis.URL.revokeObjectURL = vi.fn();

  service.downloadDocument('d1', 'Mistelbach.xlsx');

  const req = httpMock.expectOne(`${environment.webApiUrl}import/documents/d1/download`);
  expect(req.request.responseType).toBe('blob');
  req.flush(blob);

  expect(anchors[0].download).toBe('Mistelbach.xlsx');
  expect(anchors[0].click).toHaveBeenCalled();
  expect(globalThis.URL.revokeObjectURL).toHaveBeenCalledWith('blob:url');
});
```

**Store layer** — assert population and that it's independent of the wizard's busy flag
(`src/ui/src/app/store/features/with-imports.spec.ts`):

```typescript
it('calls ImportService.listDocuments and populates importDocuments', () => {
  const svc = { listDocuments: vi.fn().mockReturnValue(of(docs)) };
  const store = buildStore(svc);
  store.loadDocuments('house-1');
  TestBed.flushEffects();
  expect(svc.listDocuments).toHaveBeenCalledWith('house-1');
  expect(store.importDocuments()).toEqual(docs);
});

it('does not disturb an in-progress A1/A2 draft', () => {
  const svc = { ingestMieterliste: vi.fn().mockReturnValue(of({ Draft: draft() })), listDocuments: vi.fn().mockReturnValue(of([])) };
  const store = buildStore(svc);
  store.ingestFile(new File(['x'], 'a.xlsx'));
  TestBed.flushEffects();
  store.loadDocuments('house-1');
  TestBed.flushEffects();
  expect(store.importDraft()).not.toBeNull(); // untouched
});
```

**Component layer** — assert the list renders and the download button fires
(`src/ui/src/app/resources/components/house-edit/house-edit.component.spec.ts`):

```typescript
it('renders a row per retained document with kind badge, size, and date', () => {
  importServiceSpy.listDocuments.mockReturnValue(of([doc]));
  fixture.componentRef.setInput('id', 'h1');
  fixture.detectChanges();
  const text = fixture.nativeElement.textContent as string;
  expect(text).toContain('Mistelbach.xlsx');
  expect(text).toContain('Mieterliste');
});

it('renders a working download button that calls downloadDocument on click', () => {
  importServiceSpy.listDocuments.mockReturnValue(of([doc]));
  fixture.componentRef.setInput('id', 'h1');
  fixture.detectChanges();
  const button = fixture.nativeElement.querySelector('button[aria-label="Herunterladen"]') as HTMLButtonElement;
  button.click();
  expect(importServiceSpy.downloadDocument).toHaveBeenCalledWith('d1', 'Mistelbach.xlsx');
});
```

## Checklist

- [ ] `ImportDocumentDto`-style list DTO defined once, next to any related draft types.
- [ ] `listDocuments(entityId?)` and `downloadDocument(id, fileName)` both live in a service —
      never a component.
- [ ] Download never uses a plain `<a href="...">` at an authenticated API route — always
      `HttpClient.get(..., { responseType: 'blob' })` → `createObjectURL` → anchor `click()` →
      `revokeObjectURL`.
- [ ] The list's loading flag is its own state field, independent of any unrelated
      ingest/commit/save busy flag.
- [ ] Rendered list: filename, a kind/type chip, human-size, date, and a **black/neutral**
      download icon button — never gold (download isn't a mutation).
- [ ] Empty state text for "no documents yet", not a blank table.
- [ ] Any draft type carrying a passthrough field (like `SourceDocument`) only needs the
      field added to its TS interface — immutable `{ ...current, ...patch }` patch methods
      preserve it automatically; don't hand-thread it through every patch call site.
- [ ] Vitest at all three layers: service (URL + blob/anchor mechanics), store (population +
      "doesn't disturb unrelated state"), component (renders rows, download button fires).

## Related

- [`file-import-wiz`](file-import-wiz.md) — the import wizard whose drafts carry
  `SourceDocument`; this pattern is its "A3 Dokument-Ablage" companion.
- [`angular-file-dropzone`](angular-file-dropzone.md) — the upload side this pattern's
  documents originated from.
- [`angular-signal-store-design`](angular-signal-store-design.md) — why the list gets its
  own state slice/loading flag instead of reusing an unrelated one.
- [`angular-http`](angular-http.md) — `HttpClient` mutation/blob conventions, `rxMethod`.
- `bico-brand` skill — the two-color button rule (`download` is black, never gold).
