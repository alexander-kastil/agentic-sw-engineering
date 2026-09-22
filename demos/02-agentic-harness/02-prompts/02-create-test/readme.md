# Create Unit Tests with XUnit

This demo uses the [csharp-xunit.prompt.md](/.github/prompts/csharp-xunit.prompt.md) prompt file to generate comprehensive unit tests for the copilot-api project. Prompt files encapsulate testing best practices, making it easy to create consistent, high-quality test suites without manually referencing documentation.

## What You'll Learn

The demo covers creating XUnit tests that follow proven patterns for C# projects. You'll see how to structure test classes, use data-driven tests with [Theory], mock dependencies with Moq, and organize tests for maintainability. The prompt file guides Copilot to generate tests that cover both happy paths and edge cases, ensuring robust validation of your API controllers and models.

## Key Technical Patterns

The generated tests demonstrate proper use of XUnit fixtures for shared context, the Arrange-Act-Assert pattern for clarity, and parameterized tests using InlineData for testing multiple scenarios. By referencing the prompt file, you avoid context switching between your IDE and external documentation, keeping the testing workflow fast and consistent.
