# Angular Draggable Splitter

A hand-rolled, reusable **draggable splitter** (resizable two-pane layout: drag a
vertical divider to resize the left/right panes) for standalone Angular 22
(signals + `OnPush`). No third-party library — `@angular/cdk`, `angular-split`,
and `angular-resizable-element` are all unnecessary for a single vertical divider,
and the hand-rolled version is less code with exact px control.

Use this when a fixed `grid-template-columns` split (e.g. `[1fr_16rem]`) should
become user-resizable, with the chosen width persisted across reloads.

## Design decisions (the ones that matter)

- **Resize ONE pane, measure from its own edge.** Pick the pane that resizes
  (usually the right/side pane) and store *its* width as the single source of
  truth. Compute width from the container edge to the pointer:
  `rightWidth = containerRect.right - pointer.clientX`. Anchoring to an edge (not
  a running delta) means no drift and no "grab offset" bookkeeping.
- **State = one `linkedSignal`, not `signal` + manual init.** Seed it lazily from
  `localStorage` (clamped), but keep it freely settable by drag/keyboard
  afterwards. `linkedSignal(() => readInitialWidth())` gives exactly this: a
  computed seed that a `.set()`/`.update()` can override.
- **Drive layout from a CSS var via a host style binding**, not by mutating
  styles imperatively. `host: { '[style.--ux-splitter-right]': 'rightWidthPx()' }`
  keeps it declarative and OnPush-friendly; the SCSS reads `var(--…-right)` in
  `grid-template-columns`.
- **Pointer Events + Pointer Capture on the divider itself** — no
  document-level listeners, no `Renderer2`, no manual add/removeEventListener.
  `setPointerCapture(pointerId)` on `pointerdown` routes every subsequent
  `pointermove`/`pointerup` to the divider even when the pointer leaves it.
- **`touch-action: none`** on the divider so touch drags don't scroll the page.
- **Persist in an `effect`, guarded.** Wrap `window`/`localStorage` access in a
  `typeof window === 'undefined'` check + `try/catch` (quota / disabled storage /
  SSR) so resizing still works when persistence can't.

## Component TS (the essential shape)

```ts
@Component({
  selector: 'ux-splitter',
  templateUrl: './splitter.component.html',
  styleUrl: './splitter.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { '[style.--ux-splitter-right]': 'rightWidthPx()' },
})
export class SplitterComponent {
  private readonly elementRef = inject(ElementRef<HTMLElement>);

  readonly storageKey = input.required<string>();   // one key per usage site
  readonly initial = input(320);
  readonly min = input(200);
  readonly max = input(560);
  readonly step = input(16);                         // px per Arrow key

  // Seeded from localStorage (clamped) yet freely settable by drag/keys.
  protected readonly rightWidth = linkedSignal<number>(() => this.readInitialWidth());
  protected readonly rightWidthPx = computed(() => `${this.rightWidth()}px`);
  protected readonly dragging = signal(false);

  constructor() {
    effect(() => {
      const key = this.storageKey();
      const width = this.rightWidth();
      if (!key || typeof window === 'undefined') return;
      try { window.localStorage.setItem(key, String(width)); } catch { /* storage disabled */ }
    });
  }

  protected onPointerDown(e: PointerEvent): void {
    (e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId);
    this.dragging.set(true);
    e.preventDefault();
  }
  protected onPointerMove(e: PointerEvent): void {
    if (!this.dragging()) return;
    const rect = this.elementRef.nativeElement.getBoundingClientRect();
    this.rightWidth.set(this.clamp(rect.right - e.clientX, this.min(), this.max()));
  }
  protected onPointerUp(e: PointerEvent): void {
    if (!this.dragging()) return;
    this.dragging.set(false);
    const el = e.currentTarget as HTMLElement;
    if (el.hasPointerCapture?.(e.pointerId)) el.releasePointerCapture(e.pointerId);
  }

  protected growRight(): void  { this.rightWidth.update(w => this.clamp(w + this.step(), this.min(), this.max())); }
  protected shrinkRight(): void { this.rightWidth.update(w => this.clamp(w - this.step(), this.min(), this.max())); }

  private readInitialWidth(): number {
    const fallback = this.clamp(this.initial(), this.min(), this.max());
    if (typeof window === 'undefined') return fallback;
    const key = this.storageKey();
    if (!key) return fallback;
    try {
      const raw = window.localStorage.getItem(key);
      if (raw === null) return fallback;
      const n = Number(raw);
      return Number.isFinite(n) ? this.clamp(n, this.min(), this.max()) : fallback;
    } catch { return fallback; }
  }
  private clamp(v: number, min: number, max: number): number { return Math.min(Math.max(v, min), max); }
}
```

