"""Category DTOs."""

from app.schemas import CamelModel


class CategoryResponseDto(CamelModel):
    """A category as returned by the API."""

    id: int
    name: str
    description: str
    display_order: int
    is_active: bool
    created_date: str
