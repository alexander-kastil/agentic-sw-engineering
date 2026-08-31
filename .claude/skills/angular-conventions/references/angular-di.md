# Angular Dependency Injection

Configure and use dependency injection in Angular v20+ with `inject()` and providers.

## Basic Injection

### Using inject()

Prefer `inject()` over constructor injection:

```typescript
import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from './user.service';

@Component({
  selector: 'app-user-list',
  template: `...`,
})
export class UserList {
  // Inject dependencies
  private http = inject(HttpClient);
  private userService = inject(User);
  
  // Can use immediately
  users = this.userService.getUsers();
}
```

### Injectable Services

```typescript
import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root', // Singleton at root level
})
export class User {
  private http = inject(HttpClient);
  
  private users = signal<User[]>([]);
  readonly users$ = this.users.asReadonly();
  
  async loadUsers() {
    const users = await firstValueFrom(
      this.http.get<User[]>('/api/users')
    );
    this.users.set(users);
  }
}
```

## Provider Scopes

### Root Level (Singleton)

```typescript
// Recommended: providedIn
@Injectable({
  providedIn: 'root',
})
export class Auth {}

// Alternative: in app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    Auth,
  ],
};
```

### Component Level (Instance per Component)

```typescript
@Component({
  selector: 'app-editor',
  providers: [EditorState], // New instance for each component
  template: `...`,
})
export class Editor {
  private editorState = inject(EditorState);
}
```

### Route Level

```typescript
export const routes: Routes = [
  {
    path: 'admin',
    providers: [Admin], // Shared within this route tree
    children: [
      { path: '', component: AdminDashboard },
      { path: 'users', component: AdminUsers },
    ],
  },
];
```

## Injection Tokens

### Creating Tokens

```typescript
import { InjectionToken } from '@angular/core';

// Simple value token
export const API_URL = new InjectionToken<string>('API_URL');

// Object token
export interface AppConfig {
  apiUrl: string;
  features: {
    darkMode: boolean;
    analytics: boolean;
  };
}

export const APP_CONFIG = new InjectionToken<AppConfig>('APP_CONFIG');

// Token with factory (self-providing)
export const WINDOW = new InjectionToken<Window>('Window', {
  providedIn: 'root',
  factory: () => window,
});

export const LOCAL_STORAGE = new InjectionToken<Storage>('LocalStorage', {
  providedIn: 'root',
  factory: () => localStorage,
});
```

### Providing Token Values

```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    { provide: API_URL, useValue: 'https://api.example.com' },
    {
      provide: APP_CONFIG,
      useValue: {
        apiUrl: 'https://api.example.com',
        features: { darkMode: true, analytics: true },
      },
    },
  ],
};
```

### Injecting Tokens

```typescript
@Injectable({ providedIn: 'root' })
export class Api {
  private apiUrl = inject(API_URL);
  private config = inject(APP_CONFIG);
  private window = inject(WINDOW);
  
  getBaseUrl(): string {
    return this.apiUrl;
  }
}
```

## Provider Types

### useClass

```typescript
// Provide implementation
{ provide: Logger, useClass: ConsoleLogger }

// Conditional implementation
{
  provide: Logger,
  useClass: environment.production
    ? ProductionLogger
    : ConsoleLogger,
}
```

### useValue

```typescript
// Static values
{ provide: API_URL, useValue: 'https://api.example.com' }

// Configuration objects
{ provide: APP_CONFIG, useValue: { theme: 'dark', language: 'en' } }
```

### useFactory

```typescript
// Factory with dependencies
{
  provide: User,
  useFactory: (http: HttpClient, config: AppConfig) => {
    return new User(http, config.apiUrl);
  },
  deps: [HttpClient, APP_CONFIG],
}

// Async factory (not recommended - use provideAppInitializer)
{
  provide: CONFIG,
  useFactory: () => fetch('/config.json').then(r => r.json()),
}
```

### useExisting

```typescript
// Alias to existing provider
{ provide: AbstractLogger, useExisting: ConsoleLogger }

// Multiple tokens pointing to same instance
providers: [
  ConsoleLogger,
  { provide: Logger, useExisting: ConsoleLogger },
  { provide: ErrorLogger, useExisting: ConsoleLogger },
]
```

## Injection Options

### Optional Injection

```typescript
@Component({...})
export class My {
  // Returns null if not provided
  private analytics = inject(Analytics, { optional: true });
  
  trackEvent(name: string) {
    this.analytics?.track(name);
  }
}
```

### Self, SkipSelf, Host

```typescript
@Component({
  providers: [Local],
})
export class Parent {
  // Only look in this component's injector
  private local = inject(Local, { self: true });
}

@Component({...})
export class Child {
  // Skip this component, look in parent
  private parentService = inject(ParentSvc, { skipSelf: true });

  // Only look up to host component
  private hostService = inject(Host, { host: true });
}
```

