# Angular Routing

Configure routing in Angular v20+ with lazy loading, functional guards, and signal-based route parameters.

## Basic Setup

```typescript
// app.routes.ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: Home },
  { path: 'about', component: About },
  { path: '**', component: NotFound },
];

// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
  ],
};

// app.component.ts
import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <nav>
      <a routerLink="/home" routerLinkActive="active">Home</a>
      <a routerLink="/about" routerLinkActive="active">About</a>
    </nav>
    <router-outlet />
  `,
})
export class App {}
```

## Lazy Loading

Load feature modules on demand:

```typescript
// app.routes.ts
export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: Home },
  
  // Lazy load entire feature
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.routes').then(m => m.adminRoutes),
  },
  
  // Lazy load single component
  {
    path: 'settings',
    loadComponent: () => import('./settings/settings.component').then(m => m.Settings),
  },
];

// admin/admin.routes.ts
export const adminRoutes: Routes = [
  { path: '', component: AdminDashboard },
  { path: 'users', component: AdminUsers },
  { path: 'settings', component: AdminSettings },
];
```

## Route Parameters

### With Signal Inputs (Recommended)

```typescript
// Route config
{ path: 'users/:id', component: UserDetail }

// Component - use input() for route params
import { Component, input, computed } from '@angular/core';

@Component({
  selector: 'app-user-detail',
  template: `
    <h1>User {{ id() }}</h1>
  `,
})
export class UserDetail {
  // Route param as signal input
  id = input.required<string>();
  
  // Computed based on route param
  userId = computed(() => parseInt(this.id(), 10));
}
```

Enable with `withComponentInputBinding()`:

```typescript
// app.config.ts
import { provideRouter, withComponentInputBinding } from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding()),
  ],
};
```

#### A parent's `:param` needs `paramsInheritanceStrategy: 'always'` to reach a child input

`withComponentInputBinding()` alone is not enough when the `:param` is declared on a **parent** route
and consumed by a **child** component. Angular's default strategy is `emptyOnly`, which merges a
parent's params into a child only through path-less (empty-path) segments. Give the parent named
children and the merge stops: the child's `input.required<string>()` is never set and throws
`NG0950: Input "id" is required but no value is available yet` (see `angular-antipatterns.md` for the
other cause of that same error).

NG0950 is the loud version, and only a **required** input produces it. A plain `input<string>()` on the
same child simply stays at its default forever: no error, no console line, and a page that renders with
one field permanently empty. Check the strategy first whenever a child reads a parent's `:param` and
gets nothing, whether or not anything threw.

What makes it hard to spot is that the component worked before it moved:

```typescript
// worked: the param and the component sit on one route
{ path: 'projects/:id', loadComponent: () => import('./project-detail').then(m => m.ProjectDetail) }

// throws NG0950: :id is now on the parent, and 'draft' is not an empty path
{
  path: 'projects/:id',
  loadComponent: () => import('./project-shell').then(m => m.ProjectShell),
  children: [
    { path: 'draft', component: ProjectDraft },          // id = input.required<string>()
    { path: 'storyboard', component: ProjectStoryboard },
    { path: 'composition', component: ProjectComposition },
  ],
}
```

Fix it once in `provideRouter`, not by re-reading the param from `ActivatedRoute.parent` in every child:

```typescript
import { provideRouter, withComponentInputBinding, withRouterConfig } from '@angular/router';

provideRouter(
  routes,
  withComponentInputBinding(),
  withRouterConfig({ paramsInheritanceStrategy: 'always' }),
)
```

`withRouterConfig` takes one options object, so an app already passing it for `onSameUrlNavigation`
adds the key to that object rather than calling the feature twice.

**Proving it still holds**: route-test a child, never the shell. With the strategy set, navigate to
`/projects/42/draft` and assert the child renders `42`; then delete the `withRouterConfig` line and
re-run, and require NG0950. A test that passes both ways is asserting on the shell, which receives the
param either way.

### Query Parameters

```typescript
// Route: /search?q=angular&page=1

@Component({...})
export class Search {
  // Query params as inputs
  q = input<string>('');
  page = input<string>('1');
  
  currentPage = computed(() => parseInt(this.page(), 10));
}
```

### With ActivatedRoute (Alternative)

```typescript
import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';

@Component({...})
export class UserDetail {
  private route = inject(ActivatedRoute);
  
