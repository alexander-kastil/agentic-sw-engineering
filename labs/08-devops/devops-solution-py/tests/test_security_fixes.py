import dataclasses
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

from contoso_shop_easy.data.order_repository import OrderRepository
from contoso_shop_easy.data.product_repository import ProductRepository
from contoso_shop_easy.models.order import PaymentInfo
from contoso_shop_easy.security.security_validator import SecurityValidator
from contoso_shop_easy.services.payment_service import PaymentService
from contoso_shop_easy.services.product_service import ProductService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_process_payment_does_not_log_full_card_number_or_cvv(capsys):
    payment_service = PaymentService(OrderRepository())
    card_number = "4532015112830366"
    cvv = "987"

    assert payment_service.process_payment(card_number, "Test User", "12/30", cvv, Decimal("100")) is True

    log = capsys.readouterr().out
    assert card_number not in log
    assert cvv not in log
    assert "0366" in log


def test_validate_credit_card_does_not_log_full_card_number(capsys):
    validator = SecurityValidator()
    card_number = "4111111111111111"

    assert validator.validate_credit_card(card_number) is True

    log = capsys.readouterr().out
    assert card_number not in log
    assert "1111" in log


def test_search_products_does_not_log_simulated_sql_query(capsys):
    product_service = ProductService(ProductRepository())

    results = product_service.search_products("laptop")

    assert "SELECT * FROM Products" not in capsys.readouterr().out
    assert results


def test_search_products_sanitizes_malicious_input():
    product_service = ProductService(ProductRepository())

    assert product_service.search_products("'; DROP TABLE Products; --") == []


def test_search_products_caps_search_term_length():
    product_service = ProductService(ProductRepository())

    assert len(product_service._sanitize_search_term("x" * 500)) == ProductService.MAX_SEARCH_TERM_LENGTH


def test_payment_info_has_no_card_number_or_cvv_field():
    field_names = {f.name for f in dataclasses.fields(PaymentInfo)}

    assert "card_number" not in field_names
    assert "cvv" not in field_names
    assert {"card_last_four_digits", "card_type"} <= field_names


def test_detect_card_type():
    assert PaymentService._detect_card_type("4532015112830366") == "Visa"
    assert PaymentService._detect_card_type("5555555555554444") == "Mastercard"
    assert PaymentService._detect_card_type("378282246310005") == "American Express"
    assert PaymentService._detect_card_type("6011111111111117") == "Discover"


def test_full_demo_run_leaks_no_card_data_or_sql():
    result = subprocess.run(
        [sys.executable, "-m", "contoso_shop_easy"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    log = result.stdout

    for card_number in ("4532015112830366", "5555555555554444", "4111111111111111"):
        assert card_number not in log
    assert "CVV:" not in log
    assert "SQL Query" not in log
    assert "Total products in catalog: 40" in log
    assert "Payment completed - Card: ****0366" in log
