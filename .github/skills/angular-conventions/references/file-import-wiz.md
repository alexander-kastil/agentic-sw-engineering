# File Import Wizard (Angular client)

A standalone, multi-step **file-import wizard** — upload a document, let the API turn it into an editable draft (AI/parsing server-side), review/correct it, optionally refine it with an AI assistant, then commit. Client pattern distilled from `vouchers-ai/src/vouchers-ui` (`vouchers/voucher-booking-wiz/`) and adapted to maintenance-planner's Angular 22 + `@ngrx/signals` AppStore stack.

> The **server side** of this pattern (ingest / categorize / assist / confirm endpoints, OCR + AI draft generation, blob + EF persistence) lives in the `dotnet-conventions` skill → [`file-import-ingest`](../../dotnet-conventions/references/file-import-ingest.md). This reference is the Angular client only.

## When to use

- Building any "import a file → check what we extracted → save" flow: Mieterlisten (→ `HouseUnit`), the monthly maintenance worklist (→ `House`/`Product`/schedules), or any Excel/PDF the Hausverwaltungen send.
- The AI file-drop automations described in `docs/ai-automations/readme.md`.
- Fed by the [`angular-file-dropzone`](angular-file-dropzone.md) control on step 1.

## Architecture at a glance

| Concern | Where it lives |
|---|---|
| Step machine, selected line, view toggles | **local `signal()`s** in the wizard component |
| Draft, samples, busy flag, assistant messages, saved id | **AppStore slice** (surface store signals directly) |
| File → draft, chat, commit | **`rxMethod`s on the store**, calling the API — never client-side parsing |
| Review/mapping UI | **reuse the feature's normal edit components** bound to the draft's row array |
| Wizard shell | native modal (`role="dialog" aria-modal`), ESC to close, focus-trapped |

Key rule: **the component holds only view state; all import *data* lives in the store.** The wizard surfaces `store.importDraft()`, `store.importBusy()`, etc. directly, and mutates the draft through one `applyDraftPatch(partial)` store method (immutable patch). No client-side xlsx/pdf/csv library — the file is shipped as `FormData` and the API returns a full editable draft DTO.

## Step flow

`type Step = 1 | 2 | 3` — a hand-rolled rail (`@for` pills + `@if (step()===n)` bodies), **not** Angular Material stepper:

1. **Hochladen (Upload)** — `<app-file-dropzone>` + optional mobile `capture="environment"` input. While `busy()`, show an "wird analysiert…" status card.
2. **Prüfen (Review / column-mapping)** — reuse the feature's existing edit form + table bound to `draft().Rows`. The user corrects the AI's field mapping (which column → which entity field, house/product association, dates). Each edit calls `applyDraftPatch`.
3. **Assistent (optional AI refine)** — a chat panel over `{ Draft, Messages }`; the API may return a structured `PatchJson` that gets merged into the draft. Also surfaces "ähnliche" prior imports as one-click templates.

## Reference implementation

`src/ui/src/app/<feature>/import-wizard/import-wizard.ts`

