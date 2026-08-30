# Angular Table Column Layout

Stable column geometry for a data table whose rows are loaded a page at a time
(server-side sort plus infinite scroll). Covers the two failure modes that look
opposite but share one cause: **columns that jump**, and **columns that overflow**.

Use this before adding sorting, filtering, resizing, or column visibility to any
list view. Get the geometry right first; every later feature builds on it.

## The data-table family, in order

These three leaves are meant to be applied in sequence. Each one assumes the
previous is already in place, and later leaves tighten earlier rules.

1. **`angular-table-column-layout`** (this file): pin the geometry so columns stop
   moving. Prerequisite for the other two.
2. **`angular-table-column-resize`**: let the user drag column widths, persist them,
   and stop the flexible column from collapsing. **Supersedes the fit invariant
   stated here** with a stronger one.
3. **`angular-table-column-visibility`**: let the user show and hide columns, which
   changes which columns compete for width, so it must be built on the sizing model
   from leaf 2.

Skipping ahead does not work: resizing on an unpinned table reintroduces the jump,
and visibility on a naive sizing model produces a column crushed to a few pixels.

## The bug: sorting shifts every column sideways

Symptom: click a sort header and the whole table visibly jumps horizontally.
Measured on a real admin list view (six columns, server-side sort, infinite
scroll), sorting by the last text column:

```
column      before   after
Type          420      434
Name          545      576
Contact       680      722
Preferred     912      980
```

Cause: `<table class="w-full">` with no `table-fixed` uses **auto** table layout,
so each column is as wide as its widest loaded cell. Sorting is server-side and
the list is infinite-scroll, so a sort click reloads a *different first page* of
rows. Different rows means a different widest cell means every column recomputes.

The row content changing is correct. The columns moving is not.

This is invisible in dev with 5 seed rows and obvious in production with 80. It
also fires on filter changes, on search, and on the first infinite-scroll append,
so "it only happens when I sort" is usually an under-report.

## Fix, part 1: pin the layout

```html
<table class="w-full table-fixed text-sm">
```

`table-fixed` (CSS `table-layout: fixed`) makes column widths come from the
`<th>` widths and the table width only, never from cell content. Widths are then
computed once from the header row instead of being re-derived per page.

Consequences to handle, not optional:

- Overflow no longer auto-expands a column, so any cell whose content can exceed
  its width needs `truncate` (or an explicit wrap rule). Long emails and free-text
  date fields are the usual offenders. Prefer truncation with the full value still
  reachable through an existing expand-row control over a `title` tooltip.
- Responsive columns (`hidden lg:table-cell`, `hidden xl:table-cell`) keep working:
  a `display: none` column does not participate in the fixed layout at all.

## Fix, part 2: the defaults must fit the container

`table-fixed` alone trades a jump for an overflow. Giving every column an explicit
width and letting the sum exceed the container produces this, measured on the same
page right after the naive fix:

```
container (overflow-x wrapper) clientWidth : 895
table scrollWidth                          : 1036
overflow                                   : 141px
Date 160 | Type 144 | Name 176 | Contact 220 | Preferred 256 | Actions 80
```

The last column (row actions) was pushed entirely outside the visible area behind
a horizontal scrollbar, which is worse for the user than the jump that was fixed.

**The trap to avoid:** CSS2.1 section 17.5.2 says a browser distributes *surplus*
width proportionally when the specified widths sum to **less** than the table
width. That is true, and it is the reason all-explicit widths feel safe. It says
nothing about the deficit case. When the widths sum to **more** than the
container there is nothing to distribute and the table simply overflows. Reasoning
from the surplus rule alone is how the regression above got shipped.

Two workable shapes, both fine:

1. **Leave one column unsized.** Size every column except the widest free-text one
   (contact/email is the natural candidate). It absorbs the remainder, so the sum
   can never exceed the container. Write an explicit width for it only if and when
   the user drags it.
2. **Size all columns, but budget them.** Every column explicit, with the defaults
   chosen so they fit the *narrowest* container in which they are all visible.

Whichever you pick, the invariant is the same and it is what to assert in review:

> In the default, never-resized state the table has **zero horizontal overflow**
> and the last column is **fully visible**.

Verify it at three widths, because the container changes independently of the
viewport:

1. Around 1200 CSS px with the sidebar nav **expanded** (the tightest common case).
2. Same viewport with the nav **collapsed** (wider container, same columns).
3. At `xl` and above, where an `xl:table-cell` column appears and needs its own budget.

