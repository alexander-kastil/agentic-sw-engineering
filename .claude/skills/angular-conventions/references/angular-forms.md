# Angular Signal Forms

Build type-safe, reactive forms using Angular's Signal Forms API. Signal Forms provide automatic two-way binding, schema-based validation, and reactive field state.

Signal Forms (`form()` + `[formField]` from `@angular/forms/signals`) are the mandated standard for Angular 22+ signal-based applications, used for every input including single-field ones like a year dropdown. Do not replace `form()`/`FormField` with plain `linkedSignal` + native `[value]`/`(change)` bindings, and do not switch such an app back to Reactive Forms. Specs or optimization docs that recommend "replace `form()` with a plain signal for simple selects" should be pushed back on, not applied. Removing `FormField` imports or rewriting to native bindings breaks pattern consistency and will be rejected. When in doubt, keep Signal Forms. Reactive Forms patterns at the bottom of this file are retained only for maintenance of legacy codebases and for complex, dynamic forms in existing codebases.

**Stability caveat.** Signal Forms are recommended for new signal-based applications and are shipped and fully functional as of Angular **22** — `@angular/forms/signals` is present and works, and the 21 → 22 upgrade brought no Signal Forms API delta (`form()`, `FormField`, `required()`, `email()`, `disabled()`, `hidden()` are unchanged). But **every exported symbol is still `@experimental` in 22**. Signal Forms is the standard for signal-based apps, but re-verify the API surface whenever `@angular/core`/`@angular/forms` are upgraded, since experimental signatures can change.

## Gotchas

### No HTML validation attributes on `[formField]`

Do not put `required`, `maxlength`, `minlength`, or any other HTML validation attribute on an element that has `[formField]`. Angular raises NG8022 at compile time.

```typescript
// WRONG — causes NG8022
// <input [formField]="form.name" required maxlength="100" />

// CORRECT — use schema validators
const myForm = form(this.model, (s) => {
  required(s.name, { message: 'Name is required' });
  maxLength(s.name, 100, { message: 'Max 100 characters' });
});
```

### Integer ID fields must be `string` in the form model

`[formField]` on a `<select>` expects the bound field to be typed as `string`. If an ID field (e.g. `typeId`, `contractId`, `memberId`) is typed as `number | null` in the form model, the select binding will not round-trip correctly. Declare the field as `string` in the form interface and cast back to a number when emitting.

```typescript
interface ContractFormData {
  typeId: string;
  memberId: string;
  amount: number | null;
}

const model = signal<ContractFormData>({ typeId: '', memberId: '', amount: null });
const contractForm = form(model);
```

```html
<select [formField]="contractForm.typeId">
  @for (t of types(); track t.id) {
    <option [value]="t.id">{{ t.name }}</option>
  }
</select>
```

```typescript
onSave() {
  const f = this.model();
  const payload = {
    typeId: f.typeId ? +f.typeId : null,
    memberId: f.memberId ? +f.memberId : null,
    amount: f.amount,
  };
}
```

### Native time inputs — enforcing minute steps

`<input type="time" step="300">` (300s = 5 min) restricts spinner increments and constraint
validation to 5-minute marks, but does **not** restrict Chrome's dropdown/list time picker —
that list still offers every minute (00, 01, 02 …). `step` alone cannot force 5-minute-only
selection.

Pair `step` with a snap-to-nearest-step correction on `(change)`, so a picker click or pasted
value gets rounded after the fact. Reuse an existing helper rather than reimplementing it — e.g.
a `roundTimeStringToStep(time, stepMinutes)` util under the app's shared utils
(`<app>/shared/utils/time-functions.ts`, unit-tested in `time-functions.spec.ts`). Wire it into
the start/end time fields of the component's `.ts` and `.html` like this:

```typescript
snapTimeToStep(controlName: 'StartTime' | 'EndTime', event: Event): void {
  const value = (event.target as HTMLInputElement).value;
  const rounded = roundTimeStringToStep(value, 5);
  // patch rounded value back into the form model
}
```

```html
<input type="time" step="300" [formField]="form.StartTime" (change)="snapTimeToStep('StartTime', $event)" />
```

