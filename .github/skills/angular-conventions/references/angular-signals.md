# Angular Signals

Signals are Angular's reactive primitive for state management. They provide synchronous, fine-grained reactivity.

## Core Signal APIs

### signal() - Writable State

```typescript
import { signal } from '@angular/core';

// Create writable signal
const count = signal(0);

// Read value
console.log(count()); // 0

// Set new value
count.set(5);

// Update based on current value
count.update(c => c + 1);

// With explicit type
const user = signal<User | null>(null);
user.set({ id: 1, name: 'Alice' });
```

### computed() - Derived State

```typescript
import { signal, computed } from '@angular/core';

const firstName = signal('John');
const lastName = signal('Doe');

// Derived signal - automatically updates when dependencies change
const fullName = computed(() => `${firstName()} ${lastName()}`);

console.log(fullName()); // "John Doe"
firstName.set('Jane');
console.log(fullName()); // "Jane Doe"

// Computed with complex logic
const items = signal<Item[]>([]);
const filter = signal('');

const filteredItems = computed(() => {
  const query = filter().toLowerCase();
  return items().filter(item => 
    item.name.toLowerCase().includes(query)
  );
});

const totalPrice = computed(() => 
  filteredItems().reduce((sum, item) => sum + item.price, 0)
);
```

### linkedSignal() - Dependent State with Reset

```typescript
import { signal, linkedSignal } from '@angular/core';

const options = signal(['A', 'B', 'C']);

// Resets to first option when options change
const selected = linkedSignal(() => options()[0]);

console.log(selected()); // "A"
selected.set('B');       // User selects B
console.log(selected()); // "B"
options.set(['X', 'Y']); // Options change
console.log(selected()); // "X" - auto-reset to first

// With previous value access
const items = signal<Item[]>([]);

const selectedItem = linkedSignal<Item[], Item | null>({
  source: () => items(),
  computation: (newItems, previous) => {
    // Try to preserve selection if item still exists
    const prevItem = previous?.value;
    if (prevItem && newItems.some(i => i.id === prevItem.id)) {
      return prevItem;
    }
    return newItems[0] ?? null;
  },
});
```

### effect() - Side Effects

```typescript
import { signal, effect, inject, DestroyRef } from '@angular/core';

@Component({...})
export class Search {
  query = signal('');
  
  constructor() {
    // Effect runs when query changes
    effect(() => {
      console.log('Search query:', this.query());
    });
    
    // Effect with cleanup
    effect((onCleanup) => {
      const timer = setInterval(() => {
        console.log('Current query:', this.query());
      }, 1000);
      
      onCleanup(() => clearInterval(timer));
    });
  }
}
```

**Effect rules:**
- Run in injection context (constructor or with `runInInjectionContext`)
- Automatically cleaned up when component destroys

## Component State Pattern

```typescript
@Component({
  selector: 'app-todo-list',
  template: `
    <input [value]="newTodo()" (input)="newTodo.set($any($event.target).value)" />
    <button (click)="addTodo()" [disabled]="!canAdd()">Add</button>
    
    <ul>
      @for (todo of filteredTodos(); track todo.id) {
        <li [class.done]="todo.done">
          {{ todo.text }}
          <button (click)="toggleTodo(todo.id)">Toggle</button>
        </li>
      }
    </ul>
    
    <p>{{ remaining() }} remaining</p>
  `,
})
export class TodoList {
  // State
  todos = signal<Todo[]>([]);
  newTodo = signal('');
  filter = signal<'all' | 'active' | 'done'>('all');
  
  // Derived state
  canAdd = computed(() => this.newTodo().trim().length > 0);
  
  filteredTodos = computed(() => {
    const todos = this.todos();
    switch (this.filter()) {
      case 'active': return todos.filter(t => !t.done);
      case 'done': return todos.filter(t => t.done);
      default: return todos;
    }
  });
  
  remaining = computed(() => 
    this.todos().filter(t => !t.done).length
  );
  
  // Actions
  addTodo() {
    const text = this.newTodo().trim();
    if (text) {
      this.todos.update(todos => [
        ...todos,
        { id: crypto.randomUUID(), text, done: false }
      ]);
      this.newTodo.set('');
    }
  }
  
  toggleTodo(id: string) {
    this.todos.update(todos =>
      todos.map(t => t.id === id ? { ...t, done: !t.done } : t)
    );
  }
}
```

