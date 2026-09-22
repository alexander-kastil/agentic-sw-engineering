# Page Chrome: One Hero, Routed Tabs, KPI Bands

How to give a set of authenticated app pages one shared visual grammar — hero, KPI band, tab nav —
without duplicating headings or fighting Angular's style encapsulation.

Use this when pages "look unrelated", when a page shows two stacked headlines, when a long section
list should become tabs, or when explanatory prose should become scannable figures.

## The rhythm

Every page in the set repeats the same four-part structure, in this order:

```
eyebrow + H1   ->   KPI band   ->   tab nav   ->   view (router-outlet)
```

Non-negotiable rules:

1. **Exactly one eyebrow and one H1 per page.**
2. **A tab label is the name of its section, so a view never repeats its own tab label as a heading.**
3. A view may carry an H2 only when it *says more* than its tab (`Conversation` → `Conversation record`
   is a near-echo and adds nothing; `Billing` → `Billing: engagement to date` earns its place).

### The "double headline" smell

The most common failure is promoting a panel into a tab but leaving the panel's own header behind:

```html
<!-- WRONG: two eyebrow+headline pairs stacked, ~120px apart -->
<section class="page-hero">
  <p class="eyebrow">Deployment · Green &amp; Blue</p>
  <h1>Where every app actually runs.</h1>
</section>
<app-infra-panel />   <!-- which itself renders: eyebrow "Infrastructure" + h2 "Fleet & Ports" -->
```

When a panel becomes a tab, **delete its header in the same change** — the tab label now carries it.
A panel that was designed as a standalone block almost always ships its own eyebrow, title and KPI
rail; all three move up to the page shell or disappear.

## Shared CSS: an imported file, not global `styles.css`

Cross-page primitives (`.page-hero`, `.page-kpis`, `.view-nav`) must live in a plain CSS file that
each component `@import`s from its own `styleUrl`:

```
src/app/shared/page-chrome.css
```

```css
/* dashboard.css, deployment-page.css, billing-shell.css */
@import '../../shared/page-chrome.css';
```

**Do not put them in the global `styles.css`.** Angular's default emulated encapsulation rewrites
component rules with an attribute selector, so a component's own `.kpi` always outranks a global
`.kpi` — but the global rule still *applies* its base properties to that element. Any generic class
name (`.kpi`, `.card`, `.tile`) will silently bleed into unrelated components that happen to use the
same word. Importing into the component keeps every rule scoped, and the `@import` is resolved at
build time so there is no extra request.

Corollary: when a shared primitive would collide with an existing component class, **prefix it**
(`.page-kpi`, not `.kpi`) rather than hunting down the collisions.

### Every consumer imports it, including child components

The shells listed above are not the only importers. Emulated encapsulation scopes an imported rule to
the template of the component that imported it, so a **child component rendered inside an importing
shell inherits nothing**. A tab view whose own template renders `<ul class="page-kpis page-kpis--sub">`
must `@import 'page-chrome.css'` itself, even though its parent shell already does.

This failure is quiet and easy to misread as a data bug. The classes are intact in the DOM inspector,
the build is clean, the tests are green, the markup is correct: only the rendered pixels are wrong, and
the element falls back to browser defaults (a bare `<ul>` with disc bullets, value and label with no
separation). Confirm by reading computed styles, not by eye:

```js
getComputedStyle(document.querySelector('.page-kpis--sub'))
// broken: display "block", listStyleType "disc", gridTemplateColumns "none"
// fixed:  display "grid",  listStyleType "none", gridTemplateColumns "177px 177px ..."
```

Re-check the component style budget afterwards: `@import` inlines the whole shared file into every
importing component's stylesheet, so each new importer pays its full size again.

## Converting stacked sections into routed tabs

Prefer **child routes** over a local `signal()` for tab state: routes give deep links, working
browser back, and a shareable URL per view.

```ts
{
  path: 'deployment',
  loadComponent: () => import('./deployment-page').then((m) => m.DeploymentPage),
  canActivate: [authGuard],
  children: [
    { path: '', redirectTo: 'fleet', pathMatch: 'full' },
    { path: 'fleet', loadComponent: () => import('./infra-panel').then((m) => m.InfraPanel) },
    { path: 'graph', loadComponent: () => import('./graph-tab').then((m) => m.GraphTab) },
    { path: '**', redirectTo: 'fleet' },
  ],
}
```

Route straight to the existing standalone components; no wrapper component is needed. Keep the
`redirectTo` **and** the `**` fallback so a stale bookmark lands on the first tab instead of a blank
outlet.

Tab nav markup, with `ariaCurrentWhenActive` for assistive tech:

```html
<nav class="view-nav" aria-label="Views">
  @for (tab of tabs; track tab.path) {
    <a [routerLink]="tab.path" routerLinkActive="active"
       ariaCurrentWhenActive="page" [routerLinkActiveOptions]="linkMatch">{{ tab.label }}</a>
  }
</nav>
```

```ts
readonly linkMatch: IsActiveMatchOptions = {
  paths: 'exact', queryParams: 'subset', matrixParams: 'ignored', fragment: 'ignored',
};
```

### Reading the active tab in the shell

To show a per-tab lede without a wrapper component, derive it from navigation rather than injecting
route data:

```ts
private readonly url = toSignal(
  this.router.events.pipe(
    filter((e): e is NavigationEnd => e instanceof NavigationEnd),
    map((e) => e.urlAfterRedirects),
  ),
  { initialValue: this.router.url },
);

readonly activeTab = computed(
  () => this.tabs.find((t) => this.url().includes(`/deployment/${t.path}`)) ?? this.tabs[0],
);
```

`initialValue: this.router.url` matters: `NavigationEnd` has usually already fired by the time the
shell is constructed, so without it the first render has no active tab.

## KPI bands

A KPI band replaces explanatory prose with figures. Value first, then label, then a one-line
provenance sub-label:

```html
<ul class="page-kpis" aria-label="Engagement to date">
  @for (kpi of kpis(); track kpi.key) {
    <li class="page-kpi">
      <span class="page-kpi-value" [class.accent]="kpi.accent" [class.compact]="kpi.compact">{{ kpi.value }}</span>
      <span class="page-kpi-label">{{ kpi.label }}</span>
      <span class="page-kpi-sub">{{ kpi.sub }}</span>
    </li>
  }
</ul>
```

Three modifiers earn their keep:

| Modifier | Why |
| --- | --- |
| `--kpi-cols` custom property | One custom property drives the column count; media queries override the property (`6 → 3 → 2`) instead of restating `grid-template-columns` per breakpoint. |
| `.compact` on the value | Long values (a date range, a hostname) wrap to two lines and grow **every** tile in the row, because grid rows are equal height. A smaller font on just those tiles keeps the band one line tall. |
| `.page-kpis--sub` on the band | A view that carries its own figures under a page-level band needs one step less weight, or the two bands read as repetition instead of hierarchy. Same grammar, smaller value font, tighter padding. |

Always set `grid-template-columns: repeat(var(--kpi-cols), minmax(0, 1fr))` — `minmax(0, 1fr)` (not
`1fr`) is what stops a long unbroken value from blowing out the track.

Add `font-variant-numeric: tabular-nums` on the band so figures do not jitter between states.

## Prose → figures, without losing facts

When replacing a paragraph with KPIs, **every fact in the paragraph must land somewhere.** The
paragraph usually contains two different things:

- **Quantities** → KPI tiles (count, total, rate, span, sources).
- **Scope statements** ("we include X, we deliberately exclude Y") → a two-column list with distinct
  markers, not another paragraph:

```html
<div class="scope">
  <div class="scope-col scope-col--in">   <p class="scope-h">In the record</p>          <ul class="scope-list">…</ul></div>
  <div class="scope-col scope-col--out">  <p class="scope-h">Deliberately excluded</p>  <ul class="scope-list">…</ul></div>
</div>
```

Use a glyph *and* a colour on the markers (`✓` green / `✕` red via `::before`), never colour alone —
colour-only meaning fails WCAG and fails for anyone printing the page.

## Prose runs the full container width

**Do not put a `ch` measure cap on prose in a dashboard app.** No `max-width: 60ch` on a lede, no
`72ch` on an error paragraph, no `82ch` on a section intro. The "65 characters is optimal measure"
advice comes from article typography and does not apply to a wide operations UI, where the customer
reads a short sentence above a full-width grid and the cap just leaves a ragged column of dead space.

This recurs because it is the default instinct of whoever writes the next component's stylesheet.
One codebase accumulated nine of them, one per component, and each fix removed only the reported
instance. When you remove one, **grep the whole app** (`max-width:\s*\d+ch`) and remove them all.

Two categories are legitimate and must survive the sweep:

| Keep | Why |
| --- | --- |
| Identity chips (`.user-chip`, `.user-badge`, a name next to a logout button) | They pair `max-width` with `overflow: hidden; text-overflow: ellipsis` — the cap *is* the truncation mechanism |
| Headline caps (`h1 { max-width: 28ch }`) | A deliberate wrap decision about a display face, not a measure applied to body copy. Decide separately, do not sweep blind |

