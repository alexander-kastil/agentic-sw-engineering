# Angular HTTP & Data Fetching

Fetch data in Angular using signal-based `resource()`, `httpResource()`, and the traditional `HttpClient`.

## httpResource() - Signal-Based HTTP

`httpResource()` wraps HttpClient with signal-based state management:

```typescript
import { Component, signal } from '@angular/core';
import { httpResource } from '@angular/common/http';

interface User {
  id: number;
  name: string;
  email: string;
}

@Component({
  selector: 'app-user-profile',
  template: `
    @if (userResource.isLoading()) {
      <p>Loading...</p>
    } @else if (userResource.error()) {
      <p>Error: {{ userResource.error()?.message }}</p>
      <button (click)="userResource.reload()">Retry</button>
    } @else if (userResource.hasValue()) {
      <h1>{{ userResource.value().name }}</h1>
      <p>{{ userResource.value().email }}</p>
    }
  `,
})
export class UserProfile {
  userId = signal('123');
  
  // Reactive HTTP resource - refetches when userId changes
  userResource = httpResource<User>(() => `/api/users/${this.userId()}`);
}
```

### httpResource Options

```typescript
// Simple GET request
userResource = httpResource<User>(() => `/api/users/${this.userId()}`);

// With full request options
userResource = httpResource<User>(() => ({
  url: `/api/users/${this.userId()}`,
  method: 'GET',
  headers: { 'Authorization': `Bearer ${this.token()}` },
  params: { include: 'profile' },
}));

// With default value
usersResource = httpResource<User[]>(() => '/api/users', {
  defaultValue: [],
});

// Skip request when params undefined
userResource = httpResource<User>(() => {
  const id = this.userId();
  return id ? `/api/users/${id}` : undefined;
});
```

### Resource State

```typescript
// Status signals
userResource.value()      // Current value or undefined
userResource.hasValue()   // Boolean - has resolved value
userResource.error()      // Error or undefined
userResource.isLoading()  // Boolean - currently loading
userResource.status()     // 'idle' | 'loading' | 'reloading' | 'resolved' | 'error' | 'local'

// Actions
userResource.reload()     // Manually trigger reload
userResource.set(value)   // Set local value
userResource.update(fn)   // Update local value
```

## resource() - Generic Async Data

For non-HTTP async operations or custom fetch logic:

```typescript
import { resource, signal } from '@angular/core';

@Component({...})
export class Search {
  query = signal('');
  
  searchResource = resource({
    // Reactive params - triggers reload when changed
    params: () => ({ q: this.query() }),
    
    // Async loader function
    loader: async ({ params, abortSignal }) => {
      if (!params.q) return [];
      
      const response = await fetch(`/api/search?q=${params.q}`, {
        signal: abortSignal,
      });
      return response.json() as Promise<SearchResult[]>;
    },
  });
}
```

### Resource with Default Value

```typescript
todosResource = resource({
  defaultValue: [] as Todo[],
  params: () => ({ filter: this.filter() }),
  loader: async ({ params }) => {
    const res = await fetch(`/api/todos?filter=${params.filter}`);
    return res.json();
  },
});

// value() returns Todo[] (never undefined)
```

### Conditional Loading

```typescript
const userId = signal<string | null>(null);

userResource = resource({
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

## HttpClient - Traditional Approach

For complex scenarios or when you need Observable operators:

```typescript
import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';

@Component({...})
export class Users {
  private http = inject(HttpClient);
  
  // Convert Observable to Signal
  users = toSignal(
    this.http.get<User[]>('/api/users'),
    { initialValue: [] }
  );
  
  // Or use Observable directly
  users$ = this.http.get<User[]>('/api/users');
}
```

### HTTP Methods

```typescript
private http = inject(HttpClient);

// GET
getUser(id: string) {
  return this.http.get<User>(`/api/users/${id}`);
}

// POST
createUser(user: CreateUserDto) {
  return this.http.post<User>('/api/users', user);
}

// PUT
updateUser(id: string, user: UpdateUserDto) {
  return this.http.put<User>(`/api/users/${id}`, user);
}

