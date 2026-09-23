"""FastAPI dependency providers: database connection, services, and the signed-in user."""

import secrets
import sqlite3
from collections.abc import Iterator
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status

from app.database import open_connection
from app.schemas.auth import UserInfoDto
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.product_service import ProductService

AUTH_COOKIE = ".ContosoInventory.Auth"

_sessions: dict[str, UserInfoDto] = {}


def start_session(user: UserInfoDto) -> str:
    """Create a session for the user and return its opaque token."""
    token = secrets.token_urlsafe(32)
    _sessions[token] = user
    return token


def end_session(token: str | None) -> None:
    """Discard the session behind the token, if any."""
    if token is not None:
        _sessions.pop(token, None)


def get_connection() -> Iterator[sqlite3.Connection]:
    """Yield one SQLite connection per request."""
    connection = open_connection()
    try:
        yield connection
    finally:
        connection.close()


def get_auth_service(connection: Annotated[sqlite3.Connection, Depends(get_connection)]) -> AuthService:
    """Provide the authentication service."""
    return AuthService(connection)


def get_category_service(connection: Annotated[sqlite3.Connection, Depends(get_connection)]) -> CategoryService:
    """Provide the category service."""
    return CategoryService(connection)


def get_product_service(connection: Annotated[sqlite3.Connection, Depends(get_connection)]) -> ProductService:
    """Provide the product service."""
    return ProductService(connection)


def get_current_user(
    token: Annotated[str | None, Cookie(alias=AUTH_COOKIE)] = None,
) -> UserInfoDto:
    """Return the signed-in user, or reject the request with 401."""
    user = _sessions.get(token) if token else None
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")
    return user


def require_admin(user: Annotated[UserInfoDto, Depends(get_current_user)]) -> UserInfoDto:
    """Return the signed-in user when they hold the Admin role, otherwise reject with 403."""
    if user.role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required.")
    return user
