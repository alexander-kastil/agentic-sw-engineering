# HR Current State Ledger

## Process

- Step: a chef hands in notice and a vacancy row is added to the Vacancies sheet with the title, skills, and languages; tool: Excel; time: 5 minutes (process-notes.md, line 7)
- Step: the HR assistant is asked in Copilot Chat to list all employees, then their skills are copied into the Staff Copy sheet so they can be filtered; tools: Copilot Chat and Excel; time: 20 minutes (process-notes.md, line 8)
- Step: the Staff Copy sheet is filtered by skill and matching names are typed into the Internal Candidates column; tool: Excel; time: 15 minutes (process-notes.md, line 9)
- Step: after two Staff Copy names are found to be out of date, the HR assistant is asked again and the rows are fixed by hand; tools: Copilot Chat and Excel; time: 15 minutes (process-notes.md, line 10)
- Step: the vacancy owner is emailed with the candidate list pasted from Excel; tool: Outlook; time: 10 minutes (process-notes.md, line 11)
- Step: a second bar vacancy repeats the same workflow of adding a new row, re-copying staff, filtering, and typing names; tools: Excel and Copilot Chat; time: 40 minutes (process-notes.md, line 12)
- Step: when an internal candidate moves into the role, the employee role is updated through the HR assistant and the vacancy Status is set to Filled; tools: Copilot Chat and Excel; time: 10 minutes (process-notes.md, line 13)
- Step: the weekly open-positions summary is sent by counting open rows and reading Days Open; tools: Excel and Outlook; time: 15 minutes (process-notes.md, line 14)
- Process note: the biggest cost is re-copying staff into Excel each time because the HR assistant knows the employees but not the vacancies, and Days Open is the only metric management asks for (process-notes.md, line 16)
- Manual copy steps:
  - Employee skills are copied from Copilot Chat into the Staff Copy sheet (process-notes.md, line 8)
  - Out-of-date Staff Copy rows are manually corrected in Excel after checking Copilot Chat again (process-notes.md, line 10)
  - The candidate list is pasted from Excel into an Outlook email (process-notes.md, line 11)
  - Staff data is re-copied for the second vacancy as part of repeating the workflow (process-notes.md, line 12)
  - Re-copying staff into Excel every time is explicitly called out as the main cost in the process (process-notes.md, line 16)
## Excel

### Vacancies

- Sheet `Vacancies` is a primary worksheet in `vacancies-tracker.xlsx` with headers in A1:J1 and data through row 4.
- Column `Id` at A1 (sheet `Vacancies`, column A / cell A1); sample values: A2 `V-001`, A3 `V-002`, A4 `V-003`.
- Column `Title` at B1 (sheet `Vacancies`, column B / cell B1); sample values: B2 `Sous Chef`, B3 `Bartender`, B4 `Host`.
- Column `Department` at C1 (sheet `Vacancies`, column C / cell C1); sample values: C2 `Kitchen`, C3 `Bar`, C4 `Front of House`.
- Column `Required Skills` at D1 (sheet `Vacancies`, column D / cell D1); sample values: D2 `Menu Planning; Food Safety`, D3 `Mixology; Customer Engagement`, D4 `Customer Service`.
- Column `Languages` at E1 (sheet `Vacancies`, column E / cell E1); sample values: E2 `English; Spanish`, E3 `English`, E4 `English; German`.
- Column `Status` at F1 (sheet `Vacancies`, column F / cell F1); sample values: F2 `Open`, F3 `Open`, F4 `Filled`.
- Column `Opened` at G1 (sheet `Vacancies`, column G / cell G1); sample values: G2 `2026-09-14 00:00:00`, G3 `2026-09-16 00:00:00`, G4 `2026-08-03 00:00:00`.
- Column `Days Open` at H1 (sheet `Vacancies`, column H / cell H1); sample values: H2 `=IF(F2="Open",TODAY()-G2,"")`, H3 `=IF(F3="Open",TODAY()-G3,"")`, H4 `=IF(F4="Open",TODAY()-G4,"")`.
- Column `Internal Candidates` at I1 (sheet `Vacancies`, column I / cell I1); sample values: I2 `Carlos Gomez; Ahmed Khan`, I3 `Sofia Fernandez`, I4 `Olga Petrova`.
- Column `Owner` at J1 (sheet `Vacancies`, column J / cell J1); sample values: J2 `Anna Schmidt`, J3 `Anna Schmidt`, J4 `Luca Rossi`.
- H2: `=IF(F2="Open",TODAY()-G2,"")` (vacancies-tracker.xlsx, sheet `Vacancies`, cell H2).
- H3: `=IF(F3="Open",TODAY()-G3,"")` (vacancies-tracker.xlsx, sheet `Vacancies`, cell H3).
- H4: `=IF(F4="Open",TODAY()-G4,"")` (vacancies-tracker.xlsx, sheet `Vacancies`, cell H4).
- No data validation rules were present on sheet `Vacancies`.
- No conditional formatting rules were present on sheet `Vacancies`.
- No merged cell ranges were present on sheet `Vacancies`.
- Column `Status` values on sheet `Vacancies` (vacancies-tracker.xlsx) counted: `Open`: 2, `Filled`: 1.

