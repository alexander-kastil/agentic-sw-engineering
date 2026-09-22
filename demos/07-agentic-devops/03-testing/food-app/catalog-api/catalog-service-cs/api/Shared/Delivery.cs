namespace FoodApp
{
    public class Delivery
    {
        private decimal baseRate = 0.2M;

        public decimal GetDeliveryCost(decimal distance)
        {
            return distance * baseRate;
        }
    }
}