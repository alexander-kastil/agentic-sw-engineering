# Angular File Drop Zone

A reusable, standalone **file drop zone** for the maintenance-planner UI (`src/ui`) — the entry control for every AI file-ingest automation (home chat, automations page, reservation attachments). Pattern distilled from `vouchers-ai/src/vouchers-ui` (`shared/file-upload/`) and adapted to this repo's Angular 22 + `@ngrx/signals` AppStore + bico-brand stack.

## When to use

- Adding a "drag a file here or click to browse" control anywhere in `src/ui`.
- Wiring the home-chat or automations file-drop entry points (see `docs/ai-automations/readme.md`).
- You need drag-and-drop + click-to-browse with keyboard/a11y support and no external library.

## Core principles (why this shape)

1. **The drop target is a `<button>`, not a `<div>`.** You get focus, Enter/Space activation, and `aria-label` for free — no manual `tabindex`/`keydown` wiring.
2. **A hidden `<input type="file" class="sr-only">` is the real picker.** The button's click opens it via `viewChild`.
3. **One `dragging = signal(false)`** drives the active style through `[class.*-active]="dragging()"`. `dragover → true`, `dragleave`/`drop → false`. Every drag handler calls `event.preventDefault()` (without it the browser navigates to the dropped file).
4. **One private `emit(list: FileList | null)`** normalizes both sources (drop's `dataTransfer.files` and input's `input.files`): guard empty → `Array.from` → slice to `[files[0]]` unless `multiple` is set.
5. **Reset `input.value = ''` after selection** so re-picking the *same* file fires `change` again.
6. **The component is store- and HTTP-agnostic.** It emits `output<File[]>()` and nothing else. No type/size validation inside — `accept` only hints the native picker; real validation belongs to the host or the API. The host wires the emitted files to the AppStore.

## Reference implementation

`src/ui/src/app/shared/file-dropzone/file-dropzone.ts`

```ts
import { booleanAttribute, ChangeDetectionStrategy, Component, ElementRef, input, output, signal, viewChild } from '@angular/core';

@Component({
  selector: 'app-file-dropzone',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './file-dropzone.html',
  styleUrl: './file-dropzone.css',
})
export class FileDropzone {
  label = input<string>('');
  accept = input<string>('');                 // e.g. '.xlsx,.pdf,application/pdf'
  multiple = input(false, { transform: booleanAttribute });
  busy = input(false, { transform: booleanAttribute });
  progress = input<number | null>(null);

  filesSelected = output<File[]>();           // the ONLY output — host owns what happens next

  protected dragging = signal(false);
  private fileInput = viewChild.required<ElementRef<HTMLInputElement>>('fileInput');

  open() { this.fileInput().nativeElement.click(); }

  onSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    this.emit(input.files);
    input.value = '';                         // allow re-selecting the same file
  }

  onDragOver(event: DragEvent)  { event.preventDefault(); this.dragging.set(true); }
  onDragLeave(event: DragEvent) { event.preventDefault(); this.dragging.set(false); }
  onDrop(event: DragEvent) {
    event.preventDefault();
    this.dragging.set(false);
    this.emit(event.dataTransfer?.files ?? null);
  }

  private emit(list: FileList | null) {
    if (!list || list.length === 0) return;
    const files = Array.from(list);
    this.filesSelected.emit(this.multiple() ? files : [files[0]]);
  }
}
```

`src/ui/src/app/shared/file-dropzone/file-dropzone.html`

```html
<button type="button" class="dz" [class.dz-active]="dragging()"
  [attr.aria-label]="label() ? label() + ' hochladen' : 'Datei hochladen'"
  (click)="open()"
  (dragover)="onDragOver($event)" (dragleave)="onDragLeave($event)" (drop)="onDrop($event)">
  <span class="mdi mdi-cloud-upload dz-icon" aria-hidden="true"></span>
  @if (label()) { <span class="dz-label">{{ label() }}</span> }
  <span class="dz-hint">Hierher ziehen oder klicken</span>
  @if (busy()) {
    <div class="dz-progress" role="progressbar" [attr.aria-valuenow]="progress() ?? 0">
      <div class="dz-progress-bar" [style.width.%]="progress() ?? 0"></div>
    </div>
  }
</button>
<input #fileInput type="file" class="sr-only"
  [accept]="accept()" [multiple]="multiple()" (change)="onSelect($event)" />
```

