-- Adds the Products table backing the Product Inventory feature.
-- Target: ContosoInventory.Server/App_Data/ContosoInventory.db (SQLite)
-- Hand-written per repository policy: no EF Core migration was generated for this change.
-- Idempotent: safe to run against a database that already has the table.

CREATE TABLE IF NOT EXISTS "Products" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Products" PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT NOT NULL,
    "Sku" TEXT NOT NULL,
    "Description" TEXT NOT NULL,
    "Price" TEXT NOT NULL,
    "StockQuantity" INTEGER NOT NULL,
    "CategoryId" INTEGER NOT NULL,
    "CreatedDate" TEXT NOT NULL,
    "LastUpdatedDate" TEXT NOT NULL,
    CONSTRAINT "FK_Products_Categories_CategoryId" FOREIGN KEY ("CategoryId") REFERENCES "Categories" ("Id") ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_Products_Sku" ON "Products" ("Sku");

CREATE INDEX IF NOT EXISTS "IX_Products_CategoryId" ON "Products" ("CategoryId");

-- Verification (run after applying): expect 0 rows on a freshly created table.
-- SELECT COUNT(*) AS RowsFound FROM "Products";