## RxJS Interop

### toSignal() - Observable to Signal

```typescript
import { toSignal } from '@angular/core/rxjs-interop';
import { interval } from 'rxjs';

@Component({...})
export class Timer {
  private http = inject(HttpClient);
  
  // From observable - requires initial value or allowUndefined
  counter = toSignal(interval(1000), { initialValue: 0 });
  
  // From HTTP - undefined until loaded
  users = toSignal(this.http.get<User[]>('/api/users'));
  
  // With requireSync for synchronous observables (BehaviorSubject)
  private user$ = new BehaviorSubject<User | null>(null);
  currentUser = toSignal(this.user$, { requireSync: true });
}
```

### toObservable() - Signal to Observable

```typescript
import { toObservable } from '@angular/core/rxjs-interop';
import { switchMap, debounceTime } from 'rxjs';

@Component({...})
export class Search {
  query = signal('');
  
  private http = inject(HttpClient);
  
  // Convert signal to observable for RxJS operators
  results = toSignal(
    toObservable(this.query).pipe(
      debounceTime(300),
      switchMap(q => this.http.get<Result[]>(`/api/search?q=${q}`))
    ),
    { initialValue: [] }
  );
}
```

## Signal Equality

```typescript
// Custom equality function
const user = signal<User>(
  { id: 1, name: 'Alice' },
  { equal: (a, b) => a.id === b.id }
);

// Only triggers updates when ID changes
user.set({ id: 1, name: 'Alice Updated' }); // No update
user.set({ id: 2, name: 'Bob' }); // Triggers update
```

## Untracked Reads

```typescript
import { untracked } from '@angular/core';

const a = signal(1);
const b = signal(2);

// Only depends on 'a', not 'b'
const result = computed(() => {
  const aVal = a();
  const bVal = untracked(() => b());
  return aVal + bVal;
});
```

### Gotcha: effects track EVERY synchronous read, including hidden ones inside called methods

An `effect()`/`computed()` records a dependency on **every** signal read during its synchronous run — not just the ones you named at the top, but any incidental read deep inside a method, service, or HTTP interceptor it calls on the same call stack. If that same signal is then written as a side effect, the effect reschedules itself → **infinite loop** (under zoneless change detection this hangs the browser).

Classic trigger: an `effect()` that fires an HTTP request, where a global "activity"/"loading" interceptor reads-then-writes a shared `pendingRequests` (or `isBusy`) signal on every request. The effect silently takes a dependency on that counter; its own request bumps it, which reschedules the effect, which fires another request — a self-sustaining request storm independent of the data.

**Rule:** read your intended dependency signals explicitly at the top of the effect, then wrap any side-effecting call (anything that issues HTTP or otherwise touches shared store signals) in `untracked()`:

```typescript
onChange = effect(() => {
  const id = this.selectedId();          // real deps, read tracked
  if (id) {
    untracked(() => this.loadDetails());  // side effect — do NOT track its internal reads
  }
});
```

Symptom to recognize: an endless stream of identical requests in the network/API console after a component with an `effect()` mounts, where the effect's named dependencies never actually change value.

## Service State Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class Auth {
  // Private writable state
  private _user = signal<User | null>(null);
  private _loading = signal(false);
  
  // Public read-only signals
  readonly user = this._user.asReadonly();
  readonly loading = this._loading.asReadonly();
  readonly isAuthenticated = computed(() => this._user() !== null);
  
  private http = inject(HttpClient);
  
  async login(credentials: Credentials): Promise<void> {
    this._loading.set(true);
    try {
      const user = await firstValueFrom(
        this.http.post<User>('/api/login', credentials)
      );
      this._user.set(user);
    } finally {
      this._loading.set(false);
    }
  }
  
  logout(): void {
    this._user.set(null);
  }
}
```

## Resource API

The `resource()` API handles async data fetching with signals:

```typescript
import { resource, signal, computed } from '@angular/core';

@Component({...})
export class UserProfile {
  userId = signal<string>('');
  
