# A CSS change that has no effect

Two failure modes look identical from the outside: you edit a stylesheet, the build goes green, the page
reloads, and the layout is unchanged. One is a CSS bug that fails silently; the other is a build that
never shipped your file. Tell them apart before editing anything else, because the fixes are opposite.

## Diagnose first: is the rule even in the page?

Read the CSSOM. It is the only ground truth for "did my edit actually reach the browser" — the file on
disk, a green build, and a hard reload all lie about this.

```js
let hits = [];
for (const ss of document.styleSheets) {
  let rules; try { rules = ss.cssRules } catch (e) { continue }   // cross-origin sheets throw
  for (const r of rules) if ((r.cssText || '').includes('.my-selector')) hits.push(r.cssText);
}
hits;
```

Then compare the served rule text against the file:

| CSSOM shows | Meaning | Fix |
| --- | --- | --- |
| The **old** declarations | The dev server is serving a stale bundle | Restart the dev server (below) |
| The **new** declarations, but `getComputedStyle` disagrees with them | A real CSS bug — specificity, cascade, or a rule that cannot match | Fix the CSS (below) |
| The rule is absent entirely | Wrong component scope, or the file is not imported | Check `styleUrl` / the selector's `_ngcontent` scope |

Pair it with the computed value of the property you are fighting:

```js
getComputedStyle(document.querySelector('.my-selector')).flexDirection
```

A green `ng build` proves the file compiles. It proves nothing about whether the rule matches.

## Cause 1: the dev server is serving a stale bundle

A long-running `ng serve` can keep serving an hours-old bundle indefinitely. It survives Ctrl+Shift+R,
`location.reload()`, and touching the file to bump its mtime, because the staleness is server-side: the
watcher missed the change or a rebuild failed and the server kept the last good output. A concurrent
process writing into `src/` (another agent, another editor, a `run build` in the same tree) makes a
half-written file transiently unresolvable, which is enough to wedge the rebuild.

Confirm the source is actually correct before blaming the server, by checking the *production* output:

```bash
npm --prefix <app> run build
grep -rlo "flex:0 1 124px" dist/            # the new declaration, minified
grep -rlo "container-type:inline-size" dist/ # the old one should be gone
```

If `dist/` has the new CSS and the CSSOM has the old, it is the dev server. Restart it — same command,
same port; it is a localhost process and the restart is immediately reversible:

```bash
# find it, then restart with the original command
# Windows: Get-CimInstance Win32_Process -Filter "ProcessId=<pid>" | Select CommandLine
npm --prefix <app> start
```

Expect the restart to also pull in unrelated in-flight edits from other sessions in the same tree.
Re-read what changed on screen before attributing any of it to your own work.

## Cause 2: a container query cannot match its own container

`container-type` establishes a query container for that element's **descendants**. The element that
declares it can never match its own `@container` rule. This fails silently: valid CSS, green build, rule
simply never applies.

```css
/* BROKEN — .card-top declares the container and is also the query target */
.card-top { display: flex; flex-direction: column; container-type: inline-size; }
@container (min-width: 300px) {
  .card-top { flex-direction: row; }   /* never applies, at any width */
  .card-side { flex: 0 0 124px; }      /* applies — it is a descendant */
}
```

The half-applied result is the tell: children pick up their container-query declarations while the
container keeps its base layout, so you get a correctly-sized child in a wrongly-stacked parent.

Two fixes:

```css
/* A: move the container up one level — query the parent, style the child */
.card { container-type: inline-size; }
@container (min-width: 300px) {
  .card-top { flex-direction: row; }
}
```

```css
/* B (preferred for "sits beside, else wraps below"): plain flex-wrap, no query at all */
.card-top  { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 10px 14px; }
.card-main { flex: 1 1 220px; min-width: 0; }   /* basis = the width it needs to stay on one line */
.card-side { flex: 0 1 124px; max-width: 124px; }
```

Option B needs no container at all: the wrap threshold is `main-basis + side-basis + gap`, so choose the
main basis as the narrowest width at which sharing the line still looks right. Prefer it whenever the
requirement is one-dimensional; reach for a container query only when the child must restyle itself
(not merely reflow) based on the space it was given.

## Cause 3: an unlayered global rule beats your Tailwind utility

Tailwind v4 emits its utilities inside `@layer`. Any plain rule you wrote in `styles.css` outside a layer is
**unlayered**, and per the CSS Cascade Layers spec unlayered declarations always win over layered ones,
regardless of specificity or source order. So a hand-rolled global component class silently defeats the
utility you add next to it:

```html
<!-- .btn-ghost:hover is unlayered in styles.css, so hover:text-danger NEVER applies -->
<button class="btn btn-ghost hover:text-danger hover:bg-danger/10">Delete</button>

<!-- .btn sets cursor: pointer unlayered, so cursor-not-allowed NEVER applies -->
<button class="btn cursor-not-allowed" aria-disabled="true">Unavailable</button>
```

Nothing errors, the class is present in the DOM, and reading the markup tells you nothing. Confirm with the
computed style, not the class list:

```js
const b = document.querySelector('button.btn-ghost');
getComputedStyle(b).cursor;            // 'pointer' even though cursor-not-allowed is on the element
```

Two ways out, in order of preference:

1. **Drop the global class** for that control and build it from plain utilities. This is right for one-off
   controls (pills, chips, an aria-disabled mock button) that need hover or cursor treatment the base class
   forbids.
2. **Change the global class** in `styles.css`, or move it into a layer, when the override should apply
   everywhere. Only do this deliberately: it reflavors every button in the app.

The same trap applies to any hand-written global (`.field`, `.filter-input`, `.popup-actionbar`). Treat a
global component class and a Tailwind state utility on the same element as mutually exclusive until proven
otherwise.

## Cause 4: the class exists, but in another component's stylesheet

Component styles are scoped by an `_ngcontent-*` attribute, so a class name is only global if it was
written in `styles.css`. Reusing a class you found in a sibling component's CSS produces no error, no
warning, and no styling: the element renders with the browser's defaults.

This one arrives most often through delegation. A prompt says "reuse the existing `.kv` row treatment",
the agent greps, finds `.kv` in `infra-panel.css`, uses the class name in a different component, and
reports the work as done. The build is green and every test passes, because neither has an opinion
about whether a rule matched.

The tell is UA-default rendering of semantic markup, which reads as "unfinished" rather than "broken":

```html
<!-- .kv / .kv-row live in another component's stylesheet, so this is an unstyled <dl> -->
<dl class="kv">
  <div class="kv-row"><dt>Datenbank</dt><dd>verbunden</dd></div>
</dl>
```

A bare `<dl>` renders `dt` as a block and indents `dd` by the UA's `margin-inline-start: 40px`, so
label and value stack instead of forming a two-column row and every row costs double the height. In a
height-constrained surface (a dialog capped at 50vh) that is the difference between fitting and not.

Diagnose with the CSSOM query above: the rule text **is** present in the page (the other component
shipped it), but its selector carries a different `_ngcontent` attribute than your element. Present in
the CSSOM, absent from `getComputedStyle`, is the signature.

Fix by deciding where the rule belongs:

1. **Copy the declarations into the consuming component's own stylesheet** when the treatment is local
   to that component. Set `margin: 0` on `dd` explicitly, since you are now overriding a UA default.
2. **Promote it to global `styles.css`** only when it is genuinely shared page chrome, knowing that
   reflavors every current and future user of the class.

When delegating, name the file a reusable rule lives in and state whether it is global or
component-scoped. "Reuse the existing X styling" without that is an instruction to copy a class name,
which is exactly the failure.

## Cause 5: the font file cannot honour the weight you declared

`font-weight: 300` against a font family that only ships a static 400 face does not error, does not warn,
and does not fall back visibly. The browser either renders 400 outright or synthesizes a faux-light, so
the heading looks *approximately* right in a screenshot while being a different weight than the one the
design calls for. Nothing in the build, the CSSOM or `getComputedStyle` disagrees with you:
`getComputedStyle(el).fontWeight` faithfully returns `300` because that is what the cascade resolved. It
says nothing about what was rasterized.

The same trap sits in `@font-face`. Declaring `font-weight: 100 900` over a static file is legal CSS and
the browser accepts the range without checking the file, so the declaration is not evidence either.

**The cheap check comes first, and it is a grep, not a measurement.** Before reaching for `fontTools` or
advance widths, list the faces the app actually loads for that family:

```bash
grep -n -A4 "font-family: *['\"]?Montserrat" src/<app>/src/styles.css | grep -n "font-weight"
```

A display family is routinely loaded at heading weights only (700/800/900 and nothing lighter). An element
set in that family renders at the nearest AVAILABLE weight, so `font-weight: 400` on it is a no-op and the
text stays bold no matter what the declaration says. This is the shape the failure takes in a real app: a
list view whose value cells already declared `font-weight: 400` and still rendered bold, because the cells
carried `font-family: var(--font-display)` and that family had no face below 700.

**When the family has no face at the weight you want, the fix is the family, not the weight.** Dropping the
display-font override so the element inherits the body family (which does ship 300-700) is the only edit
that changes what is rasterized; editing the number again changes nothing and reads in the diff as though
it should have. So when a weight declaration is already correct and the text is still bold, stop editing
the weight and go look at which family the element is in.

