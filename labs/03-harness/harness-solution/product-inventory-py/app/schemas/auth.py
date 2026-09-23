"""Authentication DTOs."""

from pydantic import Field

from app.schemas import CamelModel


class LoginDto(CamelModel):
    """Credentials posted to the login endpoint."""

    email: str = Field(min_length=3, max_length=256)
    password: str = Field(min_length=1, max_length=128)


class UserInfoDto(CamelModel):
    """The signed-in user returned after login."""

    email: str
    display_name: str
    role: str
