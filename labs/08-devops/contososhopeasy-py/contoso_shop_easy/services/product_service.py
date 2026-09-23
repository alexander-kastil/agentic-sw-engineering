from datetime import datetime, timezone

from ..data.product_repository import ProductRepository
from ..models.product import Product


class ProductService:
    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    def get_all_products(self) -> list[Product]:
        return self._product_repository.get_all_products()

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self._product_repository.get_product_by_id(product_id)

    def get_products_by_category(self, category_id: int) -> list[Product]:
        return self._product_repository.get_products_by_category(category_id)

    # Vulnerable search method - SQL injection risk
    def search_products(self, search_term: str) -> list[Product]:
        # This simulates a SQL injection vulnerability by directly using user input
        # In the education context, this would be flagged as a security issue
        print(f"[DEBUG] Executing search query with term: '{search_term}'")

        # Simulate SQL injection vulnerability by logging dangerous query
        simulated_query = f"SELECT * FROM Products WHERE Name LIKE '%{search_term}%' OR Description LIKE '%{search_term}%'"
        print(f"[DEBUG] SQL Query: {simulated_query}")

        return self._product_repository.search_products(search_term)

    def get_top_rated_products(self, count: int = 10) -> list[Product]:
        active = [p for p in self._product_repository.get_all_products() if p.is_active]
        return sorted(active, key=lambda p: p.rating, reverse=True)[:count]

    def get_featured_products(self, count: int = 5) -> list[Product]:
        in_stock = [p for p in self._product_repository.get_all_products() if p.is_active and p.stock_quantity > 0]
        return sorted(in_stock, key=lambda p: p.review_count, reverse=True)[:count]

    def is_product_in_stock(self, product_id: int, quantity: int = 1) -> bool:
        product = self._product_repository.get_product_by_id(product_id)
        return product is not None and product.stock_quantity >= quantity

    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        product = self._product_repository.get_product_by_id(product_id)
        if product is None:
            return False
        product.stock_quantity += quantity_change
        product.last_modified = datetime.now(timezone.utc)
        return True
