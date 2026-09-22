# Angular Grid Drag-and-Drop (Pointer Events, No CDK)

A project-agnostic pattern for dragging cards onto grid cells (e.g. a day × time
schedule) and for reordering list rows, using only native **Pointer Events** —
no `@angular/cdk/drag-drop`, no `Renderer2`, no document-level listeners beyond
pointer capture. Use it when a repo does not carry `@angular/cdk` and needs
drag-and-drop for exactly one or two surfaces, where adding a 200KB+ dependency
for one directive isn't worth it.

> **Source note.** This reference distills the *architecture* of bauer-sport's
> schedule/staffing grids (`src/admin.citythong.at/src/app/schedule/`,
> `.../staffing/`) — signals-based drag state, `document.elementsFromPoint()` +
> `data-*` attributes to resolve the drop target, and hand-rolled auto-scroll.
> That source, however, delegates pointer capture and the drag gesture itself
> to `@angular/cdk/drag-drop`'s `CdkDrag` directive (used only in free-drag
> mode, without `CdkDropList`) — it does not call `pointerdown`/`pointermove`
> directly. Since `@angular/cdk` is **not** installed in this repo
> (`src/ui/package.json` has no `@angular/cdk` entry), the TS shape below
> reimplements `CdkDrag`'s pointer-capture mechanics with raw Pointer Events so
> the same architecture is available with zero added dependency. Reordering
> follows bauer-sport's `gallery-image-manager.ts`, which uses the **native
> HTML5 Drag and Drop API** (`dragstart`/`dragover`/`drop`, `DragEvent` +
> `dataTransfer`) rather than Pointer Events — noted as an alternative below.

## Design decisions

| Concern | Decision | Why |
| --- | --- | --- |
| Drag gesture | Pointer Events (`pointerdown`/`pointermove`/`pointerup`/`pointercancel`) + `setPointerCapture` on the source element | One unified event model for mouse, touch, and pen; no separate `touchstart`/`mousedown` handling |
| Click vs. drag | A movement threshold (~6px) or a touch-only `dragStartDelay` gates when a drag "engages" | A tap must still fire `click` to open/edit; only a real drag should suppress it |
| Drop-target lookup | Container resolves `document.elementsFromPoint(x, y)` on every `pointermove`, then reads `data-*` attributes off the first matching element | A schedule grid has dozens–hundreds of cells; one container-level lookup beats binding `(pointerenter)` to every cell, and stays correct even when overlay cards sit on top of cells |
| Overlay passthrough | Absolutely-positioned card wrappers get `pointer-events: none`; only the card itself is `pointer-events: all` | `elementsFromPoint` skips `pointer-events: none` elements during hit-testing, so the lookup falls through wrapper anchors straight to the grid cell underneath |
| Disabled sources | A `disabled` input short-circuits the `pointerdown` handler before any drag state is touched | A truly disabled item should never emit `dragStarted`, not just look disabled |
| Invalid targets | The resolved cell carries its own `blocked`/`occupied` flag; the container renders a distinct "not-allowed" highlight and refuses to persist on drop | One `dragOverCell` signal isn't enough once some cells are droppable and others aren't — validity must travel with the resolved target |
| Reordering | Rewrite an `{id, order}[]` array locally (optimistic), then persist the whole array to the backend | Matches how a sortable list is usually stored — a `SortOrder`/`order` column per row |
| State | `signal()` per concern (`draggedItem`, `dragOverCell`, `isDragging`) on `OnPush` components — no `BehaviorSubject`, no manual change detection | Signal reads in the template auto-invalidate the view; consistent with the rest of the app |

## Essential TS shape

### Draggable source (`draggable-item.ts`)

