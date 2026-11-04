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

    MAX_SEARCH_TERM_LENGTH = 100
    DISALLOWED_SEARCH_CHARACTERS = ("'", '"', ";", "<", ">", "-")

    # Search method with input sanitization to prevent SQL injection
    def search_products(self, search_term: str) -> list[Product]:
        if not search_term or not search_term.strip():
            return []

        sanitized_search_term = self._sanitize_search_term(search_term)

        return self._product_repository.search_products(sanitized_search_term)

    # Removes SQL metacharacters and enforces a maximum length before the term reaches the data layer
    def _sanitize_search_term(self, search_term: str) -> str:
        sanitized = search_term.strip()[: self.MAX_SEARCH_TERM_LENGTH]

        for character in self.DISALLOWED_SEARCH_CHARACTERS:
            sanitized = sanitized.replace(character, "")

        return sanitized

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
