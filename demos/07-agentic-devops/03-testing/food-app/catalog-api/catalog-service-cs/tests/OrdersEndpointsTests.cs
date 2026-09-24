using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using FoodApp;
using Xunit;

namespace FoodApp.Tests
{
    public sealed class OrdersEndpointsTests : IDisposable
    {
        private readonly CatalogApiFactory factory = new();
        private readonly HttpClient client;

        public OrdersEndpointsTests()
        {
            client = factory.CreateClient();
        }

        private static CreateOrderRequest ValidRequest() => new()
        {
            Items = new List<OrderItemRequest>
            {
                new() { Id = 1, Name = "Hand pulled Noodles", Quantity = 2, Price = 17 },
                new() { Id = 3, Name = "Wiener Schnitzel", Quantity = 1, Price = 18 }
            }
        };

        [Fact]
        public async Task CreateOrder_ValidRequest_ReturnsCreatedOrder()
        {
            var response = await client.PostAsJsonAsync("/orders", ValidRequest());
            var order = await response.Content.ReadFromJsonAsync<Order>();

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            Assert.NotNull(order);
            Assert.True(order!.ID > 0);
            Assert.Equal(2, order.Items.Count);
        }

        [Fact]
        public async Task CreateOrder_CalculatesTotalPriceFromItems()
        {
            var response = await client.PostAsJsonAsync("/orders", ValidRequest());
            var order = await response.Content.ReadFromJsonAsync<Order>();

            Assert.NotNull(order);
            Assert.Equal(2 * 17 + 1 * 18, order!.TotalPrice);
        }

        [Fact]
        public async Task CreateOrder_EmptyItems_ReturnsBadRequest()
        {
            var request = new CreateOrderRequest { Items = new List<OrderItemRequest>() };

            var response = await client.PostAsJsonAsync("/orders", request);

            Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        }

        [Fact]
        public async Task CreateOrder_NullItems_ReturnsBadRequest()
        {
            var request = new CreateOrderRequest { Items = null };

            var response = await client.PostAsJsonAsync("/orders", request);

            Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        }

        [Fact]
        public async Task GetOrders_ReturnsCreatedOrder()
        {
            await client.PostAsJsonAsync("/orders", ValidRequest());

            var orders = await client.GetFromJsonAsync<List<Order>>("/orders");

            Assert.NotNull(orders);
            Assert.Single(orders!);
        }

        [Fact]
        public async Task GetOrder_ExistingOrder_ReturnsOrder()
        {
            var createResponse = await client.PostAsJsonAsync("/orders", ValidRequest());
            var created = await createResponse.Content.ReadFromJsonAsync<Order>();

            var fetched = await client.GetFromJsonAsync<Order>($"/orders/{created!.ID}");

            Assert.NotNull(fetched);
            Assert.Equal(created.ID, fetched!.ID);
            Assert.Equal(2, fetched.Items.Count);
        }

        [Fact]
        public async Task GetOrder_MissingOrder_ReturnsNotFound()
        {
            var response = await client.GetAsync("/orders/9999");

            Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        }

        public void Dispose()
        {
            client.Dispose();
            factory.Dispose();
        }
    }
}
