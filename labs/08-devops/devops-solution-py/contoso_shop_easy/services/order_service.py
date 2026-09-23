from datetime import datetime, timezone
from decimal import Decimal

from ..data.order_repository import OrderRepository
from ..models.order import Order, OrderItem, OrderStatus
from .product_service import ProductService
from .user_service import UserService


class OrderService:
    def __init__(self, order_repository: OrderRepository, product_service: ProductService, user_service: UserService) -> None:
        self._order_repository = order_repository
        self._product_service = product_service
        self._user_service = user_service

    def create_order(self, user_id: int, items: list[OrderItem]) -> Order:
        user = self._user_service.get_user(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} not found")

        # Generate order number - Security vulnerability: predictable order numbers
        order_number = self._generate_order_number(user_id)

        order = Order(
            id=self._order_repository.get_next_order_id(),
            user_id=user_id,
            order_number=order_number,
            status=OrderStatus.PENDING,
        )

        subtotal = Decimal("0")
        for item in items:
            product = self._product_service.get_product_by_id(item.product_id)
            if product is None:
                print(f"[WARNING] Product {item.product_id} not found, skipping item")
                continue

            if not self._product_service.is_product_in_stock(item.product_id, item.quantity):
                print(f"[WARNING] Insufficient stock for product {product.name}")
                continue

            order_item = OrderItem(
                id=len(order.order_items) + 1,
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price,
                total_price=product.price * item.quantity,
                product=product,
            )

            order.order_items.append(order_item)
            subtotal += order_item.total_price

            # Update stock
            self._product_service.update_stock(item.product_id, -item.quantity)

        # Calculate totals
        order.sub_total = subtotal
        order.tax_amount = subtotal * Decimal("0.08")  # 8% tax
        order.shipping_cost = self._calculate_shipping_cost(subtotal)
        order.total_amount = order.sub_total + order.tax_amount + order.shipping_cost

        self._order_repository.add_order(order)

        print(f"[INFO] Order created: {order_number} for user {user.username}")
        print(f"[DEBUG] Order total: ${order.total_amount}")

        return order

    def get_order(self, order_id: int) -> Order | None:
        return self._order_repository.get_order_by_id(order_id)

    def get_order_by_number(self, order_number: str) -> Order | None:
        return self._order_repository.get_order_by_number(order_number)

    def get_user_orders(self, user_id: int) -> list[Order]:
        return self._order_repository.get_orders_by_user_id(user_id)

    def update_order_status(self, order_id: int, status: OrderStatus) -> bool:
        order = self._order_repository.get_order_by_id(order_id)
        if order is None:
            return False

        order.status = status
        if status == OrderStatus.SHIPPED:
            order.shipped_date = datetime.now(timezone.utc)
            order.tracking_number = self._generate_tracking_number(order.order_number)
        elif status == OrderStatus.DELIVERED:
            order.delivered_date = datetime.now(timezone.utc)

        print(f"[INFO] Order {order.order_number} status updated to {status.name.title()}")
        return True

    def cancel_order(self, order_id: int) -> bool:
        order = self._order_repository.get_order_by_id(order_id)
        if order is None or order.status != OrderStatus.PENDING:
            return False

        # Restore stock
        for item in order.order_items:
            self._product_service.update_stock(item.product_id, item.quantity)

        order.status = OrderStatus.CANCELLED
        print(f"[INFO] Order {order.order_number} has been cancelled")
        return True

    # Security vulnerability: Predictable order number generation
    def _generate_order_number(self, user_id: int) -> str:
        timestamp = datetime.now().strftime("%Y%m%d")
        order_count = len(self._order_repository.get_orders_by_user_id(user_id)) + 1
        return f"ORD-{timestamp}-{user_id:04d}-{order_count:03d}"

    def _calculate_shipping_cost(self, subtotal: Decimal) -> Decimal:
        if subtotal >= 100:
            return Decimal("0")  # Free shipping over $100
        if subtotal >= 50:
            return Decimal("5.99")
        return Decimal("9.99")

    # Security vulnerability: Predictable tracking number generation
    def _generate_tracking_number(self, order_number: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"TRK{timestamp}{order_number.replace('-', '')[3:9]}"

    def get_all_orders(self) -> list[Order]:
        return self._order_repository.get_all_orders()

    def get_total_revenue(self) -> Decimal:
        return self._order_repository.get_total_revenue()
