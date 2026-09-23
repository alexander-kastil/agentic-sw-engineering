from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from .product import Product
from .user import Address


class OrderStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    SHIPPED = 3
    DELIVERED = 4
    CANCELLED = 5
    RETURNED = 6


class PaymentMethod(Enum):
    CREDIT_CARD = 1
    DEBIT_CARD = 2
    PAYPAL = 3
    BANK_TRANSFER = 4


class PaymentStatus(Enum):
    PENDING = 1
    APPROVED = 2
    DECLINED = 3
    REFUNDED = 4


@dataclass
class OrderItem:
    id: int = 0
    order_id: int = 0
    product_id: int = 0
    quantity: int = 0
    unit_price: Decimal = Decimal("0")
    total_price: Decimal = Decimal("0")
    product: Product | None = None


@dataclass
class PaymentInfo:
    id: int = 0
    order_id: int = 0
    method: PaymentMethod = PaymentMethod.CREDIT_CARD
    card_number: str = ""  # This will be a security vulnerability - storing full card numbers
    card_holder_name: str = ""
    expiry_date: str = ""
    cvv: str = ""  # Another security vulnerability - storing CVV
    amount: Decimal = Decimal("0")
    processed_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: str | None = None


@dataclass
class Order:
    id: int = 0
    user_id: int = 0
    order_number: str = ""
    order_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: OrderStatus = OrderStatus.PENDING
    sub_total: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    shipping_cost: Decimal = Decimal("0")
    total_amount: Decimal = Decimal("0")
    order_items: list[OrderItem] = field(default_factory=list)
    shipping_address: Address | None = None
    billing_address: Address | None = None
    payment_info: PaymentInfo | None = None
    notes: str | None = None
    shipped_date: datetime | None = None
    delivered_date: datetime | None = None
    tracking_number: str | None = None