```ts
import { AfterViewInit, ChangeDetectionStrategy, Component, computed, effect, inject, input, output, signal } from '@angular/core';
import { AppStore } from '../../store/app.store';
import { FileDropzone } from '../../shared/file-dropzone/file-dropzone';

type Step = 1 | 2 | 3;

@Component({
  selector: 'app-import-wizard',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [FileDropzone /* , edit form/table, chat panel */],
  templateUrl: './import-wizard.html',
  styleUrl: './import-wizard.css',
})
export class ImportWizard implements AfterViewInit {
  initialFile = input<File | null>(null);   // pre-supplied (e.g. from a global drop)
  closed = output<void>();

  private store = inject(AppStore);

  // view state — local signals only
  protected step = signal<Step>(1);
  protected selectedIndex = signal(0);

  // import data — surfaced straight from the store
  protected draft   = this.store.importDraft;
  protected busy    = this.store.importBusy;
  protected samples = this.store.importSamples;
  protected messages = this.store.assistMessages;

  protected rows = computed(() => this.draft()?.Rows ?? []);
  protected selectedRow = computed(() => this.rows()[this.selectedIndex()] ?? null);

  private handledInitial: File | null = null;
  private ingested = signal(false);
  private accepting = signal(false);

  constructor() {
    // 1. auto-ingest a pre-supplied file exactly once
    effect(() => {
      const file = this.initialFile();
      if (file && file !== this.handledInitial && !this.ingested()) {
        this.handledInitial = file; this.ingested.set(true);
        this.store.ingestFile({ file, review: false });
      }
    });
    // 2. when a draft lands on step 1, advance to review
    effect(() => {
      if (this.draft() && this.step() === 1 && this.ingested()) { this.ingested.set(false); this.step.set(2); }
    });
    // 3. when the committed record gets an id, clear + close
    effect(() => {
      const id = this.store.lastImportedId();
      if (this.accepting() && id) { this.accepting.set(false); this.store.clearImport(); this.closed.emit(); }
    });
  }

  ngAfterViewInit() { /* focus the backdrop for ESC/trap */ }

  onFilesSelected(files: File[]) {
    const file = files[0];
    if (!file) return;
    this.ingested.set(true);
    this.store.ingestFile({ file, review: false });
  }

  next() { if (this.step() < 3) this.step.update(s => (s + 1) as Step); }
  goTo(s: Step) { this.step.set(s); }

  onRowChange(partial: Record<string, unknown>) {
    const current = this.draft(); if (!current) return;
    const idx = this.selectedIndex();
    const Rows = current.Rows.map((r, i) => i === idx ? { ...r, ...partial } : r);
    this.store.applyDraftPatch({ Rows });
  }

  accept() {                              // "Übernehmen": walk to step 3, then commit
    if (!this.draft() || this.busy()) return;
    if (this.step() < 3) { this.next(); return; }
    this.accepting.set(true);
    this.store.commitDraft();
  }

  close() { this.store.clearImport(); this.closed.emit(); }
}
```

### Store slice (`@ngrx/signals`) — the ingest state machine

Add to the AppStore as its own feature (`withImports`) or fold into `withTasks`. See [`angular-signal-store-design`](angular-signal-store-design.md) and [`angular-http`](angular-http.md).

```ts
export function withImports() {
  return signalStoreFeature(
    withState({
      importDraft: null as ImportDraft | null,
      importSamples: [] as ImportSample[],
      importBusy: false,
      assistMessages: [] as AssistMessage[],
      lastImportedId: null as string | null,
    }),
    withMethods((store, svc = inject(ImportService)) => ({
      applyDraftPatch(patch: Partial<ImportDraft>) {
        const d = store.importDraft(); if (!d) return;
        patchState(store, { importDraft: { ...d, ...patch } });
      },
      clearImport() {
        patchState(store, { importDraft: null, importSamples: [], assistMessages: [], lastImportedId: null });
      },
      ingestFile: rxMethod<{ file: File; review: boolean }>(pipe(
        tap(() => patchState(store, { importBusy: true })),
        switchMap(({ file, review }) => svc.ingest(file, review).pipe(tapResponse({
          next: (r) => patchState(store, { importDraft: r.Draft, importSamples: r.Samples ?? [] }),
          error: () => { /* AILogger / toast */ },
          finalize: () => patchState(store, { importBusy: false }),
        }))),
      )),
      assist: rxMethod<{ text: string }>(pipe(
        switchMap(({ text }) => {
          const messages = [...store.assistMessages(), { Role: 'user', Content: text }];
          patchState(store, { assistMessages: messages, importBusy: true });
          return svc.assist({ Draft: store.importDraft()!, Messages: messages }).pipe(tapResponse({
            next: (r) => {
              patchState(store, { assistMessages: [...store.assistMessages(), { Role: 'assistant', Content: r.Reply }] });
              if (r.PatchJson) patchState(store, { importDraft: { ...store.importDraft()!, ...JSON.parse(r.PatchJson) } });
            },
            error: () => {},
            finalize: () => patchState(store, { importBusy: false }),
          }));
        }),
      )),
      commitDraft: rxMethod<void>(pipe(
        switchMap(() => svc.confirm(store.importDraft()!).pipe(tapResponse({
          next: (saved) => patchState(store, { lastImportedId: saved.Id /*, merge into the target list slice */ }),
          error: () => {},
        }))),
      )),
    })),
  );
}
```

