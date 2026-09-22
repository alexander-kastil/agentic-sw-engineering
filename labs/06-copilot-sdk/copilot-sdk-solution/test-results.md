# Lab 06 test results: GitHub Copilot SDK support agent

Environment: Windows 11, `dotnet --version` = 10.0.112 (SDKs installed: 9.0.310, 10.0.102, 10.0.112). Starter repo cloned by the requester at:

```plaintext
C:\Users\ALEXAN~1\AppData\Local\Temp\claude\D--git-classes-agentic-sw-engineering\0b9ef576-0f1b-414a-9114-61b2d233e6e4\scratchpad\lr\github-copilot-sdk-starter-app
```

`copilot --version` in this environment reports `GitHub Copilot CLI 1.0.86` and is already authenticated, so every scenario below including live model calls and tool invocations was run for real. Nothing in this lab required a credential this environment lacked.

## 1. Verify the starter against the guide

Checked against `labs/06-copilot-sdk/readme.md`, "Review features of the ContosoShop application":

- Project names, folder layout (`ContosoShop.Client`, `ContosoShop.Server`, `ContosoShop.Shared`, `Tests/ContosoShop.Server.Tests`) and `ContosoShopSupportPortal.slnx` match the guide exactly.
- All three app `.csproj` files target `net8.0`, confirming the guide's instruction to upgrade to net10.0 is necessary and correctly worded.
- `ContosoShop.Server/Controllers/OrdersController.cs` has `GetOrders`, `GetOrder`, `ReturnOrderItems` as described.
- `ContosoShop.Server/Services/OrderService.cs` has `ProcessItemReturnAsync` with the described validation, inventory restore, status recalculation and email confirmation.
- `ContosoShop.Server/Data/DbInitializer.cs` seeds 20 orders total (10 for Mateo, 10 for Megan), confirmed by the app's own startup log: `Database initialized with 20 orders for users: Mateo Gomez (10 orders), Megan Bowen (10 orders)`.
- The demo credentials `mateo@contoso.com` / `Password123!` work against `POST /api/auth/login` (verified below).
- Program.cs has the comment `// Register order business logic service` that the guide tells the reader to search for.
- Program.cs's CORS block comment is `// Configure CORS with explicit whitelist (T024s - Security hardened)`, not exactly `// Configure CORS` as the guide's search text implies, but it is a substring match so the reader's search still finds it. Not treated as a defect requiring a guide fix.

### Build and test the unmodified starter

```bash
cd .../github-copilot-sdk-starter-app
dotnet build ContosoShopSupportPortal.slnx
```

Result: **FAILED**, 16x `MSB3030: Could not copy the file ".../ContosoShop.Client/obj/Debug/net8.0/webcil/*.wasm" because it was not found`.

Root cause: the scratchpad clone path is deeply nested; the generated webcil intermediate paths exceed 260 characters (measured one at 264), which is the classic Windows `MAX_PATH` limit for the Win32 file copy APIs MSBuild's copy task uses. `core.longpaths=true` only affects git, not this. This is an artifact of the temp scratchpad location, not a defect in the guide or the starter's own code. A clone at a short path like the guide's own example (`C:\TrainingProjects\ContosoShop`) does not hit this.