### Staff Copy

- Sheet `Staff Copy` appears to be a secondary reference/supporting sheet in `vacancies-tracker.xlsx` with headers in A1:E1 and data through row 7.
- Column `Name` at A1 (sheet `Staff Copy`, column A / cell A1); sample values: A2 `Carlos Gomez`, A3 `Marie Dubois`, A4 `Luca Rossi`.
- Column `Role` at B1 (sheet `Staff Copy`, column B / cell B1); sample values: B2 `Sous Chef`, B3 `Pastry Chef`, B4 `Head Waiter`.
- Column `Skills` at C1 (sheet `Staff Copy`, column C / cell C1); sample values: C2 `Sous Chef; Menu Planning; Food Safety; Inventory Management`, C3 `Pastry Chef; Dessert Creation; Baking; Team Leadership`, C4 `Head Waiter; Customer Service; Wine Pairing`.
- Column `Languages` at D1 (sheet `Staff Copy`, column D / cell D1); sample values: D2 `Spanish; English; French`, D3 `French; English; Italian`, D4 `Italian; English`.
- Column `Copied On` at E1 (sheet `Staff Copy`, column E / cell E1); sample values: E2 `2026-09-14 00:00:00`, E3 `2026-09-14 00:00:00`, E4 `2026-09-14 00:00:00`.
- No formula cells were present on sheet `Staff Copy`.
- No data validation rules were present on sheet `Staff Copy`.
- No conditional formatting rules were present on sheet `Staff Copy`.
- No merged cell ranges were present on sheet `Staff Copy`.

### Workbook-level findings

- Workbook `vacancies-tracker.xlsx` contains exactly two worksheets: `Vacancies` and `Staff Copy`.
- No workbook-level named ranges or defined names were present in `vacancies-tracker.xlsx`.

