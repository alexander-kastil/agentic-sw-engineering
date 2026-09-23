from datetime import datetime


class SecurityValidator:
    # Security vulnerability: Hardcoded admin credentials (simplified to avoid GitHub Secret Scanning)
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "password123"
    SESSION_PREFIX = "session"

    def __init__(self) -> None:
        print("[DEBUG] SecurityValidator initialized")
        print(f"[DEBUG] Admin credentials: {self.ADMIN_USERNAME}/{self.ADMIN_PASSWORD}")

    # Vulnerable input validation - accepts dangerous characters
    def validate_input(self, value: str, field_name: str) -> bool:
        if not value:
            print(f"[WARNING] Empty input for {field_name}")
            return False

        # Security vulnerability: Log sensitive input data
        print(f"[DEBUG] Validating {field_name}: '{value}'")

        # Security vulnerability: No proper sanitization for SQL injection
        if "'" in value or '"' in value or ";" in value:
            print(f"[WARNING] Potentially dangerous characters detected in {field_name}: {value}")
            # But still return True - vulnerability!

        # Security vulnerability: Accept script tags and other dangerous content
        if "<script>" in value or "javascript:" in value:
            print(f"[WARNING] Script content detected in {field_name}: {value}")
            # But still return True - vulnerability!

        return True  # Always returns True - major vulnerability

    # Vulnerable email validation
    def validate_email(self, email: str) -> bool:
        if not email:
            return False

        # Security vulnerability: Log email addresses
        print(f"[DEBUG] Validating email: {email}")

        # Security vulnerability: Weak email validation
        return "@" in email and "." in email

    # Vulnerable password strength check
    def validate_password_strength(self, password: str) -> bool:
        if not password:
            return False

        # Security vulnerability: Log password in plaintext
        print(f"[DEBUG] Checking password strength: {password}")

        # Security vulnerability: Very weak password requirements
        if len(password) < 4:
            print("[WARNING] Password too short (minimum 4 characters)")
            return False

        # Security vulnerability: No complexity requirements
        print("[INFO] Password meets minimum requirements")
        return True

    # Credit card validation with masked logging
    def validate_credit_card(self, card_number: str) -> bool:
        if not card_number:
            return False

        print(f"[DEBUG] Validating credit card ending in {self._mask_card_number(card_number)}")

        # Remove spaces and dashes
        card_number = card_number.replace(" ", "").replace("-", "")

        # Security vulnerability: Accept any numeric string of reasonable length
        if 13 <= len(card_number) <= 19 and card_number.isdigit():
            print("[INFO] Credit card format appears valid")
            return True

        print("[WARNING] Invalid credit card format")
        return False

    # Returns only the last 4 digits of the card number for safe logging
    @staticmethod
    def _mask_card_number(card_number: str) -> str:
        digits_only = "".join(c for c in card_number if c.isdigit())
        return digits_only[-4:]

    # Security vulnerability: Predictable token generation (simplified)
    def generate_session_token(self, username: str) -> str:
        # Security vulnerability: Log token generation
        print(f"[DEBUG] Generating session token for user: {username}")

        # Security vulnerability: Predictable token based on username and timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        token = f"{self.SESSION_PREFIX}_{username}_{timestamp}"

        # Security vulnerability: Log the generated token
        print(f"[DEBUG] Generated token: {token}")

        return token

    # Method to check if user is admin (vulnerable)
    def is_admin_user(self, username: str, password: str) -> bool:
        # Security vulnerability: Log admin login attempts
        print(f"[DEBUG] Admin login attempt - Username: {username}, Password: {password}")

        # Security vulnerability: Hardcoded credentials comparison
        is_admin = username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD

        if is_admin:
            print("[INFO] Admin login successful")
        else:
            print("[WARNING] Admin login failed")

        return is_admin

    # Vulnerable sanitization method
    def sanitize_input(self, value: str) -> str:
        if not value:
            return ""

        # Security vulnerability: Log original input
        print(f"[DEBUG] Sanitizing input: '{value}'")

        # Security vulnerability: Incomplete sanitization
        sanitized = value.replace("<script>", "").replace("</script>", "")

        # Security vulnerability: Log sanitized input
        print(f"[DEBUG] Sanitized result: '{sanitized}'")

        return sanitized

    # Method to display known security vulnerabilities (for educational purposes)
    def display_known_vulnerabilities(self) -> None:
        print("=== Known Security Vulnerabilities ===")

        # Security vulnerability: Display sensitive configuration (but avoid secret scanning triggers)
        print(f"Admin Username: {self.ADMIN_USERNAME}")
        print(f"Admin Password: {self.ADMIN_PASSWORD}")
        print(f"Session Token Prefix: {self.SESSION_PREFIX}")

        print("Input validation: ENABLED (but vulnerable)")
        print("Password encryption: MD5 (WEAK)")
        print("Credit card storage: LAST 4 DIGITS ONLY, NO CVV (SECURE)")
        print("Logging level: DEBUG (EXPOSES SENSITIVE DATA)")
        print("SQL injection protection: ENABLED (search input sanitized)")
        print("XSS protection: MINIMAL")

        print("=== End Vulnerability List ===")

    # Vulnerable method to validate file uploads
    def validate_file_upload(self, filename: str, file_content: bytes) -> bool:
        # Security vulnerability: Log filename and file size
        print(f"[DEBUG] Validating file upload: {filename}, Size: {len(file_content)} bytes")

        # Security vulnerability: No proper file type validation
        if filename.endswith(".exe") or filename.endswith(".bat"):
            print("[WARNING] Potentially dangerous file type detected")
            # But still return True - vulnerability!

        # Security vulnerability: No file size limits
        print("[INFO] File upload validation passed")
        return True
