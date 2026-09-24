using System.ComponentModel;
using System.Text.Json;
using System.Text.Json.Serialization;
using GitHub.Copilot;
using Microsoft.Extensions.AI;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var port = int.Parse(Environment.GetEnvironmentVariable("PORT") ?? "8080");
var model = Environment.GetEnvironmentVariable("COPILOT_MODEL") ?? "gpt-5-mini";
var runtimeUrl = Environment.GetEnvironmentVariable("COPILOT_RUNTIME_URL");

object GetServiceStatus([Description("The service name")] string service) => new
{
    service,
    status = "running",
    revision = Environment.GetEnvironmentVariable("CONTAINER_APP_REVISION") ?? "local",
    region = Environment.GetEnvironmentVariable("AZURE_REGION") ?? "local",
};

var getServiceStatusTool = CopilotTool.DefineTool(
    GetServiceStatus,
    new CopilotToolOptions { SkipPermission = true },
    new AIFunctionFactoryOptions
    {
        Name = "get_service_status",
        Description = "Get the current deployment status of an internal service",
    });

var client = new CopilotClient(new CopilotClientOptions
{
    Connection = runtimeUrl is null ? null : RuntimeConnection.ForUri(runtimeUrl, null),
});

var ready = false;

async Task<string> AskAsync(string prompt)
{
    await using var session = await client.CreateSessionAsync(new SessionConfig
    {
        Model = model,
        Tools = new List<AIFunctionDeclaration> { getServiceStatusTool },
        AvailableTools = new List<string> { "custom:*" },
    });
    var response = await session.SendAndWaitAsync(new MessageOptions { Prompt = prompt });
    return response?.Data?.Content ?? "";
}

app.MapGet("/health", () => Results.Json(
    new { status = ready ? "ok" : "starting", model, runtime = runtimeUrl ?? "bundled" },
    statusCode: ready ? 200 : 503));

app.MapPost("/ask", async (HttpRequest request) =>
{
    using var reader = new StreamReader(request.Body);
    var raw = await reader.ReadToEndAsync();
    var body = string.IsNullOrWhiteSpace(raw) ? null : JsonSerializer.Deserialize<AskRequest>(raw);
    if (string.IsNullOrEmpty(body?.Prompt))
        return Results.Json(new { error = "body must be {\"prompt\": \"...\"}" }, statusCode: 400);
    return Results.Json(new { answer = await AskAsync(body.Prompt) });
});

app.MapFallback(() => Results.Json(new { error = "try GET /health or POST /ask" }, statusCode: 404));

app.Lifetime.ApplicationStopping.Register(() => client.StopAsync().GetAwaiter().GetResult());

await client.StartAsync();
ready = true;

app.Urls.Add($"http://0.0.0.0:{port}");
await app.RunAsync();

record AskRequest([property: JsonPropertyName("prompt")] string? Prompt);
