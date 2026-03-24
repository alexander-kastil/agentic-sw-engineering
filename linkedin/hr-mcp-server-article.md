# Your AI Assistant Can't See Your Employee Data. Here's How to Fix It.

Most enterprise AI integrations stop at the chat box. You connect a large language model to a product, give it a friendly UI, and declare success. But the moment your team asks it anything meaningful—"Who on the team speaks Spanish and has food safety certification?"—it shrugs. It doesn't know. It can't look it up. You've built an intelligent front end on top of a blind back end.

This is the gap the **Model Context Protocol (MCP)** was designed to close. And building a real MCP server on top of live business data is more straightforward than most engineers expect—once you understand the architecture.

This article walks through a production-grade HR MCP server built in .NET 10. The same patterns apply whether you're building for HR, finance, inventory, or any domain where AI needs real, queryable data to be genuinely useful.

---

## The Problem With "AI-Connected" Systems

When organizations add AI to existing software, they typically do one of two things:

1. **Feed static exports to the model.** A CSV of employees gets pasted into a prompt. Works once, stale immediately.
2. **Build a custom integration layer.** A REST API that the AI calls through a brittle, hand-rolled connector. Works until something changes.

Neither approach scales. The first is manual. The second requires rebuilding the integration every time the AI tool changes—and AI tools change constantly.

What's missing is a **standard contract** between AI assistants and the data systems they need to reach. That's exactly what MCP provides.

---

## What MCP Actually Is (Without the Hype)

The Model Context Protocol is a specification—not a library, not a platform. It defines a structured way for AI models to discover and invoke "tools" that live outside the model itself.

Think of it as a universal adapter. Instead of building a custom plugin for each AI assistant your team uses, you build one MCP server. GitHub Copilot, Claude, and any other MCP-compatible client can then find and call your tools using the same protocol.

The protocol handles:

- **Tool discovery**: The client asks the server "what can you do?" and gets a machine-readable list back
- **Invocation**: Strongly typed parameters, documented descriptions, standardized result formats
- **Transport**: Both stdio (local tool processes) and HTTP (remote services) are supported

For enterprise software, HTTP transport is the practical choice. It means your MCP server is a normal web service: deployed to App Service, versioned, monitored, and secured like anything else in your stack.

---

## What the HR MCP Server Does

The HR MCP server is an ASP.NET Core application that exposes five tools over HTTP:

- **list_employees** — returns the full employee roster with roles, skills, and languages
- **search_employees** — finds employees by name, email, skill, or current role
- **add_employee** — creates a new record with optional skills and language metadata
- **update_employee** — modifies any field on an existing employee by email
- **remove_employee** — deletes a record by email

Behind these tools: Entity Framework Core against SQL Server, a clean service layer, and a database seeded with realistic data at startup. The MCP layer is the thin surface that exposes this existing architecture to AI clients.

The entire setup happens in twelve lines of startup code:

```csharp
builder.Services.AddDbContext<EmployeeDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("EmployeeDatabase")));

builder.Services.AddScoped<IEmployeeService, EmployeeService>();

builder.Services.AddMcpServer()
    .WithHttpTransport()
    .WithToolsFromAssembly();

// ...

app.MapMcp();
```

That's the full MCP registration. The protocol handling, transport negotiation, and tool schema generation are all handled by the SDK.

---

## Why the Tool Design Matters More Than the Infrastructure

The infrastructure is easy. The tool design is where most MCP implementations go wrong.

A common mistake is exposing your database schema directly as tools. You end up with tools like `get_employee_by_id` or `update_employee_field(table, column, value)`. These force the AI to understand your internal data model, which defeats the purpose. The tools should represent **business operations**, not database operations.

The HR tools in this server follow the right pattern. Here's `SearchEmployees`:

```csharp
[McpServerTool]
[Description("Searches for employees by name, email, skills, or current role")]
public async Task<EmployeeCollection> SearchEmployees(
    [Description("Search term to find in employee data")] string searchTerm)
{
    var matchingEmployees = await _employeeService.SearchEmployeesAsync(searchTerm);
    return new EmployeeCollection { Employees = matchingEmployees };
}
```

Three things worth noticing:

**The description is written for the model, not the developer.** The `[Description]` attribute isn't just documentation—the SDK serializes it into the tool schema that AI clients read to decide which tool to call. Vague descriptions produce wrong tool selection. Clear descriptions produce reliable behavior.