`src/ui/src/app/shared/file-dropzone/file-dropzone.css` — use **bico-brand** tokens (charcoal border, mustard-gold on hover/active) rather than the raw hex below; keep the dashed-border + hover-recolor shape:

```css
.dz {
  display: flex; flex-direction: column; align-items: center; gap: .5rem;
  width: 100%; padding: 1.5rem;
  border: 1.5px dashed var(--dz-border, theme(colors.gray.300));
  border-radius: .5rem; background: transparent; cursor: pointer;
  transition: border-color .15s, background .15s, color .15s;
}
.dz:hover  { border-color: var(--dz-accent, theme(colors.amber.500)); color: var(--dz-accent); }
.dz-active { border-color: var(--dz-accent); background: var(--dz-accent-weak, theme(colors.amber.50)); color: var(--dz-accent); }
.dz-progress { width: 100%; height: 4px; background: rgb(0 0 0 / .08); border-radius: 2px; overflow: hidden; }
.dz-progress-bar { height: 100%; background: var(--dz-accent); transition: width .2s; }
```

> If the app is fully Tailwind-utility (no component CSS), express the states inline instead: `[class.border-amber-500]="dragging()" [class.bg-amber-50]="dragging()"` on the button, and drop the `.css` file.

## Host wiring (AppStore, this repo)

The host feature owns the store call. Files flow into the matching `@ngrx/signals` slice — e.g. an import automation in `withTasks`/a new `withImports` feature:

```ts
@Component({ /* … */ imports: [FileDropzone] })
export class SomeAutomationPanel {
  private store = inject(AppStore);

  onFilesSelected(files: File[]) {
    const file = files[0];
    if (!file) return;
    this.store.ingestFile({ file, kind: 'mieterliste' });   // rxMethod on the store — see angular-http / with-tasks
  }
}
```

```html
<app-file-dropzone
  label="Mieterliste (Excel oder PDF)"
  accept=".xlsx,.pdf,application/pdf"
  [busy]="store.isBusy()"
  (filesSelected)="onFilesSelected($event)" />
```

### Store-event variant (shared/global drop target)

For a drop zone that lives in a shared shell (e.g. a global sidebar or the home shell) and must route to whichever feature is active, don't use a local `output` — fire a **store event** instead and let features react in an `effect()`:

```ts
// in the drop handler
onDrop(e: DragEvent) {
  e.preventDefault(); this.dragging.set(false);
  const files = Array.from(e.dataTransfer?.files ?? []);
  if (files.length) this.store.fireFileDrop({ files });     // { seq, files } event on the store
}
```

```ts
// in the active feature
constructor() {
  effect(() => {
    const evt = this.store.fileDropEvent();
    if (!evt || evt.seq === this.lastSeq) return;
    this.lastSeq = evt.seq;
    this.categorizeAndRoute(evt.files[0]);   // e.g. API /documents/categorize → open the right wizard
  });
}
```

## Checklist

- [ ] Standalone, `OnPush`, signal inputs/outputs (no decorators).
- [ ] Drop target is a `<button>`; picker is a hidden `sr-only <input type="file">`.
- [ ] `preventDefault()` on `dragover`/`dragleave`/`drop`.
- [ ] Single `emit()` normalizes `dataTransfer.files` and `input.files`; `input.value=''` reset.
- [ ] `multiple` gate slices to `[files[0]]` when off.
- [ ] No store/HTTP/validation coupling inside the component — host wires `filesSelected` to the AppStore.
- [ ] Styling via bico-brand tokens; active state is a `[class.*-active]="dragging()"` binding.
- [ ] Vitest: assert `filesSelected` emits on drop and on change, respects `multiple`, and toggles `dragging`.

## Related

- [`file-import-wiz`](file-import-wiz.md) — the multi-step wizard the drop zone feeds.
- [`angular-http`](angular-http.md) — `rxMethod` + `FormData` upload to the API.
- [`angular-signal-store-design`](angular-signal-store-design.md) — where ingest state lives.
- `bico-brand` skill — the mustard-gold + charcoal tokens for the zone styling.
