import time
from calendar import monthrange
from datetime import datetime, timezone
from decimal import Decimal

from ..data.order_repository import OrderRepository
from ..models.order import PaymentInfo, PaymentMethod, PaymentStatus


class PaymentService:
    # Security vulnerability: Hardcoded configuration values (but won't trigger GitHub Secret Scanning)
    PAYMENT_GATEWAY_URL = "https://api.contoso-payments.com"
    MERCHANT_NAME = "ContosoShopEasy"
    GATEWAY_VERSION = "v2.1"

    def __init__(self, order_repository: OrderRepository) -> None:
        self._order_repository = order_repository

    # Payment processing method
    def process_payment(self, card_number: str, card_holder_name: str, expiry_date: str, cvv: str, amount: Decimal) -> bool:
        card_last_four_digits = self._mask_card_number(card_number)

        print(f"[DEBUG] Processing payment for card ending in {card_last_four_digits}")
        print(f"[DEBUG] Card holder: {card_holder_name}")
        print(f"[DEBUG] Amount: ${amount}")

        # Security vulnerability: Log configuration details
        print(f"[DEBUG] Using payment gateway: {self.PAYMENT_GATEWAY_URL}")
        print(f"[DEBUG] Merchant: {self.MERCHANT_NAME}")
        print(f"[DEBUG] Gateway version: {self.GATEWAY_VERSION}")

        # Simulate payment validation (vulnerable)
        if not self._validate_card_number(card_number):
            print(f"[ERROR] Invalid card number ending in {card_last_four_digits}")
            return False

        if not self._validate_expiry_date(expiry_date):
            print(f"[ERROR] Invalid or expired date: {expiry_date}")
            return False

        # Simulate payment processing
        print("[INFO] Connecting to payment gateway...")
        time.sleep(1)  # Simulate network delay

        # Security vulnerability: Generate predictable transaction IDs
        transaction_id = self._generate_transaction_id(card_number, amount)

        payment_info = PaymentInfo(
            method=PaymentMethod.CREDIT_CARD,
            card_last_four_digits=card_last_four_digits,
            card_type=self._detect_card_type(card_number),
            card_holder_name=card_holder_name,
            expiry_date=expiry_date,
            amount=amount,
            processed_date=datetime.now(timezone.utc),
            status=PaymentStatus.APPROVED,
            transaction_id=transaction_id,
        )

        print("[SUCCESS] Payment processed successfully!")
        print(f"[DEBUG] Transaction ID: {transaction_id}")

        print(f"[LOG] Payment completed - Card: ****{payment_info.card_last_four_digits}, Amount: ${amount}, Transaction: {transaction_id}")

        return True

    # Returns only the last 4 digits of the card number for safe display and logging
    @staticmethod
    def _mask_card_number(card_number: str) -> str:
        digits_only = "".join(c for c in (card_number or "") if c.isdigit())
        return digits_only[-4:]

    # Detects the card brand from the Issuer Identification Number range
    @staticmethod
    def _detect_card_type(card_number: str) -> str:
        digits_only = "".join(c for c in (card_number or "") if c.isdigit())

        if digits_only.startswith("4"):
            return "Visa"
        if len(digits_only) >= 2 and 51 <= int(digits_only[:2]) <= 55:
            return "Mastercard"
        if digits_only.startswith(("34", "37")):
            return "American Express"
        if digits_only.startswith(("6011", "65")):
            return "Discover"
        return "Unknown"

    # Vulnerable card validation
    def _validate_card_number(self, card_number: str) -> bool:
        # Security vulnerability: Weak validation - only checks length
        if not card_number:
            return False

        # Remove spaces and dashes
        card_number = card_number.replace(" ", "").replace("-", "")

        # Security vulnerability: Accept any 13-19 digit number
        return 13 <= len(card_number) <= 19 and card_number.isdigit()

    def _validate_expiry_date(self, expiry_date: str) -> bool:
        # Security vulnerability: Basic validation only
        if not expiry_date or "/" not in expiry_date:
            return False

        parts = expiry_date.split("/")
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            return False

        month, year = int(parts[0]), int(parts[1])
        if year < 100:
            year += 2000  # Convert YY to YYYY
        expiry = datetime(year, month, monthrange(year, month)[1])
        return expiry >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Security vulnerability: Predictable transaction ID generation
    def _generate_transaction_id(self, card_number: str, amount: Decimal) -> str:
        # Vulnerable: Using predictable pattern
        last_four = card_number[-4:]
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        amount_str = f"{amount:.2f}".replace(".", "")

        return f"TXN_{timestamp}_{last_four}_{amount_str}"

    def refund_payment(self, transaction_id: str, amount: Decimal) -> bool:
        # Security vulnerability: Log refund details
        print(f"[DEBUG] Processing refund for transaction: {transaction_id}, Amount: ${amount}")
        print(f"[DEBUG] Using payment gateway: {self.PAYMENT_GATEWAY_URL}")

        # Simulate refund processing
        print("[INFO] Processing refund...")
        time.sleep(0.5)

        print(f"[SUCCESS] Refund processed for transaction: {transaction_id}")
        return True

    # Method to get payment history - with security issues
    def get_payment_history(self, user_id: int) -> list[PaymentInfo]:
        print(f"[DEBUG] Retrieving payment history for user: {user_id}")

        # In a real app, this would query the database
        # For demo purposes, we'll return an empty list
        return []