// PATCH
patchUser(id: string, changes: Partial<User>) {
  return this.http.patch<User>(`/api/users/${id}`, changes);
}

// DELETE
deleteUser(id: string) {
  return this.http.delete<void>(`/api/users/${id}`);
}
```

### Request Options

```typescript
this.http.get<User[]>('/api/users', {
  headers: {
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json',
  },
  params: {
    page: '1',
    limit: '10',
    sort: 'name',
  },
  observe: 'response', // Get full HttpResponse
  responseType: 'json',
});
```

## Interceptors

### Functional Interceptor (Recommended)

```typescript
// auth.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(Auth);
  const token = authService.token();
  
  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    });
  }
  
  return next(req);
};

// error.interceptor.ts
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        inject(Router).navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
};

// logging.interceptor.ts
export const loggingInterceptor: HttpInterceptorFn = (req, next) => {
  const started = Date.now();
  return next(req).pipe(
    tap({
      next: () => console.log(`${req.method} ${req.url} - ${Date.now() - started}ms`),
      error: (err) => console.error(`${req.method} ${req.url} failed`, err),
    })
  );
};
```

### Register Interceptors

```typescript
// app.config.ts
import { provideHttpClient, withInterceptors } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([
        authInterceptor,
        errorInterceptor,
        loggingInterceptor,
      ])
    ),
  ],
};
```

## Error Handling

### With httpResource

```typescript
@Component({
  template: `
    @if (userResource.error(); as error) {
      <div class="error">
        <p>{{ getErrorMessage(error) }}</p>
        <button (click)="userResource.reload()">Retry</button>
      </div>
    }
  `,
})
export class UserCmpt {
  userResource = httpResource<User>(() => `/api/users/${this.userId()}`);
  
  getErrorMessage(error: unknown): string {
    if (error instanceof HttpErrorResponse) {
      return error.error?.message || `Error ${error.status}: ${error.statusText}`;
    }
    return 'An unexpected error occurred';
  }
}
```

### With HttpClient

```typescript
import { catchError, retry } from 'rxjs';

getUser(id: string) {
  return this.http.get<User>(`/api/users/${id}`).pipe(
    retry(2), // Retry up to 2 times
    catchError((error: HttpErrorResponse) => {
      console.error('Error fetching user:', error);
      return throwError(() => new Error('Failed to load user'));
    })
  );
}
```

## Guard Array Responses Before Storing

TypeScript HTTP types are wishes, not guarantees. The actual JSON can arrive as `null` (CORS or SSL failures, API quirks) even when the declared type is `T[]`. Angular's native `@for` then throws `TypeError: newCollection[Symbol.iterator] is not a function` at runtime on the next change detection, and the bug stays silent until that response lands.

When storing array responses in an NgRx SignalStore via `tapResponse` (or any `patchState` of a list signal), wrap with `Array.isArray`:

```typescript
next: (items) => patchState(store, { items: Array.isArray(items) ? items : [] })
```

Apply the same guard to nested arrays inside response objects, for example `detail.Entries`, `detail.Quotas`.

## Loading States Pattern

```typescript
@Component({
  template: `
    @switch (dataResource.status()) {
      @case ('idle') {
        <p>Enter a search term</p>
      }
      @case ('loading') {
        <app-spinner />
      }
      @case ('reloading') {
        <app-data [data]="dataResource.value()" />
        <app-spinner size="small" />
      }
      @case ('resolved') {
        <app-data [data]="dataResource.value()" />
      }
      @case ('error') {
        <app-error 
          [error]="dataResource.error()" 
          (retry)="dataResource.reload()" 
        />
      }
    }
  `,
})
export class Data {
  query = signal('');
  dataResource = httpResource<Data[]>(() => 
    this.query() ? `/api/search?q=${this.query()}` : undefined
  );
}
```

## Service Layer Pattern

Encapsulate HTTP logic in services:

```typescript
import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { httpResource } from '@angular/common/http';

export interface User {
  id: string;
  name: string;
  email: string;
}

@Injectable({ providedIn: 'root' })
export class User {
  private http = inject(HttpClient);
  private baseUrl = '/api/users';
  
