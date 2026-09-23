"""Read operations for inventory categories."""

import sqlite3
from typing import Protocol

from app.schemas.category import CategoryResponseDto


class CategoryServiceProtocol(Protocol):
    """Operations for reading inventory categories."""

    def get_all_categories(self) -> list[CategoryResponseDto]:
        """Return every category ordered by display order."""


class CategoryService:
    """Reads categories from the Categories table."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def get_all_categories(self) -> list[CategoryResponseDto]:
        """Return every category ordered by display order."""
        rows = self._connection.execute(
            'SELECT "Id", "Name", "Description", "DisplayOrder", "IsActive", "CreatedDate" '
            'FROM "Categories" ORDER BY "DisplayOrder"'
        ).fetchall()
        return [
            CategoryResponseDto(
                id=row["Id"],
                name=row["Name"],
                description=row["Description"],
                display_order=row["DisplayOrder"],
                is_active=bool(row["IsActive"]),
                created_date=row["CreatedDate"],
            )
            for row in rows
        ]