**Prove the face is variable before you declare a weight it might not have.**

The reliable check is the font's table directory: a variable font carries an `fvar` (font variations) table.

```bash
python -c "from fontTools.ttLib import TTFont; print(sorted(TTFont('font.woff2').keys()))"
```

`fonttools` (with `brotli` for WOFF2) is the correct tool. If it is not available, decode the table
directory by hand, and know the trap that makes the obvious shortcut lie:

- **A byte-grep for the literal string `fvar` in a WOFF2 finds nothing even when the table is present.**
  WOFF2 replaces each 4-byte tag with a one-byte flag whose low 6 bits index a fixed known-tags table
  (`fvar` is index 47, `gvar` 48, `avar` 39). Only tags absent from that table (index 63) are written out
  literally, which is why `STAT` and `HVAR` *do* show up in a raw grep. Finding `STAT` is a good hint the
  font is variable; not finding `fvar` is not evidence of anything.

The empirical proof needs no tooling at all and is the one to fall back on: **measure advance widths
across the weight axis in the live page.**

```js
const el = document.createElement('span');
el.style.cssText = 'position:absolute;visibility:hidden;white-space:pre;font-size:100px;font-family:"YourFamily"';
el.textContent = 'Handgloves 0123456789';
document.body.appendChild(el);
const out = {};
for (const w of [100, 200, 300, 400, 500, 600, 700, 800, 900]) {
  el.style.fontWeight = w;
  out[w] = Math.round(el.getBoundingClientRect().width * 100) / 100;
}
el.remove(); out;
```

| Widths look like | Meaning |
| --- | --- |
| Distinct and monotonically increasing across the range | A real variable face: the engine is interpolating |
| One value repeated, with a jump only at 700 | A single static face plus synthetic bold |
| Two or three clusters | Only the static faces actually loaded; every other weight snaps to the nearest |

Distinct monotonic widths are the only evidence that a declared weight is genuinely rendered. Take that
measurement before you write a weight into a design token, and before you report a typography change as
done, because a screenshot cannot tell the difference and neither can review.

## Cause 6: the production build inlined critical CSS and the CSP blocked it

This one only appears **after deploying**. Local `ng serve` looks perfect, the production build is green,
and the deployed app renders with no styling at all: raw stacked text, no colours, no layout.

With `optimization.styles.inlineCritical` on (the default in a production configuration), the Angular
build rewrites the stylesheet link into a deferred load:

```html
<link rel="stylesheet" href="styles-XXXX.css" media="print" onload="this.media='all'">
```

The sheet is fetched but applies to `print` only until that inline `onload` handler flips `media`. Under a
`Content-Security-Policy` with `script-src 'self'` and no `'unsafe-inline'`, the browser refuses to run the
handler, `media` never flips, and the entire stylesheet stays inert. There is no build error and no failed
request: the CSS downloads with a 200 and simply never applies.

```jsonc
// angular.json → architect.build.configurations.production
"optimization": {
  "scripts": true,
  "fonts": true,
  "styles": { "minify": true, "inlineCritical": false }
}
```

Set it before the first deploy of any SPA that ships its own CSP, which is every container image whose
nginx or Caddy config sets security headers. Confirm it from the deployed page rather than the build log:

```js
[...document.querySelectorAll('link[rel=stylesheet]')].map(l => [l.href, l.media])
```

Any row whose media is still `print` is this bug. A console entry about a blocked inline event handler is
the corroborating signal, and it is easy to miss among CSP noise.

## Verify the reflow, do not assume it

Measure the outcome rather than trusting the rule you just wrote:

```js
const m = document.querySelector('.card-main').getBoundingClientRect();
const s = document.querySelector('.card-side').getBoundingClientRect();
({ sameLine: Math.abs(m.top - s.top) < 2, mainW: Math.round(m.width), sideW: Math.round(s.width) })
```

To check the wrap threshold without resizing the window (window resizing is unreliable when the window
is maximized), drive the container width in-page, measure at each step, and restore it:

```js
const el = document.querySelector('.grid'); const prev = el.style.cssText;
const out = {};
for (const w of [1100, 900, 760, 620]) {
  el.style.width = w + 'px'; el.getBoundingClientRect();
  const m = document.querySelector('.card-main').getBoundingClientRect();
  const s = document.querySelector('.card-side').getBoundingClientRect();
  out[w] = { sameLine: Math.abs(m.top - s.top) < 2 };
}
el.style.cssText = prev; out;
```

A screenshot remains the acceptance criterion; these reads are for locating the fault, not for signing
off on it.