  // Convert route params to signal
  id = toSignal(
    this.route.paramMap.pipe(map(params => params.get('id'))),
    { initialValue: null }
  );
  
  // Query params
  query = toSignal(
    this.route.queryParamMap.pipe(map(params => params.get('q'))),
    { initialValue: '' }
  );
}
```

## Functional Guards

### Auth Guard

```typescript
// guards/auth.guard.ts
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(Auth);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  
  // Redirect to login with return URL
  return router.createUrlTree(['/login'], {
    queryParams: { returnUrl: state.url },
  });
};

// Usage in routes
{
  path: 'dashboard',
  component: Dashboard,
  canActivate: [authGuard],
}
```

### Role Guard

```typescript
export const roleGuard = (allowedRoles: string[]): CanActivateFn => {
  return (route, state) => {
    const authService = inject(Auth);
    const router = inject(Router);
    
    const userRole = authService.currentUser()?.role;
    
    if (userRole && allowedRoles.includes(userRole)) {
      return true;
    }
    
    return router.createUrlTree(['/unauthorized']);
  };
};

// Usage
{
  path: 'admin',
  component: Admin,
  canActivate: [authGuard, roleGuard(['admin', 'superadmin'])],
}
```

### Can Deactivate Guard

```typescript
export interface CanDeactivate {
  canDeactivate: () => boolean | Promise<boolean>;
}

export const unsavedChangesGuard: CanDeactivateFn<CanDeactivate> = (component) => {
  if (component.canDeactivate()) {
    return true;
  }
  
  return confirm('You have unsaved changes. Leave anyway?');
};

// Component implementation
@Component({...})
export class Edit implements CanDeactivate {
  form = inject(FormBuilder).group({...});
  
  canDeactivate(): boolean {
    return !this.form.dirty;
  }
}

// Route
{
  path: 'edit/:id',
  component: Edit,
  canDeactivate: [unsavedChangesGuard],
}
```

## Resolvers

Pre-fetch data before route activation:

```typescript
// resolvers/user.resolver.ts
import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';

export const userResolver: ResolveFn<User> = (route) => {
  const userService = inject(User);
  const id = route.paramMap.get('id')!;
  return userService.getById(id);
};

// Route config
{
  path: 'users/:id',
  component: UserDetail,
  resolve: { user: userResolver },
}

// Component - access resolved data via input
@Component({...})
export class UserDetail {
  user = input.required<User>();
}
```

## Gotcha: `router.url` includes the query string, so exact-match route checks break on deep links

`router.url` and `NavigationEnd.urlAfterRedirects` carry the **full URL including `?query` and `#fragment`**. A route-derived `computed()` / `linkedSignal()` that decides behavior by **exact equality** on that value silently falls through the moment any query param is present:

```typescript
// current URL signal (from router.url / NavigationEnd)
private currentUrl = toSignal(/* … router.events → urlAfterRedirects … */, { initialValue: this.router.url });

// BUG: returns null as soon as the route is reached with a query param
mode = computed(() => {
  const url = this.currentUrl();
  if (url === '/orders')   return 'a';   // fails for '/orders?reopenId=16'
  if (url === '/invoices') return 'b';
  return null;                           // ← unintended fallback on any deep link
});
```

Symptom: a route-conditional feature works from a plain in-app navigation but **misbehaves when the same route is reached WITH a query param** — e.g. reopening a modal/wizard via `/orders?reopenId=16` picks the *wrong* variant because the exact match fails and a downstream `?? 'fallback'` kicks in. It looks like a state bug but it's the URL comparison.

Fix — strip query/fragment before an exact-equality compare, and keep exact equality (do NOT loosen to `startsWith`, which would wrongly match sub-routes like `/orders/123`):

```typescript
const url = this.currentUrl().split('?')[0].split('#')[0];
if (url === '/orders') return 'a';
```

Note: `startsWith` checks (e.g. auto-expand a nav group for a route tree) are already immune since the query suffix rides along harmlessly; it is **exact-equality** checks that are the trap. Read the query param itself via `ActivatedRoute.queryParamMap` (a flat object for the whole URL), not by parsing `router.url`.

## Nested Routes

