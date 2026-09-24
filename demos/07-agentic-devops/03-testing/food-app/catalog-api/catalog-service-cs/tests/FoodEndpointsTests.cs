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
    public sealed class FoodEndpointsTests : IDisposable
    {
        private readonly CatalogApiFactory factory = new();
        private readonly HttpClient client;

        public FoodEndpointsTests()
        {
            client = factory.CreateClient();
        }

        [Fact]
        public async Task GetFood_ReturnsSeededItems()
        {
            var items = await client.GetFromJsonAsync<List<CatalogItem>>("/food");

            Assert.NotNull(items);
            Assert.Equal(5, items!.Count);
            Assert.Contains(items, i => i.Name == "Hand pulled Noodles");
        }

        [Fact]
        public async Task GetById_ExistingItem_ReturnsItem()
        {
            var item = await client.GetFromJsonAsync<CatalogItem>("/food/1");

            Assert.NotNull(item);
            Assert.Equal(1, item!.ID);
            Assert.Equal("Hand pulled Noodles", item.Name);
        }

        [Fact]
        public async Task GetById_MissingItem_ReturnsOkWithNullBody()
        {
            var response = await client.GetAsync("/food/9999");
            var body = await response.Content.ReadAsStringAsync();

            Assert.Equal(HttpStatusCode.NoContent, response.StatusCode);
            Assert.Empty(body);
        }

        [Fact]
        public async Task CreateFood_PersistsNewItem()
        {
            var newItem = new CatalogItem
            {
                Name = "Vegan Bowl",
                Price = 14,
                InStock = 20,
                PictureUrl = "vegan-bowl.png",
                Description = "Grain bowl with seasonal vegetables."
            };

            var response = await client.PostAsJsonAsync("/food", newItem);
            var created = await response.Content.ReadFromJsonAsync<CatalogItem>();

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            Assert.NotNull(created);
            Assert.True(created!.ID > 5);

            var fetched = await client.GetFromJsonAsync<CatalogItem>($"/food/{created.ID}");
            Assert.NotNull(fetched);
            Assert.Equal("Vegan Bowl", fetched!.Name);
        }

        [Fact]
        public async Task UpdateFood_ModifiesExistingItem()
        {
            var updated = new CatalogItem
            {
                ID = 1,
                Name = "Hand pulled Noodles Deluxe",
                Price = 19,
                InStock = 5,
                PictureUrl = "hand-pulled-noodles.png",
                Description = "Updated description."
            };

            var response = await client.PutAsJsonAsync("/food", updated);

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var fetched = await client.GetFromJsonAsync<CatalogItem>("/food/1");
            Assert.NotNull(fetched);
            Assert.Equal("Hand pulled Noodles Deluxe", fetched!.Name);
            Assert.Equal(19, fetched.Price);
        }

        [Fact]
        public async Task DeleteFood_ExistingItem_RemovesIt()
        {
            var response = await client.DeleteAsync("/food/1");

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var fetchResponse = await client.GetAsync("/food/1");
            var body = await fetchResponse.Content.ReadAsStringAsync();

            Assert.Equal(HttpStatusCode.NoContent, fetchResponse.StatusCode);
            Assert.Empty(body);
        }

        [Fact]
        public async Task DeleteFood_MissingItem_ReturnsOk()
        {
            var response = await client.DeleteAsync("/food/9999");

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        public void Dispose()
        {
            client.Dispose();
            factory.Dispose();
        }
    }
}