### Service (`FormData` upload; mutations use `HttpClient`, not `httpResource`)

```ts
@Injectable({ providedIn: 'root' })
export class ImportService {
  private http = inject(HttpClient);
  private base = inject(APP_CONFIG).webApiUrl;

  ingest(file: File, review: boolean) {
    const fd = new FormData(); fd.append('file', file);
    return this.http.post<IngestionResult>(`${this.base}/import/ingest?review=${review}`, fd);
  }
  assist(body: { Draft: ImportDraft; Messages: AssistMessage[] }) {
    return this.http.post<AssistResult>(`${this.base}/import/assist`, body);
  }
  confirm(draft: ImportDraft) {
    return this.http.post<{ Id: string }>(`${this.base}/import/confirm`, draft);
  }
}
```

## Two entry paths (mirror them)

1. **Explicit** — a toolbar "Importieren" button sets `importVisible.set(true)`; template renders `@if (importVisible()) { <app-import-wizard (closed)="onClosed()" /> }`; the user uploads inside step 1.
2. **Global drop** — a shared drop target fires a store file-drop event; a host `effect()` calls the API to categorize the file, sets `pendingImportFile` + `importVisible`; the wizard's `initialFile` effect auto-ingests and jumps straight to review (step 2). See the store-event variant in [`angular-file-dropzone`](angular-file-dropzone.md).

## Pitfalls

- **Don't parse the file in the browser.** No xlsx/pdf/csv lib on the client — the API owns extraction so the AI/OCR and column-mapping logic live in one place.
- **Draft lives in the store, not the component** — otherwise the assistant step and the review step fight over two copies.
- **Guard the auto-ingest effect** with a `handledInitial` reference + `ingested` flag, or a re-render re-uploads the same file.
- **Zero ids on commit** server-side (`EMPTY_GUID` → insert); the client just posts the reviewed draft.
- **`applyDraftPatch` must be immutable** (`{ ...d, ...patch }`, `Rows.map(...)`) so OnPush + signals see the change.
- **The review step's entity selects need the resources loaded — resolve them on the host route.** The Objekt/Produkt pickers on step 2 read AppStore resource lists (`store.houseKeyValues` / `productKeyValues`, backed by `withResources`). Those are empty until `ResourcesService.loadAllResources()` runs, which only happens on a fresh login warm-up or via the `allResourcesResolver` wired onto the `planning`/`timesheet` route trees. If the wizard's host route (e.g. `/tasks/new` in `tasks.routes.ts`) does **not** wire `resolve: { resolved: allResourcesResolver }`, the `ux-filter-select` correctly renders **"No results"** — the picker isn't broken, its input array is just empty. Because it depends on whether the user already visited a resource-loading route, the bug reads as *intermittent* ("again the filter is broken with no data"). Fix: add the resolver to the route (see [`angular-routing`](angular-routing.md) → Resolvers).

## Checklist

- [ ] Standalone `OnPush`; `step = signal<1|2|3>()`; pill rail via `@for`, bodies via `@if`.
- [ ] All import data in the AppStore slice; component holds only view state.
- [ ] Three `effect()`s: auto-ingest-once, draft→advance, saved-id→close.
- [ ] Review step reuses existing edit form/table bound to `draft().Rows`; edits via `applyDraftPatch`.
- [ ] Optional assist step merges returned `PatchJson`.
- [ ] Both entry paths wired (explicit button + global drop).
- [ ] Vitest: draft advances the step, patch is immutable, commit emits `closed` on saved id.

## Related

- [`angular-file-dropzone`](angular-file-dropzone.md) — the step-1 upload control.
- [`angular-signal-store-design`](angular-signal-store-design.md) / [`angular-http`](angular-http.md) — store slice + `rxMethod`/`FormData`.
- `dotnet-conventions` → [`file-import-ingest`](../../dotnet-conventions/references/file-import-ingest.md) — the server ingest/AI/commit side.
- `docs/ai-automations/readme.md` — where these wizards plug into the app's automations.
