## When to use

Naming a type/member, structuring files and namespaces, choosing an architecture/design pattern, or
applying SOLID/code-quality rules. The neighbouring concerns have their own reference files:
[`di-and-lifetimes`](di-and-lifetimes.md), [`async-patterns`](async-patterns.md),
[`configuration-and-logging`](configuration-and-logging.md),
[`json-casing-contract`](json-casing-contract.md) and
[`app-lifecycle-and-watch`](app-lifecycle-and-watch.md).

## Naming Conventions

- Use `PascalCase` for all public classes, methods, and properties
- Use `camelCase` for private fields and local variables

## Documentation & Structure

- Create comprehensive XML documentation comments for all public classes, interfaces, methods, and properties
- Include parameter descriptions and return value descriptions in XML comments
- Follow the established namespace structure: {Core|Console|App|Service}.{Feature}

## Design Patterns & Architecture

- Use .NET primary constructors with no private backing fields unless additional logic is required; migrate existing classes to primary constructors where feasible
- Use primary constructor syntax for dependency injection (e.g., `public class MyClass(IDependency dependency)`)
- Implement the Command Handler pattern with generic base classes (e.g., `CommandHandler<TOptions>`)
- Use interface segregation with clear naming conventions (prefix interfaces with 'I')
- Follow the Factory pattern for complex object creation.

See [`di-and-lifetimes`](di-and-lifetimes.md) for the full primary-constructor, dependency-injection,
service-lifetime and disposal conventions.

## Resource Management & Localization

- Use ResourceManager for localized messages and error strings
- Separate LogMessages and ErrorMessages resource files
- Access resources via `_resourceManager.GetString("MessageKey")`

## Testing Standards

- Use xUnit with FluentAssertions for assertions and NSubstitute for mocking, or the project's chosen equivalents
- Follow AAA pattern (Arrange, Act, Assert)
- Test both success and failure scenarios
- Include null parameter validation tests

See [`dotnet-testing`](dotnet-testing.md) for the full xUnit / FluentAssertions / NSubstitute reference.

## Performance & Security

- Use C# 14 features and .NET 10 optimizations where applicable
- Implement proper input validation and sanitization
- Use parameterized queries for database operations
- Follow secure coding practices for AI/ML operations

## Code Quality (SOLID)

- Ensure SOLID principles compliance
- Avoid code duplication through base classes and utilities
- Use meaningful names that reflect domain concepts
- Keep methods focused and cohesive
- Implement proper disposal patterns (`IDisposable` / `IAsyncDisposable`) for all resources

## Classify domain rows by a discriminator, never by a numeric range

A chart of accounts grew a block of private accounts that must stay out of every business
calculation. The correct exclusion is an explicit discriminator: an enum member (`Type = Privat`)
that no business query references, so the new rows are invisible to those queries by construction
rather than by a filter somebody has to remember to add. Every consumer (saldo engines, VAT and
declaration builders, the NL query layer) already narrowed on the type, so nothing downstream needed
touching.

The number range is belt and braces on top of it, and this is where it goes wrong. The guard was
first written as an open-ended predicate:

```csharp
if (account.Number >= 9500) { /* must be Privat */ }
```

That is false for every row that sits above the intended band for unrelated reasons: 10000 asset
purchases, 10001/10002 tax-office accounts, 10010+ special expenses. An unbounded comparison silently
reclassified all of them. Bound the band on both ends and enforce it once, at the write boundary
(the controller's `Post`/`Put`), never scattered across readers:

```csharp
if (account.Number is >= 9500 and <= 9999) { /* must be Privat, and Kennzahl must be null */ }
```

Two rules fall out, and they generalise past accounting to any status/tier/category band:

- **The discriminator is the semantics; the range is a sanity check.** If removing the range guard
  changes a calculated result, the classification was leaking through the number and the consumers
  are filtering on the wrong thing.
- **Any range predicate needs both ends.** `>= N` asserts something about every value that will ever
  exist above `N`, including the ones added next year. Write the closed interval, and check what
  already lives above the upper bound before choosing it.
