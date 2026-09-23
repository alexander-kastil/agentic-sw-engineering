from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user_id, get_order_service
from app.models import ReturnItemRequest
from app.services.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("")
def get_orders(user_id: int = Depends(get_current_user_id), orders: OrderService = Depends(get_order_service)):
    return orders.get_orders(user_id)


@router.get("/{order_id}")
def get_order(order_id: int, user_id: int = Depends(get_current_user_id), orders: OrderService = Depends(get_order_service)):
    order = orders.get_order(order_id, user_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/{order_id}/return")
async def return_order_items(
    order_id: int,
    body: ReturnItemRequest,
    user_id: int = Depends(get_current_user_id),
    orders: OrderService = Depends(get_order_service),
):
    if orders.get_order(order_id, user_id) is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if not await orders.process_item_return(order_id, body.items):
        raise HTTPException(status_code=400, detail="The return could not be processed")
    return orders.get_order(order_id, user_id)
