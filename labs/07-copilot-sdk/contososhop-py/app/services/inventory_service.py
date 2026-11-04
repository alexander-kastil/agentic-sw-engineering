import sqlite3


class InventoryService:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def list_products(self) -> list[dict]:
        rows = self.db.execute(
            "SELECT id, item_number, name, price, stock, returned FROM products ORDER BY item_number"
        ).fetchall()
        return [dict(row) for row in rows]

    def restore_stock(self, product_id: int, quantity: int) -> None:
        self.db.execute(
            "UPDATE products SET stock = stock + ?, returned = returned + ? WHERE id = ?",
            (quantity, quantity, product_id),
        )