  // Resource fetches data when params change
  userResource = resource({
    params: () => ({ id: this.userId() }),
    loader: async ({ params, abortSignal }) => {
      const response = await fetch(`/api/users/${params.id}`, {
        signal: abortSignal,
      });
      return response.json() as Promise<User>;
    },
  });
  
  // Access resource state
  user = computed(() => this.userResource.value());
  isLoading = computed(() => this.userResource.isLoading());
  error = computed(() => this.userResource.error());
}
```

### Resource Status

```typescript
const userResource = resource({...});

// Status signals
userResource.value();      // Current value or undefined
userResource.hasValue();   // Boolean - has resolved value
userResource.error();      // Error or undefined
userResource.isLoading();  // Boolean - currently loading
userResource.status();     // 'idle' | 'loading' | 'reloading' | 'resolved' | 'error' | 'local'

// Manual reload
userResource.reload();

// Local updates
userResource.set(newValue);
userResource.update(current => ({ ...current, name: 'Updated' }));
```

### Resource with Default Value

```typescript
const todosResource = resource({
  defaultValue: [] as Todo[],
  params: () => ({ filter: this.filter() }),
  loader: async ({ params }) => {
    const response = await fetch(`/api/todos?filter=${params.filter}`);
    return response.json();
  },
});

// value() returns Todo[] (never undefined due to defaultValue)
```

### Conditional Loading

```typescript
const userId = signal<string | null>(null);

const userResource = resource({
  params: () => {
    const id = userId();
    // Return undefined to skip loading
    return id ? { id } : undefined;
  },
  loader: async ({ params }) => {
    return fetch(`/api/users/${params.id}`).then(r => r.json());
  },
});
// Status is 'idle' when params returns undefined
```

## Signal Store Pattern

For complex state, create a dedicated store:

```typescript
interface ProductState {
  products: Product[];
  selectedId: string | null;
  filter: string;
  loading: boolean;
  error: string | null;
}

@Injectable({ providedIn: 'root' })
export class ProductSt {
  // Private state
  private state = signal<ProductState>({
    products: [],
    selectedId: null,
    filter: '',
    loading: false,
    error: null,
  });
  
  // Selectors (computed signals)
  readonly products = computed(() => this.state().products);
  readonly selectedId = computed(() => this.state().selectedId);
  readonly filter = computed(() => this.state().filter);
  readonly loading = computed(() => this.state().loading);
  readonly error = computed(() => this.state().error);
  
  readonly filteredProducts = computed(() => {
    const { products, filter } = this.state();
    if (!filter) return products;
    return products.filter(p => 
      p.name.toLowerCase().includes(filter.toLowerCase())
    );
  });
  
  readonly selectedProduct = computed(() => {
    const { products, selectedId } = this.state();
    return products.find(p => p.id === selectedId) ?? null;
  });
  
  private http = inject(HttpClient);
  
  // Actions
  setFilter(filter: string): void {
    this.state.update(s => ({ ...s, filter }));
  }
  
  selectProduct(id: string | null): void {
    this.state.update(s => ({ ...s, selectedId: id }));
  }
  
  async loadProducts(): Promise<void> {
    this.state.update(s => ({ ...s, loading: true, error: null }));
    
    try {
      const products = await firstValueFrom(
        this.http.get<Product[]>('/api/products')
      );
      this.state.update(s => ({ ...s, products, loading: false }));
    } catch (err) {
      this.state.update(s => ({ 
        ...s, 
        loading: false, 
        error: 'Failed to load products' 
      }));
    }
  }
  
  async addProduct(product: Omit<Product, 'id'>): Promise<void> {
    const newProduct = await firstValueFrom(
      this.http.post<Product>('/api/products', product)
    );
    this.state.update(s => ({
      ...s,
      products: [...s.products, newProduct],
    }));
  }
}
```

## Form State with Signals

```typescript
interface FormState<T> {
  value: T;
  touched: boolean;
  dirty: boolean;
  valid: boolean;
  errors: string[];
}

