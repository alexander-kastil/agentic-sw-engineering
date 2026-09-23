# Contoso Inventory API - Coding Standards

## Naming Conventions
- Use PascalCase for class names (e.g., ProductService, CreateProductDto).
- Use snake_case for functions, methods, variables, and module names.
- Prefix private attributes and helper functions with an underscore (e.g., _connection).
- Use UPPER_SNAKE_CASE for module-level constants.

## Architecture Patterns
- Follow the repository pattern for all data access operations. SQL lives in service classes, never in routers.
- Use FastAPI dependency injection (Depends) for all service dependencies. Wire providers in app/dependencies.py.
- Separate business logic into service classes. Routers should only handle HTTP concerns.
- Use Pydantic models (DTOs) for API request and response payloads. Never return raw database rows.

## Error Handling
- Raise specific exceptions (ValueError, LookupError) from services; translate them to HTTPException in routers.
- Return appropriate HTTP status codes (200 for success, 201 for created, 400 for bad requests, 404 for not found, 500 for server errors).
- Log significant operations with the logging module using %-style parameters, never f-strings.
- Include meaningful error messages in API responses.

## Documentation
- Include docstrings on all public modules, classes, and functions.
- Use type hints on every function signature.

## Database
- Every schema or data change ships as a hand-written SQL delta script in db/deltas/.
- Never use Alembic or any other migration generator.

## Testing
- Write unit tests using pytest and FastAPI's TestClient.
- Follow the Arrange-Act-Assert pattern in test functions.
- Name test functions using the pattern: test_function_scenario_expected_result.