  // Current user ID for reactive fetching
  private currentUserId = signal<string | null>(null);
  
  // Reactive resource that updates when currentUserId changes
  currentUser = httpResource<User>(() => {
    const id = this.currentUserId();
    return id ? `${this.baseUrl}/${id}` : undefined;
  });
  
  // Set current user to fetch
  selectUser(id: string) {
    this.currentUserId.set(id);
  }
  
  // CRUD operations
  getAll() {
    return this.http.get<User[]>(this.baseUrl);
  }
  
  getById(id: string) {
    return this.http.get<User>(`${this.baseUrl}/${id}`);
  }
  
  create(user: Omit<User, 'id'>) {
    return this.http.post<User>(this.baseUrl, user);
  }
  
  update(id: string, user: Partial<User>) {
    return this.http.patch<User>(`${this.baseUrl}/${id}`, user);
  }
  
  delete(id: string) {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
```

## Caching Strategies

### Simple In-Memory Cache

```typescript
@Injectable({ providedIn: 'root' })
export class CachedUser {
  private http = inject(HttpClient);
  private cache = new Map<string, { data: User; timestamp: number }>();
  private cacheDuration = 5 * 60 * 1000; // 5 minutes
  
  getUser(id: string): Observable<User> {
    const cached = this.cache.get(id);
    
    if (cached && Date.now() - cached.timestamp < this.cacheDuration) {
      return of(cached.data);
    }
    
    return this.http.get<User>(`/api/users/${id}`).pipe(
      tap(user => {
        this.cache.set(id, { data: user, timestamp: Date.now() });
      })
    );
  }
  
  invalidateCache(id?: string) {
    if (id) {
      this.cache.delete(id);
    } else {
      this.cache.clear();
    }
  }
}
```

### Signal-Based Cache

```typescript
@Injectable({ providedIn: 'root' })
export class UserCache {
  private http = inject(HttpClient);
  
  // Cache as signal
  private usersCache = signal<Map<string, User>>(new Map());
  
  // Computed for easy access
  users = computed(() => Array.from(this.usersCache().values()));
  
  getUser(id: string): User | undefined {
    return this.usersCache().get(id);
  }
  
  async fetchUser(id: string): Promise<User> {
    const cached = this.getUser(id);
    if (cached) return cached;
    
    const user = await firstValueFrom(
      this.http.get<User>(`/api/users/${id}`)
    );
    
    this.usersCache.update(cache => {
      const newCache = new Map(cache);
      newCache.set(id, user);
      return newCache;
    });
    
    return user;
  }
}
```

## Pagination

### Paginated Resource

```typescript
interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

@Component({
  template: `
    @if (usersResource.isLoading()) {
      <app-spinner />
    } @else if (usersResource.hasValue()) {
      <ul>
        @for (user of usersResource.value().data; track user.id) {
          <li>{{ user.name }}</li>
        }
      </ul>
      
      <div class="pagination">
        <button 
          (click)="prevPage()" 
          [disabled]="page() === 1"
        >Previous</button>
        
        <span>Page {{ page() }} of {{ usersResource.value().totalPages }}</span>
        
        <button 
          (click)="nextPage()" 
          [disabled]="page() >= usersResource.value().totalPages"
        >Next</button>
      </div>
    }
  `,
})
export class UsersList {
  page = signal(1);
  pageSize = signal(10);
  
  usersResource = httpResource<PaginatedResponse<User>>(() => ({
    url: '/api/users',
    params: {
      page: this.page().toString(),
      pageSize: this.pageSize().toString(),
    },
  }));
  
  nextPage() {
    this.page.update(p => p + 1);
  }
  
  prevPage() {
    this.page.update(p => Math.max(1, p - 1));
  }
}
```

### Infinite Scroll

```typescript
@Component({
  template: `
    <ul>
      @for (user of allUsers(); track user.id) {
        <li>{{ user.name }}</li>
      }
    </ul>
    
    @if (isLoading()) {
      <app-spinner />
    }
    
    @if (hasMore()) {
      <button (click)="loadMore()">Load More</button>
    }
  `,
})
export class InfiniteUsers {
  private http = inject(HttpClient);
  
  private page = signal(1);
  private users = signal<User[]>([]);
  private totalPages = signal(1);
  
  allUsers = this.users.asReadonly();
  isLoading = signal(false);
  hasMore = computed(() => this.page() < this.totalPages());
  
  constructor() {
    this.loadPage(1);
  }
  
  loadMore() {
    this.loadPage(this.page() + 1);
  }
  
  private async loadPage(page: number) {
    this.isLoading.set(true);
    
    try {
      const response = await firstValueFrom(
        this.http.get<PaginatedResponse<User>>('/api/users', {
          params: { page: page.toString(), pageSize: '20' },
        })
      );
      
      this.users.update(users => [...users, ...response.data]);
      this.page.set(page);
      this.totalPages.set(response.totalPages);
    } finally {
      this.isLoading.set(false);
    }
  }
}
```

## File Upload

### Single File Upload

```typescript
@Component({
  template: `
    <input type="file" (change)="onFileSelected($event)" />
    
    @if (uploadProgress() !== null) {
      <progress [value]="uploadProgress()" max="100"></progress>
    }
  `,
})
export class FileUpload {
  private http = inject(HttpClient);
  
  uploadProgress = signal<number | null>(null);
  
  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    this.http.post('/api/upload', formData, {
      reportProgress: true,
      observe: 'events',
    }).subscribe(event => {
      if (event.type === HttpEventType.UploadProgress && event.total) {
        this.uploadProgress.set(Math.round(100 * event.loaded / event.total));
      } else if (event.type === HttpEventType.Response) {
        this.uploadProgress.set(null);
        console.log('Upload complete:', event.body);
      }
    });
  }
}
```

### Multiple Files

```typescript
uploadFiles(files: FileList) {
  const formData = new FormData();
  
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  
  return this.http.post<{ urls: string[] }>('/api/upload-multiple', formData);
}
```

## Request Cancellation

### With resource()

```typescript
// resource() automatically handles cancellation via abortSignal
searchResource = resource({
  params: () => ({ q: this.query() }),
  loader: async ({ params, abortSignal }) => {
    const response = await fetch(`/api/search?q=${params.q}`, {
      signal: abortSignal, // Cancels if params change
    });
    return response.json();
  },
});
```

### With HttpClient

```typescript
@Component({...})
export class Search implements OnDestroy {
  private http = inject(HttpClient);
  private destroyRef = inject(DestroyRef);
  
