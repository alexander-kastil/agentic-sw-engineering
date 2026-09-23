from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Category:
    id: int = 0
    name: str = ""
    description: str = ""
    parent_category_id: int | None = None
    is_active: bool = True
    created_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