Whenever a native time field must be constrained to N-minute intervals, use **both**
`step` (spinner/validity + a11y) **and** the snap-on-change correction (gates the picker
list and any typed/pasted value).

## Basic Setup

```typescript
import { Component, signal } from '@angular/core';
import { form, FormField, required, email } from '@angular/forms/signals';

interface LoginData {
  email: string;
  password: string;
}

@Component({
  selector: 'app-login',
  imports: [FormField],
  template: `
    <form (submit)="onSubmit($event)">
      <label>
        Email
        <input type="email" [formField]="loginForm.email" />
      </label>
      @if (loginForm.email().touched() && loginForm.email().invalid()) {
        <p class="error">{{ loginForm.email().errors()[0].message }}</p>
      }
      
      <label>
        Password
        <input type="password" [formField]="loginForm.password" />
      </label>
      @if (loginForm.password().touched() && loginForm.password().invalid()) {
        <p class="error">{{ loginForm.password().errors()[0].message }}</p>
      }
      
      <button type="submit" [disabled]="loginForm().invalid()">Login</button>
    </form>
  `,
})
export class Login {
  // Form model - a writable signal
  loginModel = signal<LoginData>({
    email: '',
    password: '',
  });
  
  // Create form with validation schema
  loginForm = form(this.loginModel, (schemaPath) => {
    required(schemaPath.email, { message: 'Email is required' });
    email(schemaPath.email, { message: 'Enter a valid email address' });
    required(schemaPath.password, { message: 'Password is required' });
  });
  
  onSubmit(event: Event) {
    event.preventDefault();
    if (this.loginForm().valid()) {
      const credentials = this.loginModel();
      console.log('Submitting:', credentials);
    }
  }
}
```

## Boolean toggles / checkbox binding

`[formField]` binds natively to `<input type="checkbox">` via `element.checked` and the
`input`/`blur` DOM events — no custom `FormValueControl` wrapper is needed for a boolean field.

```html
<input type="checkbox" [formField]="settingsForm.enabled" />
```

```typescript
enabledModel = signal({ enabled: false });
enabledForm = form(this.enabledModel);
```

Where an app renders boolean toggles as a slide-toggle rather than a bare checkbox, the real
`<input>` stays under a shared `.toggle` component (e.g. `theme/components.scss`) — visually
hidden but focusable, with `role="switch"`:

```html
<label class="toggle">
  <input type="checkbox" role="switch" class="toggle__input" [formField]="testForm.enabled" aria-label="Testen" />
  <span class="toggle__track"></span>
  <span class="toggle__label">Testen</span>
</label>
```

**One-element variant, where the app has no shared component to hang the spans on.** Style the input
itself with `appearance: none` and draw the thumb with `::after`, so there is no track or label span
and nothing to keep in sync:

```html
<label class="switch">
  <input type="checkbox" role="switch" [formField]="detailForm.mfa" />
  MFA
</label>
```

```css
.switch input { appearance: none; position: relative; width: 2.75rem; height: 1.5rem; border-radius: var(--radius-pill); }
.switch input::after { content: ''; position: absolute; top: 50%; left: 0.15rem; width: 1.1rem; height: 1.1rem; transform: translateY(-50%); border-radius: 50%; transition: left 0.15s ease; }
.switch input:checked::after { left: calc(100% - 1.25rem); }
```

Same guarantees as the three-span version, because the input is still a real focusable checkbox:
`[formField]`, keyboard, and `role="switch"` all behave. Pick the shared component where one exists;
pick this where adding one would be the only reason to create a component. Either way the shared CSS
lives in one file (`shared/styles/toggle.css`) that component styles `@import`, never inline per screen.
Check for an existing toggle in the repo before writing a third variant.

**Dynamic-key boolean fields** — a `Record<string, boolean>` model whose keys are only known at
runtime (e.g. one boolean per dynamic table column) works the same way, because
`FieldTree<Record<string, boolean>>` structurally has an index signature:

```typescript
boolModel = signal<Record<string, boolean>>({});
boolForm = form(this.boolModel);
```

```html
<input type="checkbox" [formField]="boolForm[col.Name]" />
```

## Form Models

Form models are writable signals that serve as the single source of truth:

```typescript
// Define interface for type safety
interface UserProfile {
  name: string;
  email: string;
  age: number | null;
  preferences: {
    newsletter: boolean;
    theme: 'light' | 'dark';
  };
}

// Create model signal with initial values
const userModel = signal<UserProfile>({
  name: '',
  email: '',
  age: null,
  preferences: {
    newsletter: false,
    theme: 'light',
  },
});

// Create form from model
const userForm = form(userModel);

// Access nested fields via dot notation
userForm.name                    // FieldTree<string>
userForm.preferences.theme       // FieldTree<'light' | 'dark'>
```

### Reading Values

```typescript
// Read entire model
const data = this.userModel();

// Read field value via field state
const name = this.userForm.name().value();
const theme = this.userForm.preferences.theme().value();
```

### Updating Values

```typescript
// Replace entire model
this.userModel.set({
  name: 'Alice',
  email: 'alice@example.com',
  age: 30,
  preferences: { newsletter: true, theme: 'dark' },
});

// Update single field
this.userForm.name().value.set('Bob');
this.userForm.age().value.update(age => (age ?? 0) + 1);
```

## Field State

Each field provides reactive signals for validation, interaction, and availability:

```typescript
const emailField = this.form.email();

// Validation state
emailField.valid()      // true if passes all validation
emailField.invalid()    // true if has validation errors
emailField.errors()     // array of error objects
emailField.pending()    // true if async validation in progress

// Interaction state
emailField.touched()    // true after focus + blur — ONLY for [formField]-bound controls
emailField.dirty()      // true after user modification

// Availability state
emailField.disabled()   // true if field is disabled
emailField.hidden()     // true if field should be hidden
emailField.readonly()   // true if field is readonly

// Value
emailField.value()      // current field value (signal)
```

### Form-Level State

The form itself is also a field with aggregated state:

```typescript
// Form is valid when all interactive fields are valid
this.form().valid()

// Form is touched when any field is touched
this.form().touched()

// Form is dirty when any field is modified
this.form().dirty()
```

## Validation

### Built-in Validators

```typescript
import { 
  form, required, email, min, max, 
  minLength, maxLength, pattern 
} from '@angular/forms/signals';

const userForm = form(this.userModel, (schemaPath) => {
  // Required field
  required(schemaPath.name, { message: 'Name is required' });
  
  // Email format
  email(schemaPath.email, { message: 'Invalid email' });
  
  // Numeric range
  min(schemaPath.age, 18, { message: 'Must be 18+' });
  max(schemaPath.age, 120, { message: 'Invalid age' });
  
  // String/array length
  minLength(schemaPath.password, 8, { message: 'Min 8 characters' });
  maxLength(schemaPath.bio, 500, { message: 'Max 500 characters' });
  
  // Regex pattern
  pattern(schemaPath.phone, /^\d{3}-\d{3}-\d{4}$/, {
    message: 'Format: 555-123-4567',
  });
});
```

### Conditional Validation

```typescript
const orderForm = form(this.orderModel, (schemaPath) => {
  required(schemaPath.promoCode, {
    message: 'Promo code required for discounts',
    when: ({ valueOf }) => valueOf(schemaPath.applyDiscount),
  });
});
```

**Toggle gates a sibling field.** A boolean toggle (`enabled`) that both makes a sibling field
`required` and `disabled` when off — the pattern used e.g. in an admin test-panel:

```typescript
testModel = signal({ enabled: false, receiver: '' });
testForm = form(this.testModel, (p) => {
  required(p.receiver, { message: 'Email address is required', when: ({ valueOf }) => valueOf(p.enabled) });
  email(p.receiver, { when: ({ valueOf }) => valueOf(p.enabled) });
  disabled(p.receiver, ({ valueOf }) => !valueOf(p.enabled));
});
```

```html
<input type="email" [formField]="testForm.receiver" />
@if (testForm.receiver().touched() && testForm.receiver().invalid()) {
  <span class="error">{{ testForm.receiver().errors()[0].message }}</span>
}
```

Gate validation display on `touched()` so no error shows before interaction, and gate `required`
on the controlling toggle so the field isn't required while the feature is off.

