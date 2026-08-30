# Angular Bottom Sheet (Native `<dialog>`, No CDK)

In apps with **no Angular Material and no `@angular/cdk`**, the natural modal
primitive is the native `<dialog>` element — opened imperatively with
`showModal()`/`close()` and styled via a shared `.dialog` layer. A bottom sheet
is just a variant of that same convention: instead of a centered card, the
`<dialog>` is pinned to the bottom of the viewport, full-width, and slides up on
open. Reuse the app's existing dialog styling (titlebar / close button / body);
only the outer geometry and entrance transition differ.

> **Two component shapes.** Native `<dialog>` modals in Angular tend to appear in
> one of two shapes — pick per use:
>
> 1. **Component owns its `<dialog>` internally** — exposes public
>    `open()`/`close()` methods; the host embeds `<app-x-bottom-sheet #sheet>`
>    once and drives it imperatively (`this.sheet().open()`). This is the shape
>    below — the one meant to be dropped into a host template and driven from
>    outside.
> 2. **Container drives a `<dialog #ref>` element directly** — via
>    `viewChild<ElementRef<HTMLDialogElement>>` + an `effect()` reacting to a
>    signal. Prefer this only when the dialog is tightly bound to one parent's
>    state.
>
> The bottom sheet follows shape 1.

## When to use a bottom sheet vs. a centered `.dialog`

| Use `.dialog` (centered) when… | Use a bottom sheet when… |
| --- | --- |
| The content is a form or needs the user's full attention (confirmations, edit forms) | The content is a short list of actions or a compact status/detail panel (a quick-actions menu, a mobile-friendly detail card) |
| Desktop-first content, comfortable at any viewport width | Content reads naturally full-width and anchored to a thumb-reachable zone on mobile/tablet |
| The interaction should feel modal and centered | The interaction should feel like a drawer sliding up from the device edge |

Both variants are native `<dialog>` under the hood — same `showModal()` /
`close()` mechanics, same `::backdrop` scrim, same focus-trap behavior. Only
the geometry and entrance transition differ.

## Design decisions

| Concern | Decision | Why |
| --- | --- | --- |
| Modal primitive | Native `<dialog>` + `showModal()`/`close()` | No CDK overlay available; the `<dialog>` is in the top layer already |
| Component shape | The bottom sheet owns its `<dialog>` internally (`viewChild` + private show/hide) and exposes public `open()`/`close()` | The host embeds `<app-x-bottom-sheet #sheet>` once and drives it imperatively, instead of owning the `<dialog>` ref itself |
| Positioning | `position: fixed`, `inset: auto 0 0 0`, `width: 100%`, geometry set on the `<dialog>` itself (not a wrapping `<div>`) so the UA's default `dialog[open]` centering is overridden | A `<dialog>` is top-layer already; no extra stacking context or portal needed |
| Entrance transition | CSS `transition` on `transform: translateY(...)`, toggled by an `[open]`-scoped class flip on the next frame (`requestAnimationFrame`) after `showModal()` | `showModal()` makes the dialog visible instantly (no CSS transition fires on the `display: none → flex` jump); animating a `transform` after paint gives the slide-up without the View Transitions API |
| Backdrop | `::backdrop` on the same `<dialog>` | Free with the native element; no extra scrim `<div>` |
| Close affordances | Drag handle / explicit close button (click) + native `cancel` event (Esc) + backdrop click (`mousedown` on `event.target === dialogEl`) | Covers the standard Esc-to-close and click-outside conventions |
| Focus | `showModal()` auto-focuses the first focusable descendant and traps Tab; on close, refocus the element that had focus before opening (captured in `open()`) | WCAG AA — focus must return to the trigger, not silently reset to `<body>` |
| Change detection | `ChangeDetectionStrategy.OnPush`, all state in `signal()` | Standalone-Angular house style |

## Minimal working example

### `x-bottom-sheet.component.ts`

```typescript
import { ChangeDetectionStrategy, Component, ElementRef, signal, viewChild } from '@angular/core';

/**
 * Generic bottom sheet shell — embed once per host (`<app-x-bottom-sheet #sheet>`)
 * and drive it imperatively via `open()`/`close()`:
 *
 *   <app-x-bottom-sheet #sheet>
 *     <span sheet-title>Quick actions</span>
 *     ...projected content...
 *   </app-x-bottom-sheet>
 *   ...
 *   this.sheet().open();
 */
