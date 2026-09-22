---
name: 'Service Layer Standards'
description: 'Coding standards for business logic service classes'
applyTo: '**/Services/**/*.cs'
---
# Service Layer Standards

- Define a corresponding interface for every service class (e.g., IProductService for ProductService).
- Use async/await for all I/O-bound operations (database calls, HTTP requests, file I/O).
- Accept and return DTOs, not database entities.
- Include comprehensive input validation at the start of each public method.
- Throw specific exception types (ArgumentException, InvalidOperationException) rather than generic Exception.
- Log significant operations using ILogger<T> with structured logging parameters.
