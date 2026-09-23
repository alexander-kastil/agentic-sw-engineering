"""Login and logout endpoints backed by an HttpOnly session cookie."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from app.dependencies import AUTH_COOKIE, end_session, get_auth_service, get_current_user, start_session
from app.schemas.auth import LoginDto, UserInfoDto
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=UserInfoDto, status_code=status.HTTP_200_OK)
def login(
    dto: LoginDto,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserInfoDto:
    """Sign in and set the session cookie."""
    user = auth_service.authenticate(dto.email, dto.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    response.set_cookie(
        AUTH_COOKIE, start_session(user), httponly=True, samesite="strict", max_age=30 * 60
    )
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    token: Annotated[str | None, Cookie(alias=AUTH_COOKIE)] = None,
) -> None:
    """Sign out and clear the session cookie."""
    end_session(token)
    response.delete_cookie(AUTH_COOKIE)


@router.get("/me", response_model=UserInfoDto, status_code=status.HTTP_200_OK)
def me(user: Annotated[UserInfoDto, Depends(get_current_user)]) -> UserInfoDto:
    """Return the signed-in user."""
    return user
