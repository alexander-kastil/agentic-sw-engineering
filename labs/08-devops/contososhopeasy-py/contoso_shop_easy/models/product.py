from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal


@dataclass
class Product:
    id: int = 0
    name: str = ""
    description: str = ""
    price: Decimal = Decimal("0")
    category_id: int = 0
    brand: str = ""
    sku: str = ""
    stock_quantity: int = 0
    image_url: str = ""
    rating: float = 0.0
    review_count: int = 0
    is_active: bool = True
    created_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
