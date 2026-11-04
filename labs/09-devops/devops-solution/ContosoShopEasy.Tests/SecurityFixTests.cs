using ContosoShopEasy.Data;
using ContosoShopEasy.Models;
using ContosoShopEasy.Security;
using ContosoShopEasy.Services;
using Xunit;

namespace ContosoShopEasy.Tests
{
    public class SecurityFixTests
    {
        [Fact]
        public void ProcessPayment_DoesNotLogFullCardNumberOrCvv()
        {
            var orderRepository = new OrderRepository();
            var paymentService = new PaymentService(orderRepository);
            string cardNumber = "4532015112830366";
            string cvv = "123";

            string log = CaptureConsoleOutput(() =>
                paymentService.ProcessPayment(cardNumber, "Test User", "12/30", cvv, 100m));

            Assert.DoesNotContain(cardNumber, log);
            Assert.DoesNotContain(cvv, log);
            Assert.Contains("0366", log);
        }

        [Fact]
        public void ValidateCreditCard_DoesNotLogFullCardNumber()
        {
            var validator = new SecurityValidator();
            string cardNumber = "4111111111111111";

            string log = CaptureConsoleOutput(() => validator.ValidateCreditCard(cardNumber));

            Assert.DoesNotContain(cardNumber, log);
            Assert.Contains("1111", log);
        }

        [Fact]
        public void SearchProducts_DoesNotLogSimulatedSqlQuery()
        {
            var productRepository = new ProductRepository();
            var productService = new ProductService(productRepository);
            List<Product> results = new();

            string log = CaptureConsoleOutput(() => results = productService.SearchProducts("laptop"));

            Assert.DoesNotContain("SELECT * FROM Products", log);
            Assert.NotEmpty(results);
        }

        [Fact]
        public void SearchProducts_SanitizesMaliciousInputWithoutThrowing()
        {
            var productRepository = new ProductRepository();
            var productService = new ProductService(productRepository);

            var results = productService.SearchProducts("'; DROP TABLE Products; --");

            Assert.NotNull(results);
            Assert.Empty(results);
        }

        [Fact]
        public void PaymentInfo_HasNoCardNumberOrCvvProperty()
        {
            var paymentInfoType = typeof(PaymentInfo);

            Assert.Null(paymentInfoType.GetProperty("CardNumber"));
            Assert.Null(paymentInfoType.GetProperty("CVV"));
            Assert.NotNull(paymentInfoType.GetProperty("CardLastFourDigits"));
            Assert.NotNull(paymentInfoType.GetProperty("CardType"));
        }

        private static string CaptureConsoleOutput(Action action)
        {
            var originalOut = Console.Out;
            var writer = new StringWriter();
            Console.SetOut(writer);
            try
            {
                action();
            }
            finally
            {
                Console.SetOut(originalOut);
            }

            return writer.ToString();
        }
    }
}
