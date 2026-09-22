# Lab 06 solution: GitHub Copilot SDK support agent

Final, verified working versions of every file that [`labs/06-copilot-sdk/readme.md`](../readme.md) adds or changes in the `github-copilot-sdk-starter-app` project, laid out under this folder mirroring their real relative paths inside that starter repo. See [`test-results.md`](test-results.md) for the exact commands run, their output, and every defect found in the guide's original code.

## File map

| File in this folder | Guide section | What it is |
|---|---|---|
| `ContosoShop.Server/ContosoShop.Server.csproj` | Install the GitHub Copilot SDK components | Adds `GitHub.Copilot.SDK` and `Microsoft.Extensions.AI` package references |
| `ContosoShop.Server/Services/SupportAgentTools.cs` | Create the agent tools service | The four tool methods the agent calls: `GetOrderDetailsAsync`, `GetUserOrdersSummaryAsync`, `ProcessReturnAsync`, `SendCustomerEmailAsync` |
| `ContosoShop.Server/Program.cs` | Create the agent tools service / Configure the GitHub Copilot SDK agent | Registers `SupportAgentTools` and the `CopilotClient` singleton, and starts the client after `builder.Build()` |
| `ContosoShop.Shared/Models/SupportQuery.cs` | Configure the GitHub Copilot SDK agent and expose an API endpoint | `SupportQuery` request DTO and `SupportResponse` response DTO |
| `ContosoShop.Server/Controllers/SupportAgentController.cs` | Configure the GitHub Copilot SDK agent and expose an API endpoint | `POST /api/supportagent/ask`: defines the four AI tools, creates a Copilot session with the system prompt, and returns the agent's answer |
| `ContosoShop.Client/Services/SupportAgentService.cs` | Update the Blazor frontend to interact with the agent | Client-side HTTP wrapper that posts a question to `api/supportagent/ask` |
| `ContosoShop.Client/Program.cs` | Update the Blazor frontend to interact with the agent | Registers `SupportAgentService` in the WebAssembly DI container |
| `ContosoShop.Client/Pages/Support.razor` | Update the Blazor frontend to interact with the agent | Replaces the "coming soon" placeholder with the interactive chat UI |

## What changed relative to the guide's printed code

The guide's code as printed does not compile against the real `GitHub.Copilot.SDK` 1.0.15-preview.0 package. Every difference between the files here and the guide's original snippets is listed with its compiler error in [`test-results.md`](test-results.md) and has already been applied to [`../readme.md`](../readme.md) in place. The two changes worth calling out because they are not simple renames:

- `SupportAgentController.cs` sets `OnPermissionRequest` on the `SessionConfig` to auto-approve tool calls. Without it, the SDK's default permission gate blocks every custom tool call and the agent falls back to an "unable to access order details due to a permission issue" answer instead of real data.
- The `OnPermissionRequest` assignment and the `CreateSessionAsync` call are wrapped in `#pragma warning disable GHCP001` / `restore` because `GitHub.Copilot.Rpc.PermissionDecision` is marked experimental by the SDK and the compiler rejects its use otherwise.