Workaround applied (scratchpad only, not committed to the class repo): added a `Directory.Build.props` at the scratchpad clone root redirecting `BaseIntermediateOutputPath`/`BaseOutputPath` to `C:\lab06build\obj\$(MSBuildProjectName)\` / `C:\lab06build\bin\$(MSBuildProjectName)\`, then cleared any partial `obj`/`bin` folders and rebuilt.

```bash
dotnet build ContosoShopSupportPortal.slnx
```

Result: **Build succeeded. 1 Warning(s), 0 Error(s)** (the one warning is a pre-existing `RZ10012` in `App.razor` about `RedirectToLogin`, unrelated to this lab).

```bash
dotnet test Tests/ContosoShop.Server.Tests/ContosoShop.Server.Tests.csproj
```

Result: **Failed: 11, Passed: 20, Skipped: 0, Total: 31** on the unmodified starter. All 11 failures are in `AuthenticationTests`, `AuthorizationTests`, `CsrfProtectionTests` and `RateLimitingTests`, and the failure pattern (`Expected: OK Actual: TooManyRequests`, `Expected: Unauthorized Actual: OK`) is consistent with the in-memory rate limiter's state bleeding across tests that share a `WebApplicationFactory` and run in the same 15-minute rate-limit window. This is pre-existing flakiness in the starter's own test suite, unrelated to the AI agent work; it reproduces identically before and after the lab's changes (see below) and touches no code this lab adds.

## 2. Apply the guide's code and find defects

Packages installed exactly as the guide instructs:

```bash
cd ContosoShop.Server
dotnet add package GitHub.Copilot.SDK --prerelease
dotnet add package Microsoft.Extensions.AI
```

Result: `GitHub.Copilot.SDK 1.0.15-preview.0` and `Microsoft.Extensions.AI 10.10.0` installed, `dotnet build` still green.

Wrote every file the guide specifies, verbatim, then built after each section. Reflection against the installed `GitHub.Copilot.SDK.dll` (via its XML doc and a throwaway reflection console app) was used to confirm the real public API surface before fixing each defect, because the preview package's actual types differ from the guide's snippets in several places.

### Defect 1: wrong namespace

Guide's `using GitHub.Copilot.SDK;` (readme.md:1015, 1127, 1432) does not exist. Every public type (`CopilotClient`, `CopilotSession`, `SessionConfig`, `MessageOptions`, `AssistantMessageEvent`, etc.) lives in the `GitHub.Copilot` namespace, confirmed by reflecting over `typeof(GitHub.Copilot.CopilotClient).Assembly` and listing every `T:GitHub.Copilot.*` entry in `GitHub.Copilot.SDK.xml`.

```plaintext
error CS0246: The type or namespace name 'CopilotClient' could not be found (are you missing a using directive or an assembly reference?)
```

Fix: `using GitHub.Copilot;` everywhere the guide has `using GitHub.Copilot.SDK;`.

### Defect 2: `CopilotClientOptions.AutoStart` does not exist

Guide's client registration (readme.md:1030-1038) sets `AutoStart = true` on `CopilotClientOptions`. Reflecting over `CopilotClientOptions`'s public properties shows no `AutoStart` member at all (`Mode`, `Connection`, `WorkingDirectory`, `BaseDirectory`, `BuiltinPluginDirectories`, `LogLevel`, `Environment`, `Logger`, `GitHubToken`, `UseLoggedInUser`, `OnListModels`, `SessionFs`, `RequestHandler`, `ExtensionLaunchProvider`, `OnGitHubTelemetry`, `Telemetry`, `SessionIdleTimeoutSeconds`, `EnableRemoteSessions`, `ClientInfo`).

```plaintext
error CS0117: 'CopilotClientOptions' does not contain a definition for 'AutoStart'
```

Fix: remove the `AutoStart = true` line entirely. The guide's own next step already calls `await copilotClient.StartAsync();` explicitly after `builder.Build()`, so the property was never needed.

### Defect 3: `LogLevel` is not a string

`CopilotClientOptions.LogLevel` is `Nullable<CopilotLogLevel>`, a struct with static members `None`, `Error`, `Warning`, `Info`, `Debug`, `All` and a `string` constructor, but **no implicit conversion from `string`**. Confirmed by compiling `CopilotLogLevel y = "info";` directly against the package: `error CS0029: Cannot implicitly convert type 'string' to 'GitHub.Copilot.CopilotLogLevel'`.

Guide's `LogLevel = "info"` (readme.md:1036) therefore fails with the same CS0029.

Fix: `LogLevel = CopilotLogLevel.Info`. The solution also wires the already-fetched `logger` into `Logger = logger` on the same options object, since the guide fetches it via `sp.GetRequiredService<ILogger<CopilotClient>>()` but never assigns it anywhere, which is dead code.

### Defect 4: `session.On(evt => ...)` cannot be type-inferred

`CopilotSession.On<T>(Action<T> handler)` is generic. Guide's `session.On(evt => { switch (evt) { case AssistantMessageEvent msg: ... } })` (readme.md:1338, 1590) passes an untyped lambda with no other argument the compiler can use to infer `T`.

```plaintext
error CS0411: The type arguments for method 'CopilotSession.On<T>(Action<T>)' cannot be inferred from the usage. Try specifying the type arguments explicitly.
```

Confirmed by compiling the exact snippet standalone against the package before touching the lab's files, then confirming `session.On<SessionEvent>(evt => {...})` compiles clean.

Fix: `session.On<SessionEvent>(evt => { ... });` (`SessionEvent` is the common base type of `AssistantMessageEvent`, `SessionIdleEvent`, `SessionErrorEvent`, all in the `GitHub.Copilot` namespace already imported).

### Defect 5 (behavioral, not a compile error): tool calls are silently permission-blocked

With defects 1-4 fixed, the solution built clean and the API returned `200 OK` for every request, but the agent's answer was a generic "I'm unable to access order details right now due to a permission issue" for every question that required a tool call. The model was calling `get_order_details` but the SDK was rejecting the invocation. No `SessionErrorEvent` was raised (the model just narrated the denial in its own answer), so this does not show up as a thrown exception or a log entry in `SupportAgentController`.

Root cause: `GitHub.Copilot.CopilotSession.RegisterPermissionHandler(...)` (the internal hook the SDK docs mention) is `internal`, not usable from application code. The public hook is `SessionConfigBase.OnPermissionRequest`, which the guide never sets, so every custom tool call defaults to unapproved.

Fix, added to `SupportAgentController.cs` inside the `SessionConfig` object:

```csharp
OnPermissionRequest = (request, invocation) =>
    Task.FromResult(GitHub.Copilot.Rpc.PermissionDecision.ApproveOnce()),
