# Catalog Service - App Modernization

Catalog Services hast 2 main issues:

-The initial project was based on Application Insights SDK 2.23.0, which supports custom ITelemetryInitializer implementations for setting cloud role names. An attempted upgrade to SDK 3.0.0 failed because version 3.x removed the ITelemetryInitializer pattern as part of a breaking change toward OpenTelemetry. The current version remains at 2.23.0 to maintain compatibility with the FoodTelemetryInitializer.

- The initial project was based on Swashbuckle.AspNetCore for OpenAPI documentation, which was the standard pre-.NET 9 approach. It should be replaced because ASP.NET Core .NET 10 includes built-in OpenAPI support through Microsoft.AspNetCore.OpenApi, and Scalar.AspNetCore provides a more modern, lightweight UI alternative with better mobile support—making them the recommended choice for .NET 10 projects.