@Component({
  selector: 'app-x-bottom-sheet',
  templateUrl: './x-bottom-sheet.component.html',
  styleUrls: ['./x-bottom-sheet.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class XBottomSheetComponent {
  private readonly dialogEl = viewChild<ElementRef<HTMLDialogElement>>('sheetEl');

  /** Drives the slide-up transition — false immediately after `showModal()`,
   * flipped true one frame later so the `transform` transition actually fires
   * (see "Entrance transition" above). */
  protected readonly visible = signal(false);

  private lastFocused: HTMLElement | null = null;

  open(): void {
    const el = this.dialogEl()?.nativeElement;
    if (!el || el.open) return;

    this.lastFocused = document.activeElement as HTMLElement | null;
    el.showModal();

    requestAnimationFrame(() => this.visible.set(true));
  }

  close(): void {
    const el = this.dialogEl()?.nativeElement;
    if (!el || !el.open) return;

    this.visible.set(false);
    // Let the slide-down transition play before the native close() removes
    // the dialog from the top layer — match the transition duration in the
    // stylesheet (200ms). Skip the wait if the user prefers reduced motion.
    const prefersReducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    const delay = prefersReducedMotion ? 0 : 200;
    setTimeout(() => el.close(), delay);
  }

  /** Native `cancel` fires on Esc before `close`; add `preventDefault()` here
   * only if the host needs a "confirm before dismiss" guard. */
  protected onDialogClosed(): void {
    this.visible.set(false);
    this.lastFocused?.focus();
    this.lastFocused = null;
  }

  /** Closes on a backdrop click — `showModal()` puts click targets for the
   * backdrop itself on the `<dialog>` element (not a descendant), so comparing
   * `event.target` to the dialog element distinguishes a backdrop click from
   * a click inside the sheet content. */
  protected onBackdropClick(event: MouseEvent): void {
    if (event.target === this.dialogEl()?.nativeElement) {
      this.close();
    }
  }
}
```

### `x-bottom-sheet.component.html`

Reuse the app's shared dialog classes (titlebar / close / body) — only the outer
`<dialog>` and the drag handle are bottom-sheet-specific:

```html
<dialog
  #sheetEl
  class="x-bottom-sheet"
  [class.x-bottom-sheet--visible]="visible()"
  (close)="onDialogClosed()"
  (mousedown)="onBackdropClick($event)"
>
  <div class="x-bottom-sheet__handle" aria-hidden="true"></div>

  <div class="dialog__titlebar">
    <span class="dialog__title"><ng-content select="[sheet-title]" /></span>
    <button type="button" class="dialog__close" aria-label="Close" (click)="close()">✕</button>
  </div>

  <div class="dialog__body">
    <ng-content />
  </div>
</dialog>
```

### `x-bottom-sheet.component.scss`

```scss
// Bottom-sheet variant of the shared `.dialog` shell — reuses the app's
// `.dialog__titlebar`/`.dialog__title`/`.dialog__close`/`.dialog__body` classes
// verbatim; only the outer `<dialog>` geometry + transition differ from the
// centered dialog shell.
.x-bottom-sheet {
  box-sizing: border-box;
  position: fixed;
  inset: auto 0 0 0;
  width: 100%;
  max-width: none;
  max-height: min(80vh, 720px);
  margin: 0;
  padding: 0;
  border: none;
  border-radius: 12px 12px 0 0;
  box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  transform: translateY(100%);
  transition: transform 200ms ease-out;

  // Scope to `&[open]`: `dialog:not([open]) { display: none }` is a UA rule that
  // an unconditional author `display` would incorrectly out-cascade.
  &[open] {
    display: flex;
    flex-direction: column;
  }

  &.x-bottom-sheet--visible {
    transform: translateY(0);
  }

  &::backdrop {
    background: rgba(28, 28, 28, 0.5);
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
}

.x-bottom-sheet__handle {
  flex: 0 0 auto;
  width: 36px;
  height: 4px;
  margin: 8px auto 0;
  border-radius: 2px;
  background: var(--divider-color, #d4d0c8);
}
```

Swap the hardcoded colors for the host design system's tokens (divider / scrim /
accent) when reusing.

### Usage from a host

```html
<!-- host.component.html -->
<app-x-bottom-sheet #sheet>
  <span sheet-title>Quick actions</span>
  <!-- any projected content -->
</app-x-bottom-sheet>

<button type="button" (click)="sheet().open()">Open</button>
```

```typescript
// host.component.ts
import { Component, viewChild } from '@angular/core';
import { XBottomSheetComponent } from '../shared/x-bottom-sheet/x-bottom-sheet.component';

@Component({
  selector: 'app-host',
  templateUrl: './host.component.html',
  imports: [XBottomSheetComponent],
})
export class HostComponent {
  protected readonly sheet = viewChild.required(XBottomSheetComponent);
}
```

## Testing

Follow `angular-testing.md`'s Vitest conventions. `jsdom` does not implement
`HTMLDialogElement.showModal`/`close`, so polyfill them in your test setup
(toggling the `open` attribute) — then `sheet().open()` / `sheet().close()` work
in specs without further mocking:

```typescript
it('opens and closes the sheet, returning focus to the trigger', async () => {
  const trigger: HTMLButtonElement = fixture.nativeElement.querySelector('button');
  trigger.focus();

  component.sheet().open();
  fixture.detectChanges();
  expect(fixture.nativeElement.querySelector('dialog').hasAttribute('open')).toBe(true);

  component.sheet().close();
  await new Promise((r) => setTimeout(r, 0));
  expect(document.activeElement).toBe(trigger);
});
```
