# Angular Table Column Resize

User-draggable column widths for a data table, persisted per user. Standalone
Angular 22, signals, `OnPush`, no CDK and no third-party grid.

Read `angular-table-column-layout.md` first. Resizing only makes sense on a table
that is already `table-fixed` with a stable geometry, and the auto-fill rule below
is what keeps resizing from breaking that stability.

## The handle

A small attribute directive on a `<span>` inside each resizable `<th>`, using
Pointer Events plus `setPointerCapture` (same mechanism as
`angular-draggable-splitter.md`: no document-level listeners, no `Renderer2`,
no manual add/removeEventListener).

Non-obvious requirements, each of which is a real bug if missed:

- **The drag must not trigger the column's sort.** Sort headers are click
  activated, and a drag ends in a click. Track whether the pointer actually moved
  (a small threshold, a couple of px, so a jittery click still counts as a click),
  and on the trailing `click` call `preventDefault()`/`stopPropagation()` when it
  moved. Verify by asserting `aria-sort` is unchanged after a drag.
- **Read the drag-start width from the live `<th>`**, via its rendered box, not
  from the bound input value. A flexible column's bound value can be a nominal
  placeholder rather than its real rendered width, and starting from that makes the
  column jump on the first drag. Reading the element is also correct for every
  other column, so there is no reason to special-case it.
- **`touch-action: none`** on the handle so touch drags do not scroll the page.
- **Clamp to a per-column minimum** chosen from real measured content, not guessed
  character counts. Columns that cannot ellipsize (a date, a badge or pill) need a
  minimum that fits their content exactly, because below it they visibly bleed.
  Columns with `truncate` can go much smaller safely.
- **Keyboard**: the handle is focusable, `role="separator"`,
  `aria-orientation="vertical"`, live `aria-valuemin`/`valuemax`/`valuenow`, and
  Left/Right arrows adjust by a step. Label it in the app's UI language.
- **Double-click resets that column** to its default. Keep the defaults in code as
  the single source of truth so a reset is always possible.

## The flexible column, and why it needs an explicit width

The tempting design is to leave one column (the widest free-text one, usually
contact/email) unsized so it soaks up whatever the others leave. It is
overflow-proof by construction, and it is **not collapse-proof**. Measured on a
real admin list view at an 821px CSS viewport with the sidebar expanded, once a
responsive column dropped out:

```
Date 152 | Type 136 | Name 144 | Contact 4 | Actions 80
wrapper clientWidth 525, scrollWidth 525, overflow 0
```

Zero overflow, and the contact column rendered **four pixels wide** with no email
visible at all. The invariant "no horizontal overflow" was satisfied by a
completely broken table. Losing the column's content is worse than the scrollbar
it was avoiding.

Adding `min-width` to the table does not rescue this either. With
`table-layout: fixed`, a `min-width` on a cell is not honoured, and forcing the
table's own box wider leaves the surplus unallocated: the table box grew to the
min-width while the flexible cell still rendered at 36.7px against a 110px
minimum, with the difference sitting as an unclaimed gap.

**What works: compute the flexible column's width in JS and always render it
explicitly.**

```
autoWidth = max(
  thisColumn.minWidth,
  wrapper.clientWidth - sum(width of every OTHER column that is CURRENTLY visible)
)
```

Keep that as a pure function taking a list of visible widths, so it is unit
testable and nothing hardcodes one particular column set. Drive recomputation
from a `ResizeObserver` on the scroll wrapper plus an effect over the persisted
widths and the visibility state. Below the floor the column keeps its minimum, the
row simply becomes wider than the wrapper, and the existing `overflow-x-auto`
scrolls. That is the same "explicit widths outgrow the container" path a manual
resize already relies on, so there is one behaviour, not two.

The invariant, which supersedes the weaker one in `angular-table-column-layout.md`:

> Zero horizontal overflow in the default state, **and** every visible column at
> or above its legible minimum in **every** reachable state. When those two cannot
> both hold, the scrollbar wins. Never crush a column.

## Persistence

Per-user UI preference: a `signalStoreFeature` slice backed by `localStorage`
under a namespaced key, reads and writes wrapped in `try/catch` so blocked storage
degrades to non-persistent. Not a DB-backed app-settings layer, which is app-wide
config and a different concern.

Two rules that were each learned the hard way:

- **Version the payload**: `{ v: 2, widths: { ... } }`. Discard the whole payload
  on a version mismatch (and on a payload with no version at all). Without this,
  changing a default is a silent no-op for every existing user. This actually
  happened: a stale `{"date":160,"type":158,...}` from a previous build overrode
  every new default and reintroduced a 141px overflow, while the same build
  verified clean in a browser profile that had no key.
- **Store only what the user actually changed.** Do not pre-fill storage with the
  defaults on load. A sparse map means a future defaults change reaches everyone
  who never touched that column, with nothing to migrate, and it makes reset a
  uniform "delete the override" for every column including the flexible one.

Commit widths to storage on drag end, not on every pointermove.

## Verifying

Geometry reads go stale. On this page `getBoundingClientRect` **and**
`offsetWidth` both returned a column at 347px and the wrapper overflowing by 196px
while a screenshot of the same moment showed the table fitting perfectly, with the
column at its correct 157px. Forcing a reflow (writing `scrollLeft`) made the reads
agree with the pixels.

So:

- **A screenshot is the ground truth.** Confirm the visual result first.
- If you need numbers, force a reflow before reading, and prefer a **behavioural**
  test to a geometry read: set `wrapper.scrollLeft = 999`, read it back, and set it
  to 0. A value of 0 proves there is no horizontal overflow; a non-zero value is
  the exact overflow. That cannot go stale the way a measured box can.
- Verify in the **same browser profile the user has**, with the storage keys
  removed. A different profile has different storage and a different window size,
  which is precisely how the two defects above passed an agent's own verification.

Check after any change: drag grows/shrinks and clamps at the minimum, the trailing
click does not sort, dblclick resets, arrows adjust, the width survives a reload,
and the flexible column never renders below its minimum in any visibility
combination.
