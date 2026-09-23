"""Read-only category endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_category_service, get_current_user
from app.schemas.category import CategoryResponseDto
from app.services.category_service import CategoryService

router = APIRouter(prefix="/api/categories", tags=["Categories"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[CategoryResponseDto], status_code=status.HTTP_200_OK)
def get_all_categories(
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> list[CategoryResponseDto]:
    """Return every category."""
    return category_service.get_all_categories()
