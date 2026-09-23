"""User authentication against PBKDF2 password hashes."""

import hashlib
import hmac
import logging
import sqlite3
from typing import Protocol

from app.schemas.auth import UserInfoDto

logger = logging.getLogger(__name__)


class AuthServiceProtocol(Protocol):
    """Operations for verifying user credentials."""

    def authenticate(self, email: str, password: str) -> UserInfoDto | None:
        """Return the user when the credentials match, otherwise None."""


class AuthService:
    """Verifies credentials stored in the Users table."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def authenticate(self, email: str, password: str) -> UserInfoDto | None:
        """Return the user when the credentials match, otherwise None."""
        row = self._connection.execute(
            'SELECT "Email", "DisplayName", "PasswordHash", "Role" FROM "Users" WHERE "Email" = ? COLLATE NOCASE',
            (email,),
        ).fetchone()
        if row is None or not _verify_password(password, row["PasswordHash"]):
            logger.info("Failed login for %s.", email)
            return None
        logger.info("User %s signed in.", row["Email"])
        return UserInfoDto(email=row["Email"], display_name=row["DisplayName"], role=row["Role"])


def _verify_password(password: str, stored_hash: str) -> bool:
    _, iterations, salt, expected = stored_hash.split("$")
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(iterations)).hex()
    return hmac.compare_digest(actual, expected)
