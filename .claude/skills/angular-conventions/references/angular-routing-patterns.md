# Angular Routing Patterns

## Table of Contents
- [Route Configuration Options](#route-configuration-options)
- [Authentication Flow](#authentication-flow)
- [Breadcrumbs](#breadcrumbs)
- [Tab Navigation](#tab-navigation)
- [Modal Routes](#modal-routes)
- [Preloading Strategies](#preloading-strategies)
- [Renaming a Route Segment](#renaming-a-route-segment)

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

## Renaming a Route Segment

Renaming `/deployment` to `/operations` is **not** a one-line edit in the routes file. The old name
leaks into files the compiler will never connect to the route definition, and into visible copy that no
grep for `path:` will ever surface. Sweep all six categories before declaring it done.

| # | Where the old name hides | Symptom if missed |
| --- | --- | --- |
| 1 | `path:` in the route config | The route 404s (or hits the catch-all) |
| 2 | `routerLink` in templates | Dead nav link |
| 3 | **URL strings inside components** | Compiles and renders, but derived state is silently wrong |
| 4 | **Guards / resolvers building `UrlTree`s** | Redirect lands on the old, now nonexistent path |
| 5 | **Visible copy echoing the old name** | Page contradicts its own nav item |
| 6 | Docs, skills, READMEs, E2E specs | Stale instructions that outlive everyone's memory |

Category 5 is the one that gets discovered by the user rather than by you, one item at a time. The nav
link's own text is only the first tier: the same word typically also sits in the page eyebrow, in
section headings, and in tab labels, in three different files, none of which contain the URL at all.
Grepping the segment finds none of them, because the copy says `Deployment` while the route says
`/deployment`.

**So enumerate before editing.** Grep the bare *word*, case-insensitively, across templates and
component TypeScript, and put the full list of visible occurrences in front of the user up front:

```bash
grep -rni "deployment" --include="*.html" --include="*.ts" src/app | grep -v "\.spec\.ts"
```

Then ask which tiers should follow the rename, because they are genuinely independent decisions: a
section heading like `App Deployments` describes its *content* and may be better renamed to something
accurate rather than mechanically to the new nav word. Doing one tier and waiting to be told about the
next turns a single change into three round trips.

Categories 3 and 4 are the dangerous ones because nothing fails loudly. A tab shell that derives its
active tab from the URL is the classic case:

```ts
// Breaks silently on rename: builds fine, no tab ever matches, always falls back to tabs[0]
readonly activeTab = computed(
  () => this.tabs.find((tab) => this.url().includes(`/deployment/${tab.path}`)) ?? this.tabs[0],
);
```

Same for a guard that hardcodes the segment while building a redirect:

```ts
return router.createUrlTree([tab === 'graph' ? '/deployment' : '/dashboard'], { queryParams });
```

Find every occurrence before editing anything, and grep for the bare segment rather than only `path:`:

```bash
grep -rn "/deployment" --include="*.ts" --include="*.html" src/
```

### Keep the old URL working

Existing links, bookmarks, and anything already shared with a customer must not break. Add a legacy
alias, and use `pathMatch: 'prefix'` rather than `'full'`: a local (non-absolute) `redirectTo` with
prefix matching automatically carries the remaining segments over, so child routes forward too.

```ts
{ path: 'operations', /* ...the real route with its children... */ },

// Legacy alias: /deployment/fleet -> /operations/fleet, /deployment -> /operations
{ path: 'deployment', redirectTo: 'operations', pathMatch: 'prefix' },

{ path: '**', redirectTo: '' },   // aliases must come BEFORE the catch-all
```

With `pathMatch: 'full'` only the bare `/deployment` would redirect and every deep link would fall
through to the catch-all instead.

### Scope discipline

"Change the URL" means the URL. A route segment, the component file/folder, the class name, and the
nav label are four independent things that merely happen to share a word today. Rename only what was
asked: leaving `DeploymentPage` and `deployment.data.ts` untouched under an `/operations` URL is
correct, not an inconsistency to tidy up. Verify the result by loading both the new URL and the old
one, and confirm the active-state highlight still follows the route.
