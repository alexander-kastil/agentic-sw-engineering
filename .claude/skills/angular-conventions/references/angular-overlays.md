# Angular Overlays, Dialogs & Popups

Patterns for modal dialogs, confirm popups, and any overlay UI. Covers ESC-to-close,
nested-overlay handling, and making native browser controls match a dark theme.

## Close-on-ESC as a reusable directive (not per-component listeners)

Do **not** scatter `@HostListener('document:keydown.escape')` across every component
that owns a popup. It does not compose: when a confirm dialog is shown over an edit
dialog, both listeners fire on ESC and both close — the user loses their whole form.

Instead use one attribute directive backed by a shared stack so only the **topmost**
overlay reacts. Because overlays live inside `@if (visible())`, the directive instance
is created/destroyed with the popup, so it self-registers and self-unregisters — no
`visible()` guard needed inside the handler.

```ts
// shared/close-on-escape/escape-stack.service.ts
import { Injectable } from '@angular/core';
import type { CloseOnEscape } from './close-on-escape.directive';

@Injectable({ providedIn: 'root' })
export class EscapeStack {
  private readonly stack: CloseOnEscape[] = [];
  push(dir: CloseOnEscape): void { this.stack.push(dir); }
  remove(dir: CloseOnEscape): void {
    const i = this.stack.lastIndexOf(dir);
    if (i !== -1) this.stack.splice(i, 1);
  }
  isTopmost(dir: CloseOnEscape): boolean {
    return this.stack[this.stack.length - 1] === dir;
  }
  hasOpen(): boolean { return this.stack.length > 0; }
}
```

```ts
// shared/close-on-escape/close-on-escape.directive.ts
import { Directive, HostListener, OnDestroy, OnInit, inject, output } from '@angular/core';
import { EscapeStack } from './escape-stack.service';

@Directive({ selector: '[appCloseOnEscape]' })
export class CloseOnEscape implements OnInit, OnDestroy {
  private readonly stack = inject(EscapeStack);

  // alias === selector → consume it like a native event: (appCloseOnEscape)="..."
  readonly closed = output<void>({ alias: 'appCloseOnEscape' });

  ngOnInit(): void { this.stack.push(this); }
  ngOnDestroy(): void { this.stack.remove(this); }

  // $event is typed Event, NOT KeyboardEvent — typing it KeyboardEvent is a TS2345
  // build error ("Argument of type 'Event' is not assignable to KeyboardEvent").
  @HostListener('document:keydown.escape', ['$event'])
  protected onEscape(event: Event): void {
    if (this.stack.isTopmost(this)) {
      event.stopPropagation();
      this.closed.emit();
    }
  }
}
```

Usage on each overlay root (the `@if`-gated element):

```html
<div class="fixed inset-0 ..." role="dialog" aria-modal="true"
     (appCloseOnEscape)="cancelled.emit()">
  ...
</div>
```

### Key points

- **`output({ alias: '<selector>' })`** lets the directive be bound like a native event.
  Just adding `(appCloseOnEscape)="..."` also satisfies the `[appCloseOnEscape]` selector,
  so no bare attribute is needed — exactly like `(click)`.
- **Topmost-only** dispatch fixes nested popups (confirm over dialog). Registration order
  follows component init order, so the most recently opened overlay is last in the stack.
- For a component that has **non-modal** inline ESC behavior (e.g. stop an inline video,
  collapse an inline panel) alongside directive-managed modals, keep its `@HostListener`
  but guard it: `if (this.escapeStack.hasOpen()) return;` so it defers to open overlays.
- Centralizing this also removes duplicated `host: { '(document:keydown.escape)': ... }`
  blocks from shared dialog components.

## Native browser controls in a dark theme

Native `<input type="time|date">` picker popups, `<select>` dropdown lists, calendar
popups, and scrollbars are rendered by the browser, not your CSS — they default to the
OS light theme and look wrong inside a dark dialog. Opt every native control into dark
rendering with one line:

```css
/* styles.css */
html,
body {
  color-scheme: dark;
}
```

This is the correct fix — not re-skinning each control with brittle
`::-webkit-calendar-picker-indicator` / `appearance: none` hacks. Verify the actual
native popup (open the time picker) in Chrome, since the picker chrome is outside the
DOM/a11y snapshot and only shows in a screenshot.