#### A custom control gets none of that wiring

`touched()` flips on blur because `[formField]` installs the listener. A custom component that
wraps its own `<input>` (an autocomplete, a combobox, a currency field) is not `[formField]`-bound,
so blur is invisible to the form and `touched()` stays `false` forever — the error branch above can
never render, while a plain `[formField]` control sitting next to it behaves correctly. That
contrast is the diagnostic: if validation works on some fields in a form and not others, compare
how each is bound before looking at the validators.

The component emits blur; the parent marks the field:

```typescript
// custom control
readonly inputBlur = output<void>();
protected onBlur() { this.inputBlur.emit(); }
```

```html
<app-autocomplete [value]="model().Text" (valueChange)="onTextChange($event)" (inputBlur)="onTextBlur()" />
```

```typescript
// parent
protected onTextBlur() { this.headerForm.Text().markAsTouched(); }
```

Two failure modes, and one symptom covers both: the handler exists but never calls
`markAsTouched()`, or the `(inputBlur)` binding is missing from the template so blur is dropped
silently. Both fields in one form failed this way for different reasons — check each binding
individually rather than fixing the first and assuming the second matches.

### Custom Validators

```typescript
import { validate } from '@angular/forms/signals';

const signupForm = form(this.signupModel, (schemaPath) => {
  // Custom validation logic
  validate(schemaPath.username, ({ value }) => {
    if (value().includes(' ')) {
      return { kind: 'noSpaces', message: 'Username cannot contain spaces' };
    }
    return null;
  });
});
```

### Cross-Field Validation

```typescript
const passwordForm = form(this.passwordModel, (schemaPath) => {
  required(schemaPath.password);
  required(schemaPath.confirmPassword);
  
  // Compare fields
  validate(schemaPath.confirmPassword, ({ value, valueOf }) => {
    if (value() !== valueOf(schemaPath.password)) {
      return { kind: 'mismatch', message: 'Passwords do not match' };
    }
    return null;
  });
});
```

### Async Validation

```typescript
import { validateHttp } from '@angular/forms/signals';

const signupForm = form(this.signupModel, (schemaPath) => {
  validateHttp(schemaPath.username, {
    request: ({ value }) => `/api/check-username?u=${value()}`,
    onSuccess: (response: { taken: boolean }) => {
      if (response.taken) {
        return { kind: 'taken', message: 'Username already taken' };
      }
      return null;
    },
    onError: () => ({
      kind: 'networkError',
      message: 'Could not verify username',
    }),
  });
});
```

## Conditional Fields

### Hidden Fields

```typescript
import { hidden } from '@angular/forms/signals';

const profileForm = form(this.profileModel, (schemaPath) => {
  hidden(schemaPath.publicUrl, ({ valueOf }) => !valueOf(schemaPath.isPublic));
});
```

```html
@if (!profileForm.publicUrl().hidden()) {
  <input [formField]="profileForm.publicUrl" />
}
```

### Disabled Fields

```typescript
import { disabled } from '@angular/forms/signals';

const orderForm = form(this.orderModel, (schemaPath) => {
  disabled(schemaPath.couponCode, ({ valueOf }) => valueOf(schemaPath.total) < 50);
});
```

### Readonly Fields

```typescript
import { readonly } from '@angular/forms/signals';

const accountForm = form(this.accountModel, (schemaPath) => {
  readonly(schemaPath.username); // Always readonly
});
```

## Form Submission

```typescript
import { submit } from '@angular/forms/signals';

@Component({
  template: `
    <form (submit)="onSubmit($event)">
      <input [formField]="form.email" />
      <input [formField]="form.password" />
      <button type="submit" [disabled]="form().invalid()">Submit</button>
    </form>
  `,
})
export class Login {
  model = signal({ email: '', password: '' });
  form = form(this.model, (schemaPath) => {
    required(schemaPath.email);
    required(schemaPath.password);
  });
  
  onSubmit(event: Event) {
    event.preventDefault();
    
    // submit() marks all fields touched and runs callback if valid
    submit(this.form, async () => {
      await this.authService.login(this.model());
    });
  }
}
```

## Arrays and Dynamic Fields

