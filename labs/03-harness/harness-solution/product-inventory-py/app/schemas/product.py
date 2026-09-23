"""Product DTOs, one per operation, following the same pattern as the Category feature."""

from pydantic import Field

from app.schemas import CamelModel


class ProductResponseDto(CamelModel):
    """A product as returned by the API, including its category name."""

    id: int
    name: str
    sku: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    category_name: str
    created_date: str
    last_updated_date: str


class CreateProductDto(CamelModel):
    """Payload for creating a product."""

    name: str = Field(min_length=2, max_length=150)
    sku: str = Field(min_length=2, max_length=50)
    description: str = Field(max_length=500)
    price: float = Field(ge=0.01, le=1_000_000)
    stock_quantity: int = Field(ge=0)
    category_id: int


class UpdateProductDto(CreateProductDto):
    """Payload for replacing a product's editable fields."""


class RestockProductDto(CamelModel):
    """Payload for adding stock to a product."""

    quantity: int = Field(ge=1)
