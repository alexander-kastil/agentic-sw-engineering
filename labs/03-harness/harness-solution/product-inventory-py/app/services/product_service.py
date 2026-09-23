"""Operations for managing inventory products."""

import logging
import sqlite3
from datetime import datetime, timezone
from typing import Protocol

from app.schemas.product import CreateProductDto, ProductResponseDto, UpdateProductDto

logger = logging.getLogger(__name__)

_SELECT_PRODUCT = (
    'SELECT p."Id", p."Name", p."Sku", p."Description", p."Price", p."StockQuantity", '
    'p."CategoryId", c."Name" AS "CategoryName", p."CreatedDate", p."LastUpdatedDate" '
    'FROM "Products" p JOIN "Categories" c ON c."Id" = p."CategoryId"'
)


class ProductServiceProtocol(Protocol):
    """Operations for managing inventory products."""

    def get_all_products(self, category_id: int | None) -> list[ProductResponseDto]:
        """Return all products, optionally filtered by category."""

    def get_product_by_id(self, product_id: int) -> ProductResponseDto | None:
        """Return a product, or None if it does not exist."""

    def create_product(self, dto: CreateProductDto) -> ProductResponseDto:
        """Create a product. Raises ValueError for a duplicate SKU or unknown category."""

    def update_product(self, product_id: int, dto: UpdateProductDto) -> ProductResponseDto | None:
        """Update a product, or return None if it does not exist. Raises ValueError like create."""

    def delete_product(self, product_id: int) -> bool:
        """Delete a product and return whether it existed."""

    def restock(self, product_id: int, quantity: int) -> ProductResponseDto | None:
        """Add stock to a product, or return None if it does not exist."""


class ProductService:
    """SQLite implementation of the product operations."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def get_all_products(self, category_id: int | None) -> list[ProductResponseDto]:
        """Return all products ordered by name, optionally filtered by category."""
        if category_id is None:
            rows = self._connection.execute(f'{_SELECT_PRODUCT} ORDER BY p."Name"').fetchall()
        else:
            rows = self._connection.execute(
                f'{_SELECT_PRODUCT} WHERE p."CategoryId" = ? ORDER BY p."Name"', (category_id,)
            ).fetchall()
        return [_map_to_dto(row) for row in rows]

    def get_product_by_id(self, product_id: int) -> ProductResponseDto | None:
        """Return a product, or None if it does not exist."""
        row = self._connection.execute(f'{_SELECT_PRODUCT} WHERE p."Id" = ?', (product_id,)).fetchone()
        return None if row is None else _map_to_dto(row)

    def create_product(self, dto: CreateProductDto) -> ProductResponseDto:
        """Create a product. Raises ValueError for a duplicate SKU or unknown category."""
        self._ensure_category_exists(dto.category_id)
        self._ensure_sku_is_free(dto.sku, None)
        now = _utc_now()
        with self._connection:
            cursor = self._connection.execute(
                'INSERT INTO "Products" ("Name", "Sku", "Description", "Price", "StockQuantity", '
                '"CategoryId", "CreatedDate", "LastUpdatedDate") VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (dto.name, dto.sku, dto.description, dto.price, dto.stock_quantity, dto.category_id, now, now),
            )
        logger.info("Product created: %s (ID: %s).", dto.name, cursor.lastrowid)
        return self.get_product_by_id(cursor.lastrowid)

    def update_product(self, product_id: int, dto: UpdateProductDto) -> ProductResponseDto | None:
        """Update a product, or return None if it does not exist. Raises ValueError like create."""
        if self.get_product_by_id(product_id) is None:
            return None
        self._ensure_category_exists(dto.category_id)
        self._ensure_sku_is_free(dto.sku, product_id)
        with self._connection:
            self._connection.execute(
                'UPDATE "Products" SET "Name" = ?, "Sku" = ?, "Description" = ?, "Price" = ?, '
                '"StockQuantity" = ?, "CategoryId" = ?, "LastUpdatedDate" = ? WHERE "Id" = ?',
                (dto.name, dto.sku, dto.description, dto.price, dto.stock_quantity, dto.category_id,
                 _utc_now(), product_id),
            )
        logger.info("Product updated: %s (ID: %s).", dto.name, product_id)
        return self.get_product_by_id(product_id)

    def delete_product(self, product_id: int) -> bool:
        """Delete a product and return whether it existed."""
        with self._connection:
            cursor = self._connection.execute('DELETE FROM "Products" WHERE "Id" = ?', (product_id,))
        if cursor.rowcount == 0:
            return False
        logger.info("Product deleted: ID %s.", product_id)
        return True

    def restock(self, product_id: int, quantity: int) -> ProductResponseDto | None:
        """Add stock to a product, or return None if it does not exist."""
        with self._connection:
            cursor = self._connection.execute(
                'UPDATE "Products" SET "StockQuantity" = "StockQuantity" + ?, "LastUpdatedDate" = ? WHERE "Id" = ?',
                (quantity, _utc_now(), product_id),
            )
        if cursor.rowcount == 0:
            return None
        product = self.get_product_by_id(product_id)
        logger.info("Product restocked: ID %s by %s. New stock: %s.", product_id, quantity, product.stock_quantity)
        return product

    def _ensure_category_exists(self, category_id: int) -> None:
        row = self._connection.execute('SELECT 1 FROM "Categories" WHERE "Id" = ?', (category_id,)).fetchone()
        if row is None:
            raise ValueError(f"Category with ID {category_id} doesn't exist.")

    def _ensure_sku_is_free(self, sku: str, product_id: int | None) -> None:
        row = self._connection.execute(
            'SELECT 1 FROM "Products" WHERE "Sku" = ? COLLATE NOCASE AND "Id" IS NOT ?', (sku, product_id)
        ).fetchone()
        if row is not None:
            raise ValueError(f"A product with the SKU '{sku}' already exists.")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(tzinfo=None).isoformat()


def _map_to_dto(row: sqlite3.Row) -> ProductResponseDto:
    return ProductResponseDto(
        id=row["Id"],
        name=row["Name"],
        sku=row["Sku"],
        description=row["Description"],
        price=row["Price"],
        stock_quantity=row["StockQuantity"],
        category_id=row["CategoryId"],
        category_name=row["CategoryName"],
        created_date=row["CreatedDate"],
        last_updated_date=row["LastUpdatedDate"],
    )
