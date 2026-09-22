# Test Results

Environment: Windows 11, .NET SDKs installed: 9.0.310, 10.0.102, 10.0.112 (`dotnet --list-sdks`). Starter repo cloned at `C:\Users\ALEXAN~1\AppData\Local\Temp\claude\D--git-classes-agentic-sw-engineering\0b9ef576-0f1b-414a-9114-61b2d233e6e4\scratchpad\lr\github-copilot-customization-starter-app`.

## Long-path issue with the scratchpad clone

`dotnet build` from the scratchpad clone's path fails with:

```text
C:\Program Files\dotnet\sdk\10.0.112\Microsoft.Common.CurrentVersion.targets(4903,5): error MSB3030: Could not copy the file "obj\Debug\net10.0\ContosoInventory.Shared.dll" because it was not found.
```

The DLL exists on disk (verified directly); the full destination path is around 260 characters, the classic Win32 `MAX_PATH` limit, and `core.longpaths=true` (a Git setting) does not make MSBuild's copy task long-path aware. This is an artifact of the scratchpad's deeply nested temp path, not a defect in the starter app or the guide. Worked around by copying the solution to `C:\co\ContosoInventory` (a short path) for every build, run, and test below.

## Step 1: verify starter app claims against the real files

| Guide claim | Command / check | Result |
|---|---|---|
| Three-project architecture (Server, Client, Shared) | `ls ContosoInventory` | Pass |
| `ContosoInventory.Server/Data/Migrations/` folder | `ls ContosoInventory.Server` | Fail: actual path is `ContosoInventory.Server/Migrations/` (no `Data/` segment). Fixed in `readme.md`. |
| Controllers: `AuthController.cs`, `CategoriesController.cs` | `ls ContosoInventory.Server/Controllers` | Pass |
| `CategoriesController` has 6 endpoints (GetAll, GetById, Create, Update, Delete, ToggleActive) | Read `CategoriesController.cs` | Pass |
| Shared DTOs: `CategoryResponseDto`, `CreateCategoryDto`, `UpdateCategoryDto`, `LoginDto`, `UserInfoDto` | `ls ContosoInventory.Shared/DTOs` | Pass |
| "The project targets .NET 8 by default... update to .NET 10" | `cat *.csproj` | Pass: all three `.csproj` files had `<TargetFramework>net8.0</TargetFramework>` |
| Login credentials `mateo@contoso.com` / `Password123!` (Admin), `megan@contoso.com` / `Password123!` (Viewer) | Read `DbInitializer.cs`, then live login | Pass |
| Server listens on `http://localhost:5240` | Read `launchSettings.json`, then live run | Pass |
| "nine total categories, nine active, and zero inactive" | `GET /api/categories` after login | Pass (see below). The repo ships a pre-seeded `App_Data/ContosoInventory.db` committed to git (`git ls-files` confirms it), which already has 9 categories all active; `DbInitializer.cs` alone (an empty DB) would only seed 8, one of them inactive, but that code path never runs against a fresh clone because the checked-in `.db` file is not empty. |
| Viewer role can read but not write categories | Live login as Megan, `POST /api/categories` | Pass: 403 |

### Retargeting to .NET 10

```powershell
sed -i 's/<TargetFramework>net8.0<\/TargetFramework>/<TargetFramework>net10.0<\/TargetFramework>/' ContosoInventory.Server/ContosoInventory.Server.csproj ContosoInventory.Client/ContosoInventory.Client.csproj ContosoInventory.Shared/ContosoInventory.Shared.csproj
```

### Build (from the short path `C:\co\ContosoInventory`, after retargeting, before the Product feature)

```powershell
dotnet build ContosoInventory.sln
```

