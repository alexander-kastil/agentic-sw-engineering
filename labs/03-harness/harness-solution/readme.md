# Harness Solution

This folder is the reference solution for [the lab](../readme.md). The lab has the reader drive GitHub Copilot's chat UI, agents dropdown, and handoff buttons interactively, so the artifacts here are the parts that can be authored and verified mechanically: the customization files GitHub Copilot reads, and the Product Inventory feature those chained agents were supposed to produce.

## `.github/`

The four customization surfaces from the lab, authored with the exact content the guide specifies:

- `copilot-instructions.md`: repository-level coding standards (naming, architecture, error handling, documentation, testing).
- `instructions/controllers.instructions.md`, `instructions/services.instructions.md`: path-specific guidance scoped by `applyTo` glob.
- `prompts/generate-api-docs.prompt.md`: the reusable `/generate-api-docs` slash command.
- `agents/planner.agent.md`, `agents/implementer.agent.md`, `agents/reviewer.agent.md`: the three chained custom agents with their handoffs.

Drop this `.github` folder into the root of a ContosoInventory checkout to reproduce the lab's configuration.

## `product-inventory/`

The Product Inventory feature the Planner -> Implementer -> Reviewer chain builds in the lab's last task, implemented by hand against the real ContosoInventory starter app and verified end-to-end (see `test-results.md`). Files mirror their real paths under the ContosoInventory solution:

- `ContosoInventory.Server/Models/Product.cs`: the entity, with a `CategoryId` foreign key and a `Category` navigation property.
- `ContosoInventory.Shared/DTOs/ProductResponseDto.cs`, `CreateProductDto.cs`, `UpdateProductDto.cs`, `RestockProductDto.cs`: request/response payloads, following the same DTO-per-operation pattern as the Category feature.
- `ContosoInventory.Server/Services/IProductService.cs`, `ProductService.cs`: the service interface and EF Core implementation (SKU uniqueness check, category existence check, restock).
- `ContosoInventory.Server/Controllers/ProductsController.cs`: CRUD plus `POST /api/products/{id}/restock`, `[Authorize]` on the controller and `[Authorize(Roles = "Admin")]` on every write action.
- `ContosoInventory.Server/Data/InventoryContext.cs`: full updated file, adding `DbSet<Product>` and the `Product` entity configuration (unique index on `Sku`, cascade delete on `CategoryId`).
- `ContosoInventory.Server/Program.cs`: full updated file, registering `IProductService`.
- `db/deltas/2026-09-21-add-products-table.sql`: the hand-written SQL delta script that creates the `Products` table. This repository's rule prohibits EF Core migrations everywhere, including in lab solution content, so no migration was generated for this schema change; the script is idempotent (`CREATE TABLE IF NOT EXISTS`) and was applied directly to the SQLite database for verification. Per the `sql-delta-scripts` convention, this file lives at the ContosoInventory solution root under `db/`, not inside a `.csproj` directory.

## Endpoints added

| Method | Route | Auth |
|---|---|---|
| GET | `/api/products` (optional `?categoryId=`) | Any authenticated user |
| GET | `/api/products/{id}` | Any authenticated user |
| POST | `/api/products` | Admin |
| PUT | `/api/products/{id}` | Admin |
| DELETE | `/api/products/{id}` | Admin |
| POST | `/api/products/{id}/restock` | Admin |

## Deviation from the lab's plan prompt

The lab's Planner prompt says "add Product to the DbContext and create a migration." This solution adds `Product` to `InventoryContext` but does not create an EF Core migration, because this repository prohibits EF Core migrations everywhere (`dotnet ef migrations`, `dotnet ef database update`, a `Migrations` folder, `Database.Migrate()`/`EnsureCreated()` beyond what the starter already has). The schema change ships as the hand-written SQL delta script instead. The existing `ContosoInventory.Server/Migrations/` folder from the starter app is untouched.
