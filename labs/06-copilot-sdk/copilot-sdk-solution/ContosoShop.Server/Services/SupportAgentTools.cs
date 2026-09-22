using ContosoShop.Server.Data;
using ContosoShop.Shared.Models;
using ContosoShop.Shared.DTOs;
using Microsoft.EntityFrameworkCore;

namespace ContosoShop.Server.Services;

/// <summary>
/// Provides tool functions that the AI support agent can invoke
/// to look up order information and process returns.
/// </summary>
public class SupportAgentTools
{
    private readonly ContosoContext _context;
    private readonly IOrderService _orderService;
    private readonly IEmailService _emailService;
    private readonly ILogger<SupportAgentTools> _logger;

    public SupportAgentTools(
        ContosoContext context,
        IOrderService orderService,
        IEmailService emailService,
        ILogger<SupportAgentTools> logger)
    {
        _context = context;
        _orderService = orderService;
        _emailService = emailService;
        _logger = logger;
    }

    /// <summary>
    /// Gets the status and details of a specific order by order ID.
    /// The AI agent calls this tool when a user asks about their order status.
    /// </summary>
    public async Task<string> GetOrderDetailsAsync(int orderId, int userId)
    {
        _logger.LogInformation("Agent tool invoked: GetOrderDetails for orderId {OrderId}, userId {UserId}", orderId, userId);

        var order = await _context.Orders
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == orderId && o.UserId == userId);

        if (order == null)
        {
            return $"I could not find order #{orderId} associated with your account. Please double-check the order number.";
        }

        var statusMessage = order.Status switch
        {
            OrderStatus.Processing => "is currently being processed and has not shipped yet",
            OrderStatus.Shipped => order.ShipDate.HasValue
                ? $"was shipped on {order.ShipDate.Value:MMMM dd, yyyy} and is on its way"
                : "has been shipped and is on its way",
            OrderStatus.Delivered => order.DeliveryDate.HasValue
                ? $"was delivered on {order.DeliveryDate.Value:MMMM dd, yyyy}"
                : "has been delivered",
            OrderStatus.PartialReturn => "has been partially returned (some items have been returned, others are still with you)",
            OrderStatus.Returned => "has been fully returned and a refund was issued",
            _ => "has an unknown status"
        };

        var itemSummary = string.Join(", ", order.Items.Select(i =>
        {
            var itemInfo = $"{i.ProductName} (Id: {i.Id}, qty: {i.Quantity}, ${i.Price:F2} each";
            if (i.ReturnedQuantity > 0)
            {
                itemInfo += $", {i.ReturnedQuantity} returned, {i.RemainingQuantity} remaining";
            }
            itemInfo += ")";
            return itemInfo;
        }));

