# Spec: Port `angular-devops` features to `react-devops`

## Overview

Bring `src/react/react-devops` to feature parity with `src/angular/angular-devops`. Both apps serve the same "Food Shop" demo but the React project is missing the environment-scoped greeting, coverage configuration, and a hardened nginx config.

---

## Current State

| Feature                                      | Angular    | React      |
| -------------------------------------------- | ---------- | ---------- |
| Heading ("Food Shop")                        | ✅         | ✅         |
| `food.png` image                             | ✅         | ✅         |
| Click counter                                | ✅         | ✅         |
| Environment greeting                         | ✅         | ❌         |
| Unit tests (Vitest)                          | ✅ 3 tests | ✅ 3 tests |
| Unit test coverage (cobertura)               | ✅         | ❌         |
| `npm test` / `npm run test:coverage` scripts | ✅         | ❌         |
| E2E tests (Playwright)                       | ✅ 3 tests | ✅ 3 tests |
| Greeting unit test                           | ✅         | ❌         |
| Greeting E2E test                            | ✅         | ❌         |
| Multi-stage Dockerfile                       | ✅         | ✅         |
| nginx gzip + optimized config                | ✅         | ❌         |

---

## What Needs to Be Built

### 1. Environment greeting via Vite env var

Angular uses `environment.ts` with a `greeting` token (`{{greeting}}`) replaced at CI/CD time. Vite's equivalent is `VITE_*` env vars.

- Create `src/env.ts` exporting `greeting = import.meta.env.VITE_GREETING ?? 'Hello Development Environment'`
- Display the greeting as an `<h5>` below `<h1>` in `App.tsx`

**Angular source:**

```ts
// environment.ts (production)
export const environment = { greeting: '{{greeting}}' };

// environment.development.ts
export const environment = { greeting: 'Hello Development Environment' };
```

**React equivalent:**

```ts
// src/env.ts
export const greeting = import.meta.env.VITE_GREETING ?? 'Hello Development Environment';
```

### 2. Update `App.tsx`

Add the greeting display:

```tsx
import { greeting } from './env';

// Inside JSX:
<h5>{greeting}</h5>
```

### 3. Add greeting unit test in `App.test.tsx`

```ts
it('renders greeting text', () => {
  render(<App />);
  const h5 = screen.getByRole('heading', { level: 5 });
  expect(h5).toHaveTextContent('Hello Development Environment');
});
```

### 4. Add greeting E2E test in `e2e/playwright/app.e2e.spec.ts`

```ts
test('renders greeting text', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 5 })).toBeVisible();
});
```

### 5. Add Vitest coverage configuration

Update `vitest.config.ts` to mirror Angular's coverage setup (cobertura format for Azure DevOps):

```ts
coverage: {
  provider: 'v8',
  reporter: ['text', 'html', 'cobertura'],
  reportsDirectory: './coverage',
  include: ['src/**/*.{ts,tsx}'],
  exclude: ['src/**/*.test.tsx', 'src/main.tsx', 'src/setup.ts'],
},
```

Also add `@vitest/coverage-v8` to `devDependencies`.

### 6. Add `test` and `test:coverage` npm scripts

Update `package.json` scripts to match Angular's conventions:

```json
"test": "vitest run",
"test:watch": "vitest",
"test:coverage": "vitest run --coverage"
```

### 7. Harden `conf/nginx.conf`

Replace the minimal config with gzip compression matching the Angular config:

```nginx
server {
    listen 0.0.0.0:80;
    listen [::]:80;
    default_type application/octet-stream;

    gzip                    on;
    gzip_comp_level         6;
    gzip_vary               on;
    gzip_min_length         1000;
    gzip_proxied            any;
    gzip_types              text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_buffers            16 8k;
    client_max_body_size    256M;

    root /usr/share/nginx/html;

    location / {
        try_files $uri $uri/ /index.html =404;
    }
}
```

---

## Files to Create or Modify

| File                                                    | Action     | Notes                                                                               |
| ------------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------- |
| `src/react/react-devops/src/env.ts`                     | **Create** | Vite env var wrapper for greeting                                                   |
| `src/react/react-devops/src/App.tsx`                    | **Modify** | Import `greeting`, add `<h5>`                                                       |
| `src/react/react-devops/src/App.test.tsx`               | **Modify** | Add greeting unit test                                                              |
| `src/react/react-devops/e2e/playwright/app.e2e.spec.ts` | **Modify** | Add greeting E2E test                                                               |
| `src/react/react-devops/vitest.config.ts`               | **Modify** | Add coverage block                                                                  |
| `src/react/react-devops/package.json`                   | **Modify** | Add `test`, `test:watch`, `test:coverage` scripts; add `@vitest/coverage-v8` devDep |
| `src/react/react-devops/conf/nginx.conf`                | **Modify** | Add gzip compression                                                                |

---

## Key Decisions

- **`VITE_GREETING` not `REACT_APP_*`** — project uses Vite, not CRA. Env vars must be prefixed `VITE_`.
- **Fallback value** — default to `'Hello Development Environment'` so the app works locally without any `.env` file, matching Angular's `environment.development.ts`.
- **`vitest run` for `test` script** — runs once without watch mode, matching Angular's `ng test --watch=false`.
- **No `.env` files committed** — the `{{greeting}}` substitution is done at CI/CD time (token replacement in pipeline), same as Angular. No `.env` file needed in the repo.

## Out of Scope

- Adding Angular router equivalent (both apps have no routes)
- Migrating the Angular app
- Azure DevOps pipeline changes
- Any styling / visual redesign
