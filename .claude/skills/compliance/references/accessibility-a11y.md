---
name: accessibility-a11y
description: >-
  Compliance leaf for web accessibility (a11y). Covers the regulatory frame
  (European Accessibility Act, Web Accessibility Directive, Austrian
  Barrierefreiheitsgesetz), WCAG 2.1 AA as the practical conformance target, the
  best-practice checklist (semantic HTML, ARIA, contrast, focus, keyboard,
  images, responsive, testing), an audit workflow, and field-tested fix recipes
  for auditing legacy and CMS-exported static sites. Use when asked to "check
  accessibility", "a11y audit", "WCAG compliance", "is this site accessible",
  "EAA / Barrierefreiheit", "fix accessibility findings", or when shipping a
  customer-facing site that must be inclusive.
metadata:
  type: reference
---

# Accessibility (a11y) — compliance leaf

Accessibility is a compliance domain, not just a UX nicety: EU and Austrian law now
require it for a growing set of products and services, and WCAG is the standard courts
and auditors measure against. This leaf covers the regulatory frame, the conformance
target, the best-practice checklist, the audit workflow, and the fix recipes proven on
this repo's sites.

> **Not legal advice.** This is engineering-team orientation. A formal conformance claim
> (an accessibility statement under the EAA/WAD) needs review by counsel or the
> accessibility officer before it goes external.

## Regulatory frame (verify current dates/scope before relying on them)

| Instrument | Who it binds | Standard it points to |
| --- | --- | --- |
| **European Accessibility Act (EAA)**, Directive (EU) 2019/882 | Private-sector products/services: e-commerce, consumer banking, e-books, electronic communications, transport ticketing, etc. Applies from 28 June 2025. | EN 301 549 → WCAG |
| **Web Accessibility Directive (WAD)**, Directive (EU) 2016/2102 | Public-sector bodies' websites and mobile apps | EN 301 549 → WCAG 2.1 AA |
| **Austria: Barrierefreiheitsgesetz (BaFG)** | National transposition of the EAA | EN 301 549 |
| **EN 301 549** | Harmonized EU standard | Currently maps to **WCAG 2.1 level AA** (moving toward 2.2) |

**Applicability nuance.** A purely informational marketing or property-rental site (for
example wine71) is not clearly inside the EAA's enumerated services, so strict legal
bindingness may not apply; a booking/e-commerce/banking flow generally is. Regardless of
strict scope, **target WCAG 2.1 AA** as the safe, defensible baseline for any
customer-facing site.

## Conformance target

Aim for **WCAG 2.1 AA**. The four principles (POUR): Perceivable, Operable,
Understandable, Robust. The findings below are grouped by the WCAG success criteria they
map to so an audit can cite them.

## Best-practice checklist

### Semantic HTML
- Use `<header>`, `<main>`, `<nav>`, `<footer>`, `<article>`, `<section>`, `<aside>` as landmarks for screen-reader navigation.
- Use `<button>` for actions and `<a href>` for navigation. Do not fake either with a bare `<div>`/`<span>` or an `<a>` without `href`.
- Proper heading hierarchy (h1-h6), no skipped levels; one `<h1>` per page. Visual "headings" built from styled `<p>` break the outline: flag them.
- Avoid deprecated markup.

### Forms
- Every input has a programmatic label (`<label for>` + `id`). A hidden label must use a screen-reader-only technique, **not** `display:none` (see the `hidden`-vs-`sr-only` trap below).
- Group related controls with `<fieldset>`/`<legend>`.
- Use correct input types (`email`, `tel`, `number`). Placeholder is a hint, never the label.
- Clear, associated error/validation messages.

### ARIA (native first)
- Prefer native HTML; reach for ARIA only where HTML falls short.
- `aria-label` / `aria-labelledby` for controls without visible text (icon-only buttons).
- `aria-expanded` on disclosure/menu toggles, kept in sync in JS.
- `aria-hidden="true"` on purely decorative icons (icon-font `<i>`, inline SVG sparks).
- `aria-current="page"` for the active nav item.
- `role="button"` only on a non-button that acts as a button; **never** on a real link that navigates.

### Color & contrast (WCAG 1.4.3 / 1.4.1)
- Text contrast at least 4.5:1 (3:1 for large text). Verify hero text over photos and light-on-light buttons.
- Never convey information by color alone; pair with text, icon, or pattern.

