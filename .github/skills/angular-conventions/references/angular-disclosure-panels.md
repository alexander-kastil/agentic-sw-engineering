# Collapsible Panels Inside Equal-Height Card Grids

Proven on the `bauerprosport.com` deployment page (`infra-panel`), where a card grid needed both
uniform card heights and a collapsed-by-default "Status-Details" disclosure. The two requirements
fight each other, and the failure is silent: the class toggles, ARIA flips, nothing opens.

## The core conflict

Equal-height cards are usually written as:

```css
.grid  { display: grid; align-items: stretch; }
.card  { display: flex; flex-direction: column; height: 100%; }
.trigger { margin-top: auto; }          /* pin footer to the bottom */
```

`height: 100%` turns the card into a **fixed-height** flex container, and `margin-top: auto` on the
trigger consumes every remaining pixel. A disclosure panel below it is then a flex item with **zero
free space**, so both common animation techniques collapse to nothing:

- `grid-template-rows: 1fr` resolves to `0px` — `fr` distributes *free* space, and there is none.
- `max-height: 420px` never applies either, because the panel's own content box is already zero.

Symptom: `aria-expanded` becomes `true`, the `--open` class is present in `className`, and
`getComputedStyle(panel).maxHeight` still reads `0px`. Easy to misread as a CSS cascade bug and burn
an hour chasing specificity that is not the problem.

## The fix

**Drop `height: 100%`.** Grid items already stretch to the row height under the default
`align-items: stretch`, so equal heights survive — and without the percentage the row is free to
grow when a card expands, re-stretching its siblings so they stay level.

```css
.card          { display: flex; flex-direction: column; }   /* no height: 100% */
.trigger       { margin-top: auto; flex-shrink: 0; min-height: 44px; }
.details       { flex-shrink: 0; display: grid; grid-template-rows: 0fr; opacity: 0;
                 transition: grid-template-rows 200ms ease-out, opacity 200ms ease-out; }
.details-inner { min-height: 0; overflow: hidden; }
```

```html
<div class="details"
     [style.grid-template-rows]="expanded() ? '1fr' : '0fr'"
     [style.opacity]="expanded() ? 1 : 0"
     [id]="detailsId" role="region" [attr.aria-labelledby]="triggerId">
  <div class="details-inner">…</div>
</div>
```

`0fr → 1fr` is height-agnostic: no magic ceiling to outgrow, and no need to measure `scrollHeight`.
Prefer it over `max-height`, which always needs an arbitrary number that silently clips one day.

## Drive the open state with a style binding, not only a class

A scoped `.details--open` class rule can fail to take effect while the identical declarations applied
inline work immediately. Angular's emulated encapsulation rewrites both the base and the modifier to
the same `[_ngcontent-*]` specificity, so ordering and specificity look correct while the modifier
still loses.

**Rule: bind the state-carrying properties with `[style.*]`.** Inline styles win unconditionally and
cannot be defeated by a scoped-selector mismatch. Keep the class only if something else hooks it.

This is a state binding, not the `[ngStyle]` anti-pattern — `[style.prop]` is the sanctioned form.

## Accessibility contract

Non-negotiable on any disclosure:

- Trigger is a real `<button type="button">`, `min-height: 44px`, visible `:focus-visible` ring.
- `[attr.aria-expanded]` on the trigger, `[attr.aria-controls]` → the panel's `[id]`.
- Panel carries `role="region"` + `[attr.aria-labelledby]` → the trigger's `[id]`.
- Ids unique per card — derive from the item id, never a bare index.
- Severity must survive collapse: reflect the worst contained state on the collapsed trigger (a
  tinted count badge), so a warning is visible without expanding.
- Wrap transitions in `@media (prefers-reduced-motion: reduce) { transition: none; }`.

## Verification

Do not trust in-page measurement alone. During this work `getComputedStyle` and
`getBoundingClientRect` returned stale values through the browser MCP — reporting `max-height: 0px`
on an element whose live `style` attribute read `max-height: 600px`, and unchanged card heights in a
frame where the cards had visibly grown.

**A screenshot is the ground truth.** Confirm collapsed and expanded visually, and treat numeric
reads as a supporting signal only. See also: click coordinates from `getBoundingClientRect()` are CSS
pixels and will miss if the screenshot is captured at a different scale — take a screenshot first and
click the coordinates you see in it.
