# Catalog Service - App Modernization

Catalog Services hast 2 main issues:

-The initial project was based on Application Insights SDK 2.23.0, which supports custom ITelemetryInitializer implementations for setting cloud role names. An attempted upgrade to SDK 3.0.0 failed because version 3.x removed the ITelemetryInitializer pattern as part of a breaking change toward OpenTelemetry. The current version remains at 2.23.0 to maintain compatibility with the FoodTelemetryInitializer.

- The initial project was based on Swashbuckle.AspNetCore for OpenAPI documentation, which was the standard pre-.NET 9 approach. It should be replaced because ASP.NET Core .NET 10 includes built-in OpenAPI support through Microsoft.AspNetCore.OpenApi, and Scalar.AspNetCore provides a more modern, lightweight UI alternative with better mobile support—making them the recommended choice for .NET 10 projects.

## Configuration Before Running

`appsettings.json` ships without credentials. The service runs as is: `App:UseSQLite` is `true` and telemetry is off while the Application Insights connection string is empty. Supply the two values below before running against Azure SQL or Application Insights, and keep them out of `appsettings.json`.

Run from the folder that holds `catalog-service.csproj`:

```bash
dotnet user-secrets init
dotnet user-secrets set "ApplicationInsights:ConnectionString" "InstrumentationKey=<your-key>;IngestionEndpoint=<your-ingestion-endpoint>"
dotnet user-secrets set "App:ConnectionStrings:SQLServerConnection" "Server=tcp:<your-sql-server>.database.windows.net,1433;Initial Catalog=<your-database>;User ID=<your-sql-user>;Password=<your-sql-password>;Encrypt=True;"
```

In Docker or CI, pass the same two keys as environment variables instead:

```bash
ApplicationInsights__ConnectionString
App__ConnectionStrings__SQLServerConnection
```