### Focus & keyboard (WCAG 2.1.1 / 2.4.7)
- Everything operable by mouse must be operable by keyboard; no keyboard traps.
- Visible focus indicator on all interactive elements; do not strip `outline` without a replacement.
- Logical tab order; `tabindex="0"` for natural order, `-1` for programmatic focus only.
- Touch/click targets at least 44x44 px.

### Images & media (WCAG 1.1.1)
- Descriptive `alt` for meaningful images; `alt=""` for decorative ones. Never ship placeholder alt like `"Demo Image"`.
- Captions for video, transcripts for audio.
- Descriptive link text (avoid "click here" / bare "Read more" where the target is ambiguous).

### Responsive & user preferences
- Content reflows and stays functional to 200% zoom / 320px width.
- Respect `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`.

## Audit workflow

1. **Enumerate the surface.** For a static/multi-page site, glob the HTML and find the shared header/footer/nav so a single fix pattern can be applied across every page.
2. **Grep for the known offenders** (fast, high-signal): `lang=`, `maximum-scale|user-scalable`, icon-only `<button>`/`<a>` with only an `<i>`/`<svg>` child, `alt="Demo`, `role="button"` on `<a href>`, `class="...hidden"` on labels, `<a class="...">` with no `href` used as a control.
3. **Confirm shared strings are byte-identical** across pages before a scripted replace, so one literal find/replace is safe.
4. **Back up** touched files before a multi-file edit; record the restore path.
5. **Fix**, then **verify in a real browser**: serve the site, load at 1920x1080, screenshot to confirm no visual regression, and check the console is clean (especially after any JS change).
6. **Automated pass** with Lighthouse / axe-core for anything grep missed; then manual keyboard-only and screen-reader spot checks.

## Field-tested fix recipes (legacy / CMS-exported static sites)

These recurred on the wine71 static mirror (Bootstrap 3 / Umbraco export, 13 pages sharing one header/footer) and generalize to any scraped or legacy site:

- **Wrong page language** (WCAG 3.1.1). A German site served `<html lang="en">` (including the IE conditional-comment `<html>` tags). Fix every occurrence to the real language (`lang="de"`). This is the single highest-value one-line fix.
- **Zoom disabled** (WCAG 1.4.4 / 1.4.10). `content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"` blocks pinch-zoom. Drop `maximum-scale` and `user-scalable`.
- **Icon-only controls with no name** (WCAG 4.1.2). A search `<button>` or back-to-top `<a>` whose only child is `<i class="ion-...">` announces as nothing. Add `aria-label` to the control and `aria-hidden="true"` to the icon.
- **Anchor-as-button, not keyboard operable** (WCAG 2.1.1 / 4.1.2). A mobile menu toggle `<a class="expand">` with no `href` is unreachable by keyboard. Minimal-risk fix that preserves an existing JS click handler bound to `a.expand`: keep the element, add `role="button" tabindex="0" aria-label aria-expanded`, and add a `keydown` handler that triggers `.click()` on Enter (13) / Space (32) and keeps `aria-expanded` in sync. Changing the tag to `<button>` also works but only if you update every JS/CSS selector that targeted `a.expand`.
- **Hidden label that is hidden from everyone** (WCAG 1.3.1 / 4.1.2). A form label with Bootstrap `.hidden` (`display:none`) is removed from the accessibility tree too. Swap `hidden` for `sr-only` so it stays visually hidden but reaches screen readers. `.sr-only` ships with Bootstrap 3; confirm it exists before using it.
- **Placeholder alt text** (WCAG 1.1.1). `alt="Demo Image"` left over from a template: replace with alt that describes the actual image, or `alt=""` if decorative.
- **Misused `role="button"`** (WCAG 4.1.2). Real navigation links styled as buttons carried `role="button"`; that makes AT announce "button" for something that navigates. Remove the role from links; add `role="button"` to the elements that genuinely perform an action (for example cookie accept/decline anchors wired to a JS handler).
- **Decorative icons exposed** (WCAG 1.1.1). Icon-font chevrons/carets and inline decorative SVG need `aria-hidden="true"`.
- **When to defer.** Converting styled `<p>` "headings" to real `<h2>`/`<h3>` fixes the document outline but is invasive on a generated legacy site (touches many nodes, risks the visual system). Flag it as a recommendation and do it only with explicit go-ahead and matching styles, rather than a silent broad rewrite.

## Writing style

No em dashes in anything this leaf helps author, and none in this file. Use a colon before a
list, parentheses or commas for an aside, a semicolon or two sentences for related clauses,
and a comma or its own sentence for a hard qualifier.