```typescript
import {
  Component,
  ChangeDetectionStrategy,
  input,
  output,
  signal,
} from '@angular/core';

export interface DragPoint {
  x: number;
  y: number;
}

const DRAG_THRESHOLD_PX = 6;
const TOUCH_START_DELAY_MS = 160;

@Component({
  selector: 'app-draggable-item',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './draggable-item.html',
  styleUrl: './draggable-item.css',
  host: {
    '[class.is-dragging]': 'isDragging()',
    '[class.is-disabled]': 'disabled()',
    '[attr.data-item-id]': 'itemId()',
    '(pointerdown)': 'onPointerDown($event)',
    '(pointermove)': 'onPointerMove($event)',
    '(pointerup)': 'onPointerUp($event)',
    '(pointercancel)': 'onPointerCancel($event)',
    '(click)': 'onClick()',
    'style.touch-action': "'none'",
  },
})
export class DraggableItem {
  readonly itemId = input.required<number>();
  readonly disabled = input(false);
  readonly disabledReason = input<string | null>(null);

  readonly edit = output<number>();
  readonly dragStarted = output<number>();
  readonly dragMoved = output<DragPoint>();
  readonly dragDropped = output<DragPoint>();

  protected readonly isDragging = signal(false);

  private pointerId: number | null = null;
  private startPoint: DragPoint | null = null;
  private suppressClick = false;

  protected onPointerDown(event: PointerEvent): void {
    if (this.disabled()) return;
    this.pointerId = event.pointerId;
    this.startPoint = { x: event.clientX, y: event.clientY };
    this.suppressClick = false;
    (event.target as HTMLElement).setPointerCapture(event.pointerId);
  }

  protected onPointerMove(event: PointerEvent): void {
    if (this.pointerId !== event.pointerId || !this.startPoint) return;
    const point: DragPoint = { x: event.clientX, y: event.clientY };

    if (!this.isDragging()) {
      const dx = point.x - this.startPoint.x;
      const dy = point.y - this.startPoint.y;
      if (Math.hypot(dx, dy) < DRAG_THRESHOLD_PX) return;
      this.isDragging.set(true);
      this.suppressClick = true;
      this.dragStarted.emit(this.itemId());
    }

    event.preventDefault();
    this.dragMoved.emit(point);
  }

  protected onPointerUp(event: PointerEvent): void {
    if (this.pointerId !== event.pointerId) return;
    if (this.isDragging()) {
      this.dragDropped.emit({ x: event.clientX, y: event.clientY });
    }
    this.resetPointer(event.pointerId);
  }

  protected onPointerCancel(event: PointerEvent): void {
    if (this.pointerId !== event.pointerId) return;
    this.resetPointer(event.pointerId);
  }

  protected onClick(): void {
    if (this.suppressClick || this.disabled()) return;
    this.edit.emit(this.itemId());
  }

  private resetPointer(pointerId: number): void {
    this.isDragging.set(false);
    this.pointerId = null;
    this.startPoint = null;
  }
}
```

`dragStartDelay`-style touch behavior (press-and-hold before a drag engages, so
a swipe still scrolls) can be layered on top of this: start a
`setTimeout(TOUCH_START_DELAY_MS)` in `onPointerDown` for `event.pointerType ===
'touch'` that arms a `touchArmed` flag; gate `isDragging.set(true)` in
`onPointerMove` on that flag being set (immediately `true` for
`event.pointerType === 'mouse'`).

### Drop-target container (`drag-grid.ts`)