## Data structure
- `Tools\Models.cs` defines `Employee` and `EmployeeCollection` only; there are no other data-layer entity classes in that file (`Tools\Models.cs`, lines 10-111).
- `Employee.Id` is `int` with `[JsonIgnore]`; it is not marked with `[Key]` in the model class, but EF makes it the primary key via Fluent API (`Tools\Models.cs`, lines 12-13; `Data\EmployeeDbContext.cs`, lines 21-21).
- `Employee.FirstName` is `string` with `[JsonPropertyName("firstname")]`, default `string.Empty`; EF marks it required and limits it to 100 characters (`Tools\Models.cs`, lines 18-19; `Data\EmployeeDbContext.cs`, lines 23-25).
- `Employee.LastName` is `string` with `[JsonPropertyName("lastname")]`, default `string.Empty`; EF marks it required and limits it to 100 characters (`Tools\Models.cs`, lines 24-25; `Data\EmployeeDbContext.cs`, lines 27-29).
- `Employee.Email` is `string` with `[JsonPropertyName("email")]`, default `string.Empty`; EF marks it required, limits it to 256 characters, and creates a unique index on it (`Tools\Models.cs`, lines 30-31; `Data\EmployeeDbContext.cs`, lines 31-36).
- `Employee.SpokenLanguagesData` is persisted as `string` with `[JsonIgnore]`, default `"[]"`; EF marks it required and stores it as SQLite `TEXT` (`Tools\Models.cs`, lines 36-37; `Data\EmployeeDbContext.cs`, lines 41-43).
- `Employee.SpokenLanguages` is `List<string>` with `[NotMapped]` and `[JsonPropertyName("spoken_languages")]`; it is computed from `SpokenLanguagesData` through JSON serialize/deserialize helpers, so it is part of the API shape but not a database column (`Tools\Models.cs`, lines 42-48, 78-99).
- `Employee.SkillsData` is persisted as `string` with `[JsonIgnore]`, default `"[]"`; EF marks it required and stores it as SQLite `TEXT` (`Tools\Models.cs`, lines 53-54; `Data\EmployeeDbContext.cs`, lines 45-47).
- `Employee.Skills` is `List<string>` with `[NotMapped]` and `[JsonPropertyName("skills")]`; it is computed from `SkillsData`, so it is not mapped to a database column (`Tools\Models.cs`, lines 59-65, 96-99).
- `Employee.CurrentRole` is `string` with `[JsonPropertyName("current_role")]`, default `string.Empty`; EF limits it to 200 characters but does not call `.IsRequired()` in Fluent API (`Tools\Models.cs`, lines 70-71; `Data\EmployeeDbContext.cs`, lines 38-39).
- `Employee.FullName` is a computed read-only `string` property with no attributes; it concatenates first and last name and is not present in the database schema (`Tools\Models.cs`, lines 76-76; `hr-data.db`, `sqlite_master` table query).
- `EmployeeCollection.Employees` is `List<Employee>` initialized to an empty list; it is a container/DTO rather than a mapped EF entity, and there is no `DbSet<EmployeeCollection>` (`Tools\Models.cs`, lines 105-110; `Data\EmployeeDbContext.cs`, lines 13-13).
- `EmployeeDbContext` exposes a single `DbSet<Employee>` named `Employees`, but `OnModelCreating` remaps that entity to the physical table name `Candidates` (`Data\EmployeeDbContext.cs`, lines 13-20).
- `EmployeeDbContext` configures no foreign keys, navigation properties, owned types, junction tables, or relationships of any kind; the data layer is a single-table model (`Data\EmployeeDbContext.cs`, lines 15-48).
- `EmployeeDbContext` configures no seed data; there is no `HasData(...)` call in `OnModelCreating` (`Data\EmployeeDbContext.cs`, lines 15-48).
- The actual SQLite database file is `src\hr-mcp-server\hr-data.db`, referenced by both `appsettings.json` and `appsettings.Development.json` through `ConnectionStrings:EmployeeDatabase = Data Source=hr-data.db` (`appsettings.json`; `appsettings.Development.json`; file found by glob under `src\hr-mcp-server`).
- The live database contains one application table, `Candidates`, created as `Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT`, `FirstName TEXT NOT NULL`, `LastName TEXT NOT NULL`, `Email TEXT NOT NULL`, `SpokenLanguagesData TEXT NOT NULL`, `SkillsData TEXT NOT NULL`, and `CurrentRole TEXT NOT NULL` (`hr-data.db`, query `SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name`).
- The live database also contains a unique index `IX_Candidates_Email` on `Candidates(Email)`, matching the EF `HasIndex(...).IsUnique()` configuration (`hr-data.db`, query `SELECT type, name, tbl_name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name`; `Data\EmployeeDbContext.cs`, lines 35-36).
- Sample live rows show `SpokenLanguagesData` and `SkillsData` are stored as JSON arrays inside `TEXT` columns, for example Carlos Gomez with `"[\"Spanish\",\"English\",\"French\"]"` and `"[\"Sous Chef\",\"Menu Planning\",\"Food Safety\",\"Inventory Management\"]"` (`hr-data.db`, query `SELECT * FROM "Candidates" LIMIT 3`).
- Sample live rows confirm the table currently stores restaurant-oriented candidate/employee data such as `Carlos Gomez / Sous Chef`, `Marie Dubois / Pastry Chef`, and `Luca Rossi / Head Waiter` (`hr-data.db`, query `SELECT * FROM "Candidates" LIMIT 3`).
- Discrepancy: the EF surface uses `DbSet<Employee>` and a class named `Employee`, but the persisted table name is `Candidates`, so the conceptual model and physical table naming are not aligned (`Tools\Models.cs`, class `Employee`; `Data\EmployeeDbContext.cs`, line 19; `hr-data.db`, table `Candidates`).
- Discrepancy: `FirstName`, `LastName`, `Email`, and `CurrentRole` have EF max-length rules, but the SQLite table DDL shows plain `TEXT` columns with no length constraint enforcement in the physical schema (`Data\EmployeeDbContext.cs`, lines 23-39; `hr-data.db`, `sqlite_master` table query).
- Discrepancy: `CurrentRole` is nullable in EF configuration by omission of `.IsRequired()`, but the actual SQLite schema marks `CurrentRole TEXT NOT NULL`; because the CLR property is non-nullable `string`, the runtime model and database end up stricter than the explicit Fluent API suggests (`Tools\Models.cs`, lines 70-71; `Data\EmployeeDbContext.cs`, lines 38-39; `hr-data.db`, `sqlite_master` table query).
- Discrepancy: API-facing properties `SpokenLanguages`, `Skills`, and `FullName` do not exist as columns in the real schema; only `SpokenLanguagesData` and `SkillsData` are persisted, and `FullName` is computed at runtime (`Tools\Models.cs`, lines 42-48, 59-76; `hr-data.db`, `sqlite_master` table query).

