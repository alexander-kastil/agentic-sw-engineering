# ContosoShopEasy E-Commerce Platform (Python)

ContosoShopEasy is a console e-commerce simulation for a GitHub Copilot training course. It contains intentional security vulnerabilities and runs a complete shopping workflow that exposes them through debug output. Never use it in production.

## Architecture

- `contoso_shop_easy/models/`: `product.py`, `user.py`, `order.py`, `category.py`
- `contoso_shop_easy/services/`: `product_service.py`, `user_service.py`, `payment_service.py`, `order_service.py`
- `contoso_shop_easy/data/`: `product_repository.py`, `user_repository.py`, `order_repository.py` (in-memory stores)
- `contoso_shop_easy/security/`: `security_validator.py` (input validation and security checks, intentionally vulnerable)
- `contoso_shop_easy/__main__.py`: entry point that wires the services together and runs the demo workflow
- `.github/workflows/create-training-issues.yml`: creates the 10 security issues for the lab

## Intentional security vulnerabilities

1. SQL injection: product search builds and logs a raw SQL string from user input.
2. Weak password security: MD5 hashing, a 4-character minimum, plaintext password logging.
3. Sensitive data exposure: full card numbers and CVV codes stored and logged.
4. Hardcoded credentials: admin username and password in `SecurityValidator`.
5. Input validation issues: dangerous characters detected but accepted, weak email validation.
6. Information disclosure: verbose debug output and a printed security configuration.

## Sample data

- `diego_siciliani` (password `hello`), customer
- `henrietta_mueller` (password `test`), customer
- `admin` (password `password`), admin
- `lee_gu` (password `123456`), customer
- `pradeep_gupta` (password `123456`), employee

## Run the application

Requires Python 3.11 or later and no third-party packages. From the repository root:

```bash
python -m contoso_shop_easy
```

The run ends with 40 products in the catalog, 8 registered users (5 seeded plus 3 registered by the demo) and the total revenue across all orders.