function createFormField<T>(
  initialValue: T,
  validators: ((value: T) => string | null)[] = []
) {
  const value = signal(initialValue);
  const touched = signal(false);
  const dirty = signal(false);
  
  const errors = computed(() => {
    return validators
      .map(v => v(value()))
      .filter((e): e is string => e !== null);
  });
  
  const valid = computed(() => errors().length === 0);
  
  return {
    value,
    touched: touched.asReadonly(),
    dirty: dirty.asReadonly(),
    errors,
    valid,
    
    setValue(newValue: T) {
      value.set(newValue);
      dirty.set(true);
    },
    
    markTouched() {
      touched.set(true);
    },
    
    reset() {
      value.set(initialValue);
      touched.set(false);
      dirty.set(false);
    },
  };
}

// Usage
@Component({...})
export class Signup {
  email = createFormField('', [
    v => !v ? 'Email is required' : null,
    v => !v.includes('@') ? 'Invalid email' : null,
  ]);
  
  password = createFormField('', [
    v => !v ? 'Password is required' : null,
    v => v.length < 8 ? 'Password must be at least 8 characters' : null,
  ]);
  
  formValid = computed(() => 
    this.email.valid() && this.password.valid()
  );
}
```

## Async Operations

### Debounced Search

```typescript
@Component({...})
export class Search {
  query = signal('');
  
  private http = inject(HttpClient);
  
  // Debounced search using toObservable
  results = toSignal(
    toObservable(this.query).pipe(
      debounceTime(300),
      distinctUntilChanged(),
      filter(q => q.length >= 2),
      switchMap(q => this.http.get<Result[]>(`/api/search?q=${q}`)),
      catchError(() => of([]))
    ),
    { initialValue: [] }
  );
  
  // Loading state
  private searching = signal(false);
  readonly isSearching = this.searching.asReadonly();

  constructor() {
    // Track loading state
    effect(() => {
      const q = this.query();
      if (q.length >= 2) {
        this.searching.set(true);
      }
    });

    effect(() => {
      this.results(); // Subscribe to results
      this.searching.set(false);
    });
  }
}
```

### Optimistic Updates

```typescript
@Injectable({ providedIn: 'root' })
export class Todo {
  private todos = signal<Todo[]>([]);
  readonly items = this.todos.asReadonly();
  
  private http = inject(HttpClient);
  
  async toggleTodo(id: string): Promise<void> {
    // Optimistic update
    const previousTodos = this.todos();
    this.todos.update(todos =>
      todos.map(t => t.id === id ? { ...t, done: !t.done } : t)
    );
    
    try {
      await firstValueFrom(
        this.http.patch(`/api/todos/${id}/toggle`, {})
      );
    } catch {
      // Rollback on error
      this.todos.set(previousTodos);
    }
  }
}
```

## Testing Signals

```typescript
describe('Counter', () => {
  it('should increment count', () => {
    const component = new Counter();
    
    expect(component.count()).toBe(0);
    
    component.increment();
    expect(component.count()).toBe(1);
    
    component.increment();
    expect(component.count()).toBe(2);
  });
  
  it('should compute doubled value', () => {
    const component = new Counter();
    
    expect(component.doubled()).toBe(0);
    
    component.count.set(5);
    expect(component.doubled()).toBe(10);
  });
});

describe('ProductSt', () => {
  let store: ProductSt;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ProductSt,
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    store = TestBed.inject(ProductSt);
    httpMock = TestBed.inject(HttpTestingController);
  });
  
  it('should filter products', () => {
    // Set initial state
    store['state'].set({
      products: [
        { id: '1', name: 'Apple' },
        { id: '2', name: 'Banana' },
      ],
      selectedId: null,
      filter: '',
      loading: false,
      error: null,
    });
    
    expect(store.filteredProducts().length).toBe(2);
    
    store.setFilter('app');
    expect(store.filteredProducts().length).toBe(1);
    expect(store.filteredProducts()[0].name).toBe('Apple');
  });
});
```

## Signal Debugging

```typescript
// Debug effect to log signal changes
effect(() => {
  console.log('State changed:', {
    count: this.count(),
    items: this.items(),
    filter: this.filter(),
  });
});

// Conditional debugging
const DEBUG = signal(false);

effect(() => {
  if (untracked(() => DEBUG())) {
    console.log('Debug:', this.state());
  }
});
```