```typescript
interface Order {
  items: Array<{ product: string; quantity: number }>;
}

@Component({
  template: `
    @for (item of orderForm.items; track $index; let i = $index) {
      <div>
        <input [formField]="item.product" placeholder="Product" />
        <input [formField]="item.quantity" type="number" />
        <button type="button" (click)="removeItem(i)">Remove</button>
      </div>
    }
    <button type="button" (click)="addItem()">Add Item</button>
  `,
})
export class Order {
  orderModel = signal<Order>({
    items: [{ product: '', quantity: 1 }],
  });
  
  orderForm = form(this.orderModel, (schemaPath) => {
    applyEach(schemaPath.items, (item) => {
      required(item.product, { message: 'Product required' });
      min(item.quantity, 1, { message: 'Min quantity is 1' });
    });
  });
  
  addItem() {
    this.orderModel.update(m => ({
      ...m,
      items: [...m.items, { product: '', quantity: 1 }],
    }));
  }
  
  removeItem(index: number) {
    this.orderModel.update(m => ({
      ...m,
      items: m.items.filter((_, i) => i !== index),
    }));
  }
}
```

## Displaying Errors

```html
<input [formField]="form.email" />

@if (form.email().touched() && form.email().invalid()) {
  <ul class="errors">
    @for (error of form.email().errors(); track error) {
      <li>{{ error.message }}</li>
    }
  </ul>
}

@if (form.email().pending()) {
  <span>Validating...</span>
}
```

## Styling Based on State

```html
<input
  [formField]="form.email"
  [class.is-invalid]="form.email().touched() && form.email().invalid()"
  [class.is-valid]="form.email().touched() && form.email().valid()"
/>
```

## Reset Form

```typescript
async onSubmit() {
  if (!this.form().valid()) return;
  
  await this.api.submit(this.model());
  
  // Clear interaction state
  this.form().reset();
  
  // Clear values
  this.model.set({ email: '', password: '' });
}
```

## FormValueControl

For custom Signal Forms controls:

```typescript
interface Rating {
  rating: number;
}

import { form, FormField, FormValueControl, ValidationError, WithOptionalField } from '@angular/forms/signals';
import { MatIconModule } from '@angular/material/icon';
import { MatError } from '@angular/material/form-field';


@Component({
  selector: 'app-rating',
  imports: [MatIconModule, MatError],
  template: `
    <div class="star-rating-container">
      @for (star of starArray(); track $index) {
        <mat-icon
          (click)="rate(star)"
          class="star-icon"
          [class.readonly]="readonly()"
          [class.error]="invalid()"
          [class]="{ filled: star <= value() }"
        >
          {{ getStarIcon(star) }}
        </mat-icon>
      }
      @if (errors().at(0)?.message) {
        <mat-error>
          {{ errors().at(0)?.message }}
        </mat-error>
      }
    </div>
  `,
  styles: ``,
})
export class Rating implements FormValueControl<number> {
  // Required: The value of the control, exposed as a two-way binding.
  readonly value = model<number>(0);
  // Optional: Bindings for other form control states.
  readonly readonly = input<boolean>(false);
  readonly invalid = input<boolean>(false);
  readonly errors: InputSignal<readonly WithOptionalField<ValidationError>[]> = input<
    readonly WithOptionalField<ValidationError>[]
  >([]);

  starArray: Signal<number[]> = signal(
    Array(5)
      .fill(0)
      .map((_, i) => i + 1),
  );

  getStarIcon(index: number): string {
    const floorRating = Math.floor(this.value()); 
    if (index <= floorRating) {
      return 'star';
    } else {
      return 'star_border';
    }
  }
  rate(index: number): void {
    if (!this.readonly()) {
      this.value.set(index);
    }
  }
}


import { FormField } from '@angular/forms/signals';

@Component({
  selector: 'app-signal-forms',
  imports: [FormField, Rating],
  template: `
   <form autocomplete="off" (submit)="submit($event)">
     <div class="form-field">
          <app-rating [formField]="ratingForm.rating">
          </app-rating>
          {{ratingForm.rating().value()}}
        </div>
   </form>
  `,
  styles: ``,
})
export class SignalForms {
  readonly ratingModel = signal<Rating>({
    rating: 0,
  }); 

  readonly ratingForm = form(this.ratingModel)

  submit(event: Event): void {
    event.preventDefault();
    console.log(this.ratingForm.rating().value());
  }
}
```

