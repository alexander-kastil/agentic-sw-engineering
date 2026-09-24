# Harness Solution

[Python version](./readme-py.md)

This folder is the reference solution for [the lab](../readme.md). The lab has the reader drive GitHub Copilot's chat UI, agents dropdown, and handoff buttons interactively, so the artifacts here are the parts that can be authored and verified mechanically: the customization files GitHub Copilot reads, and the Product Inventory feature those chained agents were supposed to produce.

## `.github/`

The four customization surfaces from the lab, authored with the exact content the guide specifies:

- `copilot-instructions.md`: repository-level coding standards (naming, architecture, error handling, documentation, testing).
- `instructions/controllers.instructions.md`, `instructions/services.instructions.md`: path-specific guidance scoped by `applyTo` glob.
- `prompts/generate-api-docs.prompt.md`: the reusable `/generate-api-docs` slash command.
- `agents/planner.agent.md`, `agents/implementer.agent.md`, `agents/reviewer.agent.md`: the three chained custom agents with their handoffs.

Drop this `.github` folder into the root of a ContosoInventory checkout to reproduce the lab's configuration.

## `product-inventory/`

A complete, runnable ContosoInventory solution on .NET 10: the [starter app](https://github.com/MicrosoftLearning/github-copilot-customization-starter-app) (MIT) plus the Product Inventory feature the Planner -> Implementer -> Reviewer chain builds in the lab's last task. The projects were scaffolded with the dotnet CLI:

```powershell
dotnet new sln -n ContosoInventory
dotnet new webapi --use-controllers -n ContosoInventory.Server
dotnet new blazorwasm --empty -n ContosoInventory.Client
dotnet new classlib -n ContosoInventory.Shared
dotnet sln add ContosoInventory.Server/ContosoInventory.Server.csproj ContosoInventory.Client/ContosoInventory.Client.csproj ContosoInventory.Shared/ContosoInventory.Shared.csproj
dotnet add ContosoInventory.Server/ContosoInventory.Server.csproj reference ContosoInventory.Shared/ContosoInventory.Shared.csproj ContosoInventory.Client/ContosoInventory.Client.csproj
dotnet add ContosoInventory.Client/ContosoInventory.Client.csproj reference ContosoInventory.Shared/ContosoInventory.Shared.csproj
dotnet add ContosoInventory.Server package Microsoft.AspNetCore.Components.WebAssembly.Server
dotnet add ContosoInventory.Server package Microsoft.AspNetCore.Identity.EntityFrameworkCore
dotnet add ContosoInventory.Server package Microsoft.EntityFrameworkCore.Sqlite
dotnet add ContosoInventory.Server package Swashbuckle.AspNetCore
dotnet add ContosoInventory.Client package Microsoft.AspNetCore.Components.Authorization
dotnet add ContosoInventory.Client package Microsoft.Extensions.Http
dotnet add ContosoInventory.Shared package System.ComponentModel.Annotations
```

The Product feature:

- `ContosoInventory.Server/Models/Product.cs`: the entity, with a `CategoryId` foreign key and a `Category` navigation property.
- `ContosoInventory.Shared/DTOs/ProductResponseDto.cs`, `CreateProductDto.cs`, `UpdateProductDto.cs`, `RestockProductDto.cs`: request/response payloads, following the same DTO-per-operation pattern as the Category feature.
- `ContosoInventory.Server/Services/IProductService.cs`, `ProductService.cs`: the service interface and EF Core implementation (SKU uniqueness check, category existence check, restock).
- `ContosoInventory.Server/Controllers/ProductsController.cs`: CRUD plus `POST /api/products/{id}/restock`, `[Authorize]` on the controller and `[Authorize(Roles = "Admin")]` on every write action.
- `ContosoInventory.Server/Data/InventoryContext.cs`: adds `DbSet<Product>` and the `Product` entity configuration (unique index on `Sku`, cascade delete on `CategoryId`).
- `ContosoInventory.Server/Program.cs`: registers `IProductService`.

The schema ships as hand-written SQL delta scripts in `db/deltas/`, never as EF Core migrations:

- `2026-09-21-00-baseline.sql`: the starter schema (ASP.NET Core Identity tables and `Categories`).
- `2026-09-21-add-products-table.sql`: the `Products` table, unique index on `Sku`, cascade delete on `CategoryId`.

On startup, `Data/DbInitializer.cs` applies every script in file name order and then seeds the roles, the two users, and the categories. Every script is idempotent, so a restart is a no-op.

## Run and verify

Requires the .NET 10 SDK. Run the commands in PowerShell 7.

1. Build and start the server, and leave the terminal running:

    ```powershell
    cd labs/03-harness/harness-solution/product-inventory
    dotnet build ContosoInventory.slnx
    cd ContosoInventory.Server
    dotnet run
    ```

    Expected: `Applied 2 delta script(s)` on the first start, then `Now listening on: http://localhost:5240`. The Blazor app is at `http://localhost:5240`, the Swagger UI at `http://localhost:5240/swagger`.

1. In a second terminal, sign in as Mateo (Admin) and create a product:

    ```powershell
    $api = "http://localhost:5240/api"
    Invoke-RestMethod "$api/auth/login" -Method Post -ContentType "application/json" -Body '{"email":"mateo@contoso.com","password":"Password123!"}' -SessionVariable admin | Format-List
    $product = Invoke-RestMethod "$api/products" -Method Post -ContentType "application/json" -WebSession $admin -Body '{"name":"ThinkPad X1","sku":"TP-X1-001","description":"Business laptop","price":1499.99,"stockQuantity":10,"categoryId":1}'
    $product | Format-List
    ```

    Expected: the new product has `categoryName` `Laptops & Desktops`.

1. Exercise the rest of the Admin surface:

    ```powershell
    Invoke-RestMethod "$api/products?categoryId=1" -WebSession $admin | Format-List
    Invoke-RestMethod "$api/products/$($product.id)" -Method Put -ContentType "application/json" -WebSession $admin -Body '{"name":"ThinkPad X1 Carbon","sku":"TP-X1-001","description":"Business laptop","price":1599.99,"stockQuantity":8,"categoryId":1}' | Format-List
    Invoke-RestMethod "$api/products/$($product.id)/restock" -Method Post -ContentType "application/json" -WebSession $admin -Body '{"quantity":5}' | Format-List
    ```

    Expected: the filtered list holds the product, the update sets `stockQuantity` to `8`, and the restock raises it to `13`.

1. Sign in as Megan (Viewer) and confirm the Viewer role can read but not write:

    ```powershell
    Invoke-RestMethod "$api/auth/login" -Method Post -ContentType "application/json" -Body '{"email":"megan@contoso.com","password":"Password123!"}' -SessionVariable viewer | Format-List
    Invoke-RestMethod "$api/products" -WebSession $viewer -SkipHttpErrorCheck -StatusCodeVariable code | Out-Null; $code
    Invoke-RestMethod "$api/products/$($product.id)/restock" -Method Post -ContentType "application/json" -WebSession $viewer -Body '{"quantity":1}' -SkipHttpErrorCheck -StatusCodeVariable code | Out-Null; $code
    Invoke-RestMethod "$api/products" -SkipHttpErrorCheck -StatusCodeVariable code | Out-Null; $code
    ```

    Expected: `200` for the read, `403` for the restock, and `401` for the request without a session.

1. Delete the product as Mateo:

    ```powershell
    Invoke-RestMethod "$api/products/$($product.id)" -Method Delete -WebSession $admin -SkipHttpErrorCheck -StatusCodeVariable code; $code
    ```

    Expected: `204`. Stop the server with `Ctrl+C` in the first terminal.

Delete `ContosoInventory.Server/App_Data/` and restart to start from a clean database.

## Endpoints added

| Method | Route | Auth |
|---|---|---|
| GET | `/api/products` (optional `?categoryId=`) | Any authenticated user |
| GET | `/api/products/{id}` | Any authenticated user |
| POST | `/api/products` | Admin |
| PUT | `/api/products/{id}` | Admin |
| DELETE | `/api/products/{id}` | Admin |
| POST | `/api/products/{id}/restock` | Admin |

## Deviation from the lab

The lab's Planner prompt says "add Product to the DbContext and create a migration", and the starter applies its schema with `Database.MigrateAsync()` from a `Migrations/` folder. This solution prohibits EF Core migrations, so the `Migrations/` folder is not carried over, `DbInitializer` applies the SQL delta scripts instead of calling `MigrateAsync()`, and the Product table ships as a delta script.
