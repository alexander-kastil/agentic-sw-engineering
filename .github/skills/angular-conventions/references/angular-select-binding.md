# A plain-bound `<select>` shows nothing selected

Binding a native `<select>` without a forms API: no `ngModel`, no reactive `formControlName`, no signal
form `[formField]`. Under those APIs Angular sets the selection after the options exist and this bug
cannot happen, which is why it only ever bites the plain-binding case: a small dialog, a filter bar, a
component that keeps its state in a `signal()` and reads `(change)`.

## The symptom

The control renders with `value=""`. Neither the create-mode default nor an edit-mode prefill shows,
and the user sees a blank or first-option dropdown even though the state signal holds the right value.

```html
<select [value]="type()" (change)="type.set($any($event.target).value)">
  @for (k of kinds; track k) {
    <option [value]="k">{{ k }}</option>
  }
</select>
```

## Why

`[value]` on the `<select>` and `[value]` on each `<option>` are separate bindings, and the parent
element's binding is applied first. At the moment the select's value is assigned, its options either do
not exist yet or still carry empty values, so there is no option to match. The DOM rejects the
assignment and leaves `value` as the empty string. Nothing re-runs the select's binding afterwards,
because `type()` has not changed.

## The fix: put the state on the options

```html
<select (change)="type.set($any($event.target).value)">
  @for (k of kinds; track k) {
    <option [value]="k" [selected]="type() === k">{{ k }}</option>
  }
</select>
```

Each option decides its own selected state, so the binding order stops mattering: whichever option
matches is marked at the time its own bindings run. This works identically for a static option list
and for `@for`, and for an enum whose members are exposed on the component as a `readonly Kind = Kind`
field.

## How to prove it

Invisible to a type check and to a reading of the template, because both versions are valid Angular.
Assert the rendered selection, not the component state:

```typescript
const select: HTMLSelectElement = fixture.nativeElement.querySelector('select');
expect(select.value).toBe(Kind.A);
```

A spec that only asserts `component.type()` passes against the broken template. If a select prefill has
ever regressed in the app, that assertion is the one that was missing.

## Related

- Under Signal Forms the equivalent trap is a type mismatch, not an ordering one: a `<select>` bound
  with `[formField]` needs the field typed `string`, so an integer id must be declared as `string` in
  the form model and cast back on submit. See [`angular-forms`](angular-forms.md).
