---
description: This file describes the .NET coding conventions for the project.
---

Use `PascalCase` for all public class, method, and property names and `camelCase` for private fields and local variables.

Use .NET primary constructors with no private backing fields unless additional logic is required. Migrate existing classes to primary constructors where feasible.

Use the dotnet cli for package management and project operations.

When starting the application, always check if there is an instance already running to prevent multiple instances. If it is running with dotnet watch run, try to reuse that instance instead of starting a new one. Other wise start a new instance.