```typescript
import {
  Component,
  ChangeDetectionStrategy,
  ElementRef,
  computed,
  signal,
  viewChild,
} from '@angular/core';
import { DraggableItem, type DragPoint } from './draggable-item/draggable-item';

interface CellId {
  row: number;
  col: string;
  blocked: boolean;
}

@Component({
  selector: 'app-drag-grid',
  imports: [DraggableItem],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './drag-grid.html',
  styleUrl: './drag-grid.css',
})
export class DragGrid {
  private static readonly EDGE_PX = 64;
  private static readonly SCROLL_STEP_PX = 14;

  protected readonly draggedItemId = signal<number | null>(null);
  protected readonly dragOverCell = signal<CellId | null>(null);
  protected readonly isDragging = signal(false);

  private readonly gridWrapper = viewChild<ElementRef<HTMLElement>>('gridWrapper');

  protected readonly dragOverValid = computed(() => {
    const cell = this.dragOverCell();
    return cell !== null && !cell.blocked;
  });

  protected onDragStarted(itemId: number): void {
    this.draggedItemId.set(itemId);
    this.isDragging.set(true);
  }

  protected onDragMoved(point: DragPoint): void {
    this.dragOverCell.set(this.cellAtPoint(point));
    this.autoScroll(point);
  }

  protected onDragDropped(point: DragPoint): void {
    const itemId = this.draggedItemId();
    const cell = this.cellAtPoint(point) ?? this.dragOverCell();
    this.dragOverCell.set(null);
    this.draggedItemId.set(null);
    this.isDragging.set(false);
    if (itemId === null || cell === null || cell.blocked) return;
    this.moveItem(itemId, cell);
  }

  private moveItem(itemId: number, cell: CellId): void {
    // Persist to the backend / store here (optimistic update).
  }

  /** pointer-events:none on card overlay wrappers lets this fall through to the cell. */
  private cellAtPoint(point: DragPoint): CellId | null {
    const el = document
      .elementsFromPoint(point.x, point.y)
      .find(
        (node): node is HTMLElement =>
          node instanceof HTMLElement && node.dataset['col'] != null,
      );
    if (!el) return null;
    const row = Number(el.dataset['row']);
    const col = el.dataset['col'] ?? '';
    if (!Number.isFinite(row) || !col) return null;
    return { row, col, blocked: el.dataset['blocked'] === 'true' };
  }

  private autoScroll(point: DragPoint): void {
    const wrapper = this.gridWrapper()?.nativeElement;
    if (!wrapper) return;
    const rect = wrapper.getBoundingClientRect();
    if (point.y < rect.top + DragGrid.EDGE_PX) {
      wrapper.scrollTop -= DragGrid.SCROLL_STEP_PX;
    } else if (point.y > rect.bottom - DragGrid.EDGE_PX) {
      wrapper.scrollTop += DragGrid.SCROLL_STEP_PX;
    }
  }

  protected isCellDragOver(row: number, col: string): boolean {
    const cell = this.dragOverCell();
    return cell?.row === row && cell?.col === col && !cell.blocked;
  }

  protected isCellDragOverInvalid(row: number, col: string): boolean {
    const cell = this.dragOverCell();
    return cell?.row === row && cell?.col === col && cell.blocked;
  }
}
```

## Template

```html
<div class="drag-grid-wrapper no-scrollbar" #gridWrapper>
  <div class="drag-grid" [class.drag-grid--dragging]="isDragging()">
    @for (row of rows; track row) {
      @for (col of cols; track col) {
        <div
          class="drag-grid__cell"
          [class.drag-grid__cell--drag-over]="isCellDragOver(row, col)"
          [class.drag-grid__cell--drag-over-invalid]="isCellDragOverInvalid(row, col)"
          [attr.data-row]="row"
          [attr.data-col]="col"
          [attr.data-blocked]="isCellOccupied(row, col)"
        ></div>
      }
    }

    @for (item of items(); track item.id) {
      <div class="drag-grid__anchor" [style.top]="anchorTop(item)">
        <app-draggable-item
          [itemId]="item.id"
          [disabled]="item.locked"
          [disabledReason]="item.locked ? 'Gesperrt durch Admin' : null"
          (edit)="openEdit($event)"
          (dragStarted)="onDragStarted($event)"
          (dragMoved)="onDragMoved($event)"
          (dragDropped)="onDragDropped($event)"
        />
      </div>
    }
  </div>
</div>
```

`data-row`/`data-col` identify the cell; `data-blocked` lets `cellAtPoint()`
read occupancy straight off the DOM without a second lookup into component
state. The anchor wrapper (`drag-grid__anchor`) must be `pointer-events: none`
in CSS — only `app-draggable-item` re-enables `pointer-events: all` — so
`elementsFromPoint` passes through it to the cell beneath.

