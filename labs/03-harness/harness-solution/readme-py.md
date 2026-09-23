# Harness Solution (Python)

This is the Python variant of [the harness solution](readme.md). The customization surfaces are the same four, rewritten for a FastAPI codebase, and the Product Inventory feature the Planner -> Implementer -> Reviewer chain builds is implemented in [product-inventory-py/](product-inventory-py/) as a runnable Python API instead of a set of files for the .NET ContosoInventory starter.

There is no Python ContosoInventory starter to drop files into, so `product-inventory-py/` is self-contained: it carries the parts of the starter the feature depends on (cookie login with the Admin and Viewer roles, the seeded categories) plus the Product feature itself.

## `.github/`

The customization files live at `product-inventory-py/.github/`, the root of the Python project, so GitHub Copilot discovers them when you open that folder as the workspace:

- `copilot-instructions.md`: repository-level coding standards for Python (snake_case naming, `Depends` injection, Pydantic DTOs, docstrings and type hints, SQL delta scripts, pytest).
- `instructions/routers.instructions.md`, `instructions/services.instructions.md`: path-specific guidance scoped by `applyTo` to `**/routers/**/*.py` and `**/services/**/*.py`.
- `prompts/generate-api-docs.prompt.md`: the reusable `/generate-api-docs` slash command, pointed at a router instead of a controller.
- `agents/planner.agent.md`, `agents/implementer.agent.md`, `agents/reviewer.agent.md`: the three chained custom agents with their handoffs. The **Write Tests First** handoff asks for pytest and `TestClient` instead of xUnit and Moq.

The frontmatter follows this repository's own `.github/` files rather than the lab text: the prompt file uses `agent: 'agent'`, the Implementer's terminal tool is `execute`, and the Planner's fetch tool is `web`.

## `product-inventory-py/`

| File | Purpose |
|------|---------|
| `app/main.py` | The FastAPI app: registers the routers, adds the security headers, and returns 400 for validation errors the way `[ApiController]` does |
| `app/dependencies.py` | `Depends` providers for the SQLite connection, the services, the signed-in user (`get_current_user`) and the Admin check (`require_admin`) |
| `app/schemas/product.py` | `ProductResponseDto`, `CreateProductDto`, `UpdateProductDto`, `RestockProductDto`, serialized with camelCase keys like the .NET DTOs |
| `app/services/product_service.py` | `ProductServiceProtocol` and the SQLite `ProductService`: SKU uniqueness check (case-insensitive), category existence check, restock |
| `app/routers/products.py` | CRUD plus `POST /api/products/{product_id}/restock`; every route needs a signed-in user and every write needs Admin |
| `app/routers/auth.py`, `app/routers/categories.py` | The starter surface the feature depends on: login, logout, current user, and the category list |
| `db/deltas/2026-09-23-01-baseline.sql` | The starter schema and seed: 9 active categories, `mateo@contoso.com` (Admin) and `megan@contoso.com` (Viewer), both with `Password123!` |
| `db/deltas/2026-09-23-02-add-products-table.sql` | The hand-written delta that creates the `Products` table, unique index on `Sku`, cascade delete on `CategoryId` |
| `scripts/apply_deltas.py` | Applies every delta in file name order; every script is idempotent, so a re-run is a no-op |

No migration generator is used. The same rule as the .NET solution applies: schema changes ship as hand-written SQL delta scripts, never Alembic.

## Endpoints added

| Method | Route | Auth |
|--------|-------|------|
| GET | `/api/products` (optional `?categoryId=`) | Any authenticated user |
| GET | `/api/products/{id}` | Any authenticated user |
| POST | `/api/products` | Admin |
| PUT | `/api/products/{id}` | Admin |
| DELETE | `/api/products/{id}` | Admin |
| POST | `/api/products/{id}/restock` | Admin |

## Run and verify

Requires Python 3.10 or later. Run every command from `labs/03-harness/harness-solution/product-inventory-py` in PowerShell 7.

1. Create a virtual environment and install FastAPI and Uvicorn:

    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2. Create the database from the delta scripts:

    ```powershell
    python scripts/apply_deltas.py
    ```

    Expected: `Applied 2026-09-23-01-baseline.sql` and `Applied 2026-09-23-02-add-products-table.sql`. Running it a second time prints the same two lines and changes nothing.

3. Start the API and leave the terminal running:

    ```powershell
    uvicorn app.main:app --port 5240
    ```

    Expected: `Uvicorn running on http://127.0.0.1:5240`. The Swagger UI is at `http://127.0.0.1:5240/swagger`.

