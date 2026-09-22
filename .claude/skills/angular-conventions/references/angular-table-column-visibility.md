# Angular Table Column Visibility

A user-controlled column picker for a data table: show and hide columns, some
hidden by default, persisted per user. Standalone Angular 22, signals, `OnPush`.

Read `angular-table-column-layout.md` and `angular-table-column-resize.md` first.
Visibility changes which columns compete for width, so it is inseparable from the
sizing model.

## Placement

Put the trigger at the far right end of the existing filter bar, after the other
filter controls, with the same label-above-control treatment so its label lines up
with theirs:

```
[ SEARCH ................flexible............. ]  [ TYPE v ]  [ Columns v ]
```

The search field keeps absorbing the remaining width, the other filters keep their
natural width and shift left, and the picker is pinned right (`ml-auto`). Preserve
whatever `flex-col` / `sm:flex-row` stacking the bar already has.

A trigger button opening a checkbox list beats a right-click context menu here:
nothing signals that a context menu exists.

## Two states per column, not one

The naive model is a boolean per column. That breaks as soon as the table also has
responsive rules like `hidden lg:table-cell`, because "hidden right now" and "the
user turned it off" are different facts.

Use the same three-valued override the rest of the app uses for panel collapse
(`'expanded' | 'collapsed' | null`, where `null` means "follow the automatic
behaviour"):

- `null` (untouched): the responsive rule decides. Behaviour is unchanged from
  before the feature existed.
- `'expanded'`: visible at every width, even below its breakpoint.
- `'collapsed'`: hidden at every width.

An explicit choice wins over the breakpoint. A column the user deliberately
switched on must not vanish when they narrow the window.

This produces two distinct derived signals, and conflating them is a bug:

- `columnVisible(col)` drives the actual `<th>`/`<td>` rendering.
- `isColumnChecked(col)` drives the checkbox, and is `override !== 'collapsed'`.

A column that is checked but currently below its breakpoint shows as checked while
rendering nothing. That is correct: the user never turned it off, the viewport
narrowed. Deriving the checkbox from `columnVisible` instead would make checkboxes
flicker off as the window shrinks, which reads as the app forgetting settings.

Drive the breakpoint half from a viewport signal updated by the same
`ResizeObserver` already used for width auto-fill, rather than a second listener.

## Defaults, and the rest of the picker

- Some columns ship hidden. Express that as an explicit `'collapsed'` default for
  that column, unconditionally, not as a narrower breakpoint.
- A row-actions column is never listed and never hideable.
- **Never let the table go empty**: block hiding the last checked column, and
  disable that checkbox rather than silently ignoring the click.
- A reset action restores the default visibility set. Scope it to visibility only;
  column widths have their own per-column reset.

## Interaction with column widths

Hiding a column returns its width to the pool, showing one takes width from it, so
the sizing model must be correct for **every reachable combination**, not tuned for
the default set. Concretely: the flexible column's auto-fill sums the widths of the
columns that are *currently visible*, and the point at which the horizontal
scrollbar appears therefore moves as columns are toggled. Do not hardcode a single
global minimum that only happens to work for the default set.

All-columns-visible is the tightest combination and the one that will force the
scrollbar first. Measured on a real admin list view at a 901px container with
every column switched on:

```
Date 152 | Type 136 | Name 144 | Contact 110 | Tags 120 | Preferred 232 | Actions 80
sum 974, wrapper clientWidth 901, overflow 73, wrapper scrolls by exactly 73
```

The flexible column floored at its 110px minimum and the excess became an honest
scrollbar. That is the correct outcome, and it is what to assert.

## Overlay behaviour

Use the app's existing overlay and escape-stack machinery rather than hand-rolling
(see `angular-overlays.md`). The requirement worth stating explicitly:

> One ESC press pops exactly one layer, the topmost one, and nothing else.

With a detail row expanded and the picker open, ESC closes only the picker; the row
stays expanded. Press again and the next layer down closes. Register the dropdown
on the escape stack when it opens and unregister when it closes, and **do not add a
host or document `keydown` listener alongside it**. That parallel listener is
exactly what produces the "one ESC closed two things" bug.

Focus: move into the first control when it opens, and return to the trigger button
on every close path (ESC, backdrop click, reset).

## Persistence

Its own namespaced key, separate from the widths, with the **same versioned
envelope** (`{ v: 1, visibility: { ... } }`) and the same tolerate-anything read
that falls back to defaults on malformed or wrong-version payloads. Skipping the
version here reproduces the stale-storage bug documented in
`angular-table-column-resize.md` in a second place.

Store a sparse map of only the columns the user actually touched, so a later change
to which columns ship hidden reaches everyone who never touched them. Persist
immediately on toggle: unlike a drag, it is a discrete action with no stream of
intermediate values.

## Verifying

Same rules as the resize leaf: a screenshot is the ground truth, geometry reads go
stale, and a behavioural `scrollLeft` probe beats a measured box. Verify in the
user's own browser profile with the storage keys removed.

Check, at minimum:

- [ ] Default set renders with the hidden-by-default column off and no overflow.
- [ ] All columns on: no column below its minimum; excess becomes a scrollbar.
- [ ] Down to a single checked column: last checkbox disabled, table not empty.
- [ ] Toggle survives a reload; a wrong-version payload falls back to defaults.
- [ ] Explicit-on column stays visible below its breakpoint; untouched column still
      follows it.
- [ ] Two layers open, one ESC, only the top one closes; focus returns to the trigger.
