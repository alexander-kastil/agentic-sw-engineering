using FoodApp;
using Xunit;

namespace FoodApp.Tests
{
    public sealed class DeliveryTests
    {
        [Theory]
        [InlineData(0, 0)]
        [InlineData(10, 2.0)]
        [InlineData(25.5, 5.1)]
        public void GetDeliveryCost_ReturnsDistanceTimesBaseRate(double distance, double expectedCost)
        {
            var delivery = new Delivery();

            var cost = delivery.GetDeliveryCost((decimal)distance);

            Assert.Equal((decimal)expectedCost, cost);
        }
    }
}