```typescript
// Parent route with children
export const routes: Routes = [
  {
    path: 'products',
    component: ProductsLayout,
    children: [
      { path: '', component: ProductList },
      { path: ':id', component: ProductDetail },
      { path: ':id/edit', component: ProductEdit },
    ],
  },
];

// ProductsLayout
@Component({
  imports: [RouterOutlet],
  template: `
    <h1>Products</h1>
    <router-outlet /> <!-- Child routes render here -->
  `,
})
export class ProductsLayout {}
```

## Programmatic Navigation

```typescript
import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

@Component({...})
export class Product {
  private router = inject(Router);
  
  // Navigate to route
  goToProducts() {
    this.router.navigate(['/products']);
  }
  
  // Navigate with params
  goToProduct(id: string) {
    this.router.navigate(['/products', id]);
  }
  
  // Navigate with query params
  search(query: string) {
    this.router.navigate(['/search'], {
      queryParams: { q: query, page: 1 },
    });
  }
  
  // Navigate relative to current route
  goToEdit() {
    this.router.navigate(['edit'], { relativeTo: this.route });
  }
  
  // Replace current history entry
  replaceUrl() {
    this.router.navigate(['/new-page'], { replaceUrl: true });
  }
}
```

## Route Data

```typescript
// Static route data
{
  path: 'admin',
  component: Admin,
  data: {
    title: 'Admin Dashboard',
    roles: ['admin'],
  },
}

// Access in component
@Component({...})
export class AdminCmpt {
  title = input<string>(); // From route data
  roles = input<string[]>(); // From route data
}

// Or via ActivatedRoute
private route = inject(ActivatedRoute);
data = toSignal(this.route.data);
```

## Router Events

```typescript
import { Router, NavigationStart, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs';

@Component({...})
export class AppMain {
  private router = inject(Router);
  
  isNavigating = signal(false);
  
  constructor() {
    this.router.events.pipe(
      filter(e => e instanceof NavigationStart || e instanceof NavigationEnd)
    ).subscribe(event => {
      this.isNavigating.set(event instanceof NavigationStart);
    });
  }
}
```

## Route Configuration Options

### Full Route Options

```typescript
{
  path: 'users/:id',
  component: UserCmpt,
  
  // Lazy loading alternatives
  loadComponent: () => import('./user.component').then(m => m.UserCmpt),
  loadChildren: () => import('./user.routes').then(m => m.userRoutes),
  
  // Guards
  canActivate: [authGuard],
  canActivateChild: [authGuard],
  canDeactivate: [unsavedChangesGuard],
  canMatch: [featureFlagGuard],
  
  // Data
  resolve: { user: userResolver },
  data: { title: 'User Profile', animation: 'userPage' },
  
  // Children
  children: [...],
  
  // Outlet
  outlet: 'sidebar',
  
  // Path matching
  pathMatch: 'full', // or 'prefix'
  
  // Title
  title: 'User Profile',
  // Or dynamic title
  title: userTitleResolver,
}
```

### Dynamic Title Resolver

```typescript
export const userTitleResolver: ResolveFn<string> = (route) => {
  const userService = inject(User);
  const id = route.paramMap.get('id')!;
  return userService.getById(id).pipe(
    map(user => `${user.name} - Profile`)
  );
};
```

## Authentication Flow

### Complete Auth Setup

