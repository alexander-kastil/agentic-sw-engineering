using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Xunit;

namespace FoodApp.Tests
{
    public sealed class HealthEndpointsTests : IDisposable
    {
        private readonly CatalogApiFactory factory = new();
        private readonly HttpClient client;

        public HealthEndpointsTests()
        {
            client = factory.CreateClient();
        }

        [Fact]
        public async Task Liveness_ReturnsOk()
        {
            var response = await client.GetAsync("/health/liveness");

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task Readiness_ReturnsOk()
        {
            var response = await client.GetAsync("/health/readiness");

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task Startup_ReturnsOk()
        {
            var response = await client.GetAsync("/health/startup");

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        public void Dispose()
        {
            client.Dispose();
            factory.Dispose();
        }
    }
}