## Multi Providers

Collect multiple values for same token:

```typescript
// Token for multiple validators
export const VALIDATORS = new InjectionToken<Validator[]>('Validators');

// Provide multiple values
providers: [
  { provide: VALIDATORS, useClass: RequiredValidator, multi: true },
  { provide: VALIDATORS, useClass: EmailValidator, multi: true },
  { provide: VALIDATORS, useClass: MinLengthValidator, multi: true },
]

// Inject as array
@Injectable()
export class Validation {
  private validators = inject(VALIDATORS); // Validator[]
  
  validate(value: string): ValidationError[] {
    return this.validators
      .map(v => v.validate(value))
      .filter(Boolean);
  }
}
```

### HTTP Interceptors (Multi Provider)

```typescript
// Interceptors use multi providers internally
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([
        authInterceptor,
        loggingInterceptor,
        errorInterceptor,
      ])
    ),
  ],
};
```

## App Initializers

Run async code before app starts using `provideAppInitializer`:

```typescript
import { provideAppInitializer, inject } from '@angular/core';

export const appConfig: ApplicationConfig = {
  providers: [
    Config,
    provideAppInitializer(() => {
      const configService = inject(Config);
      return configService.loadConfig();
    }),
  ],
};
```

### Multiple Initializers

```typescript
providers: [
  provideAppInitializer(() => {
    const config = inject(Config);
    return config.load();
  }),
  provideAppInitializer(() => {
    const auth = inject(Auth);
    return auth.checkSession();
  }),
]
```

## Environment Injector

Create injectors programmatically:

```typescript
import { createEnvironmentInjector, EnvironmentInjector, inject } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class Plugin {
  private parentInjector = inject(EnvironmentInjector);
  
  loadPlugin(providers: Provider[]): EnvironmentInjector {
    return createEnvironmentInjector(providers, this.parentInjector);
  }
}
```

## runInInjectionContext

Run code with injection context:

```typescript
import { runInInjectionContext, EnvironmentInjector, inject } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class Utility {
  private injector = inject(EnvironmentInjector);
  
  executeWithDI<T>(fn: () => T): T {
    return runInInjectionContext(this.injector, fn);
  }
}

// Usage
utilityService.executeWithDI(() => {
  const http = inject(HttpClient);
  // Use http...
});
```

## Service Patterns

### Facade Service

Combine multiple services into a single API:

```typescript
@Injectable({ providedIn: 'root' })
export class ShopFacade {
  private productService = inject(Product);
  private cartService = inject(Cart);
  private orderService = inject(Order);
  
  // Expose combined state
  readonly products = this.productService.products;
  readonly cart = this.cartService.items;
  readonly cartTotal = this.cartService.total;
  
  // Unified actions
  addToCart(productId: string, quantity: number) {
    const product = this.productService.getById(productId);
    if (product) {
      this.cartService.add(product, quantity);
    }
  }
  
  async checkout() {
    const items = this.cartService.items();
    const order = await this.orderService.create(items);
    this.cartService.clear();
    return order;
  }
}
```

### State Service Pattern

```typescript
interface UserState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

@Injectable({ providedIn: 'root' })
export class UserState {
  private state = signal<UserState>({
    user: null,
    loading: false,
    error: null,
  });
  
  // Selectors
  readonly user = computed(() => this.state().user);
  readonly loading = computed(() => this.state().loading);
  readonly error = computed(() => this.state().error);
  readonly isAuthenticated = computed(() => this.state().user !== null);
  
  // Actions
  setUser(user: User) {
    this.state.update(s => ({ ...s, user, loading: false, error: null }));
  }
  
  setLoading() {
    this.state.update(s => ({ ...s, loading: true, error: null }));
  }
  
  setError(error: string) {
    this.state.update(s => ({ ...s, loading: false, error }));
  }
  
  clear() {
    this.state.set({ user: null, loading: false, error: null });
  }
}
```

### Repository Pattern

```typescript
// Generic repository interface
export abstract class Repository<T extends { id: string }> {
  abstract getAll(): Promise<T[]>;
  abstract getById(id: string): Promise<T | null>;
  abstract create(item: Omit<T, 'id'>): Promise<T>;
  abstract update(id: string, item: Partial<T>): Promise<T>;
  abstract delete(id: string): Promise<void>;
}

// HTTP implementation
@Injectable()
export class HttpUserRepo extends Repository<User> {
  private http = inject(HttpClient);
  private apiUrl = inject(API_URL);
  
  async getAll(): Promise<User[]> {
    return firstValueFrom(this.http.get<User[]>(`${this.apiUrl}/users`));
  }
  
  async getById(id: string): Promise<User | null> {
    return firstValueFrom(
      this.http.get<User>(`${this.apiUrl}/users/${id}`).pipe(
        catchError(() => of(null))
      )
    );
  }
  
  async create(user: Omit<User, 'id'>): Promise<User> {
    return firstValueFrom(this.http.post<User>(`${this.apiUrl}/users`, user));
  }
  
  async update(id: string, user: Partial<User>): Promise<User> {
    return firstValueFrom(this.http.patch<User>(`${this.apiUrl}/users/${id}`, user));
  }
  
  async delete(id: string): Promise<void> {
    await firstValueFrom(this.http.delete(`${this.apiUrl}/users/${id}`));
  }
}

// Provide implementation
{ provide: Repository, useClass: HttpUserRepo }
```

