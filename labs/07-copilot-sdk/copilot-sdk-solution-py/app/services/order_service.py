import logging
import sqlite3
from datetime import datetime, timezone

from app.models import RETURNABLE_STATUSES, OrderStatus, ReturnItem
from app.services.email_service import EmailServiceDev
from app.services.inventory_service import InventoryService

logger = logging.getLogger("contososhop.orders")


class OrderService:
    def __init__(self, db: sqlite3.Connection, inventory_service: InventoryService, email_service: EmailServiceDev):
        self.db = db
        self.inventory_service = inventory_service
        self.email_service = email_service

    def get_orders(self, user_id: int) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC", (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]

    def get_order(self, order_id: int, user_id: int) -> dict | None:
        row = self.db.execute(
            "SELECT * FROM orders WHERE id = ? AND user_id = ?", (order_id, user_id)
        ).fetchone()
        if row is None:
            return None
        order = dict(row)
        order["items"] = self.get_items(order_id)
        return order

    def get_items(self, order_id: int) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY id", (order_id,)
        ).fetchall()
        items = [dict(row) for row in rows]
        for item in items:
            item["remaining_quantity"] = item["quantity"] - item["returned_quantity"]
        return items

    async def process_item_return(self, order_id: int, return_items: list[ReturnItem]) -> bool:
        order = self.db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if order is None or OrderStatus(order["status"]) not in RETURNABLE_STATUSES:
            return False

        items = {item["id"]: item for item in self.get_items(order_id)}
        for return_item in return_items:
            item = items.get(return_item.order_item_id)
            if item is None or return_item.quantity > item["remaining_quantity"]:
                return False

        now = datetime.now(timezone.utc).isoformat()
        refund_total = 0.0
        for return_item in return_items:
            item = items[return_item.order_item_id]
            refund = round(item["price"] * return_item.quantity, 2)
            refund_total += refund
            self.db.execute(
                "INSERT INTO order_item_returns (order_item_id, quantity, reason, refund_amount, returned_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (item["id"], return_item.quantity, return_item.reason, refund, now),
            )
            self.db.execute(
                "UPDATE order_items SET returned_quantity = returned_quantity + ? WHERE id = ?",
                (return_item.quantity, item["id"]),
            )
            self.inventory_service.restore_stock(item["product_id"], return_item.quantity)

        remaining = self.db.execute(
            "SELECT SUM(quantity - returned_quantity) FROM order_items WHERE order_id = ?", (order_id,)
        ).fetchone()[0]
        status = OrderStatus.RETURNED if remaining == 0 else OrderStatus.PARTIAL_RETURN
        self.db.execute("UPDATE orders SET status = ? WHERE id = ?", (status.value, order_id))
        self.db.commit()

        user = self.db.execute("SELECT email FROM users WHERE id = ?", (order["user_id"],)).fetchone()
        await self.email_service.send_email(
            user["email"],
            f"Return confirmation for order #{order_id}",
            f"Your return has been processed. Refund amount: ${refund_total:.2f}.",
        )
        logger.info("Processed return for order %s, refund %.2f", order_id, refund_total)
        return True
