from datetime import date, timedelta

from app.database import connect
from app.models import OrderStatus
from app.security import hash_password

USERS = [
    (1, "Mateo Gomez", "mateo@contoso.com"),
    (2, "Megan Bowen", "megan@contoso.com"),
]

PRODUCTS = [
    (1, "ITM-001", "Laptop", 1299.99, 25),
    (2, "ITM-002", "Headphones", 99.99, 80),
    (3, "ITM-003", "Monitor", 349.99, 40),
    (4, "ITM-004", "Keyboard", 79.99, 120),
    (5, "ITM-005", "Mouse", 39.99, 150),
    (6, "ITM-006", "Desk Lamp", 45.00, 60),
    (7, "ITM-007", "Webcam", 89.99, 70),
    (8, "ITM-008", "USB-C Hub", 59.99, 90),
    (9, "ITM-009", "Office Chair", 249.99, 30),
    (10, "ITM-010", "Speakers", 129.99, 50),
]

ORDERS = [
    (1001, 1, 60, OrderStatus.DELIVERED, [(1, 1), (5, 1)]),
    (1002, 1, 52, OrderStatus.DELIVERED, [(2, 1), (4, 1)]),
    (1003, 1, 45, OrderStatus.RETURNED, [(7, 1)]),
    (1004, 1, 38, OrderStatus.DELIVERED, [(3, 3), (8, 1)]),
    (1005, 1, 30, OrderStatus.DELIVERED, [(6, 2), (5, 1)]),
    (1006, 1, 24, OrderStatus.PARTIAL_RETURN, [(4, 2), (2, 1)]),
    (1007, 1, 12, OrderStatus.SHIPPED, [(9, 1)]),
    (1008, 1, 18, OrderStatus.DELIVERED, [(10, 1)]),
    (1009, 1, 6, OrderStatus.SHIPPED, [(1, 1)]),
    (1010, 1, 1, OrderStatus.PROCESSING, [(3, 1), (4, 1)]),
    (1011, 2, 58, OrderStatus.DELIVERED, [(9, 1)]),
    (1012, 2, 50, OrderStatus.DELIVERED, [(3, 2)]),
    (1013, 2, 44, OrderStatus.RETURNED, [(5, 2)]),
    (1014, 2, 36, OrderStatus.DELIVERED, [(1, 1), (2, 1)]),
    (1015, 2, 28, OrderStatus.PARTIAL_RETURN, [(6, 3)]),
    (1016, 2, 20, OrderStatus.DELIVERED, [(10, 2)]),
    (1017, 2, 14, OrderStatus.SHIPPED, [(7, 1), (8, 1)]),
    (1018, 2, 9, OrderStatus.SHIPPED, [(4, 1)]),
    (1019, 2, 3, OrderStatus.PROCESSING, [(2, 2)]),
    (1020, 2, 1, OrderStatus.PROCESSING, [(9, 1), (6, 1)]),
]

RETURNED_QUANTITIES = {
    1003: {7: 1},
    1006: {2: 1},
    1013: {5: 2},
    1015: {6: 1},
}


def seed() -> None:
    with connect() as connection:
        if connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
            return

        for user_id, name, email in USERS:
            connection.execute(
                "INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?)",
                (user_id, name, email, hash_password("Password123!")),
            )

        connection.executemany(
            "INSERT INTO products (id, item_number, name, price, stock) VALUES (?, ?, ?, ?, ?)",
            PRODUCTS,
        )
        prices = {product[0]: (product[2], product[3]) for product in PRODUCTS}

        today = date.today()
        for order_id, user_id, days_ago, status, lines in ORDERS:
            order_date = today - timedelta(days=days_ago)
            ship_date = order_date + timedelta(days=1) if status != OrderStatus.PROCESSING else None
            delivered = status in {OrderStatus.DELIVERED, OrderStatus.PARTIAL_RETURN, OrderStatus.RETURNED}
            delivery_date = order_date + timedelta(days=4) if delivered else None
            total = sum(prices[product_id][1] * quantity for product_id, quantity in lines)
            connection.execute(
                "INSERT INTO orders (id, user_id, order_date, status, total_amount, ship_date, delivery_date) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    order_id,
                    user_id,
                    order_date.isoformat(),
                    status.value,
                    round(total, 2),
                    ship_date.isoformat() if ship_date else None,
                    delivery_date.isoformat() if delivery_date else None,
                ),
            )
            for product_id, quantity in lines:
                name, price = prices[product_id]
                returned = RETURNED_QUANTITIES.get(order_id, {}).get(product_id, 0)
                cursor = connection.execute(
                    "INSERT INTO order_items (order_id, product_id, product_name, quantity, price, returned_quantity) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (order_id, product_id, name, quantity, price, returned),
                )
                if returned:
                    connection.execute(
                        "INSERT INTO order_item_returns (order_item_id, quantity, reason, refund_amount, returned_at) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (cursor.lastrowid, returned, "Seeded return", round(price * returned, 2), delivery_date.isoformat()),
                    )
