from datetime import datetime, timedelta, timezone

from ..models.user import Address, User, UserRole


class UserRepository:
    def __init__(self) -> None:
        now = datetime.now(timezone.utc)
        # Pre-populate with some test users (with weak password hashes for demo)
        self._users = [
            User(1, "diego_siciliani", "diego.siciliani@email.com", "5D41402ABC4B2A76B9719D911017C592", "Diego", "Siciliani",  # MD5 hash of "hello"
                 phone_number="555-0123", date_of_birth=datetime(1990, 5, 15), role=UserRole.CUSTOMER,
                 is_email_verified=True, last_login_date=now - timedelta(days=2),
                 shipping_address=Address("123 Main St", "Anytown", "CA", "12345", "USA"),
                 billing_address=Address("123 Main St", "Anytown", "CA", "12345", "USA")),
            User(2, "henrietta_mueller", "henrietta.mueller@email.com", "098F6BCD4621D373CADE4E832627B4F6", "Henrietta", "Mueller",  # MD5 hash of "test"
                 phone_number="555-0456", date_of_birth=datetime(1985, 8, 22), role=UserRole.CUSTOMER,
                 is_email_verified=True, last_login_date=now - timedelta(hours=6),
                 shipping_address=Address("456 Oak Ave", "Springfield", "TX", "67890", "USA"),
                 billing_address=Address("456 Oak Ave", "Springfield", "TX", "67890", "USA")),
            User(3, "admin", "admin@contoso.com", "5E884898DA28047151D0E56F8DC6292773603D0D6AABBDD62A11EF721D1542D8", "Admin", "User",  # MD5 hash of "password"
                 phone_number="555-0001", date_of_birth=datetime(1980, 1, 1), role=UserRole.ADMIN,
                 is_email_verified=True, last_login_date=now - timedelta(minutes=30),
                 shipping_address=Address("789 Corporate Blvd", "Business City", "NY", "10001", "USA"),
                 billing_address=Address("789 Corporate Blvd", "Business City", "NY", "10001", "USA")),
            User(4, "lee_gu", "lee.gu@email.com", "25D55AD283AA400AF464C76D713C07AD", "Lee", "Gu",  # MD5 hash of "123456"
                 phone_number="555-0789", date_of_birth=datetime(1992, 12, 3), role=UserRole.CUSTOMER,
                 is_email_verified=False, last_login_date=now - timedelta(days=10),
                 shipping_address=Address("321 Pine St", "Riverside", "FL", "33101", "USA"),
                 billing_address=Address("321 Pine St", "Riverside", "FL", "33101", "USA")),
            User(5, "pradeep_gupta", "pradeep.gupta@email.com", "E10ADC3949BA59ABBE56E057F20F883E", "Pradeep", "Gupta",  # MD5 hash of "123456"
                 phone_number="555-0321", date_of_birth=datetime(1988, 7, 18), role=UserRole.EMPLOYEE,
                 is_email_verified=True, last_login_date=now - timedelta(days=1),
                 shipping_address=Address("654 Elm Dr", "Hometown", "WA", "98001", "USA"),
                 billing_address=Address("654 Elm Dr", "Hometown", "WA", "98001", "USA")),
        ]
        self._next_user_id = len(self._users) + 1

    def get_all_users(self) -> list[User]:
        return list(self._users)

    def get_user_by_id(self, user_id: int) -> User | None:
        return next((u for u in self._users if u.id == user_id and u.is_active), None)

    def get_user_by_username(self, username: str) -> User | None:
        if not username:
            return None
        return next((u for u in self._users if u.username.lower() == username.lower() and u.is_active), None)

    def get_user_by_email(self, email: str) -> User | None:
        if not email:
            return None
        return next((u for u in self._users if u.email.lower() == email.lower() and u.is_active), None)

    def add_user(self, user: User) -> None:
        user.id = self._next_user_id
        self._next_user_id += 1
        user.created_date = datetime.now(timezone.utc)
        self._users.append(user)

    def update_user(self, user: User) -> bool:
        existing = self.get_user_by_id(user.id)
        if existing is None:
            return False
        self._users[self._users.index(existing)] = user
        return True

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user is None:
            return False
        user.is_active = False
        return True

    def get_users_by_role(self, role: UserRole) -> list[User]:
        return [u for u in self._users if u.role == role and u.is_active]

    def search_users(self, search_term: str) -> list[User]:
        if not search_term:
            return []
        search_term = search_term.lower()
        return [
            u for u in self._users
            if u.is_active and (
                search_term in u.username.lower()
                or search_term in u.email.lower()
                or search_term in u.first_name.lower()
                or search_term in u.last_name.lower()
            )
        ]

    def get_next_user_id(self) -> int:
        return self._next_user_id

    def is_username_available(self, username: str) -> bool:
        return self.get_user_by_username(username) is None

    def is_email_available(self, email: str) -> bool:
        return self.get_user_by_email(email) is None

    # Security vulnerability: Method to get user passwords (should never exist)
    def get_user_password(self, username: str) -> str:
        user = self.get_user_by_username(username)
        return user.password_hash if user else ""

    # Security vulnerability: Method to get all user credentials
    def get_all_user_credentials(self) -> dict[str, str]:
        return {u.username: u.password_hash for u in self._users if u.is_active}
