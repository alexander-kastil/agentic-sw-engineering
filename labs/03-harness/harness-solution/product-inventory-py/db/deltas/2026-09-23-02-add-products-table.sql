CREATE TABLE IF NOT EXISTS "Products" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Products" PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT NOT NULL,
    "Sku" TEXT NOT NULL COLLATE NOCASE,
    "Description" TEXT NOT NULL,
    "Price" REAL NOT NULL,
    "StockQuantity" INTEGER NOT NULL,
    "CategoryId" INTEGER NOT NULL,
    "CreatedDate" TEXT NOT NULL,
    "LastUpdatedDate" TEXT NOT NULL,
    CONSTRAINT "FK_Products_Categories_CategoryId" FOREIGN KEY ("CategoryId") REFERENCES "Categories" ("Id") ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_Products_Sku" ON "Products" ("Sku");

CREATE INDEX IF NOT EXISTS "IX_Products_CategoryId" ON "Products" ("CategoryId");
