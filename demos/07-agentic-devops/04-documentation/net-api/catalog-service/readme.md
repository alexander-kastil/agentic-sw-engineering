# Catalog Service

| .NET Api Services         | Http Port | Https Port | Dapr Port | Dapr App ID          | Docker Port|
| -------                   | --------- | ---------- | --------- | -------------        | -----      |
| Catalog Service           | 5001      | 5021       | 5011      | catalog-service      | 5051       |

- Docker Build & Run:

    The dockerfile copies both `catalog-service/` and `food-app-common/`, so the build context is the `net-api` folder one level up, not this folder.

    ```bash
    cd ..
    docker build --rm -f catalog-service/dockerfile -t catalog-service .
    docker run -it --rm -p 5051:8080 catalog-service
    ```

    The runtime image is `aspnet:8.0-jammy-chiseled`, which listens on 8080, so map the host port onto 8080 rather than onto 80.

- Environment Variables:
    - ApplicationInsights__ConnectionString
    - App__UseSQLite
    - App__ConnectionStrings__SQLServerConnection

- Rest Tester:

    ```http
    GET http://localhost:5001/food HTTP/1.1

    ###

    POST http://localhost:5001/food HTTP/1.1
    Content-Type: application/json

    {
        "name": "Schnitzel",
        "price": 12.9
    }
    ```

- Dapr Run & Test:

    ```bash
    dapr run --app-id catalog-service --app-port 5001 --dapr-http-port 5011 --resources-path ./components -- dotnet run
    ```

    ```bash
    dapr invoke --app-id catalog-service --method food --verb GET
    ```

    ```bash
    dapr publish --publish-app-id catalog-service --pubsub food-pubsub --topic catalog-requests --data '{"name": "Schnitzel", "price": 12.9}'
    ```
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
