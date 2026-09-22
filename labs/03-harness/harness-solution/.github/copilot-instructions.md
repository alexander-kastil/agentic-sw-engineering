# Contoso Inventory API - Coding Standards

## Naming Conventions
- Use PascalCase for class names, public methods, and public properties.
- Use camelCase for local variables and method parameters.
- Prefix private fields with an underscore (e.g., _inventoryService).
- Suffix interface names with the interface prefix "I" (e.g., IInventoryService).

## Architecture Patterns
- Follow the repository pattern for all data access operations.
- Use dependency injection for all service dependencies. Register services in Program.cs.
- Separate business logic into service classes. Controllers should only handle HTTP concerns.
- Use DTOs (Data Transfer Objects) for API request and response payloads. Never expose database entities directly.

## Error Handling
- Use try-catch blocks for all external API calls and database operations.
- Return appropriate HTTP status codes (200 for success, 400 for bad requests, 404 for not found, 500 for server errors).
- Log all exceptions using ILogger<T> with structured logging.
- Include meaningful error messages in API responses.

## Documentation
- Include XML documentation comments on all public methods and classes.
- Use inline comments only for complex business logic that is not self-explanatory.

## Testing
- Write unit tests using xUnit and Moq.
- Follow the Arrange-Act-Assert pattern in test methods.
- Name test methods using the pattern: MethodName_Scenario_ExpectedResult.
