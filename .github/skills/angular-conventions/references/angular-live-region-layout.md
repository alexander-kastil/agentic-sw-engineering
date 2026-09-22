# Empty live regions and other invisible flex items that still cost a gap

An `aria-live` region has to be **in the DOM before its content changes**, otherwise screen readers
announce nothing. So the usual shape is a permanently-rendered wrapper with an `@if` inside:

```html
<div aria-live="polite">
  @if (error()) { <div class="alert">{{ error() }}</div> }
</div>
```

That wrapper is a flex item of its parent. In a `flex flex-col gap-4` form it therefore contributes a
full `gap-4` **even while it renders nothing** — an empty box of height 0 still sits between two gaps
instead of one. Two such wrappers between a textarea and a footer turn 16px of separation into 48px,
which reads as "why is there so much dead space at the bottom".

## The fix

```html
<div aria-live="polite" class="empty:absolute">
```

`:empty` matches, the element is taken out of flow, and the parent's gap collapses to a single one. The
element stays rendered and stays in the accessibility tree, so the announcement still works.

## Why not `empty:hidden`

`display: none` removes the element from the accessibility tree entirely. When content appears, the
region is inserted and populated in the same frame — the case screen readers are least reliable about.
`empty:absolute` never leaves the tree; only the box leaves the flow.

## `:empty` vs Angular's control-flow anchors

`@if` leaves a comment node behind when its branch is false. Per the CSS spec, comments do **not** affect
emptiness, so `:empty` still matches. Whitespace text nodes *would* break it, but Angular's default
`preserveWhitespaces: false` strips them from templates. Both facts have to hold; check the rendered DOM
if the rule appears not to apply.

## The general rule

In a `gap`-spaced flex or grid container, every conditionally-empty child is a hidden spacer. Audit for
them whenever spacing looks larger than the classes say: status wrappers, `aria-live` regions, an
`<span></span>` placeholder used to push a sibling to the right with `justify-between`, skeleton hosts.
Either make them `empty:absolute`, or move the conditional up so no empty element is generated at all.
