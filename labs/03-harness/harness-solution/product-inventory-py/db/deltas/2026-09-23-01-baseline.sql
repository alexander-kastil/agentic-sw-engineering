CREATE TABLE IF NOT EXISTS "Categories" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Categories" PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT NOT NULL,
    "Description" TEXT NOT NULL,
    "DisplayOrder" INTEGER NOT NULL,
    "IsActive" INTEGER NOT NULL DEFAULT 1,
    "CreatedDate" TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_Categories_Name" ON "Categories" ("Name");

CREATE TABLE IF NOT EXISTS "Users" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Users" PRIMARY KEY AUTOINCREMENT,
    "Email" TEXT NOT NULL,
    "DisplayName" TEXT NOT NULL,
    "PasswordHash" TEXT NOT NULL,
    "Role" TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "IX_Users_Email" ON "Users" ("Email");

INSERT OR IGNORE INTO "Categories" ("Name", "Description", "DisplayOrder", "IsActive", "CreatedDate") VALUES
    ('Laptops & Desktops', 'Portable and desktop computers issued to employees', 1, 1, '2026-01-01T00:00:00'),
    ('Monitors & Displays', 'External monitors, projectors, and conference room displays', 2, 1, '2026-01-01T00:00:00'),
    ('Networking Equipment', 'Routers, switches, access points, and cabling', 3, 1, '2026-01-01T00:00:00'),
    ('Printers & Scanners', 'Office printers, scanners, and multifunction devices', 4, 1, '2026-01-01T00:00:00'),
    ('Mobile Devices', 'Company phones and tablets', 5, 1, '2026-01-01T00:00:00'),
    ('Servers & Storage', 'Rack servers, NAS devices, and backup drives', 6, 1, '2026-01-01T00:00:00'),
    ('Peripherals', 'Keyboards, mice, headsets, and docking stations', 7, 1, '2026-01-01T00:00:00'),
    ('Audio & Video', 'Webcams, speakers, and meeting room equipment', 8, 1, '2026-01-01T00:00:00'),
    ('Decommissioned', 'Retired equipment awaiting disposal', 9, 1, '2026-01-01T00:00:00');

INSERT OR IGNORE INTO "Users" ("Email", "DisplayName", "PasswordHash", "Role") VALUES
    ('mateo@contoso.com', 'Mateo Gomez', 'pbkdf2_sha256$600000$6d6174656f2d73616c74$0dcff84200bfb9949d4f2996b9531d5c58360e7ca0355a674913363bf76b590a', 'Admin'),
    ('megan@contoso.com', 'Megan Bowen', 'pbkdf2_sha256$600000$6d6567616e2d73616c74$cbc6d9e47384801137c5f28826cc35fb5ac4834c0f2c0c2b833a96657eceb07b', 'Viewer');