**The parameter is intentionally broad.** A single `searchTerm` string lets the model search across name, email, skills, and role without needing to know which field to query. The service layer handles the cross-field logic. The AI just asks.

**The return type carries meaning.** Returning a typed `EmployeeCollection` rather than a raw string means the AI client can work with structured data. It can extract specific fields, perform follow-up reasoning, or present results without parsing text.

---

## The Architecture That Makes This Production-Ready

Three layers separate concerns cleanly:

**MCP Tools** → **Service Layer** → **EF Core / SQL Server**

The tools (`HRTools.cs`) handle MCP-specific concerns: parameter validation, response formatting, and the `[McpServerTool]` attribute declarations. They delegate all business logic to the service layer.

The service layer (`EmployeeService.cs`) owns the business rules: duplicate email detection, ordering by name, update patterns. It has no knowledge of MCP. You could replace the MCP transport with a REST controller tomorrow and the service layer would be unchanged.

The data layer (`EmployeeDbContext.cs`) handles persistence. JSON serialization for `SpokenLanguages` and `Skills` fields is managed transparently at the model level, so callers never see the serialization details.

This separation matters because MCP is still evolving rapidly. The SDK used here is version `0.6.0-preview.1`. Keeping the protocol handling thin and isolated means you can upgrade or swap the MCP layer without touching the business logic that everything else depends on.

---

## Deploying the Server: Local vs. Azure

The server runs locally with `dotnet run`. For team-wide access or integration with hosted AI clients, it deploys to Azure App Service as a standard web app. The inspector configuration (`inspector.config.json`) manages the endpoint switching:

```json
{
  "servers": {
    "hr-mcp": { "url": "http://localhost:47002" },
    "hr-mcp-azure-dev": { "url": "https://hr-mcp-server-copilot.azurewebsites.net" }
  }
}
```

Validation is straightforward: launch the MCP inspector, verify all five tools appear, call `list_employees`, confirm the seeded data returns. If that passes, the deployment is healthy. No custom smoke test tooling required.

This portability—local for development, cloud for production—is one of the practical advantages of HTTP transport over stdio. The AI client doesn't care where the server is running.

---

## How to Apply This Pattern to Your Systems

The HR server is a working template, not a demo. The pattern extracts directly:

1. **Identify your business operations.** Not tables, not CRUD endpoints. The operations your people actually perform: "find employees with this skill," "reassign this person," "show me everyone in this department."

2. **Build a service layer first.** The service layer is the permanent part. The MCP surface is thin. If you design from the MCP layer down, you'll couple too much to the protocol.

3. **Write descriptions for the model, not the developer.** Pretend you're writing documentation for someone who has never seen your system. That's the AI client reading your tool schema.

4. **Return structured types, not strings.** Strings require the model to parse output. Structured types let the model reason over data directly.

5. **Deploy as a normal web service.** Authentication, HTTPS, monitoring, CI/CD—none of that changes because MCP is involved. Your existing deployment patterns apply.

---

## What This Doesn't Solve

A few honest limitations worth naming.

MCP tools expose capabilities but not authorization context. The HR server in this example has no access control—any connected client can call any tool. Production deployments need to add authentication at the transport layer (API keys, Azure AD, or similar) before exposing employee data.

The protocol is also still maturing. The `0.6.0-preview.1` SDK version is not a typo. Breaking changes are likely before a stable release. Design your MCP layer to be as thin and replaceable as possible, and that upgrade cost stays low.

Finally, tool design is hard to validate without testing against real AI clients. The descriptions that seem clear to a developer often produce ambiguous tool selection in practice. Build in time to iterate on tool descriptions after initial deployment—that's usually where the real tuning happens.

---

## Closing Thought

The most valuable AI integrations aren't the ones with the best models. They're the ones where the model can actually reach the data it needs to answer the question.

MCP gives enterprise teams a durable, standard way to build that reach. An HR system that exposes structured tools isn't just "AI-ready"—it's better software. Cleaner interfaces, explicit contracts, and separated concerns benefit the humans maintaining the system long after the AI integration is forgotten.

The interesting question, for most teams, isn't whether to adopt MCP. It's which of your existing systems are worth exposing first.

---

_The HR MCP Server referenced in this article is part of the [Agentic Software Engineering](https://github.com/alexander-kastil/agentic-sw-engineering) teaching repository. The full source is available to explore, fork, and adapt._
