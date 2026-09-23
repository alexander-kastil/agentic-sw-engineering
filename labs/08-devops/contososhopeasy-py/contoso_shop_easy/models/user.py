from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class UserRole(Enum):
    CUSTOMER = 1
    ADMIN = 2
    EMPLOYEE = 3


@dataclass
class Address:
    street: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = ""
    is_default: bool = False

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}, {self.country}"


@dataclass
class User:
    id: int = 0
    username: str = ""
    email: str = ""
    password_hash: str = ""
    first_name: str = ""
    last_name: str = ""
    phone_number: str = ""
    date_of_birth: datetime | None = None
    role: UserRole = UserRole.CUSTOMER
    is_active: bool = True
    is_email_verified: bool = False
    created_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_login_date: datetime | None = None
    shipping_address: Address | None = None
    billing_address: Address | None = None
