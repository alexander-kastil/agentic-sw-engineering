import logging
import sqlite3
from collections.abc import Iterator

from fastapi import Depends, HTTPException, Request, status

from app.database import connect
from app.services.email_service import EmailServiceDev
from app.services.inventory_service import InventoryService
from app.services.order_service import OrderService
from app.services.support_agent_tools import SupportAgentTools


def get_db() -> Iterator[sqlite3.Connection]:
    connection = connect()
    try:
        yield connection
    finally:
        connection.close()


def get_email_service() -> EmailServiceDev:
    return EmailServiceDev()


def get_inventory_service(db: sqlite3.Connection = Depends(get_db)) -> InventoryService:
    return InventoryService(db)


def get_order_service(
    db: sqlite3.Connection = Depends(get_db),
    inventory_service: InventoryService = Depends(get_inventory_service),
    email_service: EmailServiceDev = Depends(get_email_service),
) -> OrderService:
    return OrderService(db, inventory_service, email_service)


def get_current_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user_id


def get_support_agent_tools(
    db: sqlite3.Connection = Depends(get_db),
    order_service: OrderService = Depends(get_order_service),
    email_service: EmailServiceDev = Depends(get_email_service),
) -> SupportAgentTools:
    return SupportAgentTools(db, order_service, email_service, logging.getLogger("contososhop.agent_tools"))
