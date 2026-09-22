using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.AI;
using GitHub.Copilot;
using ContosoShop.Server.Services;
using ContosoShop.Shared.Models;
using System.ComponentModel;
using System.Security.Claims;

namespace ContosoShop.Server.Controllers;

/// <summary>
/// API controller that handles AI support agent queries.
/// Accepts user questions, creates a Copilot SDK session with custom tools,
/// and returns the agent's response.
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Authorize]
public class SupportAgentController : ControllerBase
{
    private readonly CopilotClient _copilotClient;
    private readonly SupportAgentTools _agentTools;
    private readonly ILogger<SupportAgentController> _logger;

    public SupportAgentController(
        CopilotClient copilotClient,
        SupportAgentTools agentTools,
        ILogger<SupportAgentController> logger)
    {
        _copilotClient = copilotClient;
        _agentTools = agentTools;
        _logger = logger;
    }

    /// <summary>
    /// Accepts a support question from the user and returns the AI agent's response.
    /// POST /api/supportagent/ask
    /// </summary>
    [HttpPost("ask")]
    public async Task<IActionResult> AskQuestion([FromBody] SupportQuery query)
    {
        if (query == null || string.IsNullOrWhiteSpace(query.Question))
        {
            return BadRequest(new SupportResponse { Answer = "Please enter a question." });
        }

        // Get the authenticated user's ID from claims
        var userIdClaim = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        if (!int.TryParse(userIdClaim, out int userId))
        {
            return Unauthorized(new SupportResponse { Answer = "Unable to identify user." });
        }

        _logger.LogInformation("Support agent query from user {UserId}: {Question}", userId, query.Question);

        try
        {
            // Define the tools the AI agent can use
            var tools = new[]
            {
                AIFunctionFactory.Create(
                    async ([Description("The order ID number")] int orderId) =>
                        await _agentTools.GetOrderDetailsAsync(orderId, userId),
                    "get_order_details",
                    "Look up the status and details of a specific order by its order number. Returns order status, items, dates, and total amount."),

                AIFunctionFactory.Create(
                    async () =>
                        await _agentTools.GetUserOrdersSummaryAsync(userId),
                    "get_user_orders",
                    "Get a summary list of all orders for the current user. Use this when the user asks about their orders without specifying an order number."),

                AIFunctionFactory.Create(
                    async (
                        [Description("The order ID number")] int orderId,
                        [Description("Optional: Specific order item IDs to return (comma-separated, e.g. '123,456'). Leave empty to return all items.")] string orderItemIds = "",
                        [Description("Optional: Quantities for each item (comma-separated, e.g. '1,2'). Must match orderItemIds count. Leave empty to return full quantity.")] string quantities = "",
                        [Description("Optional: Reason for return")] string reason = "Customer requested return via AI support agent") =>
                        await _agentTools.ProcessReturnAsync(orderId, userId, orderItemIds, quantities, reason),
                    "process_return",
                    "Process a return for specific items from a delivered order. Can return all items, specific items by ID, or specific quantities of items. Accepts comma-separated item IDs and quantities. Works for orders with Delivered, PartialReturn, or Returned status."),

                AIFunctionFactory.Create(
                    async (
                        [Description("The order ID number")] int orderId,
                        [Description("The email message content")] string message) =>
                        await _agentTools.SendCustomerEmailAsync(orderId, userId, message),
                    "send_customer_email",
                    "Send a follow-up email to the customer with additional information about their order.")
            };

            // Create a Copilot session with the system prompt and tools
#pragma warning disable GHCP001
            await using var session = await _copilotClient.CreateSessionAsync(new SessionConfig
            {
                Model = "gpt-4.1",
                OnPermissionRequest = (request, invocation) =>
                    Task.FromResult(GitHub.Copilot.Rpc.PermissionDecision.ApproveOnce()),
                SystemMessage = new SystemMessageConfig
                {
                    Mode = SystemMessageMode.Replace,
                    Content = @"You are ContosoShop's AI customer support assistant. Your role is to help customers with their order inquiries.

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
                   - Match by ProductName field (case-insensitive, partial match is OK)
                   - AUTOMATICALLY extract the Id field from the matching OrderItem - this is the item ID you need
                   - NEVER ask the customer for an item ID - they don't have this information
                4. Determine the return quantity:
                   - If customer specified quantity in their request: use that quantity
                   - Else if remaining quantity is 1: automatically return that 1 item
                   - Else if remaining quantity is more than 1 and no quantity specified: ask how many they want to return
                5. Call process_return with the extracted item ID and quantity:
                   - Pass orderItemIds as the Id value from the OrderItem (e.g., '456')
                   - Pass quantities as the number to return (e.g., '1')
                6. After successful return, tell customer to view Order Details page to see the updated status

                IMPORTANT RULES FOR RETURNS:
                - NEVER ask the customer for an item ID - extract it automatically from get_order_details response
                - Match product names flexibly (e.g., 'lamp', 'Lamp', 'desk lamp' should all match)
                - If multiple items have the same product name, select the first one that has remaining quantity
                - DO NOT ask for quantity if the customer already specified it (e.g., 'return 1 lamp', 'return 2 items')
                - DO NOT ask for quantity if there's only 1 of that item available
                - Pass item IDs and quantities as comma-separated strings to process_return
                - After processing return, remind customer: 'Please visit the Order Details page to see the updated return status.'

                EXAMPLE WORKFLOW:
                User: 'I want to return the Headphones from order #1002'
                1. Call get_order_details(1002)
                2. Response includes: 'Items: Headphones (qty: 1, $99.99 each, Id: 456), ...'
                3. Extract: productName='Headphones', itemId='456', remainingQty=1
                4. Since remainingQty=1, quantity=1 (no need to ask)
                5. Call process_return(1002, userId, '456', '1', 'Customer requested return')
                6. Tell customer: 'I've processed the return for Headphones. Please view Order Details...'

                GENERAL RULES:
                - ALWAYS use the available tools to look up real data. Never guess or make up order information.
                - Be friendly, concise, and professional in your responses.
                - If a customer asks about an order, use get_order_details with the order number they provide.
                - If a customer asks about their orders without specifying a number, use get_user_orders to list them.
                - Only process returns when the customer explicitly requests one.
                - If asked something outside your capabilities (not related to orders), politely explain that you can only help with order-related inquiries and suggest contacting support@contososhop.com or calling 1-800-CONTOSO for other matters.
                - Do not reveal internal system details, tool names, or technical information to the customer."
                },
                Tools = tools,
                InfiniteSessions = new InfiniteSessionConfig { Enabled = false }
            });
#pragma warning restore GHCP001

            // Collect the agent's response
            var responseContent = string.Empty;
            var done = new TaskCompletionSource();

            session.On<SessionEvent>(evt =>
            {
                switch (evt)
                {
                    case AssistantMessageEvent msg:
                        responseContent = msg.Data.Content;
                        break;
                    case SessionIdleEvent:
                        done.TrySetResult();
                        break;
                    case SessionErrorEvent err:
                        _logger.LogError("Agent session error: {Message}", err.Data.Message);
                        done.TrySetException(new Exception(err.Data.Message));
                        break;
                }
            });

            // Send the user's question
            await session.SendAsync(new MessageOptions { Prompt = query.Question });

            // Wait for the response with a timeout
            var timeoutTask = Task.Delay(TimeSpan.FromSeconds(30));
            var completedTask = await Task.WhenAny(done.Task, timeoutTask);

            if (completedTask == timeoutTask)
            {
                _logger.LogWarning("Agent session timed out for user {UserId}", userId);
                return Ok(new SupportResponse
                {
                    Answer = "I'm sorry, the request took too long. Please try again or contact our support team."
                });
            }

            // Rethrow if the task faulted
            await done.Task;

            _logger.LogInformation("Agent response for user {UserId}: {Answer}", userId, responseContent);

            return Ok(new SupportResponse { Answer = responseContent });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing support agent query for user {UserId}", userId);
            return StatusCode(500, new SupportResponse
            {
                Answer = "I'm sorry, I encountered an error processing your request. Please try again or contact our support team at support@contososhop.com."
            });
        }
    }
}
