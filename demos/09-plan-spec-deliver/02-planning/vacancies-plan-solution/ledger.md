# Vacancies Plan Ledger

## MCP tools
- **Tool discovery attributes**
  - `HRTools` is marked with `[McpServerToolType]`, which makes the class discoverable as an MCP tool container.
  - Each exposed tool method is marked with `[McpServerTool]`.
  - Human-readable descriptions use `[Description("...")]` on both methods and parameters.
  - Minimal pattern:
    ```csharp
    [McpServerToolType]
    internal class HRTools
    {
        [McpServerTool]
        [Description("Provides the whole list of employees")]
        public async Task<EmployeeCollection> ListEmployees() { ... }
    }
    ```

- **Naming and parameter conventions**
  - No explicit tool name override is used in `HRTools.cs`; tool names therefore follow the C# method names exactly: `ListEmployees`, `AddEmployee`, `UpdateEmployee`, `RemoveEmployee`, `SearchEmployees`.
  - Required parameters are non-nullable and have no default, for example `string firstName`.
  - Optional parameters are nullable and/or have defaults, for example `string? firstName = null`, `string spokenLanguages = ""`.
  - Parameter descriptions are declared inline with `[Description(...)]`.
  - Input types are simple strings only in the current tools; list-like input is accepted as comma-separated strings and parsed internally by `ParseCommaSeparatedString(...)`.
  - `UpdateEmployee` uses the pattern “required identity parameter first, then optional patch-style parameters”.

- **Return shapes, serialization, and error handling**
  - Read tools return DTO objects: `Task<EmployeeCollection>`.
  - Mutation tools return plain status messages: `Task<string>`.
  - `EmployeeCollection` is a DTO wrapper with `List<Employee> Employees`.
  - `Employee` is a class model with JSON serialization attributes:
    - `[JsonPropertyName("firstname")]`
    - `[JsonPropertyName("lastname")]`
    - `[JsonPropertyName("email")]`
    - `[JsonPropertyName("spoken_languages")]`
    - `[JsonPropertyName("skills")]`
    - `[JsonPropertyName("current_role")]`
    - `[JsonIgnore]` hides persistence fields like `Id`, `SpokenLanguagesData`, and `SkillsData`.
  - `SpokenLanguages` and `Skills` are exposed as `List<string>` but persisted as JSON strings via `SerializeList`/`DeserializeList`.
  - Error handling in the tool layer is simple and non-exception-based for business outcomes:
    - duplicate add -> returns `"Employee with email '...' already exists."`
    - missing update/remove target -> returns `"Employee with email '...' not found."`
  - Validation exceptions are pushed down to the service layer for invalid programmer input such as null employee or blank email.

- **Existing tools in `HRTools.cs`**
  - `ListEmployees` - returns all employees as an `EmployeeCollection`.
  - `AddEmployee` - creates a new employee from required strings plus optional comma-separated languages and skills.
  - `UpdateEmployee` - updates an employee found by email using optional patch-style fields.
  - `RemoveEmployee` - deletes an employee by email.
  - `SearchEmployees` - returns employees matching a free-text term across name, email, role, skills, and spoken languages.

- **Dependency injection pattern**
  - `HRTools` uses constructor injection:
    ```csharp
    public HRTools(IEmployeeService employeeService, ILogger<HRTools> logger)
    ```
  - The tool class does **not** access `EmployeeDbContext` directly.
  - `Program.cs` registers dependencies with DI:
    - `AddDbContext<EmployeeDbContext>(...)`
    - `AddScoped<IEmployeeService, EmployeeService>()`
    - `AddMcpServer().WithHttpTransport().WithToolsFromAssembly()`
  - `EmployeeService` is the layer that receives `EmployeeDbContext` and `ILogger<EmployeeService>` via constructor injection and performs all database work.

- **Pattern to follow for new vacancy tools**
  - Add new methods to `HRTools` with `[McpServerTool]` and `[Description]`.
  - Prefer method-name-based tool names unless there is a reason to introduce an explicit override elsewhere.
  - Use non-nullable parameters for required inputs, nullable/defaulted parameters for optional inputs.
  - Return DTOs for structured query results and `string` for simple mutation outcomes, matching the existing employee tools.

## Data
- **Employee model (`Tools/Models.cs`)**
  - Properties and types:
    - `Id: int` (`[JsonIgnore]`)
    - `FirstName: string`
    - `LastName: string`
    - `Email: string`
    - `CurrentRole: string`
    - `SpokenLanguagesData: string` (`[JsonIgnore]`)
    - `SkillsData: string` (`[JsonIgnore]`)
    - `SpokenLanguages: List<string>` (`[NotMapped]`, JSON name `spoken_languages`)
    - `Skills: List<string>` (`[NotMapped]`, JSON name `skills`)
    - `FullName` is computed, not stored.
  - Skills and languages are **persisted as JSON strings in TEXT columns**, not comma-separated columns and not normalized tables:
    ```csharp
    public string SpokenLanguagesData { get; set; } = "[]";
    public List<string> SpokenLanguages
    {
        get => DeserializeList(SpokenLanguagesData);
        set => SpokenLanguagesData = SerializeList(value);
    }
    ```
  - Tool inputs use comma-separated strings in `HRTools`, but those are parsed into `List<string>` before persistence.