## Template — content projection + accessible divider

Project the two panes by attribute selector; the divider is the accessible
`separator`.

```html
<div class="ux-splitter__pane ux-splitter__pane--left">
  <ng-content select="[slot-left]" />
</div>

<div
  class="ux-splitter__divider"
  [class.is-dragging]="dragging()"
  role="separator"
  aria-orientation="vertical"
  aria-label="Resize panels"
  [attr.aria-valuemin]="min()"
  [attr.aria-valuemax]="max()"
  [attr.aria-valuenow]="rightWidth()"
  tabindex="0"
  (pointerdown)="onPointerDown($event)"
  (pointermove)="onPointerMove($event)"
  (pointerup)="onPointerUp($event)"
  (pointercancel)="onPointerUp($event)"
  (keydown.arrowleft)="growRight(); $event.preventDefault()"
  (keydown.arrowright)="shrinkRight(); $event.preventDefault()"
></div>

<div class="ux-splitter__pane ux-splitter__pane--right">
  <ng-content select="[slot-right]" />
</div>
```

**Accessibility (WAI-ARIA `separator` with resize):** `role="separator"` +
`aria-orientation="vertical"` + `tabindex="0"` makes it focusable; keep
`aria-valuemin/max/now` bound to the live signal so screen readers announce the
size; Arrow Left/Right nudge by `step` (note the direction: when the *right* pane
resizes, ArrowLeft grows it). `$event.preventDefault()` stops the arrow keys from
scrolling.

## SCSS — mobile-first, CSS-var-driven grid, grabbable divider

```scss
:host {                       // mobile: stacked column, divider hidden
  display: flex; flex-direction: column;
  min-height: 0; height: 100%; gap: var(--gap-sm);
}
.ux-splitter__pane {
  display: flex; flex-direction: column; min-width: 0; min-height: 0;
  > * { flex: 1 1 auto; min-width: 0; min-height: 0; }   // give projected child a definite height
}
.ux-splitter__divider { display: none; }

@media (min-width: 768px) {   // md+ : 1fr / 6px divider / resizable right col
  :host {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 6px minmax(0, var(--ux-splitter-right, 320px));
    gap: 0;
  }
  .ux-splitter__divider {
    display: block; position: relative; align-self: stretch;
    width: 6px; cursor: col-resize; touch-action: none; border-radius: 3px;
    background: var(--divider-color, #e5e2da);

    &::before { content: ""; position: absolute; inset: 0 -4px; }  // ~14px hit area
    &::after  { content: ""; position: absolute; top: 50%; left: 50%;
                width: 2px; height: 24px; transform: translate(-50%, -50%);
                border-radius: 1px; background: var(--grip-color, #c9c5ba); }  // grip

    &:hover, &.is-dragging, &:focus-visible { background: var(--accent-color, #e7ba43); }
    &:focus-visible { outline: 2px solid var(--accent-color, #e7ba43); outline-offset: 2px; }
    @media (prefers-reduced-motion: no-preference) { transition: background-color .15s ease; }
  }
}
```

Key CSS points:
- **Mobile-first stack, no divider below `md`** — there's nothing to drag on a
  narrow viewport; the panes just stack.
- **`minmax(0, …)` on both flexible tracks** so a pane with long content can
  actually shrink instead of blowing out the grid.
- **Thin 6px visual divider + a ~14px invisible `::before` hit area** — a 6px
  target is too thin to grab reliably.
- **Give the single projected child `flex: 1 1 auto; min-height: 0`** so its own
  internal `overflow-y:auto` scroll regions get a definite height (CSS Grid's
  default `align-items: stretch` gives the pane full row height).
- Swap the `var(--…, fallback)` colors for your design system's hairline / accent
  tokens; light up the divider in the brand accent on hover/drag/focus.

## Host usage

```html
<ux-splitter storageKey="my-view-split" [initial]="416" [min]="320" [max]="640">
  <div slot-left>…primary content…</div>
  <div slot-right>…side panel…</div>
</ux-splitter>
```

- **Unique `storageKey` per usage site** (`home-split`, `edit-split`, …) so pages
  don't share a persisted width.
