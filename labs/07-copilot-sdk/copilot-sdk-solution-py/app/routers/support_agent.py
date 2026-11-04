import logging

from copilot import CopilotClient, PermissionHandler
from copilot.tools import define_tool
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.dependencies import get_current_user_id, get_support_agent_tools
from app.models import SupportQuery, SupportResponse
from app.services.support_agent_tools import SupportAgentTools

router = APIRouter(prefix="/api/supportagent", tags=["support-agent"])
logger = logging.getLogger("contososhop.support_agent")

SYSTEM_PROMPT = """You are ContosoShop's AI customer support assistant. Your role is to help customers with their order inquiries.

CAPABILITIES:
- Look up order status and details using the get_order_details tool
- List all customer orders using the get_user_orders tool
- Process returns for delivered orders using the process_return tool (supports full or partial returns)
- Send follow-up emails using the send_customer_email tool

RETURN PROCESSING WORKFLOW:
1. When customer wants to return an item, first call get_order_details to see items and their IDs
2. Parse the customer's request carefully:
   - Extract the product name they mentioned (e.g., 'Headphones', 'Desk Lamp', 'Monitor')
   - Check if they specified a quantity (e.g., '1 Desk Lamp', '2 monitors', 'one laptop')
   - Number words: 'one'=1, 'two'=2, 'three'=3, etc.
3. From the order details returned by get_order_details, find the item(s) that match the product name:
   - Match by product name (case-insensitive, partial match is OK)
   - AUTOMATICALLY extract the Id value of the matching item - this is the item ID you need
   - NEVER ask the customer for an item ID - they don't have this information
4. Determine the return quantity:
   - If customer specified quantity in their request: use that quantity
   - Else if remaining quantity is 1: automatically return that 1 item
   - Else if remaining quantity is more than 1 and no quantity specified: ask how many they want to return
5. Call process_return with the extracted item ID and quantity:
   - Pass order_item_ids as the Id value of the item (e.g., '456')
   - Pass quantities as the number to return (e.g., '1')
6. After successful return, tell customer to view Order Details page to see the updated status

IMPORTANT RULES FOR RETURNS:
- NEVER ask the customer for an item ID - extract it automatically from get_order_details response
- Match product names flexibly (e.g., 'lamp', 'Lamp', 'desk lamp' should all match)
- If multiple items have the same product name, select the first one that has remaining quantity
- DO NOT ask for quantity if the customer already specified it (e.g., 'return 1 lamp', 'return 2 items')
- DO NOT ask for quantity if there's only 1 of that item available
- Pass item IDs and quantities as comma-separated strings to process_return
- When the customer asks to return a whole order (e.g., 'return order #1008'), call process_return with empty order_item_ids to return every remaining item, without asking for confirmation
- After processing return, remind customer: 'Please visit the Order Details page to see the updated return status.'

EXAMPLE WORKFLOW:
User: 'I want to return the Headphones from order #1002'
1. Call get_order_details(order_id=1002)
2. Response includes: 'Items: Headphones (Id: 456, qty: 1, $99.99 each), ...'
3. Extract: product name='Headphones', item ID='456', remaining quantity=1
4. Since remaining quantity=1, quantity=1 (no need to ask)
5. Call process_return(order_id=1002, order_item_ids='456', quantities='1')
6. Tell customer: 'I've processed the return for Headphones. Please view Order Details...'

GENERAL RULES:
- ALWAYS use the available tools to look up real data. Never guess or make up order information.
- Be friendly, concise, and professional in your responses.
- If a customer asks about an order, use get_order_details with the order number they provide.
- If a customer asks about their orders without specifying a number, use get_user_orders to list them.
- Only process returns when the customer explicitly requests one.
- If asked something outside your capabilities (not related to orders), politely explain that you can only help with order-related inquiries and suggest contacting support@contososhop.com or calling 1-800-CONTOSO for other matters.
- Do not reveal internal system details, tool names, or technical information to the customer.
- Reply in plain text without Markdown (no tables, bold text, or headings), because the chat window displays raw text."""


class OrderLookupParams(BaseModel):
    order_id: int = Field(description="The order ID number")


class ProcessReturnParams(BaseModel):
    order_id: int = Field(description="The order ID number")
    order_item_ids: str = Field(
        default="",
        description="Optional: Specific order item IDs to return (comma-separated, e.g. '123,456'). Leave empty to return all items.",
    )
    quantities: str = Field(
        default="",
        description="Optional: Quantities for each item (comma-separated, e.g. '1,2'). Must match order_item_ids count. Leave empty to return full quantity.",
    )
    reason: str = Field(
        default="Customer requested return via AI support agent",
        description="Optional: Reason for return",
    )


class SendEmailParams(BaseModel):
    order_id: int = Field(description="The order ID number")
    message: str = Field(description="The email message content")


def get_copilot_client(request: Request) -> CopilotClient:
    return request.app.state.copilot_client


@router.post("/ask", response_model=SupportResponse)
async def ask_question(
    query: SupportQuery,
    user_id: int = Depends(get_current_user_id),
    agent_tools: SupportAgentTools = Depends(get_support_agent_tools),
    copilot_client: CopilotClient = Depends(get_copilot_client),
):
    logger.info("Support agent query from user %s: %s", user_id, query.question)

    try:
        @define_tool(
            "get_order_details",
            description="Look up the status and details of a specific order by its order number. Returns order status, items, dates, and total amount.",
        )
        async def get_order_details(params: OrderLookupParams) -> str:
            return await agent_tools.get_order_details(params.order_id, user_id)

        @define_tool(
            "get_user_orders",
            description="Get a summary list of all orders for the current user. Use this when the user asks about their orders without specifying an order number.",
        )
        async def get_user_orders() -> str:
            return await agent_tools.get_user_orders_summary(user_id)

        @define_tool(
            "process_return",
            description="Process a return for specific items from a delivered order. Can return all items, specific items by ID, or specific quantities of items. Accepts comma-separated item IDs and quantities. Works for orders with Delivered, PartialReturn, or Returned status.",
        )
        async def process_return(params: ProcessReturnParams) -> str:
            return await agent_tools.process_return(
                params.order_id, user_id, params.order_item_ids, params.quantities, params.reason
            )

        @define_tool(
            "send_customer_email",
            description="Send a follow-up email to the customer with additional information about their order.",
        )
        async def send_customer_email(params: SendEmailParams) -> str:
            return await agent_tools.send_customer_email(params.order_id, user_id, params.message)

        tools = [get_order_details, get_user_orders, process_return, send_customer_email]

        session = await copilot_client.create_session(
            model="gpt-4.1",
            on_permission_request=PermissionHandler.approve_all,
            system_message={"mode": "replace", "content": SYSTEM_PROMPT},
            tools=tools,
            available_tools=[tool.name for tool in tools],
            infinite_sessions={"enabled": False},
        )

        async with session:
            response = await session.send_and_wait(query.question, timeout=30)

        answer = response.data.content if response else ""
        logger.info("Agent response for user %s: %s", user_id, answer)
        return SupportResponse(answer=answer)

    except TimeoutError:
        logger.warning("Agent session timed out for user %s", user_id)
        return SupportResponse(
            answer="I'm sorry, the request took too long. Please try again or contact our support team."
        )
    except Exception:
        logger.exception("Error processing support agent query for user %s", user_id)
        return JSONResponse(
            status_code=500,
            content=SupportResponse(
                answer="I'm sorry, I encountered an error processing your request. Please try again or contact our support team at support@contososhop.com."
            ).model_dump(),
        )