## Abstract Classes as Tokens

Use abstract classes for better type safety:

```typescript
// Abstract service definition
export abstract class Logger {
  abstract log(message: string): void;
  abstract error(message: string, error?: Error): void;
  abstract warn(message: string): void;
}

// Console implementation
@Injectable()
export class ConsoleLog extends Logger {
  log(message: string) {
    console.log(`[LOG] ${message}`);
  }
  
  error(message: string, error?: Error) {
    console.error(`[ERROR] ${message}`, error);
  }
  
  warn(message: string) {
    console.warn(`[WARN] ${message}`);
  }
}

// Remote implementation
@Injectable()
export class RemoteLog extends Logger {
  private http = inject(HttpClient);
  
  log(message: string) {
    this.send('log', message);
  }
  
  error(message: string, error?: Error) {
    this.send('error', message, error);
  }
  
  warn(message: string) {
    this.send('warn', message);
  }
  
  private send(level: string, message: string, error?: Error) {
    this.http.post('/api/logs', { level, message, error: error?.message }).subscribe();
  }
}

// Provide based on environment
{
  provide: Logger,
  useClass: environment.production ? RemoteLog : ConsoleLog,
}

// Inject using abstract class
@Injectable({ providedIn: 'root' })
export class User {
  private logger = inject(Logger);

  createUser(user: UserData) {
    this.logger.log(`Creating user: ${user.email}`);
    // ...
  }
}
```

## Hierarchical Injection

### Component Tree Injection

```typescript
// Parent provides service
@Component({
  selector: 'app-form-container',
  providers: [FormState],
  template: `
    <app-form-header />
    <app-form-body />
    <app-form-footer />
  `,
})
export class FormContainer {
  private formState = inject(FormState);
}

// Children share same instance
@Component({
  selector: 'app-form-body',
  template: `...`,
})
export class FormBody {
  // Gets same instance as parent
  private formState = inject(FormState);
}

// Grandchildren also share
@Component({
  selector: 'app-form-field',
  template: `...`,
})
export class FormField {
  // Gets same instance from ancestor
  private formState = inject(FormState);
}
```

### viewProviders vs providers

```typescript
@Component({
  selector: 'app-tabs',
  // providers: Available to component AND content children
  providers: [TabsSvc],

  // viewProviders: Available to component AND view children only
  // NOT available to content children (<ng-content>)
  viewProviders: [InternalTabs],
  
  template: `
    <div class="tabs">
      <ng-content /> <!-- Content children can't access viewProviders -->
    </div>
  `,
})
export class Tabs {}
```

## Dynamic Providers

### Feature Flags

```typescript
export const FEATURE_FLAGS = new InjectionToken<FeatureFlags>('FeatureFlags');

interface FeatureFlags {
  newDashboard: boolean;
  betaFeatures: boolean;
  experimentalApi: boolean;
}

// Load from API
{
  provide: FEATURE_FLAGS,
  useFactory: async () => {
    const response = await fetch('/api/features');
    return response.json();
  },
}

// Use in components
@Component({...})
export class Dashboard {
  private features = inject(FEATURE_FLAGS);
  
  showNewDashboard = this.features.newDashboard;
}
```

### Platform-Specific Services

```typescript
export abstract class Storage {
  abstract get(key: string): string | null;
  abstract set(key: string, value: string): void;
  abstract remove(key: string): void;
}

@Injectable()
export class BrowserStorage extends Storage {
  get(key: string) { return localStorage.getItem(key); }
  set(key: string, value: string) { localStorage.setItem(key, value); }
  remove(key: string) { localStorage.removeItem(key); }
}

@Injectable()
export class ServerStorage extends Storage {
  private store = new Map<string, string>();

  get(key: string) { return this.store.get(key) ?? null; }
  set(key: string, value: string) { this.store.set(key, value); }
  remove(key: string) { this.store.delete(key); }
}

// Provide based on platform
import { PLATFORM_ID, isPlatformBrowser } from '@angular/common';

{
  provide: Storage,
  useFactory: (platformId: object) => {
    return isPlatformBrowser(platformId)
      ? new BrowserStorage()
      : new ServerStorage();
  },
  deps: [PLATFORM_ID],
}
```

