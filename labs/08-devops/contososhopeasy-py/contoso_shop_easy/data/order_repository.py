from collections import Counter
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from ..models.order import Order, OrderItem, OrderStatus
from ..models.user import Address


class OrderRepository:
    def __init__(self) -> None:
        now = datetime.now(timezone.utc)
        # Pre-populate with some sample orders for demo purposes
        self._orders = [
            Order(1, 1, "ORD-20241029-0001-001", order_date=now - timedelta(days=5), status=OrderStatus.DELIVERED,
                  sub_total=Decimal("429.99"), tax_amount=Decimal("34.40"), shipping_cost=Decimal("0"),
                  total_amount=Decimal("464.39"), shipped_date=now - timedelta(days=3),
                  delivered_date=now - timedelta(days=1), tracking_number="TRK202410290001001",
                  shipping_address=Address("123 Main St", "Anytown", "CA", "12345", "USA"),
                  billing_address=Address("123 Main St", "Anytown", "CA", "12345", "USA"),
                  order_items=[OrderItem(1, 1, 29, 1, Decimal("429.99"), Decimal("429.99"))]),
            Order(2, 2, "ORD-20241028-0002-001", order_date=now - timedelta(days=3), status=OrderStatus.SHIPPED,
                  sub_total=Decimal("1899.99"), tax_amount=Decimal("152.00"), shipping_cost=Decimal("0"),
                  total_amount=Decimal("2051.99"), shipped_date=now - timedelta(days=1),
                  tracking_number="TRK202410280002001",
                  shipping_address=Address("456 Oak Ave", "Springfield", "TX", "67890", "USA"),
                  billing_address=Address("456 Oak Ave", "Springfield", "TX", "67890", "USA"),
                  order_items=[OrderItem(2, 2, 2, 1, Decimal("1899.99"), Decimal("1899.99"))]),
            Order(3, 1, "ORD-20241027-0001-002", order_date=now - timedelta(days=2), status=OrderStatus.PROCESSING,
                  sub_total=Decimal("579.97"), tax_amount=Decimal("46.40"), shipping_cost=Decimal("0"),
                  total_amount=Decimal("626.37"),
                  shipping_address=Address("123 Main St", "Anytown", "CA", "12345", "USA"),
                  billing_address=Address("123 Main St", "Anytown", "CA", "12345", "USA"),
                  order_items=[OrderItem(3, 3, 9, 1, Decimal("399.99"), Decimal("399.99")),
                               OrderItem(4, 3, 26, 4, Decimal("39.99"), Decimal("159.96"))]),
            Order(4, 4, "ORD-20241026-0004-001", order_date=now - timedelta(days=1), status=OrderStatus.PENDING,
                  sub_total=Decimal("89.97"), tax_amount=Decimal("7.20"), shipping_cost=Decimal("9.99"),
                  total_amount=Decimal("107.16"),
                  shipping_address=Address("321 Pine St", "Riverside", "FL", "33101", "USA"),
                  billing_address=Address("321 Pine St", "Riverside", "FL", "33101", "USA"),
                  order_items=[OrderItem(5, 4, 17, 1, Decimal("79.99"), Decimal("79.99")),
                               OrderItem(6, 4, 35, 1, Decimal("19.99"), Decimal("19.99"))]),
        ]
        self._next_order_id = len(self._orders) + 1

    def get_all_orders(self) -> list[Order]:
        return list(self._orders)

    def get_order_by_id(self, order_id: int) -> Order | None:
        return next((o for o in self._orders if o.id == order_id), None)

    def get_order_by_number(self, order_number: str) -> Order | None:
        if not order_number:
            return None
        return next((o for o in self._orders if o.order_number.lower() == order_number.lower()), None)

    def get_orders_by_user_id(self, user_id: int) -> list[Order]:
        return sorted((o for o in self._orders if o.user_id == user_id), key=lambda o: o.order_date, reverse=True)

    def get_orders_by_status(self, status: OrderStatus) -> list[Order]:
        return sorted((o for o in self._orders if o.status == status), key=lambda o: o.order_date, reverse=True)

    def add_order(self, order: Order) -> None:
        order.id = self._next_order_id
        self._next_order_id += 1
        order.order_date = datetime.now(timezone.utc)
        self._orders.append(order)

    def update_order(self, order: Order) -> bool:
        existing = self.get_order_by_id(order.id)
        if existing is None:
            return False
        self._orders[self._orders.index(existing)] = order
        return True

    def delete_order(self, order_id: int) -> bool:
        order = self.get_order_by_id(order_id)
        if order is None or order.status != OrderStatus.PENDING:
            return False
        self._orders.remove(order)
        return True

    def get_recent_orders(self, count: int = 10) -> list[Order]:
        return sorted(self._orders, key=lambda o: o.order_date, reverse=True)[:count]

    def get_total_revenue(self) -> Decimal:
        return sum((o.total_amount for o in self._orders if o.status != OrderStatus.CANCELLED), Decimal("0"))

    def get_order_status_counts(self) -> dict[OrderStatus, int]:
        return dict(Counter(o.status for o in self._orders))

    def get_next_order_id(self) -> int:
        return self._next_order_id

    # Security vulnerability: Method to get all order details including payment info
    def get_all_order_details_with_payments(self) -> list[dict]:
        return [
            {
                "order_id": o.id,
                "order_number": o.order_number,
                "user_id": o.user_id,
                "total_amount": o.total_amount,
                "status": o.status,
                "payment_info": o.payment_info,
                "shipping_address": str(o.shipping_address) if o.shipping_address else None,
                "billing_address": str(o.billing_address) if o.billing_address else None,
            }
            for o in self._orders
        ]
