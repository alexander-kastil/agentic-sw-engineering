# Test Results

All commands were run against `src/food-app/food-shop` (Node v24, npm on PATH, Windows). The suite in the checked-in repository is green; the heading change and its test were verified by applying this folder's `food-shop-container.component.html` and `food-shop-container.component.spec.ts` on top of the real project, running the suite, then restoring both files by hand (never with `git restore`, `git checkout`, or `git stash`, since another session shares the checkout).

## Baseline (unmodified `src/food-app/food-shop`)

```bash
cd src/food-app/food-shop
npm install
```

```text
up to date, audited 680 packages in 2s
140 packages are looking for funding
22 vulnerabilities (1 low, 6 moderate, 13 high, 2 critical)
```

```bash
npm test -- --watch=false --browsers=ChromeHeadless
```

```text
Chrome Headless 153.0.0.0 (Windows 10): Executed 0 of 4 SUCCESS (0 secs / 0 secs)
Chrome Headless 153.0.0.0 (Windows 10): Executed 4 of 4 SUCCESS (0.063 secs / 0.058 secs)
TOTAL: 4 SUCCESS
```

**Baseline suite: PASS.** All four spec files (`NavbarComponent`, `CurrentUserComponent`, `CheckoutResponseComponent`, `FoodShopContainerComponent`) pass on a clean checkout.

## Verifying the change (applied to the real project, then reverted by hand)

`food-shop-container.component.html` and `food-shop-container.component.spec.ts` from this folder were copied over the real files at:

```text
src/food-app/food-shop/src/app/food/shop/shop-container/food-shop-container.component.html
src/food-app/food-shop/src/app/food/shop/shop-container/food-shop-container.component.spec.ts
```

```bash
npm test -- --watch=false --browsers=ChromeHeadless
```

```text
Chrome Headless 153.0.0.0 (Windows 10): Executed 0 of 5 SUCCESS (0 secs / 0 secs)
Chrome Headless 153.0.0.0 (Windows 10): Executed 5 of 5 SUCCESS (0.069 secs / 0.062 secs)
TOTAL: 5 SUCCESS
```

**New heading test: PASS.** The added spec, `FoodShopContainerComponent should render the "Fresh Food, Fast" heading`, passes alongside the existing `should create` test and the other three spec files, which are unaffected. Both changed files were then restored to their exact prior content in `src/food-app/food-shop`, confirmed with `git status --short -- src/food-app/` showing no diff beyond the pre-existing test-suite fix.

```bash
npm start
```

```text
Application bundle generation complete. [4.234 seconds]
Local:   http://localhost:4200/
```

**Dev server: PASS.** Serves without error.

## Pass/fail summary

| Check | Result |
|---|---|
| Baseline suite (`npm test`, unmodified checkout) | PASS - 4 of 4 specs |
| New heading test (`FoodShopContainerComponent` heading spec) | PASS |
| No other test broken by this change | PASS - suite goes from 4 to 5 passing, no regressions |
| `npm install` | PASS |
| `npm start` | PASS |

## Desktop-app-only steps (not executable here)

Steps 1, 2 (composer/Plan tab), 3 (worktree isolation from the app), 6 (agent-attached screenshot), 7 (review-comment resolution and Agent Merge), 8 (session capability listing), 9 (scheduled automation), and 10 (VS Code external sessions list) all require the GitHub Copilot desktop app UI and were not run. The MCP/skills claim in Step 8 and the links in the Links & Resources section were checked directly against the repository instead.