        return $"Order #{order.Id} {statusMessage}. " +
                $"Order date: {order.OrderDate:MMMM dd, yyyy}. " +
                $"Total: ${order.TotalAmount:F2}. " +
                $"Items: {itemSummary}.";
    }

    /// <summary>
    /// Gets a summary of all orders for a given user.
    /// The AI agent calls this tool when a user asks about their orders
    /// without specifying a particular order number.
    /// </summary>
    public async Task<string> GetUserOrdersSummaryAsync(int userId)
    {
        _logger.LogInformation("Agent tool invoked: GetUserOrdersSummary for userId {UserId}", userId);

        var orders = await _context.Orders
            .Where(o => o.UserId == userId)
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync();

        if (!orders.Any())
        {
            return "You don't have any orders on file.";
        }

        var summaries = orders.Select(o =>
        {
            var status = o.Status switch
            {
                OrderStatus.Processing => "Processing",
                OrderStatus.Shipped => "Shipped",
                OrderStatus.Delivered => "Delivered",
                OrderStatus.PartialReturn => "Partial Return",
                OrderStatus.Returned => "Returned",
                _ => "Unknown"
            };
            return $"Order #{o.Id} - {status} - ${o.TotalAmount:F2} - Placed {o.OrderDate:MMM dd, yyyy}";
        });

        return $"You have {orders.Count} orders:\n" + string.Join("\n", summaries);
    }

    /// <summary>
    /// Processes a return for specific items in a delivered order.
    /// The AI agent calls this tool when a user wants to return items.
    /// Supports returning all items, specific items by ID, or specific quantities.
    /// </summary>
    /// <param name="orderId">The order ID to process returns for</param>
    /// <param name="userId">The authenticated user ID</param>
    /// <param name="orderItemIds">Optional: Specific order item IDs to return (comma-separated, e.g., "123,456"). If empty, returns all unreturned items.</param>
    /// <param name="quantities">Optional: Quantities for each item (comma-separated, e.g., "1,2" for items 123 and 456). Must match orderItemIds length. If empty, returns full remaining quantity for each item.</param>
    /// <param name="reason">Optional: Reason for the return</param>
    public async Task<string> ProcessReturnAsync(
        int orderId,
        int userId,
        string orderItemIds = "",
        string quantities = "",
        string reason = "Customer requested return via AI support agent")
    {
        _logger.LogInformation("Agent tool invoked: ProcessReturn for orderId {OrderId}, userId {UserId}, items: {Items}",
            orderId, userId, string.IsNullOrEmpty(orderItemIds) ? "all" : orderItemIds);

        var order = await _context.Orders
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == orderId && o.UserId == userId);

        if (order == null)
        {
            return $"I could not find order #{orderId} associated with your account.";
        }

        if (order.Status != OrderStatus.Delivered && order.Status != OrderStatus.Returned && order.Status != OrderStatus.PartialReturn)
        {
            return order.Status switch
            {
                OrderStatus.Processing => $"Order #{orderId} is still being processed and cannot be returned yet. It must be delivered first.",
                OrderStatus.Shipped => $"Order #{orderId} is currently in transit and cannot be returned until it has been delivered.",
                _ => $"Order #{orderId} has a status of {order.Status} and cannot be returned."
            };
        }

        List<ReturnItem> returnItems;

        if (!string.IsNullOrWhiteSpace(orderItemIds))
        {
            var itemIdStrings = orderItemIds.Split(',', StringSplitOptions.RemoveEmptyEntries);
            var itemIds = new List<int>();

            foreach (var idStr in itemIdStrings)
            {
                if (int.TryParse(idStr.Trim(), out int itemId))
                {
                    itemIds.Add(itemId);
                }
                else
                {
                    return $"Invalid item ID format: '{idStr}'. Please provide valid item IDs.";
                }
            }

            var itemQuantities = new List<int>();
            if (!string.IsNullOrWhiteSpace(quantities))
            {
                var quantityStrings = quantities.Split(',', StringSplitOptions.RemoveEmptyEntries);
                foreach (var qtyStr in quantityStrings)
                {
                    if (int.TryParse(qtyStr.Trim(), out int qty) && qty > 0)
                    {
                        itemQuantities.Add(qty);
                    }
                    else
                    {
                        return $"Invalid quantity format: '{qtyStr}'. Quantities must be positive numbers.";
                    }
                }

                if (itemQuantities.Count != itemIds.Count)
                {
                    return "The number of quantities must match the number of items.";
                }
            }

            returnItems = new List<ReturnItem>();
            for (int i = 0; i < itemIds.Count; i++)
            {
                var orderItem = order.Items.FirstOrDefault(item => item.Id == itemIds[i]);
                if (orderItem == null)
                {
                    return $"Item ID {itemIds[i]} was not found in order #{orderId}.";
                }

                if (orderItem.RemainingQuantity <= 0)
                {
                    return $"{orderItem.ProductName} has already been fully returned.";
                }

                var quantityToReturn = itemQuantities.Count > 0 ? itemQuantities[i] : orderItem.RemainingQuantity;

                if (quantityToReturn > orderItem.RemainingQuantity)
                {
                    return $"Cannot return {quantityToReturn} of {orderItem.ProductName}. Only {orderItem.RemainingQuantity} available to return.";
                }

                returnItems.Add(new ReturnItem
                {
                    OrderItemId = orderItem.Id,
                    Quantity = quantityToReturn,
                    Reason = reason
                });
            }
        }
        else
        {
            returnItems = order.Items
                .Where(i => i.RemainingQuantity > 0)
                .Select(i => new ReturnItem
                {
                    OrderItemId = i.Id,
                    Quantity = i.RemainingQuantity,
                    Reason = reason
                })
                .ToList();
        }

        if (!returnItems.Any())
        {
            return $"All items in order #{orderId} have already been returned.";
        }

        var success = await _orderService.ProcessItemReturnAsync(orderId, returnItems);

        if (!success)
        {
            _logger.LogError("Failed to process return for orderId {OrderId}, userId {UserId}", orderId, userId);
            return $"I was unable to process the return for order #{orderId}. Please contact our support team for assistance.";
        }

        _logger.LogInformation("Successfully processed return for orderId {OrderId}, userId {UserId}, items: {ItemCount}",
            orderId, userId, returnItems.Count);

        var refundAmount = returnItems.Sum(ri =>
        {
            var item = order.Items.First(i => i.Id == ri.OrderItemId);
            return item.Price * ri.Quantity;
        });

        var itemsSummary = string.Join(", ", returnItems.Select(ri =>
        {
            var item = order.Items.First(i => i.Id == ri.OrderItemId);
            return $"{item.ProductName} (qty: {ri.Quantity})";
        }));

        return $"I've successfully processed the return for the following items from order #{orderId}: {itemsSummary}. " +
                $"A refund of ${refundAmount:F2} will be issued to your original payment method within 5-7 business days. " +
                $"You will receive a confirmation email shortly. " +
                $"To view the updated return status, please visit the Order Details page for order #{orderId}.";
    }

    /// <summary>
    /// Sends a follow-up email to the customer regarding their order.
    /// The AI agent calls this tool to send additional information by email.
    /// </summary>
    public async Task<string> SendCustomerEmailAsync(int orderId, int userId, string message)
    {
        _logger.LogInformation("Agent tool invoked: SendCustomerEmail for orderId {OrderId}", orderId);

        var order = await _context.Orders
            .FirstOrDefaultAsync(o => o.Id == orderId && o.UserId == userId);

        if (order == null)
        {
            return $"Could not find order #{orderId} to send an email about.";
        }

        var user = await _context.Users.FindAsync(userId);
        var email = user?.Email ?? "customer@contoso.com";

        await _emailService.SendEmailAsync(email, $"Regarding your order #{orderId}", message);

        return $"I've sent an email to {email} with the details about order #{orderId}.";
    }
}