## Fitting text to one line is a copy job, not a CSS job

Asked to make five tile captions one-liners, an agent added `text-overflow: ellipsis` and shipped
`DNS löst den Namen zur festen I...` and `Feste IP, auf die alle Domains zei...`. Every caption fitted
on one line; none of them could be read. It satisfied the stated constraint exactly.

**Shorten the sentence** until it fits with room to spare. Never satisfy a length constraint on prose
with `text-overflow`, `white-space: nowrap`, or `-webkit-line-clamp`. Terse noun phrases are fine and
usually better: `DNS löst den Namen auf.`, `Feste IP für alle Domains.`

When delegating this, state the acceptance criterion as **"no ellipsis is rendered and no caption
wraps"**, not "make it fit on one line" — the second phrasing has a cheap wrong answer and an agent
will find it.

## Strip decoration from a badge, keep the noun

A badge is read out of context: away from the column header or the icon that would have supplied its
referent. `20` sitting next to a shield icon and four compliance pills means nothing; `Tests: 20`
means something. When an instruction says to shorten a label, remove the decoration (units, verbs,
`von 11 fehlgeschlagen`) and keep the noun that says what the number counts.

## Check the type ladder when unifying headings

Unifying headline styles reliably exposes an inverted scale. Measure the computed sizes before
declaring the system consistent:

| Level | Treatment |
| --- | --- |
| H1 (page hero) | uppercase display, `clamp(24px, 3.2vw, 40px)` |
| H2 (view heading) | uppercase display, `clamp(19px, 2.1vw, 27px)` |
| H3 (block heading) | uppercase display, `15px`, `letter-spacing: .06em` |

A real case: the H3 helper class was `clamp(20px, 2.4vw, 26px)` while the H2 class was
`clamp(22px, 2.6vw, 32px)` — at most viewport widths the H3 rendered as large as the H2, so the page
had no hierarchy at all. Sentence-case vs uppercase hid it until both were made uppercase.

Likewise, when two components render "the same" tile with different internal order (value-then-label
vs label-then-value from a `<dl>`), align the **surface** — radius, padding, font sizes, borders — and
accept the order difference where the markup semantics require it (`<dt>` must precede `<dd>`).

## Layout stability: reserve the scrollbar gutter

A tab or filter that swaps content of different heights makes the page's own vertical scrollbar
appear and disappear as the document crosses the viewport height. The 15px track toggling shifts
everything horizontally on every click. The customer reports it as "a vertical bar causing jumps",
and will attribute it to whatever content they were switching between: a diagram, a table, a chart.
It is never the content's width.

**Diagnose by height, not width.** Log `document.documentElement.scrollHeight` per filter state and
look for one state that sits at or below `window.innerHeight` while the others tower over it:

```js
// filter A 1847 | filter B 1305 | filter C 1305 | filter D 1305
// innerHeight ~1305 -> three of four states have no scrollbar. That is the jump.
```

**Put `scrollbar-gutter: stable` on the element whose overflow propagates to the viewport.** This is
the trap: almost every app carries `body { overflow-x: hidden }`, and because the root's overflow is
`visible`, the UA propagates *body's* overflow to the viewport. Body then owns the viewport scrollbar,
so the gutter must be declared there. On `html` it is inert:

```css
/* WRONG — computes to "stable", does absolutely nothing */
html { scrollbar-gutter: stable }
body { overflow-x: hidden }

/* RIGHT — body propagates its overflow to the viewport, so body owns the gutter */
body { overflow-x: hidden; scrollbar-gutter: stable }
```

`overflow-x: clip` instead of `hidden` does not rescue the `html` version either; clip is not a
scroll container, but the gutter still failed to reserve in Chrome. Declare it on `body` and move on.

**`getComputedStyle` returning your value is not proof the property took effect.** The inert `html`
version reported `scrollbarGutter: "stable"` while `documentElement.clientWidth` still flipped
2545 ↔ 2560 on every scope change. Only the geometric consequence proves it. Assert on
`document.body.clientWidth` plus a fixed element's `getBoundingClientRect()` across every state and
require identical numbers:

```js
// body clientWidth 2545 in all four states, controls left/right 610.33/1934.33 in all four -> fixed
```

## Verification

- A green build is not evidence a layout change works. Screenshot every route.
- Browser `resize_window` calls can report success and change nothing when the window is maximized.
  Read back `window.innerWidth` before trusting a responsive check, and say so plainly when the
  breakpoints could not be exercised.
- A CSS property that computes to the value you set may still be inert. Measure the geometry it was
  supposed to change, across every state that is supposed to stay put.
EOF
