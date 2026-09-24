using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FoodApp
{
    [Route("[controller]")]
    [ApiController]
    public class OrdersController(FoodDBContext ctx, AILogger logger) : ControllerBase
    {
        // POST /orders
        [HttpPost()]
        public async Task<ActionResult<Order>> CreateOrder([FromBody] CreateOrderRequest request)
        {
            try
            {
                logger.LogEvent("CreateOrder", $"Creating order with {request.Items.Count} items");

                if (request.Items == null || request.Items.Count == 0)
                {
                    return BadRequest("Order must contain at least one item");
                }

                var order = new Order
                {
                    CreatedAt = DateTime.UtcNow,
                    Items = new List<OrderItem>(),
                    TotalPrice = 0
                };

                decimal total = 0;
                foreach (var item in request.Items)
                {
                    total += item.Price * item.Quantity;
                    order.Items.Add(new OrderItem
                    {
                        FoodID = item.Id,
                        FoodName = item.Name,
                        Quantity = item.Quantity,
                        Price = item.Price
                    });
                }

                order.TotalPrice = total;

                ctx.Orders.Add(order);
                await ctx.SaveChangesAsync();

                logger.LogEvent("CreateOrder", $"Order created with ID {order.ID}");
                return Ok(order);
            }
            catch (Exception ex)
            {
                logger.LogEvent("CreateOrder", $"Error: {ex.Message}");
                return StatusCode(500, new { error = ex.Message });
            }
        }

        // GET /orders
        [HttpGet()]
        public async Task<IEnumerable<Order>> GetOrders()
        {
            return await ctx.Orders.Include(o => o.Items).ToArrayAsync();
        }

        // GET /orders/{id}
        [HttpGet("{id}")]
        public async Task<ActionResult<Order>> GetOrder(int id)
        {
            var order = await ctx.Orders.Include(o => o.Items).FirstOrDefaultAsync(o => o.ID == id);
            if (order == null)
                return NotFound();
            return order;
        }
    }

    public class CreateOrderRequest
    {
        public List<OrderItemRequest> Items { get; set; }
    }

    public class OrderItemRequest
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public int Quantity { get; set; }
        public decimal Price { get; set; }
    }
}