## Verifying it, not assuming it

A green build proves nothing here; this is a pure layout property. Measure it:

```js
const t = document.querySelector('table');
const wrap = t.closest('[class*="overflow-x"]') || t.parentElement;
({
  clientWidth: wrap.clientWidth,
  scrollWidth: wrap.scrollWidth,
  overflow: wrap.scrollWidth - wrap.clientWidth,   // must be 0
  columns: [...t.querySelectorAll('thead th')]
    .filter(th => getComputedStyle(th).display !== 'none')
    .map(th => [th.innerText.trim().split('\n')[0], Math.round(th.getBoundingClientRect().width)])
})
```

For the jump itself, capture the header x-positions, sort, capture again, and
require them to be identical. Screenshots are the ground truth; treat a numeric
read as a cross-check, not as the proof.

Regression checklist for any column-geometry change:

- [ ] Sort by every sortable column: header x-positions unchanged.
- [ ] Switch every filter value: header x-positions unchanged.
- [ ] Scroll far enough to append a page: header x-positions unchanged.
- [ ] Default state: `scrollWidth === clientWidth`, last column fully visible.
- [ ] Narrowest breakpoint where the responsive columns drop: still no overflow.

## When a collapsible rail owns the width, the query must be a container query

The three-width check above catches this bug. This is why a viewport breakpoint
cannot *fix* it.

A shell with a collapsible nav rail changes the row's available width without
changing the viewport by a single pixel. In an Angular secrets list (a six-column
CSS grid, `.sl-row`, not a `<table>`, same geometry problem) the rail is
`--rail-width-expanded: 13rem` against `--rail-width-collapsed: 3.5rem`: a 152px
swing that `@media (max-width: 1024px)` is structurally blind to. Tune the
breakpoint for the expanded state and the collapsed state gets rules meant for a
container 152px narrower than it is; tune it for collapsed and the expanded state
starves. There is no viewport value that is right for both, so moving the
breakpoint is not a fix, it is a choice of which state to break.

Make the row respond to its own column instead:

```css
.sl-root {
  container-type: inline-size;
}

@container (max-width: 700px) { /* was @media (max-width: 1024px) */ }
@container (max-width: 585px) { /* was @media (max-width: 900px)  */ }
```

Two mechanics that decide whether this works:

- **The container must be an ancestor of the rule's subject**, never the element
  being sized. Pick the nearest ancestor whose width already equals the row's
  content column: a plain block wrapper with no horizontal padding of its own.
  A wrapper that adds padding shifts every threshold by that padding.
- **Derive the thresholds, do not guess them.** Measure the chosen container's
  own rendered width at each old viewport breakpoint, in the rail state the
  original tuning was done in, and use those numbers. Here 1024px viewport gave a
  704px container and 900px gave 585px, so `700` and `585` keep the transition
  exactly where it already was for the tuned case and pick up the other rail
  state for free. Re-measure at the old breakpoint afterwards and require the
  same grid tracks you had before: that is the proof the conversion changed
  nothing you had already got right.

### The matrix is orientations times rail states

Checking each viewport once measures one rail state and proves nothing about the
other. Toggle the rail with its own button (a real click), never by writing to
the store, so the rendered state is the one under test.

| viewport | rail | container | `.sl-ident` | name lines |
| --- | --- | --- | --- | --- |
| 1032 x 1376 | expanded | 704 | 224.0 | 2 |
| 1032 x 1376 | collapsed | 856 | 259.4 | 1 |
| 1376 x 1032 | expanded | 1014 | 338.4 | 1 |
| 1376 x 1032 | collapsed | 1166 | 414.4 | 1 |

Those two viewports are the iPad Pro 13" (1032 x 1376 portrait, 1376 x 1032
landscape). The older 12.9" is 1024 x 1366, and **1024 is the most common
breakpoint value there is**, so that device's portrait width lands exactly on
the boundary of a rule written without thinking about it. Test the boundary
value itself, not only the values either side.

## Related

- `angular-draggable-splitter.md` for the Pointer Events plus `setPointerCapture`
  drag pattern, which is the same mechanism a column-resize handle uses.
- `angular-signal-store-design.md` for where per-user layout state belongs.
  Persisted column geometry is per-user UI preference: it goes in a
  `signalStoreFeature` slice backed by `localStorage` under a namespaced key,
  with reads and writes wrapped in `try/catch` so blocked storage degrades to
  non-persistent instead of throwing. It does not belong in any DB-backed
  application settings layer, which is app-wide config and a different concern.