```text
  ContosoInventory.Shared -> C:\co\ContosoInventory\ContosoInventory.Shared\bin\Debug\net10.0\ContosoInventory.Shared.dll
  ContosoInventory.Client -> C:\co\ContosoInventory\ContosoInventory.Client\bin\Debug\net10.0\ContosoInventory.Client.dll
  ContosoInventory.Client (Blazor output) -> C:\co\ContosoInventory\ContosoInventory.Client\bin\Debug\net10.0\wwwroot
  ContosoInventory.Server -> C:\co\ContosoInventory\ContosoInventory.Server\bin\Debug\net10.0\ContosoInventory.Server.dll

Build succeeded.
    0 Warning(s)
    0 Error(s)
```

No test project exists in the starter repo (`dotnet test` has no target).

### Run and verify seed data / roles

```powershell
dotnet run --no-build
```

```text
info: ContosoInventory.Server.Data.InventoryContext[0]
      Database migrated successfully.
info: ContosoInventory.Server.Data.InventoryContext[0]
      Roles created: Admin, Viewer.
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5240
```

```powershell
curl -s -c cookies.txt -X POST http://localhost:5240/api/auth/login -H "Content-Type: application/json" -d '{"email":"mateo@contoso.com","password":"Password123!"}'
```

```json
{"email":"mateo@contoso.com","displayName":"Mateo Gomez","role":"Admin"}
```

```powershell
curl -s -b cookies.txt http://localhost:5240/api/categories
```

Returned 9 categories, ids 1-9, every one with `"isActive":true` (includes "Laptops & Desktops", "Monitors & Displays", "Networking Equipment", ..., "Decommissioned", "UpTop").

```powershell
curl -s -c cookies_megan.txt -X POST http://localhost:5240/api/auth/login -H "Content-Type: application/json" -d '{"email":"megan@contoso.com","password":"Password123!"}'
curl -s -o /dev/null -w "%{http_code}\n" -b cookies_megan.txt -X POST http://localhost:5240/api/categories -H "Content-Type: application/json" -d '{"name":"Test","description":"Test","displayOrder":99}'
```

```text
{"email":"megan@contoso.com","displayName":"Megan Bowen","role":"Viewer"}
403
```

Server stopped: `taskkill //PID <pid> //F` against the PID bound to port 5240 (`netstat -ano | grep ":5240"`).

## Step 2: implement the Product Inventory feature

Files added/changed are listed in `readme.md`. No EF Core migration was generated; see the "Deviation" section there. The `Products` table was created by applying the hand-written delta script (`product-inventory/db/deltas/2026-09-21-add-products-table.sql`) directly to the SQLite file with a small throwaway console runner using `Microsoft.Data.Sqlite` (no `sqlite3` CLI was present on the machine):

```powershell
dotnet run -- "C:\co\ContosoInventory\ContosoInventory.Server\App_Data\ContosoInventory.db" "C:\co\ContosoInventory\db\deltas\2026-09-21-add-products-table.sql"
```

```text
SQL script applied successfully.
```

Re-run against the same database to confirm idempotence:

```text
SQL script applied successfully.
```

(`CREATE TABLE IF NOT EXISTS` / `CREATE INDEX IF NOT EXISTS`, so the second run is a no-op with no error and no schema change.)

### Build with the Product feature

```powershell
dotnet build ContosoInventory.sln
```

```text
  ContosoInventory.Shared -> C:\co\ContosoInventory\ContosoInventory.Shared\bin\Debug\net10.0\ContosoInventory.Shared.dll
  ContosoInventory.Client -> C:\co\ContosoInventory\ContosoInventory.Client\bin\Debug\net10.0\ContosoInventory.Client.dll
  ContosoInventory.Client (Blazor output) -> C:\co\ContosoInventory\ContosoInventory.Client\bin\Debug\net10.0\wwwroot
  ContosoInventory.Server -> C:\co\ContosoInventory\ContosoInventory.Server\bin\Debug\net10.0\ContosoInventory.Server.dll

Build succeeded.
    0 Warning(s)
    0 Error(s)
```

(One intermediate build failed with `CS1513: } expected` in `InventoryContext.cs` after a missing closing brace; fixed before the run above.)