4. In a second terminal, sign in as Mateo (Admin) and create a product:

    ```powershell
    $api = "http://127.0.0.1:5240/api"
    Invoke-RestMethod "$api/auth/login" -Method Post -ContentType "application/json" -Body '{"email":"mateo@contoso.com","password":"Password123!"}' -SessionVariable admin | Format-List
    $product = Invoke-RestMethod "$api/products" -Method Post -ContentType "application/json" -WebSession $admin -Body '{"name":"ThinkPad X1","sku":"TP-X1-001","description":"Business laptop","price":1499.99,"stockQuantity":10,"categoryId":1}'
    $product | Format-List
    ```

    Expected: the login returns `Mateo Gomez` with role `Admin`, and the new product has `categoryName` `Laptops & Desktops`. Each response is piped to `Format-List` so objects of different shapes all print when the block is pasted at once.

5. Exercise the rest of the Admin surface:

    ```powershell
    Invoke-RestMethod "$api/products?categoryId=1" -WebSession $admin | Format-List
    Invoke-RestMethod "$api/products/$($product.id)" -Method Put -ContentType "application/json" -WebSession $admin -Body '{"name":"ThinkPad X1 Carbon","sku":"TP-X1-001","description":"Business laptop","price":1599.99,"stockQuantity":8,"categoryId":1}' | Format-List
    Invoke-RestMethod "$api/products/$($product.id)/restock" -Method Post -ContentType "application/json" -WebSession $admin -Body '{"quantity":5}' | Format-List
    ```

    Expected: the filtered list holds the product, the update renames it and sets `stockQuantity` to `8`, and the restock raises it to `13`.

6. Check that bad input is rejected:

    ```powershell
    Invoke-RestMethod "$api/products" -Method Post -ContentType "application/json" -WebSession $admin -Body '{"name":"Ghost","sku":"GH-001","description":"x","price":10,"stockQuantity":1,"categoryId":999}' -SkipHttpErrorCheck -StatusCodeVariable code | Format-List; $code
    Invoke-RestMethod "$api/products" -Method Post -ContentType "application/json" -WebSession $admin -Body '{"name":"Copy","sku":"tp-x1-001","description":"x","price":10,"stockQuantity":1,"categoryId":1}' -SkipHttpErrorCheck -StatusCodeVariable code | Format-List; $code
    ```

    Expected: `detail : Category with ID 999 doesn't exist.` then `400`, and `detail : A product with the SKU 'tp-x1-001' already exists.` then `400`. The SKU check ignores case.

7. Sign in as Megan (Viewer) and confirm the Viewer role can read but not write:

    ```powershell
    Invoke-RestMethod "$api/auth/login" -Method Post -ContentType "application/json" -Body '{"email":"megan@contoso.com","password":"Password123!"}' -SessionVariable viewer | Format-List
    Invoke-RestMethod "$api/products" -WebSession $viewer -SkipHttpErrorCheck -StatusCodeVariable code | Out-Null; $code
    Invoke-RestMethod "$api/products/$($product.id)/restock" -Method Post -ContentType "application/json" -WebSession $viewer -Body '{"quantity":1}' -SkipHttpErrorCheck -StatusCodeVariable code | Out-Null; $code
    Invoke-RestMethod "$api/products" -SkipHttpErrorCheck -StatusCodeVariable code | Out-Null; $code
    ```

    Expected: `Megan Bowen` with role `Viewer`, then `200` for the read, `403` for the restock, and `401` for the request without a session.

8. Delete the product as Mateo:

    ```powershell
    Invoke-RestMethod "$api/products/$($product.id)" -Method Delete -WebSession $admin -SkipHttpErrorCheck -StatusCodeVariable code; $code
    ```

    Expected: `204`. Stop the server with `Ctrl+C` in the first terminal.

Sessions live in memory, so restarting the server signs everyone out. Delete `App_Data/` and re-run step 2 to start from a clean database.

## Differences from the .NET solution

| .NET solution | Python solution |
|---------------|-----------------|
| Files to copy into the ContosoInventory starter | A self-contained API with its own starter surface |
| ASP.NET Core Identity cookie | An in-memory session behind the same `.ContosoInventory.Auth` HttpOnly cookie |
| `[Authorize]` and `[Authorize(Roles = "Admin")]` | `Depends(get_current_user)` on the router and `Depends(require_admin)` on each write |
| `IProductService` interface | `ProductServiceProtocol` |
| Swagger UI at `/swagger` | FastAPI's Swagger UI, also at `/swagger` |
| No Blazor client | No client; the API is the whole surface |
