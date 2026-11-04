import hashlib
from datetime import datetime, timezone

from ..data.user_repository import UserRepository
from ..models.user import User, UserRole


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    # Vulnerable registration method - multiple security issues
    def register_user(self, username: str, email: str, password: str, first_name: str, last_name: str) -> bool:
        # Security vulnerability: Log sensitive information
        print(f"[DEBUG] Registering user: {username}, Email: {email}, Password: {password}")

        # Check if user already exists
        if self._user_repository.get_user_by_username(username) is not None:
            print(f"User {username} already exists!")
            return False

        if self._user_repository.get_user_by_email(email) is not None:
            print(f"Email {email} is already registered!")
            return False

        # Security vulnerability: Use weak MD5 hashing
        password_hash = self._get_md5_hash(password)

        user = User(
            id=self._user_repository.get_next_user_id(),
            username=username,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=UserRole.CUSTOMER,
            is_active=True,
            is_email_verified=False,
        )

        self._user_repository.add_user(user)

        # Security vulnerability: Log password hash
        print(f"[DEBUG] User created with password hash (MD5): {password_hash}")

        return True

    # Vulnerable login method
    def login_user(self, username: str, password: str) -> User | None:
        # Security vulnerability: Log password in plaintext
        print(f"[DEBUG] Login attempt for user: {username} with password: {password}")

        user = self._user_repository.get_user_by_username(username)
        if user is None:
            print(f"User {username} not found!")
            return None

        password_hash = self._get_md5_hash(password)
        if user.password_hash == password_hash:
            user.last_login_date = datetime.now(timezone.utc)
            print(f"Login successful for user: {username}")
            return user

        print(f"Invalid password for user: {username}")
        return None

    # Method to validate user input - but with vulnerabilities
    def validate_user_input(self, value: str, field_name: str) -> bool:
        # Security vulnerability: No proper input validation
        if not value:
            print(f"[WARNING] Empty input for field: {field_name}")
            return False

        # Security vulnerability: Accept potentially dangerous characters
        print(f"[DEBUG] Validating {field_name}: {value}")
        return True

    def get_user(self, user_id: int) -> User | None:
        return self._user_repository.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return self._user_repository.get_user_by_username(username)

    def get_user_by_email(self, email: str) -> User | None:
        return self._user_repository.get_user_by_email(email)

    def update_user(self, user: User) -> bool:
        return self._user_repository.update_user(user)

    def delete_user(self, user_id: int) -> bool:
        return self._user_repository.delete_user(user_id)

    def get_all_users(self) -> list[User]:
        return self._user_repository.get_all_users()

    # Vulnerable method - uses weak MD5 hashing
    def _get_md5_hash(self, value: str) -> str:
        return hashlib.md5(value.encode("utf-8")).hexdigest().upper()