- Import the standalone component into the host's `imports`.

## Testing (Vitest, behavior-level)

Cover behavior, not pixels — set inputs / simulate keys, assert the width signal
and the ARIA attributes:

- clamps to `min` and `max` (drive `growRight`/`shrinkRight` past the bounds);
- restores a persisted value from `localStorage`, and **clamps an out-of-range
  persisted value** on read;
- persists on change (assert `localStorage.getItem(key)`);
- divider exposes `role="separator"` + `aria-valuemin/max/now`;
- Arrow Left/Right adjust and clamp.

## Changing the stored unit needs a new storage key

The pixel and ratio variants persist under the same kind of key, and a value written by one is a
plausible value for the other: a stored `440` from the px build parses as a finite number, clamps into
a ratio's `[0.25, 0.6]`, and silently opens the pane at the maximum. The layout, the CSS and the
component are all correct while the split is visibly wrong, and only for people who used the earlier
build — which is everyone except a fresh browser.

- Change the key with the unit (`…-split` -> `…-split-ratio`), so an old value is simply absent.
- Validate the parsed value against the new domain, not just `Number.isFinite`: for a ratio, reject
  `parsed <= 0 || parsed >= 1` and fall back to the default.
- Verify a changed default by measuring the rendered panes after clearing the key, never on the
  browser you developed in.

## Gotchas learned in the field

- **A component named `split`/`ux-split` may be a *static* grid, not a splitter.**
  Grep the implementation before reusing — a `grid-template-columns: auto 240px`
  with an empty TS is not draggable. Don't assume the name implies drag.
- **`aria-valuenow` won't update unless bound to the live signal.** If a keyboard/
  drag resize "does nothing" in a snapshot, first check the attribute is
  `[attr.aria-valuenow]="rightWidth()"`, not a static/initial value.
- **When verifying in a browser, a click may only *hover* the divider** (shows the
  focus/hover color) without giving it keyboard focus — a keyboard-resize test can
  read as broken when it's the harness, not the code. Verify the primary
  interaction (pointer drag) directly; it exercises the real
  pointerdown→move→up→capture path.
- Persisted width survives reloads — when done testing, **clear the storage key**
  (or reset to default) so you don't leave a maxed/min width behind for the user.

## Where it's used

| Page | Component | storageKey | initial / min / max (px) | Panes |
| --- | --- | --- | --- | --- |
| `/` (home) | `home/home-chat/home-chat.component` | `home-chat-split` | 256 / 200 / 420 | chat ↔ chat-history `<aside>` (`bg-surface-alt`) |
| `/tasks/new`, `/tasks/:id` | `tasks/edit-task/edit-task.component` | `edit-task-split` | 416 / 320 / 640 | chat ↔ right meta panel |

Both previously used static `grid-template-columns` (`[1fr_16rem]`, `[1fr_26rem]`);
`ux-splitter` replaced only that inner two-column body grid — outer frames,
`bg-ink` header bars, and `h-[calc(100vh-160px)]` height math stay intact.


## API

```html
<ux-splitter storageKey="edit-task-split" [initial]="416" [min]="320" [max]="640">
  <div slot-left> …chat card… </div>
  <div slot-right> …right panel… </div>
</ux-splitter>
```

Inputs: `storageKey` (**required**, unique per usage site), `initial` (320),
`min` (200), `max` (560), `step` (16, px per Arrow key). Import
`SplitterComponent` into the host's `imports`. Content projects two panes by
attribute selector: `[slot-left]` / `[slot-right]`.


## How it works (see the file for full source)

- **Right pane is the resizable one**; its width is the single source of truth,
  measured from the container's right edge to the pointer
  (`rect.right - event.clientX`), so dragging the divider **left grows** the right
  pane. State is a `linkedSignal` seeded (clamped) from `localStorage` yet freely
  settable by drag/keyboard.
- Layout is driven by a **CSS custom property via a host style binding**:
  `host: { '[style.--ux-splitter-right]': 'rightWidthPx()' }`; the SCSS reads
  `var(--ux-splitter-right)` in `grid-template-columns`.
- Drag uses **Pointer Events + `setPointerCapture` on the divider** — no
  document listeners, no `Renderer2`. `touch-action: none` on the divider.
- Persistence is an `effect` writing `localStorage[storageKey]`, guarded for
  missing `window`/`localStorage` (SSR / quota / disabled) so resize still works
  without persistence.
