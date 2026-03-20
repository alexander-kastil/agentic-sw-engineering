---
name: optimize-a11y
description: Audit and fix accessibility issues in web UI code to meet WCAG 2.2 Level AA. Use when asked to make a page or component accessible, fix a11y issues, add keyboard support, improve screen reader compatibility, fix contrast, add ARIA, implement skip links, fix form labels, handle focus management, support forced colors / high contrast mode, or ensure reflow at 320px. Keywords: accessibility, a11y, WCAG, screen reader, keyboard navigation, ARIA, focus, contrast, high contrast, reflow, landmarks, skip link, aria-label, alt text.
---

# Accessibility Optimization Skill

Expert web accessibility implementation following WCAG 2.2 Level AA. Audits and fixes accessibility issues across structure, keyboard, contrast, ARIA, forms, images, and responsive reflow.

## When to Use This Skill

- Making a page or component WCAG 2.2 AA conformant
- Adding keyboard operability or fixing keyboard traps
- Fixing focus visibility or tab order
- Adding or correcting ARIA roles, names, states, and properties
- Fixing color contrast failures
- Supporting OS High Contrast / Forced Colors mode
- Fixing form labels, error messages, and validation feedback
- Adding alt text or hiding decorative graphics
- Implementing skip links or landmark structure
- Fixing layout to reflow correctly at 320px

## Prerequisites

- Access to the HTML/CSS/JS or component source files
- Knowledge of any UI component library in use (Fluent UI, Material, shadcn/ui, etc.)
- Browser DevTools or Accessibility Insights for verification

## Non-Negotiable Rules

1. **Conform to WCAG 2.2 Level AA** minimum; go beyond when it meaningfully improves usability.
2. **Use the project's component library** patterns first. Do not recreate patterns — find an existing usage and follow it.
3. **Prefer native HTML** over ARIA. Add ARIA only when native semantics are insufficient.
4. **Do not claim output is "fully accessible"** — recommend manual review with Accessibility Insights.

## Step-by-Step Workflow

### 1. Audit the Component or Page

Check for issues in this order:

1. **Structure** — landmarks (`header`, `nav`, `main`, `footer`), heading hierarchy (one `h1`), descriptive `<title>`.
2. **Keyboard** — every interactive element reachable by Tab, visible focus ring, no traps, static content not tabbable.
3. **Skip link** — first focusable element skips to `#maincontent`.
4. **Labels** — every control has a visible label; accessible name contains the visible label text.
5. **Forms** — `<label for>`, `aria-required`, `aria-invalid`, `aria-describedby` for errors and help text.
6. **Contrast** — text ≥ 4.5:1 (large text ≥ 3:1), focus indicators and control borders ≥ 3:1.
7. **Color** — information is never conveyed by color alone; pair with text/icon.
8. **Forced Colors** — no broken UI in `@media (forced-colors: active)`; SVG uses `currentColor`.
9. **Reflow** — layout stacks to single column at 320px; no two-dimensional scrolling for text.
10. **Images/SVGs** — informative: `alt` or `aria-label`; decorative: `alt=""` or `aria-hidden="true"`.

### 2. Apply Fixes

#### Skip link (add as first focusable element in `<header>`)

```html
<header>
  <a href="#maincontent" class="sr-only">Skip to main content</a>
</header>
<main id="maincontent" tabindex="-1">
  <h1>Page title</h1>
</main>
```

```css
.sr-only:not(:focus):not(:active) {
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
```

#### Form with accessible label, required indicator, and inline error

```html
<label for="email">
  Email <span aria-hidden="true">*</span>
</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">Enter a valid email address.</span>
```

- On submit with invalid input: focus the first invalid control.
- Remove `aria-invalid` when the field becomes valid.

#### Composite widget (roving tabindex)

```html
<ul role="listbox" aria-label="Options">
  <li role="option" tabindex="0" aria-selected="true">Item 1</li>
  <li role="option" tabindex="-1">Item 2</li>
</ul>
```

- Arrow keys move focus: swap `tabindex` values and call `.focus()`.

#### Forced Colors support

```css
/* Use currentColor for SVG icons */
svg { fill: currentColor; stroke: currentColor; }

/* Replace box-shadow focus rings with a visible outline */
.button:focus {
  box-shadow: 0 0 4px 3px rgba(90, 50, 200, .7);
  outline: 2px solid transparent; /* renders in forced-colors */
}

@media (forced-colors: active) {
  .button {
    border: 2px solid ButtonBorder;
  }
}
```

#### Reflow at 320px

```css
/* Fluid flex/grid layout */
.container { display: flex; flex-wrap: wrap; }
.item { min-width: 0; flex: 1 1 200px; }

/* Images and media */
img, video, iframe { max-width: 100%; }

/* Handle long strings */
p, td { overflow-wrap: anywhere; }
```

#### Color tokens (define once, use everywhere)

```css
:root {
  --color-bg: #ffffff;
  --color-text: #1a1a1a;
  --color-muted-text: #595959; /* ≥ 4.5:1 on white */
  --color-link: #0057b8;
  --color-border: #767676;
  --color-focus: #005fcc;
  --color-danger: #b91c1c;
  --color-success: #166534;
}
```

### 3. Final Verification Checklist

Before completing, explicitly verify each item:

| Area          | Check                                                                                                       |
| ------------- | ----------------------------------------------------------------------------------------------------------- |
| Structure     | Landmarks present; headings sequential; one `h1` per page                                                   |
| Keyboard      | All controls keyboard-operable; visible focus; no traps; skip link works                                    |
| Labels        | Every control has visible label; accessible name contains visible text                                      |
| Forms         | `<label for>`, `aria-required`, `aria-invalid` + `aria-describedby` on error; focus first invalid on submit |
| Contrast      | Text ≥ 4.5:1 (large ≥ 3:1); focus/borders ≥ 3:1; no color-only cues                                         |
| Forced Colors | UI intact in `forced-colors: active`; SVG uses `currentColor`; no `forced-color-adjust: none`               |
| Reflow        | Single-column at 320px; no two-dimensional scroll for text; controls remain operable                        |
| Graphics      | Informative: meaningful `alt`/`aria-label`; decorative: hidden                                              |
| Tables/Grids  | `<th>` for headers; grids structured with rows and cells                                                    |

## Inclusive Language Rules

- Use people-first, respectful language in user-facing text.
- Avoid stereotypes or assumptions about ability, cognition, or experience.
- Prefer plain language; keep interface clean and simple.

## References

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [Accessibility Insights](https://accessibilityinsights.io/)
- [Forced Colors explainer](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors)
