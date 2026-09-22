using ContosoShopEasy.Models;
using ContosoShopEasy.Data;

namespace ContosoShopEasy.Services
{
    public class ProductService
    {
        private readonly ProductRepository _productRepository;

        public ProductService(ProductRepository productRepository)
        {
            _productRepository = productRepository;
        }

        public List<Product> GetAllProducts()
        {
            return _productRepository.GetAllProducts();
        }

        public Product? GetProductById(int id)
        {
            return _productRepository.GetProductById(id);
        }

        public List<Product> GetProductsByCategory(int categoryId)
        {
            return _productRepository.GetProductsByCategory(categoryId);
        }

        private const int MaxSearchTermLength = 100;
        private static readonly char[] DisallowedSearchCharacters = { '\'', '"', ';', '<', '>', '-' };

        // Search method with input sanitization to prevent SQL injection
        public List<Product> SearchProducts(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
            {
                return new List<Product>();
            }

            string sanitizedSearchTerm = SanitizeSearchTerm(searchTerm);

            return _productRepository.SearchProducts(sanitizedSearchTerm);
        }

        // Removes SQL metacharacters and enforces a maximum length before the term reaches the data layer
        private static string SanitizeSearchTerm(string searchTerm)
        {
            string trimmedSearchTerm = searchTerm.Trim();

            if (trimmedSearchTerm.Length > MaxSearchTermLength)
            {
                trimmedSearchTerm = trimmedSearchTerm[..MaxSearchTermLength];
            }

            foreach (char disallowedCharacter in DisallowedSearchCharacters)
            {
                trimmedSearchTerm = trimmedSearchTerm.Replace(disallowedCharacter.ToString(), string.Empty);
            }

            return trimmedSearchTerm;
        }

        public List<Product> GetTopRatedProducts(int count = 10)
        {
            return _productRepository.GetAllProducts()
                .Where(p => p.IsActive)
                .OrderByDescending(p => p.Rating)
                .Take(count)
                .ToList();
        }

        public List<Product> GetFeaturedProducts(int count = 5)
        {
            return _productRepository.GetAllProducts()
                .Where(p => p.IsActive && p.StockQuantity > 0)
                .OrderByDescending(p => p.ReviewCount)
                .Take(count)
                .ToList();
        }

        public bool IsProductInStock(int productId, int quantity = 1)
        {
            var product = _productRepository.GetProductById(productId);
            return product != null && product.StockQuantity >= quantity;
        }

        public bool UpdateStock(int productId, int quantityChange)
        {
            var product = _productRepository.GetProductById(productId);
            if (product != null)
            {
                product.StockQuantity += quantityChange;
                product.LastModified = DateTime.UtcNow;
                return true;
            }
            return false;
        }
    }
}