- **Mobile-first:** below `md` (768px) the panes stack in one column and the
  divider is `display:none` — nothing to drag on a narrow viewport (home's aside
  must still stack below the chat, as before).


## Accessibility

`role="separator"`, `aria-orientation="vertical"`, `tabindex="0"`, live
`[attr.aria-valuemin/max/now]="…"`, and `(keydown.arrowleft)="growRight()"` /
`(keydown.arrowright)="shrinkRight()"` (both `preventDefault()`). German aria-label
"Bereichsgröße anpassen".


## Tests

`splitter.component.spec.ts` — behavior-level Vitest: clamps to min/max both
directions, restores from `localStorage`, clamps an out-of-range persisted value,
persists on change, divider ARIA attributes, Arrow keys adjust + clamp. Follow
`angular-testing` conventions when extending.


## Field gotchas

- **Verify the pointer drag, not just keyboard,** in the browser: a click may only
  *hover* the divider (gold shows) without giving it keyboard focus, so a keyboard
  test can read as broken when it's the harness. `aria-valuenow` in a snapshot is
  the reliable read of the current width.
- Persisted width survives reloads — after testing a drag, **clear the storage
  key** (`localStorage.removeItem('edit-task-split')`) so you don't leave a
  maxed/min width behind for the user.

For the full generic pattern (edge-anchored width, `linkedSignal` seed, pointer
capture, CSS-var grid, testing shape), the global copy of this reference carries a
project-agnostic version.

## Ratio-based sibling: `app-ui-split-pane` in media-creator-ui

`src/media-creator-ui/src/app/shared/ui/ui-split-pane.ts` is the same pattern with
one deliberate variant: it stores a **ratio** (`linkedSignal<number>`, clamped to
`[0.3, 0.75]`), not a pixel width, driving `grid-template-columns: minmax(0,
calc(var(--split-ratio, 0.55) * 100%)) auto minmax(0, 1fr)` through a host style
binding, restored from and persisted to `localStorage` under a per-usage
`storageKey` (the Generate page uses `mc.generate.split`). Testids: `split-pane`,
`split-start`, `split-handle`, `split-end`.

Two things an E2E spec against this component (or any host page that composes it
with a container query) needs to account for, found while writing
`e2e/tests/generate-workspace.spec.ts`:

- **A container-query breakpoint on the left pane and a persisted ratio can
  interact across test runs.** The Generate page switches its Chat/Preview tabs
  to an always-both-visible wide layout once the left pane's own inline size
  crosses a `@container` breakpoint, not the viewport width. Since that pane's
  width is `ratio * container width`, a ratio persisted by an earlier drag or
  keyboard resize can widen the left pane past the breakpoint on the very next
  test, silently flipping the layout and making the tabbed UI a spec expects
  disappear. Any spec built on the narrow, tabbed layout should clear the split
  pane's `localStorage` key before its first navigation: an `addInitScript`
  removing the key works well there, since it runs before the app's first read.
  Exactly one spec, the one that exercises drag and keyboard resize itself,
  should be allowed to write the key, and it needs a different mechanism: it
  cannot clear the key via `addInitScript`, because that script reruns on every
  navigation for the lifetime of the page, including the reload the same test
  performs later to check persistence, and it would erase the very ratio that
  reload is meant to observe. Clear it with a one-off `page.evaluate(() =>
  localStorage.removeItem(key))` followed by a single `page.reload()` before
  taking any measurement, instead.
- **Only the persistence side of the ratio's effects lags the input event that
  changed it, not the layout.** The CSS custom property that drives the grid
  track is a host style binding (`[style.--split-ratio]`), so it updates
  synchronously with the `ratio` signal and the rendered width is correct the
  moment change detection runs. The `localStorage` write sits in a separate
  `effect()`, and that one is not synchronous with the triggering event.
  Measured directly: three ArrowRight presses sent back to back can leave
  `localStorage` reflecting only the first press for a couple hundred
  milliseconds before catching up to the last, while the pane's own rendered
  width already matches the third press. A spec that reads `localStorage` right
  after the interaction can observe a stale, in-between value even though the
  DOM is already correct; poll `localStorage` until it stops changing rather
  than trusting a single read. A related race sits one step earlier, at the
  keyboard step itself: a synthetic keydown sent too soon after a `focus()`
  call can land before Chromium's own keyboard focus target has caught up with
  `document.activeElement`, so a short wait between `focus()` and the first
  key press is needed too.