## Implementation
- MCP tools exposed from `HRTools` are the five `[McpServerTool]` methods on the `[McpServerToolType]` class: `ListEmployees()` -> `Task<EmployeeCollection>` returns the full employee list by calling `GetAllEmployeesAsync()` and wrapping the result in `EmployeeCollection` (src/hr-mcp-server\Tools\HRTools.cs:29).
- Tool `AddEmployee(string firstName, string lastName, string email, string currentRole, string spokenLanguages = "", string skills = "")` -> `Task<string>` trims core fields, parses the two comma-separated list parameters into `List<string>`, calls `AddEmployeeAsync`, and returns either a duplicate-email message or a success message with the employee full name (src/hr-mcp-server\Tools\HRTools.cs:40-67).
- Tool `UpdateEmployee(string email, string? firstName = null, string? lastName = null, string? currentRole = null, string? spokenLanguages = null, string? skills = null)` -> `Task<string>` looks up an employee by email through `UpdateEmployeeAsync`, conditionally overwrites only the provided fields, reparses spoken languages and skills when present, and returns either not-found or success text (src/hr-mcp-server\Tools\HRTools.cs:70-103).
- Tool `RemoveEmployee(string email)` -> `Task<string>` removes one employee by email through `RemoveEmployeeAsync` and returns either not-found or success text (src/hr-mcp-server\Tools\HRTools.cs:106-118).
- Tool `SearchEmployees(string searchTerm)` -> `Task<EmployeeCollection>` calls `SearchEmployeesAsync(searchTerm)` and wraps the matching employees in `EmployeeCollection` (src/hr-mcp-server\Tools\HRTools.cs:121-129).
- Public service method `GetAllEmployeesAsync()` -> `Task<List<Employee>>` runs an EF Core no-tracking query against `_dbContext.Employees`, orders by `LastName` then `FirstName`, and materializes the full list with `ToListAsync()` (src/hr-mcp-server\Services\EmployeeService.cs:22-27).
- Public service method `AddEmployeeAsync(Employee employee)` -> `Task<bool>` trims `employee.Email`, checks for an existing row with `AnyAsync(c => c.Email == email)`, returns `false` on duplicates, otherwise inserts with `AddAsync`, persists with `SaveChangesAsync`, and logs the add (src/hr-mcp-server\Services\EmployeeService.cs:31-49).
- Public service method `UpdateEmployeeAsync(string email, Action<Employee> updateAction)` -> `Task<bool>` trims the email, fetches the tracked entity with `FirstOrDefaultAsync(c => c.Email == normalizedEmail)`, returns `false` when missing, otherwise applies the supplied mutation delegate, saves changes, and logs the update (src/hr-mcp-server\Services\EmployeeService.cs:52-74).
- Public service method `RemoveEmployeeAsync(string email)` -> `Task<bool>` trims the email, fetches the matching entity with `FirstOrDefaultAsync(c => c.Email == normalizedEmail)`, returns `false` when missing, otherwise removes the entity, saves changes, and logs the removal (src/hr-mcp-server\Services\EmployeeService.cs:77-96).
- Public service method `SearchEmployeesAsync(string searchTerm)` -> `Task<List<Employee>>` returns `GetAllEmployeesAsync()` when the input is blank; otherwise it loads all employees with `_dbContext.Employees.AsNoTracking().ToListAsync()` and filters in memory for case-insensitive matches across `FirstName`, `LastName`, `Email`, `CurrentRole`, any `Skills`, or any `SpokenLanguages` (src/hr-mcp-server\Services\EmployeeService.cs:99-118).
- Data storage is wired through the `EmployeeDatabase` connection string set to `Data Source=hr-data.db`, so SQLite uses a relative file named `hr-data.db`; this file is present at `src\hr-mcp-server\hr-data.db` in the repo (src/hr-mcp-server\appsettings.json:2-3).
- `Program.cs` registers the EF Core context with `builder.Services.AddDbContext<EmployeeDbContext>(options => options.UseSqlite(builder.Configuration.GetConnectionString("EmployeeDatabase")))`, registers `IEmployeeService` to `EmployeeService` as scoped, and registers MCP tooling with `AddMcpServer().WithHttpTransport().WithToolsFromAssembly()` (src/hr-mcp-server\Program.cs:9-18).
- The DbContext exposes `DbSet<Employee> Employees`, maps `Employee` to the SQLite table `Candidates`, sets `Id` as the key, requires/max-length constrains `FirstName`, `LastName`, and `Email`, creates a unique index on `Email`, and stores `SpokenLanguagesData` plus `SkillsData` as `TEXT` columns (src/hr-mcp-server\Data\EmployeeDbContext.cs:13-47).
- Startup seeding is explicit: `Program.cs` awaits `EmployeeDbInitializer.InitializeAsync(app.Services)` before `app.MapMcp()` and `app.Run()` (src/hr-mcp-server\Program.cs:23-30).
- `EmployeeDbInitializer.InitializeAsync(IServiceProvider services, CancellationToken cancellationToken = default)` creates a scope, resolves `EmployeeDbContext`, calls `context.Database.EnsureCreatedAsync()`, skips seeding when `context.Employees.AnyAsync()` finds existing rows, and otherwise inserts eight seed employees via `GetSeedEmployees()` followed by `SaveChangesAsync()` (src/hr-mcp-server\Data\EmployeeDbInitializer.cs:7-30).
- The seed set contains eight restaurant-staff records — Carlos Gomez, Marie Dubois, Luca Rossi, Anna Schmidt, Sofia Fernandez, Kenji Tanaka, Olga Ivanova, and Ahmed Hassan — each with email, role, spoken languages, and skills populated in code (src/hr-mcp-server\Data\EmployeeDbInitializer.cs:33-109).
- `HRMCPServerConfiguration` defines an `EmployeesPath` setting under section `HRMCPServer`, but `Program.cs` does not bind or use that configuration, so current persistence and startup seeding are driven by the SQLite connection string and initializer instead (src/hr-mcp-server\Configuration\HRMCPServerConfiguration.cs:1-14; src/hr-mcp-server\Program.cs:9-23).
