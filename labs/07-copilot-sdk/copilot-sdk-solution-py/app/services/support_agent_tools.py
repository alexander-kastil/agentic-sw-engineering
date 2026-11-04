import logging
import sqlite3
from datetime import date

from app.models import RETURNABLE_STATUSES, OrderStatus, ReturnItem
from app.services.email_service import EmailServiceDev
from app.services.order_service import OrderService


def _long_date(value: str) -> str:
    return date.fromisoformat(value[:10]).strftime("%B %d, %Y")


def _short_date(value: str) -> str:
    return date.fromisoformat(value[:10]).strftime("%b %d, %Y")


class SupportAgentTools:
    def __init__(
        self,
        db: sqlite3.Connection,
        order_service: OrderService,
        email_service: EmailServiceDev,
        logger: logging.Logger,
    ):
        self.db = db
        self.order_service = order_service
        self.email_service = email_service
        self.logger = logger

    async def get_order_details(self, order_id: int, user_id: int) -> str:
        self.logger.info("Agent tool invoked: get_order_details for order_id %s, user_id %s", order_id, user_id)

        order = self.order_service.get_order(order_id, user_id)
        if order is None:
            return f"I could not find order #{order_id} associated with your account. Please double-check the order number."

        status = OrderStatus(order["status"])
        if status == OrderStatus.PROCESSING:
            status_message = "is currently being processed and has not shipped yet"
        elif status == OrderStatus.SHIPPED:
            status_message = (
                f"was shipped on {_long_date(order['ship_date'])} and is on its way"
                if order["ship_date"]
                else "has been shipped and is on its way"
            )
        elif status == OrderStatus.DELIVERED:
            status_message = (
                f"was delivered on {_long_date(order['delivery_date'])}"
                if order["delivery_date"]
                else "has been delivered"
            )
        elif status == OrderStatus.PARTIAL_RETURN:
            status_message = "has been partially returned (some items have been returned, others are still with you)"
        elif status == OrderStatus.RETURNED:
            status_message = "has been fully returned and a refund was issued"
        else:
            status_message = "has an unknown status"

        item_infos = []
        for item in order["items"]:
            item_info = f"{item['product_name']} (Id: {item['id']}, qty: {item['quantity']}, ${item['price']:.2f} each"
            if item["returned_quantity"] > 0:
                item_info += f", {item['returned_quantity']} returned, {item['remaining_quantity']} remaining"
            item_infos.append(item_info + ")")

        return (
            f"Order #{order['id']} {status_message}. "
            f"Order date: {_long_date(order['order_date'])}. "
            f"Total: ${order['total_amount']:.2f}. "
            f"Items: {', '.join(item_infos)}."
        )

    async def get_user_orders_summary(self, user_id: int) -> str:
        self.logger.info("Agent tool invoked: get_user_orders_summary for user_id %s", user_id)

        orders = self.order_service.get_orders(user_id)
        if not orders:
            return "You don't have any orders on file."

        labels = {
            OrderStatus.PROCESSING: "Processing",
            OrderStatus.SHIPPED: "Shipped",
            OrderStatus.DELIVERED: "Delivered",
            OrderStatus.PARTIAL_RETURN: "Partial Return",
            OrderStatus.RETURNED: "Returned",
        }
        summaries = [
            f"Order #{order['id']} - {labels.get(OrderStatus(order['status']), 'Unknown')} - "
            f"${order['total_amount']:.2f} - Placed {_short_date(order['order_date'])}"
            for order in orders
        ]
        return f"You have {len(orders)} orders:\n" + "\n".join(summaries)

    async def process_return(
        self,
        order_id: int,
        user_id: int,
        order_item_ids: str = "",
        quantities: str = "",
        reason: str = "Customer requested return via AI support agent",
    ) -> str:
        self.logger.info(
            "Agent tool invoked: process_return for order_id %s, user_id %s, items: %s",
            order_id,
            user_id,
            order_item_ids or "all",
        )

        order = self.order_service.get_order(order_id, user_id)
        if order is None:
            return f"I could not find order #{order_id} associated with your account."

        status = OrderStatus(order["status"])
        if status not in RETURNABLE_STATUSES:
            if status == OrderStatus.PROCESSING:
                return f"Order #{order_id} is still being processed and cannot be returned yet. It must be delivered first."
            if status == OrderStatus.SHIPPED:
                return f"Order #{order_id} is currently in transit and cannot be returned until it has been delivered."
            return f"Order #{order_id} has a status of {status.value} and cannot be returned."

        items_by_id = {item["id"]: item for item in order["items"]}

        if order_item_ids.strip():
            item_ids = []
            for id_text in filter(None, (part.strip() for part in order_item_ids.split(","))):
                if not id_text.isdigit():
                    return f"Invalid item ID format: '{id_text}'. Please provide valid item IDs."
                item_ids.append(int(id_text))

            item_quantities = []
            if quantities.strip():
                for quantity_text in filter(None, (part.strip() for part in quantities.split(","))):
                    if not quantity_text.isdigit() or int(quantity_text) <= 0:
                        return f"Invalid quantity format: '{quantity_text}'. Quantities must be positive numbers."
                    item_quantities.append(int(quantity_text))

                if len(item_quantities) != len(item_ids):
                    return "The number of quantities must match the number of items."

            return_items = []
            for index, item_id in enumerate(item_ids):
                order_item = items_by_id.get(item_id)
                if order_item is None:
                    return f"Item ID {item_id} was not found in order #{order_id}."

                if order_item["remaining_quantity"] <= 0:
                    return f"{order_item['product_name']} has already been fully returned."

                quantity_to_return = item_quantities[index] if item_quantities else order_item["remaining_quantity"]
                if quantity_to_return > order_item["remaining_quantity"]:
                    return (
                        f"Cannot return {quantity_to_return} of {order_item['product_name']}. "
                        f"Only {order_item['remaining_quantity']} available to return."
                    )

                return_items.append(ReturnItem(order_item_id=item_id, quantity=quantity_to_return, reason=reason))
        else:
            return_items = [
                ReturnItem(order_item_id=item["id"], quantity=item["remaining_quantity"], reason=reason)
                for item in order["items"]
                if item["remaining_quantity"] > 0
            ]

        if not return_items:
            return f"All items in order #{order_id} have already been returned."

        if not await self.order_service.process_item_return(order_id, return_items):
            self.logger.error("Failed to process return for order_id %s, user_id %s", order_id, user_id)
            return f"I was unable to process the return for order #{order_id}. Please contact our support team for assistance."

        self.logger.info(
            "Successfully processed return for order_id %s, user_id %s, items: %s",
            order_id,
            user_id,
            len(return_items),
        )

        refund_amount = sum(items_by_id[ri.order_item_id]["price"] * ri.quantity for ri in return_items)
        items_summary = ", ".join(
            f"{items_by_id[ri.order_item_id]['product_name']} (qty: {ri.quantity})" for ri in return_items
        )

        return (
            f"I've successfully processed the return for the following items from order #{order_id}: {items_summary}. "
            f"A refund of ${refund_amount:.2f} will be issued to your original payment method within 5-7 business days. "
            "You will receive a confirmation email shortly. "
            f"To view the updated return status, please visit the Order Details page for order #{order_id}."
        )

    async def send_customer_email(self, order_id: int, user_id: int, message: str) -> str:
        self.logger.info("Agent tool invoked: send_customer_email for order_id %s", order_id)

        if self.order_service.get_order(order_id, user_id) is None:
            return f"Could not find order #{order_id} to send an email about."

        user = self.db.execute("SELECT email FROM users WHERE id = ?", (user_id,)).fetchone()
        email = user["email"] if user else "customer@contoso.com"

        await self.email_service.send_email(email, f"Regarding your order #{order_id}", message)

        return f"I've sent an email to {email} with the details about order #{order_id}."
