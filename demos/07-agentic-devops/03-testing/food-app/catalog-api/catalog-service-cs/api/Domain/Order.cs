using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace FoodApp
{
    public class Order
    {
        public int ID { get; set; }
        public System.DateTime CreatedAt { get; set; }
        public List<OrderItem> Items { get; set; } = new();
        public decimal TotalPrice { get; set; }
    }

    public class OrderItem
    {
        public int ID { get; set; }
        public int OrderID { get; set; }

        [JsonIgnore]
        public Order Order { get; set; }

        public int FoodID { get; set; }
        public string FoodName { get; set; }
        public int Quantity { get; set; }
        public decimal Price { get; set; }
    }
}