## SCSS

```css
.drag-grid__cell {
  cursor: cell;
  transition: background 0.1s;
}

.drag-grid--dragging .drag-grid__cell {
  cursor: copy;
}

.drag-grid__cell--drag-over {
  background: color-mix(in srgb, var(--color-brand) 16%, transparent);
  box-shadow: inset 0 0 0 2px color-mix(in srgb, var(--color-brand) 70%, transparent);
}

.drag-grid__cell--drag-over-invalid {
  background: color-mix(in srgb, var(--color-danger) 14%, transparent);
  box-shadow: inset 0 0 0 2px color-mix(in srgb, var(--color-danger) 60%, transparent);
  cursor: not-allowed;
}

.drag-grid__anchor {
  position: absolute;
  pointer-events: none;
}

.drag-grid__anchor app-draggable-item {
  pointer-events: all;
  display: block;
}

app-draggable-item.is-dragging {
  opacity: 0.6;
  z-index: 3;
}

app-draggable-item.is-disabled {
  cursor: not-allowed;
  opacity: 0.55;
}
```

Colors above use this repo's tokens (`--color-brand` gold, `--color-danger`);
swap in the host design system's accent/danger tokens when reusing the
pattern elsewhere.

## Disabled and not-allowed, end to end

| State | Source behavior | Target behavior |
| --- | --- | --- |
| Disabled item | `disabled()` input short-circuits `onPointerDown` before `pointerId`/`startPoint` are set — no drag can start | n/a |
| Disabled item, visual | `.is-disabled` host class sets `cursor: not-allowed`, dimmed opacity; `disabledReason` renders as `title`/tooltip | n/a |
| Occupied/blocked cell | n/a | `data-blocked="true"` flows into `cellAtPoint()`'s `blocked` flag; `dragOverCell` still resolves the cell (for the red highlight) but `onDragDropped` refuses to call `moveItem()` when `cell.blocked` is true |
| Occupied cell, visual | n/a | `drag-grid__cell--drag-over-invalid` (red ring) instead of `--drag-over` (gold ring); container cursor becomes `not-allowed` while hovering a blocked cell |

## Reordering a list

Rewrite the array locally, then persist the whole order:

```typescript
protected onReorder(draggedId: number, targetId: number | null): void {
  const current = [...this.items()];
  const dragged = current.find((i) => i.id === draggedId);
  if (!dragged) return;

  const withoutDragged = current.filter((i) => i.id !== draggedId);
  const insertIdx =
    targetId === null
      ? withoutDragged.length
      : Math.max(0, withoutDragged.findIndex((i) => i.id === targetId));
  withoutDragged.splice(insertIdx, 0, dragged);

  const ordered = withoutDragged.map((item, index) => ({ id: item.id, order: index }));
  this.items.set(withoutDragged); // optimistic local update
  this.store.reorderItems({ items: ordered }); // persist to the backend
}
```

`onReorder` can be wired to the same Pointer Events source/container pair
above (resolve the target row instead of a grid cell), or to plain
**HTML5 Drag and Drop** (`draggable="true"` + `(dragstart)`/`(dragover)`/
`(drop)`/`(dragend)`, tracking source/target ids and calling
`event.preventDefault()` in `dragover`) — the native API is simpler when the
only requirement is reordering siblings in one list, with no free 2D movement
and no custom grid-cell resolver needed.