```typescript
// auth.service.ts
@Injectable({ providedIn: 'root' })
export class Auth {
  private _user = signal<User | null>(null);
  private _token = signal<string | null>(null);
  
  readonly user = this._user.asReadonly();
  readonly isAuthenticated = computed(() => this._user() !== null);
  
  private router = inject(Router);
  private http = inject(HttpClient);
  
  async login(credentials: Credentials): Promise<boolean> {
    try {
      const response = await firstValueFrom(
        this.http.post<AuthResponse>('/api/login', credentials)
      );
      
      this._token.set(response.token);
      this._user.set(response.user);
      localStorage.setItem('token', response.token);
      
      return true;
    } catch {
      return false;
    }
  }
  
  logout(): void {
    this._user.set(null);
    this._token.set(null);
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }
  
  async checkAuth(): Promise<boolean> {
    const token = localStorage.getItem('token');
    if (!token) return false;
    
    try {
      const user = await firstValueFrom(
        this.http.get<User>('/api/me')
      );
      this._user.set(user);
      this._token.set(token);
      return true;
    } catch {
      localStorage.removeItem('token');
      return false;
    }
  }
}

// auth.guard.ts
export const authGuard: CanActivateFn = async (route, state) => {
  const authService = inject(Auth);
  const router = inject(Router);
  
  // Check if already authenticated
  if (authService.isAuthenticated()) {
    return true;
  }
  
  // Try to restore session
  const isValid = await authService.checkAuth();
  if (isValid) {
    return true;
  }
  
  // Redirect to login
  return router.createUrlTree(['/login'], {
    queryParams: { returnUrl: state.url },
  });
};

// login.component.ts
import { form, FormField, required } from '@angular/forms/signals';

interface LoginData { email: string; password: string; }

@Component({
  imports: [FormField],
  template: `
    <form (submit)="login($event)">
      <input type="email" [formField]="loginForm.email" />
      <input type="password" [formField]="loginForm.password" />
      <button type="submit" [disabled]="loginForm().invalid()">Login</button>
    </form>
  `,
})
export class Login {
  private authService = inject(Auth);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  private loginModel = signal<LoginData>({ email: '', password: '' });
  loginForm = form(this.loginModel, (s) => {
    required(s.email);
    required(s.password);
  });

  async login(event: Event) {
    event.preventDefault();
    if (!this.loginForm().valid()) return;
    const success = await this.authService.login(this.loginModel());
    if (success) {
      const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
      this.router.navigateByUrl(returnUrl);
    }
  }
}
```

### Template-driven login variant (legacy codebases)

The same login component with `[(ngModel)]`, for codebases not yet on Signal Forms:

```typescript
// login.component.ts
@Component({
  template: `
    <form (ngSubmit)="login()">
      <input [(ngModel)]="email" name="email" />
      <input [(ngModel)]="password" name="password" type="password" />
      <button type="submit">Login</button>
    </form>
  `,
})
export class Login {
  private authService = inject(Auth);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  
  email = '';
  password = '';
  
  async login() {
    const success = await this.authService.login({
      email: this.email,
      password: this.password,
    });
    
    if (success) {
      const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
      this.router.navigateByUrl(returnUrl);
    }
  }
}
```

## Breadcrumbs

```typescript
// breadcrumb.service.ts
@Injectable({ providedIn: 'root' })
export class Breadcrumb {
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  
  breadcrumbs = toSignal(
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd),
      map(() => this.buildBreadcrumbs(this.route.root))
    ),
    { initialValue: [] }
  );
  
  private buildBreadcrumbs(
    route: ActivatedRoute,
    url: string = '',
    breadcrumbs: Breadcrumb[] = []
  ): Breadcrumb[] {
    const children = route.children;
    
    if (children.length === 0) {
      return breadcrumbs;
    }
    
    for (const child of children) {
      const routeUrl = child.snapshot.url
        .map(segment => segment.path)
        .join('/');
      
      if (routeUrl) {
        url += `/${routeUrl}`;
      }
      
      const label = child.snapshot.data['breadcrumb'];
      if (label) {
        breadcrumbs.push({ label, url });
      }
      
      return this.buildBreadcrumbs(child, url, breadcrumbs);
    }
    
    return breadcrumbs;
  }
}

// Route config with breadcrumb data
export const routes: Routes = [
  {
    path: 'products',
    data: { breadcrumb: 'Products' },
    children: [
      { path: '', component: ProductList },
      {
        path: ':id',
        data: { breadcrumb: 'Product Details' },
        component: ProductDetail,
      },
    ],
  },
];

// breadcrumb.component.ts
@Component({
  selector: 'app-breadcrumb',
  template: `
    <nav aria-label="Breadcrumb">
      <ol>
        <li><a routerLink="/">Home</a></li>
        @for (crumb of breadcrumbService.breadcrumbs(); track crumb.url) {
          <li>
            <a [routerLink]="crumb.url">{{ crumb.label }}</a>
          </li>
        }
      </ol>
    </nav>
  `,
})
export class BreadcrumbCmpt {
  breadcrumbService = inject(Breadcrumb);
}
```

## Tab Navigation

```typescript
// tabs-layout.component.ts
@Component({
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="tabs">
      @for (tab of tabs; track tab.path) {
        <a 
          [routerLink]="tab.path" 
          routerLinkActive="active"
          [routerLinkActiveOptions]="{ exact: tab.exact }"
        >
          {{ tab.label }}
        </a>
      }
    </div>
    <div class="tab-content">
      <router-outlet />
    </div>
  `,
})
export class TabsLayout {
  tabs = [
    { path: './', label: 'Overview', exact: true },
    { path: 'details', label: 'Details', exact: false },
    { path: 'settings', label: 'Settings', exact: false },
  ];
}

