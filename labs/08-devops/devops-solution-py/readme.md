# Lab 08 devops solution (Python)

Refactored source for the two issues assigned in `labs/08-devops/readme-py.md`, applied to the Python ContosoShopEasy console app from `labs/08-devops/contososhopeasy-py/`. The folder is the full application after the fixes, so it runs on its own. `tests/` is a pytest suite that proves the fixes hold, since the guide's own testing step (read the console output) does not assert anything.

## Files and the issue each one resolves

- `contoso_shop_easy/models/order.py`: **Fix Credit Card Data Storage Violations**. `PaymentInfo` no longer has `card_number` or `cvv`. Replaced with `card_last_four_digits` and `card_type`.
- `contoso_shop_easy/services/payment_service.py`: **Fix Credit Card Data Storage Violations**. `process_payment` no longer logs the full card number or CVV, stores only the last four digits and detected card type on `PaymentInfo`, and masks the card number in every remaining log line. Added `_mask_card_number` and `_detect_card_type`.
- `contoso_shop_easy/security/security_validator.py`: **Fix Credit Card Data Storage Violations** and **Fix SQL Injection Vulnerability in Product Search**. `validate_credit_card` logs only the last four digits. `display_known_vulnerabilities` reports credit card storage as secure and SQL injection protection as enabled.
- `contoso_shop_easy/services/product_service.py`: **Fix SQL Injection Vulnerability in Product Search**. `search_products` no longer builds or logs the simulated SQL query string. Added `_sanitize_search_term`, which trims the term, caps it at 100 characters, and strips `' " ; < > -` before the term reaches `ProductRepository`.
- `tests/test_security_fixes.py`: new pytest suite that captures console output and asserts the vulnerabilities are gone.

`data/order_repository.py` needed no changes: it persists whatever is on `PaymentInfo`, so once `PaymentInfo` stopped carrying the full card number and CVV, the repository stopped persisting them too.

## Run

```bash
python -m contoso_shop_easy
python -m pip install pytest
python -m pytest
```

See `test-results.md` for every command run and its output.