**The reorder payload is idempotent, not self-inverting.** Persisting
`{id, order}[]` with *absolute* target indices means re-sending the same payload
sets the same indices again — it does **not** undo a previous move. To revert,
send the inverse mapping (or swap the two rows' current indices once); never
re-apply the same payload expecting it to toggle back.

### Reorder affordances — indicate *where* it lands

Reordering needs *more* drop feedback than a cell-move, not less: a cell-move
highlights the target cell, but a reorder must show the **insertion position**.
Three affordances, all proven necessary in practice — a reorder with only a
`cursor: grab` handle reads to users as "nothing is happening":

- **Grip handle at rest.** Put a visible drag-grip glyph (six-dot ⠿) on the
  handle so it reads as draggable — `cursor: grab` is discovered only on hover.
  With no icon library, an inline six-dot SVG works; mute it at rest, brighten
  on hover/focus/dragging. Hide it on the non-draggable (empty/placeholder) row.
- **Insertion-line indicator.** Render a thin accent-colored bar at the boundary
  where the row will land — not a full-row outline. Derive the edge from
  source-vs-target index: hovering a row *above* the dragged one means "insert
  before it" (top edge); *below* means "insert after it" (bottom edge), because
  an index-rewrite reorder drops the strip exactly at the target's position.
  Drive it from a `dragOverIndex` **signal** (a plain field never re-renders the
  view) and clear it on drop **and** `pointercancel`.
- **Whole-row dragging state.** Apply the dragging class to the *entire* row, not
  just the handle cell, so the whole strip visibly lifts (opacity + shadow).
  Dimming only the small handle looks like a rendering glitch.

### The handle element decides whether HTML5 drag works at all

`draggable="true"` on a `<button>` (or any form control) **does not start a drag
in Chrome**. The control swallows the drag gesture at `mousedown`, so
`dragstart` never fires from real mouse input and the feature is simply dead —
no console error, no warning, correct-looking markup.

```html
<!-- dead: Chrome never fires dragstart from a form control -->
<button type="button" class="grip" draggable="true" (dragstart)="onDragStart($event, i)">…</button>

<!-- works: non-form element, keyboard-accessible by hand -->
<span class="grip" draggable="true" role="button" tabindex="0"
      (dragstart)="onDragStart($event, i)" (dragend)="endDrag()"
      (keydown)="onHandleKeydown($event, i)">…</span>
```

The `role="button"` + `tabindex="0"` pair is not optional: the moment you stop
using `<button>` you own focusability, the accessible role, and the keyboard
path (arrow keys that move the item) yourself.

**This bug survives every test you are likely to write.** A synthetic
`element.dispatchEvent(new DragEvent('dragstart', {dataTransfer: new DataTransfer()}))`
fires the handler regardless of the element type, so Vitest specs, a
`chrome-devtools` `evaluate_script` probe, and a scripted end-to-end drag all
report success against a `<button>` handle that no user can drag. Synthetic
DragEvents prove the *handlers* are wired; they say nothing about whether the
browser will *originate* a drag. Verify origination by element type
(`grip.tagName !== 'BUTTON'`), or by dragging it by hand once.

### Gate reordering behind an explicit edit mode

On a read-first surface (a dashboard, a report, a card wall) permanent grip
handles add clutter and invite accidental reorders. Put the whole affordance
behind an edit toggle:

- An icon toggle (pencil) on the page, `aria-pressed` bound to the mode.
- Mode lives in the page component as `signal(false)`; the grid takes it as
  `readonly editMode = input(false)`.
- `@if (editMode())` around **each grip**, so no handle exists at rest.
- A command bar rendered only in edit mode, `role="toolbar"`, carrying the
  reorder hint plus the mode's commands ("Reset the order", disabled until a
  custom order exists). `position: sticky` keeps it reachable down a long page.
- Guard `onDragStart` on `editMode()` as well. Rendering is the affordance;
  the guard is the rule, and only the guard survives a stale DOM node.

Persist the order (localStorage keyed by id, or the backend) and make the reset
a command in that bar — a reorder that silently resets on reload reads as a bug,
and one with no way back traps the user.

## Testing (Vitest, behavior-level)

`jsdom` does not implement real hit-testing, so stub
`document.elementsFromPoint` rather than dispatching genuine `PointerEvent`s
into the DOM and expecting geometry to resolve:

```typescript
import { vi, describe, it, expect, beforeEach } from 'vitest';

describe('DragGrid', () => {
  beforeEach(() => {
    vi.stubGlobal('document', {
      ...document,
      elementsFromPoint: vi.fn(),
    });
  });

  it('does not resolve a cell when elementsFromPoint has no data-col element', () => {
    (document.elementsFromPoint as ReturnType<typeof vi.fn>).mockReturnValue([
      document.createElement('div'),
    ]);
    // call the component's onDragMoved / private cellAtPoint via the public
    // dragOverCell signal and assert it stays null
  });

  it('resolves row/col and blocked from a matching data-* element', () => {
    const cell = document.createElement('div');
    cell.dataset['row'] = '2';
    cell.dataset['col'] = 'wed';
    cell.dataset['blocked'] = 'true';
    (document.elementsFromPoint as ReturnType<typeof vi.fn>).mockReturnValue([cell]);
    // assert dragOverCell() === { row: 2, col: 'wed', blocked: true }
  });

  it('refuses to persist a drop onto a blocked cell', () => {
    // seed dragOverCell with blocked: true, call onDragDropped, assert the
    // store/persist method was never called
  });

  it('a disabled item never emits dragStarted', () => {
    // set disabled = true, simulate a pointerdown + pointermove past the
    // threshold, assert dragStarted was not emitted
  });

  it('a click below the movement threshold still emits edit', () => {
    // pointerdown then pointerup at the same coordinates; assert edit fires
    // and dragStarted does not
  });
});
```

Follow `angular-testing` conventions when extending — assert on emitted
outputs and public signals, not on internal event wiring.

## Gotchas

- **`pointer-events: none` on overlay wrappers is what makes `elementsFromPoint`
  work at all.** Without it, the dragged item's own absolutely-positioned
  anchor (or a sibling card) intercepts the hit-test and the resolver never
  reaches the grid cell underneath.
- **Release pointer capture on `pointercancel`, not just `pointerup`.** Browsers
  fire `pointercancel` on alt-tab, an incoming notification, or a scroll
  gesture take-over; skipping it leaves `isDragging` stuck `true` and the
  ghost styling stuck on.
- **Call `setPointerCapture` on the element that received `pointerdown`,
  never on the container** — otherwise move/up events stop arriving once the
  pointer leaves the source element's original bounds.
- **Keep the touch start delay off for mouse** (`0`) — a nonzero delay on
  desktop makes dragging feel laggy; only touch needs the press-and-hold
  window to disambiguate a drag from a scroll.
- **A single `dragOverCell` signal isn't enough once "not-allowed" targets
  exist** — resolve validity as part of the cell (`{ ...cell, blocked }`), or a
  blocked cell will show the same gold highlight as a valid one.
- **Don't wire `(pointerenter)`/`(dragenter)` per cell in a large grid.** One
  container-level `elementsFromPoint` call scales regardless of grid size and
  keeps working when cards visually overlap cells.
- **`document.elementsFromPoint` is unavailable in `jsdom`.** Stub it directly
  in tests (see above) rather than trying to dispatch real `PointerEvent`s and
  expecting the browser's layout engine to resolve targets — `jsdom` has none.
- **A disabled source must short-circuit at `pointerdown`, not just hide a CSS
  affordance** — otherwise a fast flick can still start a drag before any
  `disabled` check runs later in the handler chain.
