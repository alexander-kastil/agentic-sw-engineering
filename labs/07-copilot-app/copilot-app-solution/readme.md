# Lab 07 Solution: Copilot App Code Deliverable

The concrete, checkable output of [Lab 07](../readme.md) Step 2 (the prompt sent to the Copilot desktop app session), verified from a terminal rather than the app itself. See [test-results.md](test-results.md) for the commands run and their results.

| File | Lab step |
|---|---|
| [src/food-app/food-shop/src/app/food/shop/shop-container/food-shop-container.component.html](src/food-app/food-shop/src/app/food/shop/shop-container/food-shop-container.component.html) | Step 2 - the shop landing page had no heading before this change; adds `<h1>Fresh Food, Fast</h1>` |
| [src/food-app/food-shop/src/app/food/shop/shop-container/food-shop-container.component.spec.ts](src/food-app/food-shop/src/app/food/shop/shop-container/food-shop-container.component.spec.ts) | Step 2 - adds the unit test asserting the heading renders, alongside the DI mocks it needs to run in isolation |
| [docs/agent-runbook.md](docs/agent-runbook.md) | Step 2 - records the model, reasoning effort, and permission mode the session ran with |
| [test-results.md](test-results.md) | Steps 2 and 5 - the baseline suite run, the verified heading test, and which steps are desktop-app-only |

Paths mirror their real location in the repository (`src/food-app/food-shop/...` and `docs/...` from the repository root). None of these files are applied to `src/food-app/food-shop/` or `docs/` in the live repository; that project was left exactly as checked in.
