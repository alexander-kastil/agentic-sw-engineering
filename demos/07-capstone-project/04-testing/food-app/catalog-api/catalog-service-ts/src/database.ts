import { open, Database as SqliteDatabase } from 'sqlite';
import sqlite3 from 'sqlite3';
import path from 'path';
import { CatalogItem } from './types';

let db: SqliteDatabase<sqlite3.Database, sqlite3.Statement>;

export async function initDatabase(): Promise<SqliteDatabase<sqlite3.Database, sqlite3.Statement>> {
    const dbPath = process.env.DATABASE_URL || path.join(process.cwd(), 'food.db');

    db = await open({
        filename: dbPath,
        driver: sqlite3.Database
    });

    await db.exec('PRAGMA journal_mode = WAL');

    await createTables();
    await initializeData();

    return db;
}

async function createTables(): Promise<void> {
    await db.exec(`
    CREATE TABLE IF NOT EXISTS catalog_item (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      price REAL NOT NULL,
      in_stock INTEGER NOT NULL,
      picture_url TEXT,
      description TEXT
    )
  `);
}

async function initializeData(): Promise<void> {
    const result = await db.get('SELECT COUNT(*) as count FROM catalog_item');
    const count = result?.count || 0;

    if (count === 0) {
        const items: Omit<CatalogItem, 'id'>[] = [
            {
                name: "Hand pulled Noodles",
                inStock: 9,
                price: 17.0,
                pictureUrl: "hand-pulled-noodles.png",
                description: "Hand pulled noodles made with love by our experienced cooks from Sichuan. Served with your choice of meat, vegetables, and smashed cucumber salad."
            },
            {
                name: "Pad Kra Pao",
                inStock: 12,
                price: 16.0,
                pictureUrl: "pad-kra-pao.png",
                description: "Pad Kra Pao definitely one of the most popular spicy dishes in Thailand. Cooked with thai holy basil, long beans and chicken. Served with jasmine rice and fried egg."
            },
            {
                name: "Wiener Schnitzel",
                inStock: 13,
                price: 18.0,
                pictureUrl: "schnitzel.jpg",
                description: "Wiener Schnitzel is a traditional Austrian dish consisting of a thin slice of veal coated in breadcrumbs and fried. Served with potato salad and lemon."
            },
            {
                name: "Falafel Plate",
                inStock: 9,
                price: 12.0,
                pictureUrl: "falafel.jpg",
                description: "Falafel is a deep-fried ball, doughnut or patty made from ground chickpeas. Served with hummus, pita bread, and salad."
            },
            {
                name: "Pizza Tartufo",
                inStock: 4,
                price: 24.0,
                pictureUrl: "pizza.jpg",
                description: "Pizza truffle is well tasting, exclusive joy for your taste bud. A delight of white pizza where the protagonist is our cheese with truffle flakes."
            }
        ];

        for (const item of items) {
            await db.run(
                `INSERT INTO catalog_item (name, price, in_stock, picture_url, description)
         VALUES (?, ?, ?, ?, ?)`,
                [item.name, item.price, item.inStock, item.pictureUrl, item.description]
            );
        }
    }
}

export function getDatabase(): SqliteDatabase<sqlite3.Database, sqlite3.Statement> {
    if (!db) {
        throw new Error('Database not initialized');
    }
    return db;
}

export async function closeDatabase(): Promise<void> {
    if (db) {
        await db.close();
    }
}

export async function getAllFoodItems(): Promise<CatalogItem[]> {
    const rows = await db.all('SELECT * FROM catalog_item');
    return rows.map(row => dbRowToCatalogItem(row));
}

export async function getFoodItemById(id: number): Promise<CatalogItem | null> {
    const row = await db.get('SELECT * FROM catalog_item WHERE id = ?', [id]);
    return row ? dbRowToCatalogItem(row) : null;
}

export async function createFoodItem(item: Omit<CatalogItem, 'id'>): Promise<CatalogItem> {
    const result = await db.run(
        `INSERT INTO catalog_item (name, price, in_stock, picture_url, description)
     VALUES (?, ?, ?, ?, ?)`,
        [item.name, item.price, item.inStock, item.pictureUrl || null, item.description || null]
    );

    return {
        id: result.lastID as number,
        ...item
    };
}

export async function updateFoodItem(id: number, item: Partial<Omit<CatalogItem, 'id'>>): Promise<CatalogItem | null> {
    const existing = await getFoodItemById(id);
    if (!existing) {
        return null;
    }

    const fields: string[] = [];
    const values: any[] = [];

    if (item.name !== undefined) {
        fields.push('name = ?');
        values.push(item.name);
    }
    if (item.price !== undefined) {
        fields.push('price = ?');
        values.push(item.price);
    }
    if (item.inStock !== undefined) {
        fields.push('in_stock = ?');
        values.push(item.inStock);
    }
    if (item.pictureUrl !== undefined) {
        fields.push('picture_url = ?');
        values.push(item.pictureUrl);
    }
    if (item.description !== undefined) {
        fields.push('description = ?');
        values.push(item.description);
    }

    if (fields.length === 0) {
        return existing;
    }

    values.push(id);
    await db.run(`UPDATE catalog_item SET ${fields.join(', ')} WHERE id = ?`, values);

    return getFoodItemById(id);
}

export async function deleteFoodItem(id: number): Promise<void> {
    await db.run('DELETE FROM catalog_item WHERE id = ?', [id]);
}

function dbRowToCatalogItem(row: any): CatalogItem {
    return {
        id: row.id,
        name: row.name,
        price: row.price,
        inStock: row.in_stock,
        pictureUrl: row.picture_url,
        description: row.description
    };
}