## Testing with DI

### Mocking Services

Vitest (current convention):

```typescript
describe('UserCmpt', () => {
  let userServiceMock: { getUser: ReturnType<typeof vi.fn>; updateUser: ReturnType<typeof vi.fn> };

  beforeEach(async () => {
    userServiceMock = {
      getUser: vi.fn().mockReturnValue(of({ id: '1', name: 'Test' })),
      updateUser: vi.fn(),
    };

    await TestBed.configureTestingModule({
      imports: [UserCmpt],
      providers: [
        { provide: User, useValue: userServiceMock },
      ],
    }).compileComponents();
  });

  it('should load user', () => {
    const fixture = TestBed.createComponent(UserCmpt);
    fixture.detectChanges();

    expect(userServiceMock.getUser).toHaveBeenCalled();
  });
});
```

Jasmine/Karma (legacy projects only — prefer `vi.fn()`, see `angular-antipatterns.md`):

```typescript
describe('UserCmpt', () => {
  let userServiceSpy: jasmine.SpyObj<User>;

  beforeEach(async () => {
    userServiceSpy = jasmine.createSpyObj('User', ['getUser', 'updateUser']);
    userServiceSpy.getUser.and.returnValue(of({ id: '1', name: 'Test' }));

    await TestBed.configureTestingModule({
      imports: [UserCmpt],
      providers: [
        { provide: User, useValue: userServiceSpy },
      ],
    }).compileComponents();
  });

  it('should load user', () => {
    const fixture = TestBed.createComponent(UserCmpt);
    fixture.detectChanges();

    expect(userServiceSpy.getUser).toHaveBeenCalled();
  });
});
```

### Overriding Providers

```typescript
describe('with different config', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
    })
    .overrideProvider(APP_CONFIG, {
      useValue: { apiUrl: 'http://test-api.com' },
    })
    .compileComponents();
  });
});
```

### Testing Injection Tokens

```typescript
describe('API_URL token', () => {
  it('should provide correct URL', () => {
    TestBed.configureTestingModule({
      providers: [
        { provide: API_URL, useValue: 'https://api.test.com' },
      ],
    });
    
    const apiUrl = TestBed.inject(API_URL);
    expect(apiUrl).toBe('https://api.test.com');
  });
});
```

## DestroyRef and Cleanup

### Automatic Cleanup

```typescript
import { DestroyRef, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({...})
export class Data {
  private destroyRef = inject(DestroyRef);
  private dataService = inject(DataSvc);
  
  constructor() {
    // Auto-unsubscribe when component destroys
    this.dataService.data$
      .pipe(takeUntilDestroyed())
      .subscribe(data => {
        console.log(data);
      });
  }
  
  // Or use DestroyRef directly
  ngOnInit() {
    const subscription = this.dataService.updates$.subscribe();
    
    this.destroyRef.onDestroy(() => {
      subscription.unsubscribe();
      console.log('Cleaned up!');
    });
  }
}
```

### In Services

```typescript
@Injectable()
export class WebSocket {
  private destroyRef = inject(DestroyRef);
  private socket: WebSocket | null = null;
  
  constructor() {
    this.destroyRef.onDestroy(() => {
      this.socket?.close();
    });
  }
  
  connect(url: string) {
    this.socket = new WebSocket(url);
  }
}
```

### takeUntilDestroyed Outside Constructor

```typescript
@Component({...})
export class My {
  private destroyRef = inject(DestroyRef);

  loadData() {
    // Pass destroyRef when using outside constructor
    this.http.get('/api/data')
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe();
  }
}
```

## Injection Context Utilities

### assertInInjectionContext

```typescript
import { assertInInjectionContext, inject } from '@angular/core';

export function injectLogger(): Logger {
  assertInInjectionContext(injectLogger);
  return inject(Logger);
}

// Usage - must be called in injection context
@Component({...})
export class My2 {
  private logger = injectLogger(); // OK

  someMethod() {
    // injectLogger(); // ERROR - not in injection context
  }
}
```

### Custom inject Functions

```typescript
// Create reusable injection utilities
export function injectRouteParam(param: string): Signal<string | null> {
  assertInInjectionContext(injectRouteParam);
  
  const route = inject(ActivatedRoute);
  return toSignal(
    route.paramMap.pipe(map(params => params.get(param))),
    { initialValue: null }
  );
}

export function injectQueryParam(param: string): Signal<string | null> {
  assertInInjectionContext(injectQueryParam);
  
  const route = inject(ActivatedRoute);
  return toSignal(
    route.queryParamMap.pipe(map(params => params.get(param))),
    { initialValue: null }
  );
}

// Usage
@Component({...})
export class UserCmpt {
  userId = injectRouteParam('id');
  tab = injectQueryParam('tab');
}
```
