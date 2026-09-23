from fastapi import APIRouter, Depends

from app.dependencies import get_current_user_id, get_inventory_service
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.get("")
def get_inventory(
    _: int = Depends(get_current_user_id),
    inventory: InventoryService = Depends(get_inventory_service),
):
    return inventory.list_products()
