using System;
using System.Net;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using Xunit;

namespace FoodApp.Tests
{
    public sealed class ConfigEndpointsTests : IDisposable
    {
        private readonly CatalogApiFactory factory = new();
        private readonly HttpClient client;

        public ConfigEndpointsTests()
        {
            client = factory.CreateClient();
        }

        [Fact]
        public async Task GetConfig_ReturnsAppConfig()
        {
            var response = await client.GetAsync("/config");
            var json = await response.Content.ReadAsStringAsync();
            using var document = JsonDocument.Parse(json);

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            Assert.Equal("Catalog Service", document.RootElement.GetProperty("title").GetString());
        }

        [Fact]
        public async Task GetEnvVars_ReturnsEnvironmentVariables()
        {
            var response = await client.GetAsync("/config/getEnvVars");
            var json = await response.Content.ReadAsStringAsync();
            using var document = JsonDocument.Parse(json);

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            Assert.Equal(JsonValueKind.Object, document.RootElement.ValueKind);
        }

        [Fact]
        public async Task GetFeatureFlags_ReturnsPremiumFeatureFlag()
        {
            var response = await client.GetAsync("/config/getFeatureFlags");
            var json = await response.Content.ReadAsStringAsync();
            using var document = JsonDocument.Parse(json);

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            Assert.False(document.RootElement.GetProperty("PremiumFeature").GetBoolean());
        }

        public void Dispose()
        {
            client.Dispose();
            factory.Dispose();
        }
    }
}
