---
name: 'Service Layer Standards'
description: 'Coding standards for business logic service classes'
applyTo: '**/services/**/*.py'
---
# Service Layer Standards

- Define a typing.Protocol for every service class (e.g., ProductServiceProtocol for ProductService).
- Receive the database connection through the constructor.
- Accept and return Pydantic DTOs, not database rows.
- Include input validation at the start of each public method.
- Raise specific exception types (ValueError, LookupError) rather than a bare Exception.
- Use parameterized SQL queries only; never format values into a SQL string.
- Log significant operations with logging.getLogger(__name__) and %-style parameters.
