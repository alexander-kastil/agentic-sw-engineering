from decimal import Decimal

from .data.order_repository import OrderRepository
from .data.product_repository import ProductRepository
from .data.user_repository import UserRepository
from .models.order import OrderItem, OrderStatus
from .security.security_validator import SecurityValidator
from .services.order_service import OrderService
from .services.payment_service import PaymentService
from .services.product_service import ProductService
from .services.user_service import UserService

# Dependency injection setup (manual for simplicity in this educational project)
product_repository = ProductRepository()
user_repository = UserRepository()
order_repository = OrderRepository()

product_service = ProductService(product_repository)
user_service = UserService(user_repository)
payment_service = PaymentService(order_repository)
order_service = OrderService(order_repository, product_service, user_service)
security_validator = SecurityValidator()


def main() -> None:
    print("=== Welcome to ContosoShopEasy E-Commerce Platform ===")
    print("This application demonstrates an e-commerce system with")
    print("intentional security vulnerabilities for educational purposes.")
    print()

    # Display known vulnerabilities first (for educational purposes)
    security_validator.display_known_vulnerabilities()
    print()

    # Demonstrate the e-commerce workflow
    demonstrate_ecommerce_workflow()

    print()
    print("=== End of ContosoShopEasy Demo ===")
    print("Application completed successfully!")
    print(f"Total products in catalog: {len(product_service.get_all_products())}")
    print(f"Total registered users: {len(user_service.get_all_users())}")
    print(f"Total revenue: ${order_service.get_total_revenue():.2f}")


def demonstrate_ecommerce_workflow() -> None:
    print("=== E-Commerce Workflow Demonstration ===")

    print("\n1. PRODUCT SEARCH AND BROWSING")
    print("Searching for products...")
    demonstrate_product_search()

    print("\n2. USER REGISTRATION")
    print("Registering new users...")
    demonstrate_user_registration()

    print("\n3. USER LOGIN")
    print("Demonstrating user login...")
    demonstrate_user_login()

    print("\n4. SHOPPING CART & ORDER CREATION")
    print("Creating sample orders...")
    demonstrate_order_creation()

    print("\n5. PAYMENT PROCESSING")
    print("Processing payments...")
    demonstrate_payment_processing()

    print("\n6. ORDER MANAGEMENT")
    print("Managing order statuses...")
    demonstrate_order_management()


def demonstrate_product_search() -> None:
    # Vulnerable search - demonstrates SQL injection risk
    search_terms = ["laptop", "phone", "'; DROP TABLE Products; --", "headphones"]

    for search_term in search_terms:
        print(f"Searching for: '{search_term}'")
        results = product_service.search_products(search_term)
        print(f"Found {len(results)} products")

        if results and "DROP" not in search_term:
            first = results[0]
            print(f"  -> {first.name} - ${first.price} ({first.brand})")
        print()

    print("Featured Products:")
    for product in product_service.get_featured_products(3):
        print(f"  -> {product.name} - ${product.price} (Rating: {product.rating}/5.0)")


def demonstrate_user_registration() -> None:
    # Register new users with various security issues
    new_users = [
        ("testuser1", "test1@email.com", "weak", "Test", "User1"),
        ("admin'; DROP TABLE Users; --", "hacker@evil.com", "password123", "Hacker", "McHackface"),
        ("normaluser", "normal@email.com", "mypassword", "Normal", "Person"),
    ]

    for username, email, password, first_name, last_name in new_users:
        print(f"Registering user: {username}")

        # Vulnerable validation
        is_valid_input = security_validator.validate_input(username, "Username")
        is_valid_email = security_validator.validate_email(email)
        is_valid_password = security_validator.validate_password_strength(password)

        if is_valid_input and is_valid_email and is_valid_password:
            success = user_service.register_user(username, email, password, first_name, last_name)
            print("Registration successful!" if success else "Registration failed!")
        print()


def demonstrate_user_login() -> None:
    # Demonstrate login attempts (including admin backdoor)
    login_attempts = [
        ("diego_siciliani", "hello"),
        ("admin", "password"),
        ("testuser1", "weak"),
        ("nonexistent", "whatever"),
    ]

    for username, password in login_attempts:
        print(f"Login attempt: {username}")

        # Check if admin user (vulnerable hardcoded check)
        if security_validator.is_admin_user(username, password):
            print("ADMIN ACCESS GRANTED!")
        else:
            user = user_service.login_user(username, password)
            if user is not None:
                session_token = security_validator.generate_session_token(user.username)
                print(f"Login successful! Session token: {session_token}")
            else:
                print("Login failed!")
        print()


def demonstrate_order_creation() -> None:
    user = user_service.get_user_by_username("diego_siciliani")
    if user is None:
        return

    print(f"Creating order for user: {user.username}")

    order_items = [
        OrderItem(product_id=1, quantity=1),
        OrderItem(product_id=9, quantity=1),
    ]

    order = order_service.create_order(user.id, order_items)
    print(f"Order created: {order.order_number}")
    print(f"Order total: ${order.total_amount:.2f}")
    print(f"Items in order: {len(order.order_items)}")

    for item in order.order_items:
        print(f"  -> {item.product.name if item.product else ''} x{item.quantity} = ${item.total_price:.2f}")


def demonstrate_payment_processing() -> None:
    # Process payments with various security vulnerabilities
    payment_data = [
        ("4532015112830366", "Diego Siciliani", "12/26", "123", Decimal("2949.98")),
        ("5555555555554444", "Henrietta Mueller", "08/25", "456", Decimal("399.99")),
        ("4111111111111111", "Test User", "01/24", "789", Decimal("199.99")),
    ]

    for card_number, card_holder, expiry, cvv, amount in payment_data:
        print(f"Processing payment for {card_holder}")

        # Vulnerable credit card validation
        is_valid_card = security_validator.validate_credit_card(card_number)

        if is_valid_card:
            success = payment_service.process_payment(card_number, card_holder, expiry, cvv, amount)
            print("Payment successful!" if success else "Payment failed!")
        else:
            print("Invalid credit card format!")
        print()


def demonstrate_order_management() -> None:
    print("Recent Orders:")
    for order in order_repository.get_recent_orders(3):
        print(f"Order {order.order_number}: {order.status.name.title()} - ${order.total_amount:.2f}")

        if order.status == OrderStatus.PROCESSING:
            print(f"  -> Updating order {order.order_number} to Shipped")
            order_service.update_order_status(order.id, OrderStatus.SHIPPED)

    print("\nOrder Statistics:")
    for status, count in order_repository.get_order_status_counts().items():
        print(f"  {status.name.title()}: {count} orders")

    print(f"Total Revenue: ${order_service.get_total_revenue():.2f}")


if __name__ == "__main__":
    main()