### Run and exercise every Product endpoint as Admin (mateo@contoso.com)

```powershell
curl -s -w "\nHTTP %{http_code}\n" -b cookies.txt -X POST http://localhost:5240/api/products -H "Content-Type: application/json" -d '{"name":"ThinkPad X1","sku":"TP-X1-001","description":"Business laptop","price":1499.99,"stockQuantity":10,"categoryId":1}'
```

```text
{"id":1,"name":"ThinkPad X1","sku":"TP-X1-001","description":"Business laptop","price":1499.99,"stockQuantity":10,"categoryId":1,"categoryName":"Laptops & Desktops","createdDate":"2026-09-21T17:58:39.4713404","lastUpdatedDate":"2026-09-21T17:58:39.4713559"}
HTTP 201
```

| Check | Command | Result |
|---|---|---|
| Create product | `POST /api/products` | Pass, HTTP 201 |
| List all products | `GET /api/products` | Pass, HTTP 200, returns the created product |
| Filter by category | `GET /api/products?categoryId=1` | Pass, HTTP 200, returns the created product |
| Get by id | `GET /api/products/1` | Pass, HTTP 200 |
| Update product | `PUT /api/products/1` | Pass, HTTP 200, name/price/stock changed, `lastUpdatedDate` advanced |
| Restock | `POST /api/products/1/restock` `{"quantity":5}` | Pass, HTTP 200, stock 8 -> 13 |
| Reject unknown category | `POST /api/products` with `categoryId:999` | Pass, HTTP 400, `{"message":"Category with ID 999 doesn't exist."}` |
| Reject duplicate SKU | `POST /api/products` with existing SKU | Pass, HTTP 400, `{"message":"A product with the SKU 'TP-X1-001' already exists."}` |
| Delete product | `DELETE /api/products/1` | Pass, HTTP 204 |
| Viewer can read | `GET /api/products` as megan | Pass, HTTP 200 |
| Viewer cannot create | `POST /api/products` as megan | Pass, HTTP 403 |
| Viewer cannot restock | `POST /api/products/2/restock` as megan | Pass, HTTP 403 |

Server stopped after testing: `taskkill //PID <pid> //F` against the PID bound to port 5240.

## What could not be run mechanically (Copilot-UI-only)

These lab steps require interacting with GitHub Copilot Chat inside Visual Studio Code (sign-in, the agents dropdown, `/init`, `/agents`, the Chat Customization Diagnostics report, handoff buttons) and cannot be driven from this session:

- Importing the starter repo through the GitHub UI and cloning the imported copy (a plain clone of the public starter was used instead, which is source-identical for verification purposes).
- Running `/init` and comparing its generated file against the hand-authored `copilot-instructions.md`.
- Verifying "Code Generation: Use Instruction Files" and `chat.promptFiles` in VS Code Settings.
- Asking Copilot Chat the two verification prompts ("What naming convention...", "How should I structure data access...") and checking the **References** section.
- Opening Chat Diagnostics and confirming "3 files loaded".
- Verifying `generate-api-docs` appears in the `/` slash command list and running it against `CategoriesController.cs` through Copilot.
- Verifying **planner**, **implementer**, **reviewer** appear in the agents dropdown, selecting each one, and confirming the description text shown as the chat placeholder.
- Running the Planner agent's prompt through Copilot Chat and reviewing its generated plan.
- Clicking the **Start Implementation**, **Review Code**, and **Fix Issues** handoff buttons and watching the prefilled prompts.
- Testing the Product endpoints through the Swagger UI at `/swagger` (tested equivalently via `curl` above instead).

## Result

Starter app claims: 9 of 10 checked items pass as stated; 1 fix applied to `readme.md` (the `Migrations` folder path). Solution build: pass, 0 errors. Product Inventory feature: all 11 endpoint/authorization checks pass. SQL delta script: applied successfully, idempotent on re-run.
