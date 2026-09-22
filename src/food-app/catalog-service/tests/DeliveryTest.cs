using System.Reflection;
using System;
using Xunit;
using FoodApp;

namespace FoodApiTests
{
    public class DeliveryTest
    {
        private readonly Delivery delivery;

        public DeliveryTest()
        {
            delivery = new Delivery();
        }

        [Fact]
        public void CalaculatesDeliveryRate()
        {
            var result = delivery.GetDeliveryCost(100);
            Assert.True(result == 20);
        }
    }
}