## Reactive Forms (Production-Stable)

For production applications requiring stability guarantees, use Reactive Forms:

```typescript
import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="email" />
      @if (form.controls.email.errors?.['required'] && form.controls.email.touched) {
        <span class="error">Email is required</span>
      }
      
      <input type="password" formControlName="password" />
      
      <button type="submit" [disabled]="form.invalid">Login</button>
    </form>
  `,
})
export class Login {
  private fb = inject(FormBuilder);
  
  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });
  
  onSubmit() {
    if (this.form.valid) {
      console.log(this.form.value);
    }
  }
}
```

## Typed Reactive Forms

### Typed FormControl

```typescript
import { FormControl } from '@angular/forms';

// Inferred type: FormControl<string | null>
const name = new FormControl('');

// Non-nullable (no reset to null)
const email = new FormControl('', { nonNullable: true });
// Type: FormControl<string>

// With validators
const username = new FormControl('', {
  nonNullable: true,
  validators: [Validators.required, Validators.minLength(3)],
});
```

### Typed FormGroup

```typescript
import { FormGroup, FormControl } from '@angular/forms';

interface UserForm {
  name: FormControl<string>;
  email: FormControl<string>;
  age: FormControl<number | null>;
}

const form = new FormGroup<UserForm>({
  name: new FormControl('', { nonNullable: true }),
  email: new FormControl('', { nonNullable: true }),
  age: new FormControl<number | null>(null),
});

// Typed value access
const name: string = form.controls.name.value;
```

### NonNullableFormBuilder

```typescript
import { inject } from '@angular/core';
import { NonNullableFormBuilder } from '@angular/forms';

@Component({...})
export class Profile {
  private fb = inject(NonNullableFormBuilder);
  
  form = this.fb.group({
    name: ['', Validators.required],           // FormControl<string>
    email: ['', [Validators.required, Validators.email]],
    preferences: this.fb.group({
      newsletter: [false],                      // FormControl<boolean>
      theme: ['light' as 'light' | 'dark'],    // FormControl<'light' | 'dark'>
    }),
  });
}
```

## FormBuilder Patterns

### Nested FormGroups

```typescript
@Component({
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="name" placeholder="Name" />
      
      <div formGroupName="address">
        <input formControlName="street" placeholder="Street" />
        <input formControlName="city" placeholder="City" />
        <input formControlName="zip" placeholder="ZIP" />
      </div>
      
      <button type="submit">Submit</button>
    </form>
  `,
})
export class Profile {
  private fb = inject(NonNullableFormBuilder);
  
  form = this.fb.group({
    name: ['', Validators.required],
    address: this.fb.group({
      street: [''],
      city: ['', Validators.required],
      zip: ['', [Validators.required, Validators.pattern(/^\d{5}$/)]],
    }),
  });
}
```

## Dynamic Forms with FormArray

```typescript
import { FormArray } from '@angular/forms';

@Component({
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form">
      <div formArrayName="items">
        @for (item of items.controls; track $index; let i = $index) {
          <div [formGroupName]="i">
            <input formControlName="product" placeholder="Product" />
            <input formControlName="quantity" type="number" />
            <button type="button" (click)="removeItem(i)">Remove</button>
          </div>
        }
      </div>
      <button type="button" (click)="addItem()">Add Item</button>
    </form>
  `,
})
export class Order {
  private fb = inject(NonNullableFormBuilder);
  
  form = this.fb.group({
    items: this.fb.array([this.createItem()]),
  });
  
  get items() {
    return this.form.controls.items;
  }
  
  createItem() {
    return this.fb.group({
      product: ['', Validators.required],
      quantity: [1, [Validators.required, Validators.min(1)]],
    });
  }
  
  addItem() {
    this.items.push(this.createItem());
  }
  
  removeItem(index: number) {
    this.items.removeAt(index);
  }
}
```

## Custom Validators

### Sync Validator

```typescript
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function forbiddenValue(forbidden: string): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    return control.value === forbidden 
      ? { forbiddenValue: { value: control.value } } 
      : null;
  };
}

