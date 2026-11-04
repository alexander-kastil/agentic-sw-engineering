import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";

export const db = new DatabaseSync(fileURLToPath(new URL("../../hr-data.db", import.meta.url)));

export function ensureCreated(): void {
  db.exec(`
    PRAGMA journal_mode = 'wal';
    CREATE TABLE IF NOT EXISTS "Candidates" (
        "Id" INTEGER NOT NULL CONSTRAINT "PK_Candidates" PRIMARY KEY AUTOINCREMENT,
        "FirstName" TEXT NOT NULL,
        "LastName" TEXT NOT NULL,
        "Email" TEXT NOT NULL,
        "SpokenLanguagesData" TEXT NOT NULL,
        "SkillsData" TEXT NOT NULL,
        "CurrentRole" TEXT NOT NULL
    );
    CREATE UNIQUE INDEX IF NOT EXISTS "IX_Candidates_Email" ON "Candidates" ("Email");
  `);
}
