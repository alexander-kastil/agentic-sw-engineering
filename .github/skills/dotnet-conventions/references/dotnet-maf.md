# .NET — Microsoft Agent Framework (MAF) via Azure AI Foundry SDK

Reference for calling MAF hosted agents and prompt-based agents from a .NET ASP.NET Core application using the Azure AI Foundry SDK. Extracted from a working production .NET 10 API. All patterns are general — no project-specific names.

## NuGet Packages

```xml
<PackageReference Include="Azure.AI.Projects" Version="2.0.1" />
<PackageReference Include="Azure.AI.Extensions.OpenAI" Version="2.0.0" />
<PackageReference Include="Azure.Identity" Version="1.21.0" />
```

- Do NOT install `Azure.AI.Projects.OpenAI` (old preview) alongside `Azure.AI.Extensions.OpenAI` — they define conflicting types.
- `Azure.AI.Projects.Agents` (for CRUD on agent definitions) is separate from `Azure.AI.Extensions.OpenAI` (for running conversations).
- The old `Azure.AI.Agents.Persistent` (thread/run pattern) is deprecated and retires March 2027 — do not use for new code.

## Configuration

Define one typed options class per agent:

```csharp
public class FoundryAgentConfig
{
    public string ProjectEndpoint { get; set; } = string.Empty;

    [Required]
    public string AgentName { get; set; } = string.Empty;

    public string? LocalAgentUrl { get; set; }
}
```

`appsettings.json` structure — shared endpoint, per-agent names:

```json
{
  "Foundry": {
    "ProjectEndpoint": "https://<resource>.services.ai.azure.com/api/projects/<project>",
    "Agents": {
      "ResearchAgent": {
        "AgentName": "social-profiler"
      },
      "ContentAgent": {
        "AgentName": "content-creator-team",
        "LocalAgentUrl": "http://localhost:8088"
      }
    }
  }
}
```

- The project endpoint format is `https://<resource>.services.ai.azure.com/api/projects/<project>` — hub-based endpoints (`InferenceEndpoint=...`) are incompatible with SDK 2.x.
- Use `LocalAgentUrl` to route to a locally running agent server during development without changing production config.

## DI Registration (Program.cs)

Register named options for each agent; share the project endpoint via `PostConfigure`:

```csharp
var sharedEndpoint = builder.Configuration["Foundry:ProjectEndpoint"] ?? "";

builder.Services.Configure<FoundryAgentConfig>(
    "ResearchAgent",
    builder.Configuration.GetSection("Foundry:Agents:ResearchAgent"));

builder.Services.Configure<FoundryAgentConfig>(
    "ContentAgent",
    builder.Configuration.GetSection("Foundry:Agents:ContentAgent"));

builder.Services.PostConfigure<FoundryAgentConfig>("ResearchAgent", cfg => cfg.ProjectEndpoint = sharedEndpoint);
builder.Services.PostConfigure<FoundryAgentConfig>("ContentAgent", cfg => cfg.ProjectEndpoint = sharedEndpoint);
```

Inject in services with `IOptionsSnapshot<FoundryAgentConfig>` (scoped):

```csharp
public class ResearchService(IOptionsSnapshot<FoundryAgentConfig> agentOptions)
{
    private readonly FoundryAgentConfig _config = agentOptions.Get("ResearchAgent");
}
```

## Calling a Hosted (Prompt-Based) Foundry Agent

A hosted agent is deployed and named in the Azure AI Foundry portal. Call it with `ProjectResponsesClient`:

```csharp
using Azure.AI.Extensions.OpenAI;
using Azure.AI.Projects;
using Azure.Identity;

var projectClient = new AIProjectClient(
    new Uri(_config.ProjectEndpoint),
    new DefaultAzureCredential());

var responsesClient = projectClient.ProjectOpenAIClient
    .GetProjectResponsesClientForAgent(_config.AgentName);

var result = await responsesClient.CreateResponseAsync(userInput);
var outputText = result.Value.GetOutputText();
```

- `GetProjectResponsesClientForAgent(agentName)` looks up the agent by the name registered in Foundry.
- `GetOutputText()` is a convenience extension that concatenates all text output items from the response.
- Use `DefaultAzureCredential` for development; `ManagedIdentityCredential` for production App Service to avoid credential-chain latency.
- `#pragma warning disable OPENAI001` is required for multi-turn `ProjectConversation` types (marked experimental in the GA package).

## Multi-Turn Conversation

For stateful multi-turn conversations, use `ProjectConversation`:

```csharp
#pragma warning disable OPENAI001

var projectClient = new AIProjectClient(new Uri(_config.ProjectEndpoint), new DefaultAzureCredential());

var conversation = projectClient.ProjectOpenAIClient
    .GetProjectConversationsClient()
    .CreateProjectConversation();

var responsesClient = projectClient.ProjectOpenAIClient
    .GetProjectResponsesClientForAgent(
        defaultAgent: _config.AgentName,
        defaultConversationId: conversation.Id);

var response1 = await responsesClient.CreateResponseAsync("First question");
var response2 = await responsesClient.CreateResponseAsync("Follow-up question");

await projectClient.ProjectOpenAIClient
    .GetConversationClient()
    .DeleteConversationAsync(conversation.Id);
```

Stateless alternative — chain via `PreviousResponseId`:

```csharp
var r1 = await responsesClient.CreateResponseAsync("First question");
var r2 = await responsesClient.CreateResponseAsync(
    new CreateResponseOptions
    {
        PreviousResponseId = r1.Value.Id,
        InputItems = { ResponseItem.CreateUserMessageItem("Follow-up") }
    });
```

## Local Development Fallback

When `LocalAgentUrl` is set, POST to the local agent server instead of calling Foundry:

```csharp
private async Task<string> CallAgentAsync(string input)
{
    if (!string.IsNullOrWhiteSpace(_config.LocalAgentUrl))
    {
        using var request = new HttpRequestMessage(
            HttpMethod.Post,
            $"{_config.LocalAgentUrl.TrimEnd('/')}/responses")
        {
            Content = JsonContent.Create(new { model = _config.AgentName, input, stream = false })
        };
        request.Headers.Accept.ParseAdd("text/event-stream");

        using var response = await _httpClient.SendAsync(
            request, HttpCompletionOption.ResponseHeadersRead);
        response.EnsureSuccessStatusCode();
        return await ReadSseResponseAsync(response.Content);
    }

    var projectClient = new AIProjectClient(
        new Uri(_config.ProjectEndpoint), new DefaultAzureCredential());

    var responsesClient = projectClient.ProjectOpenAIClient
        .GetProjectResponsesClientForAgent(_config.AgentName);

    var result = await responsesClient.CreateResponseAsync(input);
    return result.Value.GetOutputText();
}
```

- The local agent server (Python `ResponsesHostServer`) sends SSE.
- Read `response.output_text.delta` events for streaming text.
- Read `response.workflow_output` for final structured output from a WorkflowBuilder agent.

## Extracting Citation URLs

Foundry agents with web-search tools annotate their responses with source URLs:

```csharp
private static IReadOnlyList<string> ExtractCitationUrls(ResponseResult response)
{
    var urls = new List<string>();

    foreach (var item in response.OutputItems)
    {
        foreach (var content in item.Content)
        {
            foreach (var annotation in content.OutputTextAnnotations)
            {
                var uri = annotation.Uri ?? annotation.Url;
                if (Uri.TryCreate(uri, UriKind.Absolute, out var parsed)
                    && (parsed.Scheme == "https" || parsed.Scheme == "http"))
                {
                    urls.Add(uri!.TrimEnd('.', ',', ';', ')'));
                }
            }
        }
    }

    return urls.Distinct(StringComparer.OrdinalIgnoreCase).ToList();
}
```

## Guarding Against Unconfigured Agents

Always guard before calling — Foundry config may be absent in environments where the agent is not deployed:

```csharp
private bool IsConfigured() =>
    !string.IsNullOrWhiteSpace(_config.AgentName)
    && (!string.IsNullOrWhiteSpace(_config.LocalAgentUrl)
        || !string.IsNullOrWhiteSpace(_config.ProjectEndpoint));

public async Task<string?> RunAsync(string input)
{
    if (!IsConfigured())
    {
        logger.LogWarning("Skipping agent call — Foundry is not configured.");
        return null;
    }
    // production path follows
}
```

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| `AmbiguousMatchException` or type conflicts | Both `Azure.AI.Projects.OpenAI` (old) and `Azure.AI.Extensions.OpenAI` (new) installed | Remove `Azure.AI.Projects.OpenAI` |
| `401` from Foundry even with valid identity | Caller lacks Foundry User RBAC role | Assign `Azure AI User` at the project scope |
| `GetOutputText()` returns empty string | Agent produced structured output with no text item | Check `OutputItems` directly or ensure the agent instructions produce text output |
| `CreateResponseAsync` throws on a hub-based endpoint | Old connection string format; SDK 2.x requires Foundry project endpoint | Update endpoint to `https://<resource>.services.ai.azure.com/api/projects/<project>` |
| `OPENAI001` compile warning | `ProjectConversation` is marked experimental in the GA package | Add `#pragma warning disable OPENAI001` above the usage site |