  query = signal('');
  results = signal<Result[]>([]);
  
  private searchSubscription?: Subscription;
  
  search() {
    // Cancel previous request
    this.searchSubscription?.unsubscribe();
    
    this.searchSubscription = this.http
      .get<Result[]>(`/api/search?q=${this.query()}`)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(results => this.results.set(results));
  }
}
```

### Debounced Search

```typescript
@Component({...})
export class SearchDebounced {
  query = signal('');
  
  private http = inject(HttpClient);
  
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
}
```

## Testing HTTP

### Testing httpResource

```typescript
describe('UserCmpt', () => {
  let component: UserCmpt;
  let httpMock: HttpTestingController;
  
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [UserCmpt],
      providers: [provideHttpClientTesting()],
    });
    
    component = TestBed.createComponent(UserCmpt).componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
  });
  
  it('should load user', () => {
    component.userId.set('123');
    
    const req = httpMock.expectOne('/api/users/123');
    req.flush({ id: '123', name: 'Test User' });
    
    expect(component.userResource.value()?.name).toBe('Test User');
  });
  
  afterEach(() => {
    httpMock.verify();
  });
});
```

### Testing Services

```typescript
describe('User', () => {
  let service: User;
  let httpMock: HttpTestingController;
  
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        User,
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });
    
    service = TestBed.inject(User);
    httpMock = TestBed.inject(HttpTestingController);
  });
  
  it('should create user', () => {
    const newUser = { name: 'Test', email: 'test@example.com' };
    
    service.create(newUser).subscribe(user => {
      expect(user.id).toBeDefined();
      expect(user.name).toBe('Test');
    });
    
    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(newUser);
    
    req.flush({ id: '1', ...newUser });
  });
});
```
