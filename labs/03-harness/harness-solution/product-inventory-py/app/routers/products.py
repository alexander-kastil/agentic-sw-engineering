"""Product endpoints: any signed-in user reads, only Admin writes."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.dependencies import get_current_user, get_product_service, require_admin
from app.schemas.product import CreateProductDto, ProductResponseDto, RestockProductDto, UpdateProductDto
from app.services.product_service import ProductService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/products", tags=["Products"], dependencies=[Depends(get_current_user)])

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.get("", response_model=list[ProductResponseDto], status_code=status.HTTP_200_OK)
def get_all_products(
    product_service: ProductServiceDep,
    category_id: Annotated[int | None, Query(alias="categoryId")] = None,
) -> list[ProductResponseDto]:
    """Return all products, optionally filtered by ?categoryId=."""
    logger.info("Retrieving all products. CategoryId filter: %s.", category_id)
    return product_service.get_all_products(category_id)


@router.get(
    "/{product_id}",
    response_model=ProductResponseDto,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Product not found"}},
)
def get_product_by_id(product_id: int, product_service: ProductServiceDep) -> ProductResponseDto:
    """Return a product by its identifier."""
    product = product_service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found.")
    return product


@router.post(
    "",
    response_model=ProductResponseDto,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
    responses={400: {"description": "Duplicate SKU or unknown category"}},
)
def create_product(dto: CreateProductDto, response: Response, product_service: ProductServiceDep) -> ProductResponseDto:
    """Create a product and point the Location header at it."""
    logger.info("Creating new product '%s'.", dto.name)
    try:
        product = product_service.create_product(dto)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    response.headers["Location"] = f"/api/products/{product.id}"
    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponseDto,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin)],
    responses={400: {"description": "Duplicate SKU or unknown category"}, 404: {"description": "Product not found"}},
)
def update_product(product_id: int, dto: UpdateProductDto, product_service: ProductServiceDep) -> ProductResponseDto:
    """Replace a product's editable fields."""
    logger.info("Updating product with ID %s.", product_id)
    try:
        product = product_service.update_product(product_id, dto)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found.")
    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
    responses={404: {"description": "Product not found"}},
)
def delete_product(product_id: int, product_service: ProductServiceDep) -> None:
    """Delete a product."""
    logger.info("Deleting product with ID %s.", product_id)
    if not product_service.delete_product(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found.")


@router.post(
    "/{product_id}/restock",
    response_model=ProductResponseDto,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin)],
    responses={404: {"description": "Product not found"}},
)
def restock(product_id: int, dto: RestockProductDto, product_service: ProductServiceDep) -> ProductResponseDto:
    """Increase a product's stock quantity."""
    logger.info("Restocking product with ID %s by %s.", product_id, dto.quantity)
    product = product_service.restock(product_id, dto.quantity)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found.")
    return product
