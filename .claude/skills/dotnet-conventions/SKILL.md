---
name: dotnet-conventions
description: 'Ensure .NET/C# code meets best practices for the solution/project. Delegates CLI commands to the dotnet-cli sub-skill.'
---

# .NET/C# Best Practices

Routes build, test, and tooling requests to the appropriate sub-skill before applying code conventions.

> ⚠️ **CRITICAL**: Always validate code practices and API usage against **Microsoft Learn** using the `microsoft-learn` MCP. Do not rely on assumptions about SDK patterns, APIs, or best practices — check the official documentation.

## Sub-skill Delegate Map

| Request type                                                | Sub-skill to invoke                              |
| ----------------------------------------------------------- | ------------------------------------------------ |
| Build, test, run, publish, format, or manage NuGet packages | [`dotnet-cli`](references/dotnet-cli.md)         |
| Naming, architecture, DI, testing, logging, and code style  | [`conventions`](references/conventions.md)       |

> Always use the dotnet CLI for package management and project operations — never edit `.csproj` files directly to add or remove packages.

---

Your task is to ensure .NET/C# code in ${selection} meets the best practices specific to this solution/project. Apply the rules in [`conventions`](references/conventions.md).