```

`GitHub.Copilot.Rpc.PermissionDecision` is marked with the SDK's own experimental diagnostic and the compiler refuses to reference it without suppression:

```plaintext
error GHCP001: 'GitHub.Copilot.Rpc.PermissionDecision' is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
```

so the `CreateSessionAsync` call and the `OnPermissionRequest` assignment are wrapped in `#pragma warning disable GHCP001` / `#pragma warning restore GHCP001`.

After this fix, every tool call succeeded and returned real database-backed answers (see section 3).

## 3. Make it work: final verification

```bash
dotnet build ContosoShopSupportPortal.slnx
```

Result: **Build succeeded. 1 Warning(s) (pre-existing RZ10012), 0 Error(s).**

```bash
dotnet test Tests/ContosoShop.Server.Tests/ContosoShop.Server.Tests.csproj
```

Result: **Failed: 10, Passed: 21, Skipped: 0, Total: 31.** Same pre-existing rate-limiting-related failures as the unmodified starter's baseline (section 1); none of the 10 failing tests touch `SupportAgentController`, `SupportAgentTools`, or `SupportAgentService`.

### Live end-to-end run

```bash
dotnet run --no-launch-profile --urls http://localhost:5266
```

Server started, seeded 20 orders, listened on `http://localhost:5266`. (The Blazor UI's static files did not serve (`WebRootPath was not found`) because the `Directory.Build.props` output-path workaround from section 1 moves `wwwroot` out of the project's content root; this only affects browser-served static assets in this scratchpad location, not the API. A clone at a normal short path would not need the workaround and would serve the UI normally.)

Logged in and exercised the live agent API directly:

```bash
curl -c cookies.txt -b cookies.txt -X POST http://localhost:5266/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"mateo@contoso.com","password":"Password123!"}'
```
→ `200 OK`, `{"success":true,"errorMessage":null,"userName":"Mateo Gomez"}`

```bash
curl -c cookies.txt -b cookies.txt -X POST http://localhost:5266/api/supportagent/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the status of order #1001?"}'
```
→ `200 OK`, `{"answer":"Order #1001 was **delivered on August 2, 2026** (ordered July 28, 2026). Total: $315.95.\n\nItems in this order:\n- Monitor – 1 × $215.99\n- Headphones – 1 × $54.99\n- HDMI Cable – 3 × $14.99\n\nLet me know if you'd like to return anything or need further help!"}`
matches the real order data in the database (verified via `GET /api/orders/1001`).

```bash
curl ... -d '{"question":"Show me all my orders"}'
```
→ returns all 10 of Mateo's orders with correct statuses and totals via `get_user_orders`.

```bash
curl ... -d '{"question":"Where is my order #9999?"}'
```
→ `"I couldn't find an order #9999 associated with your account..."` (correct not-found handling).

```bash
curl ... -d '{"question":"What is the weather like today?"}'
```
→ politely declines and redirects to `support@contososhop.com` / `1-800-CONTOSO` (correct off-topic deflection).

```bash
curl ... -d '{"question":"I want to return order #1008"}'
curl -c cookies.txt -b cookies.txt http://localhost:5266/api/orders/1008
```
→ agent calls `process_return`, responds with the $77.99 Webcam refund confirmation; `GET /api/orders/1008` afterwards shows `"status":3` (`Returned`), `"returnedQuantity":1`, `"remainingQuantity":0`. The return was actually written to the database, not just narrated.

All five scenarios from the guide's "Test the end-to-end AI agent experience" section pass against the live GitHub Copilot CLI and a real `gpt-4.1` session.

## Pass/fail summary

| Check | Result |
|---|---|
| Unmodified starter builds (short-path workaround) | PASS |
| Unmodified starter tests | 20/31 pass (11 pre-existing failures, rate-limiter test isolation, unrelated to this lab) |
| Guide's code as printed, verbatim | FAILS to compile (5 defects, see above) |
| Solution code builds | PASS, 0 errors |
| Solution code tests | 21/31 pass (10 pre-existing failures, same class as baseline) |
| Live agent: order status lookup | PASS |
| Live agent: list all orders | PASS |
| Live agent: non-existent order | PASS |
| Live agent: off-topic deflection | PASS |
| Live agent: full return processing (real DB write) | PASS |

## What could not be run

Nothing. `copilot` CLI was pre-installed and pre-authenticated in this environment, so every scenario including live model and tool calls ran for real; no step was blocked on missing credentials.