// Usage
name: ['', [Validators.required, forbiddenValue('admin')]],
```

### Cross-Field Validator

```typescript
export function passwordMatch(): ValidatorFn {
  return (group: AbstractControl): ValidationErrors | null => {
    const password = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return password === confirm ? null : { passwordMismatch: true };
  };
}

// Usage
form = this.fb.group({
  password: ['', [Validators.required, Validators.minLength(8)]],
  confirmPassword: ['', Validators.required],
}, { validators: passwordMatch() });
```

### Async Validator

```typescript
import { AsyncValidatorFn } from '@angular/forms';
import { map, catchError, of } from 'rxjs';

export function uniqueEmail(userService: User): AsyncValidatorFn {
  return (control: AbstractControl) => {
    return userService.checkEmail(control.value).pipe(
      map(exists => exists ? { emailTaken: true } : null),
      catchError(() => of(null))
    );
  };
}

// Usage
email: ['', 
  [Validators.required, Validators.email],  // sync validators
  [uniqueEmail(this.userService)]            // async validators
],
```

## Form State Management

### State Properties

```typescript
// Check states
form.valid      // All validations pass
form.invalid    // Has validation errors
form.pending    // Async validation in progress
form.dirty      // Value changed by user
form.pristine   // Value not changed
form.touched    // Control has been focused
form.untouched  // Control never focused

// Update values
form.setValue({ name: 'John', email: 'john@example.com' }); // Must include all
form.patchValue({ name: 'John' }); // Partial update

// Reset
form.reset();
form.reset({ name: 'Default' });

// Disable/Enable
form.disable();
form.enable();
form.controls.email.disable();

// Mark states
form.markAllAsTouched(); // Show all errors
form.markAsPristine();
form.markAsDirty();
```

### Value Changes Observable

```typescript
// Subscribe to value changes
form.valueChanges.subscribe(value => {
  console.log('Form value:', value);
});

// Single control with debounce
form.controls.email.valueChanges.pipe(
  debounceTime(300),
  distinctUntilChanged()
).subscribe(email => {
  this.validateEmail(email);
});

// Status changes
form.statusChanges.subscribe(status => {
  console.log('Form status:', status); // VALID, INVALID, PENDING
});
```

### Unified Events (Angular v22+)

```typescript
import { 
  ValueChangeEvent, StatusChangeEvent, 
  FormSubmittedEvent, FormResetEvent 
} from '@angular/forms';

form.events.subscribe(event => {
  if (event instanceof ValueChangeEvent) {
    console.log('Value changed:', event.value);
  }
  if (event instanceof StatusChangeEvent) {
    console.log('Status changed:', event.status);
  }
  if (event instanceof FormSubmittedEvent) {
    console.log('Form submitted');
  }
  if (event instanceof FormResetEvent) {
    console.log('Form reset');
  }
});
```

## Error Display Pattern

```typescript
@Component({
  template: `
    <input formControlName="email" />
    
    @if (form.controls.email.invalid && form.controls.email.touched) {
      <div class="errors">
        @if (form.controls.email.errors?.['required']) {
          <span>Email is required</span>
        }
        @if (form.controls.email.errors?.['email']) {
          <span>Invalid email format</span>
        }
      </div>
    }
  `,
})
export class Form {
  // Helper for cleaner templates
  hasError(controlName: string, errorKey: string): boolean {
    const control = this.form.get(controlName);
    return control?.hasError(errorKey) && control?.touched || false;
  }
}
```

## Form Submission Pattern

```typescript
@Component({
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <!-- fields -->
      <button type="submit" [disabled]="form.invalid || isSubmitting">
        {{ isSubmitting ? 'Submitting...' : 'Submit' }}
      </button>
    </form>
  `,
})
export class Form {
  isSubmitting = false;
  
  async onSubmit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    
    this.isSubmitting = true;
    try {
      await this.api.submit(this.form.getRawValue());
      this.form.reset();
    } catch (error) {
      // Handle error
    } finally {
      this.isSubmitting = false;
    }
  }
}
```
