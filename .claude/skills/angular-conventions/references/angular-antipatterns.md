# Angular Anti-Patterns

Patterns that must not appear in Angular v22+ code.

## Dependency Injection

| Wrong | Correct |
|---|---|
| `constructor(private svc: UserService)` | `svc = inject(UserService)` |
| `@Injectable({ providedIn: 'root' })` with constructor DI | Use `inject()` in field initializer |

## Templates

| Wrong | Correct |
|---|---|
| `*ngIf="condition"` | `@if (condition) { }` |
| `*ngFor="let x of list"` | `@for (x of list; track x.id) { }` |
| `*ngSwitch` | `@switch (val) { @case ('x') { } }` |
| `[ngClass]="{ active: flag }"` | `[class.active]="flag()"` |
| `[ngStyle]="{ color: val }"` | `[style.color]="val()"` |
| `@HostBinding` / `@HostListener` | `host: { '[class.x]': '...', '(click)': '...' }` |
| A scoped `--open` modifier class that silently fails to apply | Drive state-carrying properties with `[style.prop]` bindings — see `angular-disclosure-panels.md` |

## State Management

| Wrong | Correct |
|---|---|
| `BehaviorSubject` for local state | `signal()` |
| `Observable`-only state without signals | Combine with `toSignal()` or use `resource()` |
| `subscribe()` in component body | `toSignal()`, async pipe, or `resource()` |
| `@ngrx/store` class-based reducers | NgRx Signal Store (`withState`, `withMethods`) |

## Signal inputs

| Wrong | Correct |
|---|---|
| Reading a required `input()` from a field initializer | Read it from `computed`, `linkedSignal`, `effect`, or a lifecycle hook |
| `signal({ x: this.someComputedOnInput() })` as a field | `linkedSignal({ source: () => this.input().id, computation: () => ({ ... }) })` |

Required inputs are not set until after construction, so touching one while instance fields initialize throws
**`NG0950: Input "x" is required but no value is available yet`**. The failure mode is nasty: the component
never constructs, so the enclosing `@if` renders *nothing* while the button that toggles it still flips state.
It reads as "the feature was never built" rather than as an error, and the only evidence is the console.

```ts
// WRONG: calls a computed that reads this.item() during field init
protected readonly model = signal<Form>({ title: this.defaultTitle(), body: '' });

// RIGHT: lazy, and re-derives only when the selected record actually changes
protected readonly model = linkedSignal<number, Form>({
  source: () => this.item().id,
  computation: () => ({ title: this.defaultTitle(), body: '' }),
});
```

Key the `source` on a stable id rather than the object itself: a re-emitted identical object would otherwise
reset the signal and wipe whatever the user had typed. `linkedSignal` stays writable, so Signal Forms can bind
to it directly.

## Architecture

| Wrong | Correct |
|---|---|
| `NgModule` for feature organization | Standalone imports |
| `import CommonModule` | Import specific directives/pipes |
| `standalone: true` in decorator | Omit — standalone is the default in v20+ |
| Default change detection on components | `ChangeDetectionStrategy.OnPush` |

## Data Loading

| Wrong | Correct |
|---|---|
| Manual `http.get()` + `BehaviorSubject` wiring | `httpResource()` or `resource()` |
| `subscribe()` in `ngOnInit` for HTTP | `resource()` with declarative loader |

## Testing

| Wrong | Correct |
|---|---|
| Testing private methods | Test public behavior and outputs |
| Skipping error scenarios | Always test happy path + error + edge cases |
| No service mocking | Mock all external dependencies |
| `jasmine.createSpyObj` | `vi.fn()` (Vitest project uses Vitest APIs) |

## Removing Angular Material

Deleting `@angular/material` / `@angular/cdk` imports is necessary but **not sufficient** — component SCSS can still *reproduce* the Material look after the package is gone. When de-Materializing a component or app, also grep for and strip Material-mimic CSS:

| Mimic pattern | What it looks like |
|---|---|
| Elevation shadow | A `box-shadow` triple matching `0 3px 1px -2px rgba(...), 0 2px 2px 0 ..., 0 1px 5px 0 ...` (Material's elevation mixin output, hand-copied into plain CSS) |
| Material font | `font-family: Roboto` |
| Material tracking | `letter-spacing: 0.0892857143em` |

Teardown checklist:

1. `grep -rE "@angular/(material|cdk)" src` returns zero matches.
2. No `mat-`/`cdk-` markup remains in any template.
3. The Material theme import is gone from `styles.scss`.
4. No Material-mimic CSS (table above) remains in component styles.
5. Build is green.

For the full migration playbook (orchestration, the one-custom-component rule, verification
hygiene) see the `.claude/skills/tailwind-migration/` skill.

## Visually-hidden text & CSS animation

A "constant-footprint" indicator (loader, spinner, status badge shown only while busy) must occupy **identical layout** whether active or idle, or its neighbors shift when the busy state toggles. CSS transforms (`scale`, `translate`) don't affect layout; conditionally-rendered *in-flow* nodes — including screen-reader text — do.

| Wrong | Correct |
|---|---|
| `class="sr-only"` assuming a global visually-hidden utility exists | Scope the rule in the component's own styles (`position:absolute; width:1px; height:1px; margin:-1px; clip:rect(0 0 0 0); overflow:hidden; white-space:nowrap; border:0`) — many apps (and non-configured Tailwind builds) have **no** global `.sr-only`, so the "hidden" text renders in-flow and takes width |
| `@if (active()) { <span class="sr-only">Loading…</span> }` — inserting/removing the a11y text node per state | Keep the node **always present**; toggle only its text content and `aria-hidden`/`role`. Adding/removing an in-flow node reflows siblings → a visible horizontal jump the moment the state ends |
| `animation-play-state: paused` to "stop" a looping animation when idle | Freezes it on whatever random mid-cycle frame it reached. Use `animation: none` in the idle state and attach the `animation` shorthand only under the active class (`.x--active .dot { animation: … }`) so each activation restarts cleanly from 0% |

Verify a constant-footprint indicator by sampling a neighbor's `getBoundingClientRect().left` across idle→active→idle — it must not move.

## Component Composition

| Wrong | Correct |
|---|---|
| Re-hosting a shared form/table pair but binding only inputs, hard-pinning selection (`entries()[0]`) | Diff the new host against the canonical host's template and wire every output too (`(selectEntry)`, `(entryChange)`) plus selection state |
| Selection without feedback (row click changes state but no visual) | Pass a `selectedId` input and render the `bg-surface-alt` selected style (voucher-list convention) |

Real case: `voucher-booking-wiz` embedded `voucher-edit-table` without `(selectEntry)` while `voucher-edit-container` binds it — booking lines looked dead ("details not editable").


## A control whose only feedback lives in a conditionally-rendered panel

```html
@if (wideLayout() || activeTab() === 'preview') {
  <app-preview [media]="store.selected()" />
}
```

```html
<button (click)="store.select(item)">...</button>
```

Clicking the button updates the store correctly and the user sees nothing, because the element that would show the change is not in the DOM. The default tab is the other one. Every part of the data path works and the control reads as dead.

- A `@if` on a tab, a disclosure or a breakpoint removes the output element, so a correct signal write has nowhere to land. `@if` is not `[hidden]`: there is no element to inspect and no transition to notice.
- Any control whose only feedback lives in a conditionally-rendered panel must bring that panel forward when it fires. Emit from the control, and let the shell switch the tab or open the panel.
- Diagnose it the same way: before tracing the handler or the store, click the control in the running page and read back both the state and whether the output element exists. `document.querySelector('[data-testid="..."]')` returning null is the answer, not the state being wrong.
- The wide-layout arm of the condition hides the bug on your machine: at a width where both panels render, the same click looks fine.