- **An insertion line drawn on an item that clips its own overflow is invisible,
  and the class is applied correctly the whole time.** A card with
  `overflow: hidden` (usually there to round an inner image/rail against the
  card's `border-radius`) clips its own `::before`, so a bar positioned in the
  gutter (`left: -18px`) never paints, and a bar at `left: 0` paints *on top of*
  the card's own artwork where it reads as decoration rather than an insertion
  point. Fix by moving the clip inward: drop `overflow: hidden` from the card and
  give the inner element that actually needed it its own matching radius
  (`border-radius: 7px 0 0 7px` on a left rail). Verify with
  `getComputedStyle(card).overflow === 'visible'` plus a screenshot, not the
  class list — `classList` shows `--drop-before` either way.
- **A "slot taken?" check keys on the (row, position), not the entity.** When one
  entity can occupy multiple rows/strips (e.g. the same employee across several
  schedule rows), the occupancy test — the client's blocked-cell highlight AND
  the server's drop rejection — must key on the *slot* (`row + column/date`),
  never on `(entity, date)`. Keying on the entity wrongly blocks a valid move
  because that entity has an unrelated assignment elsewhere the same day. **The
  server must mirror the client's per-cell occupancy rule**, not a coarser one —
  enforce validity server-side, don't trust the client gate alone.
- **`document.elementsFromPoint` returns `[]` for points outside the visible
  viewport** — including cells scrolled out of a horizontally/vertically clipped
  grid. A drop over an off-screen target silently no-ops (the drag *starts*, the
  drop resolves to nothing). Rely on the edge auto-scroll to bring targets on
  screen; when scripting a synthetic drag to verify, assert the target center is
  within `innerWidth`/`innerHeight` first — an off-viewport target reads as a
  product bug when it's a harness artifact.
- **No droppable targets rendered at all = drag looks completely broken, and no
  amount of fixing the drag *handlers* helps.** When a grid/board only renders
  drop cells for entities that already have data (a data-gated `@for` swimlane
  loop that hits its `@empty` branch when the entity set is empty), a zero-data
  state renders **zero `data-*` targets** — `elementsFromPoint` finds nothing on
  every `pointermove`, so every drop no-ops and the pointer handlers (which are
  fine) appear dead. **Before touching the drag gesture, confirm droppable
  targets actually exist in the DOM** (not the empty state). Fix the empty case
  with an *always-present* drop surface — e.g. a persistent "new assignment"
  row/column that carries the `data-*` keys regardless of whether any entity has
  data yet. And when a drop resolves a *slot* (row/date) but not the owning
  *entity* (no lane was targeted), **prompt for the entity** (an inline picker)
  rather than silently no-op'ing — a drop that can't infer the assignee should
  ask, not do nothing. (Bico plan-board `mode="confirmed"`: an empty week
  rendered no employee lanes → nothing to drop onto; the fix added a "Neue
  Zuteilung" day-cell row plus an employee-picker dialog on a lane-less drop.)
- **Zoneless apps flush signal updates asynchronously.** After dispatching
  synthetic pointer events (browser/e2e verification), `await` an animation frame
  before reading signal-driven classes/badges (`.is-dragging`, the not-allowed
  reason) — a synchronous read misses the not-yet-rendered change.
- **`setPointerCapture` throws for a synthetic `pointerId` with no active
  pointer.** Harmless in real usage (a real `pointerdown` has an active pointer);
  it only bites when scripting `PointerEvent`s — and the state set before that
  line still applies, so the drag proceeds regardless.
- **Angular `HttpClient` with `provideHttpClient(withFetch())` issues `fetch`,
  not `XMLHttpRequest`.** To confirm a drop persisted, hook `window.fetch` (or
  watch the network panel) — an `XMLHttpRequest.prototype` spy sees nothing.

## Suggested home / reference implementation

This pattern is implemented end-to-end in the bico maintenance-planner scheduler
— `src/ui/src/app/planning/schedule/scheduler/`: `scheduler.component` is the
container / target resolver, `scheduler-cell` is the draggable source with
notified/not-allowed gating, and `scheduler-label-cell` is the row-reorder
handle (grip glyph + insertion-line indicator). Use it as the worked example:
cell-move + row-reorder + disabled/not-allowed sources + server-side occupancy
mirroring, with Vitest specs alongside each component. For any new standalone
extraction, follow the `ux-splitter` folder convention (see
`angular-draggable-splitter.md`) — one folder per component, `*.spec.ts`
alongside each.
