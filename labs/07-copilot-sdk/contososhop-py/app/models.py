from enum import StrEnum

from pydantic import BaseModel, Field


class OrderStatus(StrEnum):
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    PARTIAL_RETURN = "PartialReturn"
    RETURNED = "Returned"


RETURNABLE_STATUSES = {OrderStatus.DELIVERED, OrderStatus.PARTIAL_RETURN, OrderStatus.RETURNED}


class LoginRequest(BaseModel):
    email: str
    password: str


class ReturnItem(BaseModel):
    order_item_id: int
    quantity: int = Field(gt=0)
    reason: str = "Customer requested return"


class ReturnItemRequest(BaseModel):
    items: list[ReturnItem]