// Routes
{
  path: 'account',
  component: TabsLayout,
  children: [
    { path: '', component: AccountOverview },
    { path: 'details', component: AccountDetails },
    { path: 'settings', component: AccountSettings },
  ],
}
```

## Modal Routes

Using auxiliary outlets for modals:

```typescript
// Routes
export const routes: Routes = [
  { path: 'products', component: ProductList },
  { path: 'product-modal/:id', component: ProductModal, outlet: 'modal' },
];

// App template
@Component({
  template: `
    <router-outlet />
    <router-outlet name="modal" />
  `,
})
export class App {}

// Open modal
this.router.navigate([{ outlets: { modal: ['product-modal', productId] } }]);

// Close modal
this.router.navigate([{ outlets: { modal: null } }]);

// Link to open modal
<a [routerLink]="[{ outlets: { modal: ['product-modal', product.id] } }]">
  View Details
</a>
```

## Preloading Strategies

### Built-in Strategies

```typescript
import { 
  provideRouter, 
  withPreloading,
  PreloadAllModules,
  NoPreloading 
} from '@angular/router';

// Preload all lazy modules
provideRouter(routes, withPreloading(PreloadAllModules))

// No preloading (default)
provideRouter(routes, withPreloading(NoPreloading))
```

### Custom Preloading Strategy

```typescript
// selective-preload.strategy.ts
@Injectable({ providedIn: 'root' })
export class SelectivePreloadStrategy implements PreloadingStrategy {
  preload(route: Route, load: () => Observable<any>): Observable<any> {
    // Only preload routes marked with data.preload = true
    if (route.data?.['preload']) {
      return load();
    }
    return of(null);
  }
}

// Routes
{
  path: 'dashboard',
  loadComponent: () => import('./dashboard.component'),
  data: { preload: true }, // Will be preloaded
}

// Config
provideRouter(routes, withPreloading(SelectivePreloadStrategy))
```

### Network-Aware Preloading

```typescript
@Injectable({ providedIn: 'root' })
export class NetworkAwarePreloadStrategy implements PreloadingStrategy {
  preload(route: Route, load: () => Observable<any>): Observable<any> {
    // Check network conditions
    const connection = (navigator as any).connection;
    
    if (connection) {
      // Don't preload on slow connections
      if (connection.saveData || connection.effectiveType === '2g') {
        return of(null);
      }
    }
    
    // Preload if marked
    if (route.data?.['preload']) {
      return load();
    }
    
    return of(null);
  }
}
```

## Route Animations

```typescript
// app.routes.ts
export const routes: Routes = [
  { path: 'home', component: Home, data: { animation: 'HomePage' } },
  { path: 'about', component: About, data: { animation: 'AboutPage' } },
];

// app.component.ts
@Component({
  imports: [RouterOutlet],
  template: `
    <div [@routeAnimations]="getRouteAnimationData()">
      <router-outlet />
    </div>
  `,
  animations: [
    trigger('routeAnimations', [
      transition('HomePage <=> AboutPage', [
        style({ position: 'relative' }),
        query(':enter, :leave', [
          style({
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
          }),
        ]),
        query(':enter', [style({ left: '-100%' })]),
        query(':leave', animateChild()),
        group([
          query(':leave', [animate('300ms ease-out', style({ left: '100%' }))]),
          query(':enter', [animate('300ms ease-out', style({ left: '0%' }))]),
        ]),
      ]),
    ]),
  ],
})
export class AppMain {
  getRouteAnimationData() {
    return this.route.firstChild?.snapshot.data['animation'];
  }
}
```

## Scroll Position Restoration

```typescript
// app.config.ts
import { 
  provideRouter, 
  withInMemoryScrolling,
  withRouterConfig 
} from '@angular/router';

provideRouter(
  routes,
  withInMemoryScrolling({
    scrollPositionRestoration: 'enabled', // or 'top'
    anchorScrolling: 'enabled',
  }),
  withRouterConfig({
    onSameUrlNavigation: 'reload',
  })
)
```