- **DbContext and SQLite setup (`Data/EmployeeDbContext.cs`, `Program.cs`, `appsettings.json`)**
  - Single DbSet today:
    - `DbSet<Employee> Employees`
  - `OnModelCreating` maps `Employee` to table **`Candidates`**.
  - Key/config:
    - primary key: `Id`
    - required + max length: `FirstName` 100, `LastName` 100, `Email` 256
    - unique index on `Email`
    - `CurrentRole` max length 200
    - `SpokenLanguagesData` and `SkillsData` are required `TEXT`
  - There is **no EF value converter** for the list-like properties; the model stores backing string properties and keeps the `List<string>` properties `[NotMapped]`.
  - SQLite wiring:
    ```csharp
    builder.Services.AddDbContext<EmployeeDbContext>(options =>
        options.UseSqlite(builder.Configuration.GetConnectionString("EmployeeDatabase")));
    ```
    ```json
    "EmployeeDatabase": "Data Source=hr-data.db"
    ```
  - DB file is `hr-data.db`, relative to the app's working directory/project folder. `EmployeeDbContextFactory` uses the same connection string pattern for design-time context creation.

- **Initialization and seeding (`Data/EmployeeDbInitializer.cs`)**
  - Startup calls:
    ```csharp
    await EmployeeDbInitializer.InitializeAsync(app.Services);
    ```
  - Schema creation uses **`EnsureCreatedAsync`**, not EF migrations.
  - Seeding is inline code via `GetSeedEmployees()`, which returns 8 hard-coded employees.
  - Seeding is idempotent only at the coarse level: if **any** employee already exists (`context.Employees.AnyAsync()`), seeding is skipped.
  - Flow:
    - create DI scope
    - resolve `EmployeeDbContext`
    - `EnsureCreatedAsync`
    - if table has rows, log and stop
    - otherwise `AddRangeAsync(...)` + `SaveChangesAsync()`

- **Status/enum and querying patterns**
  - No existing enum or status field pattern was found in `src/hr-mcp-server`; there are no `enum` declarations or `Status` properties to mirror for vacancy `open/filled`.
  - Employee search logic lives in `Services/EmployeeService.cs` and currently does **in-memory matching after loading all employees**:
    ```csharp
    var employees = await _dbContext.Employees.AsNoTracking().ToListAsync();
    var matchingEmployees = employees.Where(c =>
        c.CurrentRole.ToLowerInvariant().Contains(searchTermLower) ||
        c.Skills.Any(skill => skill.ToLowerInvariant().Contains(searchTermLower)) ||
        c.SpokenLanguages.Any(lang => lang.ToLowerInvariant().Contains(searchTermLower)));
    ```
  - Because `Skills`/`SpokenLanguages` are `[NotMapped]` list wrappers over JSON `TEXT`, current skills/language matching is **not translated into SQL**.

## Verification
- Manual verification in `src/hr-mcp-server` is documented in `readme.md` and uses the MCP Inspector against the local HTTP endpoint.
- Run the local server:
  ```powershell
  dotnet run
  ```
- Launch the interactive inspector for the local server:
  ```powershell
  npx @modelcontextprotocol/inspector --config inspector.config.json --server hr-mcp
  ```
- Headless smoke-test commands from the same folder:
  ```powershell
  npx @modelcontextprotocol/inspector --cli --config inspector.config.json --server hr-mcp --method tools/list
  npx @modelcontextprotocol/inspector --cli --config inspector.config.json --server hr-mcp --method tools/call --tool-name list_employees
  ```
- `inspector.config.json` defines `mcpServers` entries only:
  - `hr-mcp`: `type: "http"`, `url: "http://localhost:47002"`
  - `hr-mcp-azure-dev`: `type: "http"`, `url: "https://hr-mcp-server-copilot.azurewebsites.net"`
  - No command, args, or env vars are configured there because the inspector connects to an already running HTTP server.
- A developer points the inspector at this server by:
  1. starting the app with `dotnet run`
  2. launching the inspector with `--config inspector.config.json --server hr-mcp`
  3. clicking **Connect** in the inspector UI
- Existing end-to-end verification steps for the employee tools:
  1. Connect with MCP Inspector.
  2. Confirm all 5 tools are listed: `list_employees`, `add_employee`, `update_employee`, `remove_employee`, `search_employees`.
  3. Call `list_employees`.
  4. Verify the response returns the 8 seeded employees.
- Generalizing that workflow for vacancy tools: add the server-side tool, start with `dotnet run`, connect via the same inspector config, confirm the new vacancy tools appear in the tool list, then call each tool and verify the response/state change end-to-end in the same way `list_employees` is checked today.
- Remote inspection is also documented:
  ```powershell
  npx @modelcontextprotocol/inspector --config inspector.config.json --server hr-mcp-azure-dev
  ```
  The readme notes this Azure App Service target is currently not provisioned, so the working verification path is the local `hr-mcp` entry.
- No automated unit or integration tests were found under `src/hr-mcp-server`: no test project, no `Microsoft.NET.Test.Sdk`, xUnit/NUnit/MSTest references, and no dedicated test folders. The only VS Code tasks present are `clean` and `publish-release`, not test runners.
