# Vacancies Feature Plan

HR needs to record open positions (vacancies) in the same `hr-mcp-server` that already manages employees, following the existing patterns exactly: a JSON-backed EF Core model persisted in SQLite via `EmployeeDbContext`/`EmployeeDbInitializer`, a `VacancyService` mirroring `EmployeeService` for business logic and in-memory matching, and a new `[McpServerToolType]` tool class exposing `AddVacancy`, `ListVacancies`, `CloseVacancy`, and `MatchVacancyCandidates` with the same required/optional parameter and DTO-return conventions used by `HRTools`. Verification reuses the project's only test method: the MCP Inspector smoke test against the local HTTP server, extended to confirm the new tools are listed and behave correctly end-to-end, since the project has no automated test suite.

## Tasks

### 1. Add the `Vacancy` model and status representation
- **Files:** `src/hr-mcp-server/Tools/Models.cs`
- **Depends on:** none
- **Details:** Add a `Vacancy` class mirroring `Employee`'s conventions: `Id: int` (`[JsonIgnore]`), `Title: string`, `RequiredSkillsData: string`/`RequiredSkills: List<string>` (`[NotMapped]`, JSON name `required_skills`), `RequiredLanguagesData: string`/`RequiredLanguages: List<string>` (`[NotMapped]`, JSON name `required_languages`), and a `Status: string` property (`"open"` or `"filled"`, JSON name `status`) with a required, defaulted value of `"open"`. Reuse the existing `SerializeList`/`DeserializeList` helpers for the JSON-backed list properties. Add a `VacancyCollection` DTO wrapper class (`List<Vacancy> Vacancies`) alongside `EmployeeCollection`.
- **Acceptance criteria:** `Vacancy` and `VacancyCollection` compile, follow the exact JSON-property-naming and `[NotMapped]`/backing-field pattern used by `Employee`, and default `Status` to `"open"` when not supplied.

### 2. Register `Vacancy` in the DbContext
- **Files:** `src/hr-mcp-server/Data/EmployeeDbContext.cs`
- **Depends on:** Task 1
- **Details:** Add `DbSet<Vacancy> Vacancies`. In `OnModelCreating`, map `Vacancy` to a `Vacancies` table, configure `Id` as primary key, `Title` required with a sensible max length (e.g. 200), `RequiredSkillsData` and `RequiredLanguagesData` as required `TEXT`, and `Status` required with a short max length (e.g. 20). No unique index is needed on `Title` (multiple vacancies can share a title).
- **Acceptance criteria:** `EmployeeDbContext` exposes `Vacancies`, `EnsureCreatedAsync` (used in initializer) creates a `Vacancies` table with the configured columns, and no changes are made to the existing `Candidates`/`Employee` mapping. Because `EnsureCreatedAsync` only creates the schema when the database file does not yet exist and never alters an existing database, an existing `src/hr-mcp-server/hr-data.db` from before this change must be deleted so the next run recreates the schema (including the new `Vacancies` table) and reseeds both tables.

### 3. Seed sample vacancies in the initializer
- **Files:** `src/hr-mcp-server/Data/EmployeeDbInitializer.cs`
- **Depends on:** Task 2
- **Details:** Add a `GetSeedVacancies()` method returning a small hard-coded list (e.g. 3-4 vacancies with varied titles, skills, languages, and at least one already `"filled"`). In `InitializeAsync`, after the existing employee `EnsureCreatedAsync`/seed check, add an equivalent idempotent check for vacancies (`if (!await context.Vacancies.AnyAsync()) { ... }`) so re-running the initializer does not duplicate vacancies, independent of the employee seeding decision.
- **Acceptance criteria:** On a fresh `hr-data.db`, both employees and vacancies are seeded; on a subsequent run with existing data, neither table is reseeded; deleting only the vacancy rows and restarting reseeds vacancies without touching existing employees (subject to the existing coarse-grained `AnyAsync` check per table).

### 4. Add `VacancyService` with matching logic
- **Files:** `src/hr-mcp-server/Services/VacancyService.cs` (new), `src/hr-mcp-server/Services/IVacancyService.cs` (new, if the project uses a separate interface file matching `IEmployeeService`'s location)
- **Depends on:** Task 2
- **Details:** Create `IVacancyService`/`VacancyService` constructor-injected with `EmployeeDbContext` and `ILogger<VacancyService>`, mirroring `EmployeeService`. Implement: `AddVacancyAsync(title, requiredSkills, requiredLanguages)` (status defaults to `"open"`); `ListVacanciesAsync(string? status = null)` returning all vacancies or filtered by status; `CloseVacancyAsync(int vacancyId)` (or by title, matching whichever identity convention is simpler—prefer `Id` since vacancy titles aren't unique) setting `Status` to `"filled"`, returning a not-found message if missing; `FindMatchingEmployeesAsync(int vacancyId)` that loads the vacancy and all employees with `AsNoTracking().ToListAsync()` (matching `EmployeeService`'s existing in-memory-matching pattern since skills/languages are `[NotMapped]`), then returns employees whose `Skills` list intersects the vacancy's `RequiredSkills` (case-insensitive), optionally reporting the match count or matched skill names.
- **Acceptance criteria:** Service methods compile and follow the existing `EmployeeService` error-message conventions (plain string outcomes for mutations, DTOs for queries); `FindMatchingEmployeesAsync` returns only employees with at least one overlapping skill, case-insensitively, and returns an empty result (not an exception) when no employees match or the vacancy id doesn't exist.

### 5. Register `VacancyService` in DI
- **Files:** `src/hr-mcp-server/Program.cs`
- **Depends on:** Task 4
- **Details:** Add `builder.Services.AddScoped<IVacancyService, VacancyService>();` next to the existing `AddScoped<IEmployeeService, EmployeeService>()` registration. No other startup changes are needed since `WithToolsFromAssembly()` auto-discovers new `[McpServerToolType]` classes.
- **Acceptance criteria:** App starts with `dotnet run` without DI resolution errors; `VacancyService` is resolvable wherever `IVacancyService` is requested.

### 6. Add vacancy MCP tools
- **Files:** `src/hr-mcp-server/Tools/VacancyTools.cs` (new)
- **Depends on:** Task 5
- **Details:** Create an `internal class VacancyTools` marked `[McpServerToolType]`, constructor-injected with `IVacancyService` and `ILogger<VacancyTools>`, exposing methods with `[McpServerTool]` + `[Description]` on the class, methods, and parameters, following `HRTools`'s naming (method name = tool name) and parameter conventions (required non-nullable params first, optional nullable/defaulted params after):
  - `AddVacancy(string title, string requiredSkills = "", string requiredLanguages = "")` → `Task<string>` (or a DTO if consistent with `AddEmployee`'s return type—check final return type of `AddEmployee` and match it) confirming creation.
  - `ListVacancies(string? status = null)` → `Task<VacancyCollection>`.
  - `CloseVacancy(int vacancyId)` → `Task<string>` confirming status change or reporting not-found.
  - `MatchVacancyCandidates(int vacancyId)` → `Task<EmployeeCollection>` (reuses the existing DTO) returning employees whose skills match the vacancy's required skills.
  Parse comma-separated `requiredSkills`/`requiredLanguages` using the existing `ParseCommaSeparatedString(...)` helper, matching `AddEmployee`'s handling.
- **Acceptance criteria:** New tools appear in `tools/list` via the MCP Inspector; parameter descriptions and required/optional shape match the conventions documented in the ledger; return types/serialization match sibling tools (`ListEmployees`/`SearchEmployees`).

### 7. Update readme with vacancy tool documentation and smoke test steps
- **Files:** `src/hr-mcp-server/readme.md`
- **Depends on:** Task 6
- **Details:** Add the four new tools to whatever tool listing/table already documents `list_employees`, `add_employee`, etc. Extend the manual smoke-test section with steps to confirm the vacancy tools are listed, seed data is present (call `list_vacancies` and expect the seeded count/status mix), and a full round trip: add a vacancy, list it as `"open"`, call `match_vacancy_candidates` against a seed vacancy whose skills overlap a seeded employee, then close it and confirm status becomes `"filled"`.
- **Acceptance criteria:** readme accurately lists all 9 tools (5 employee + 4 vacancy) and gives copy-pasteable Inspector CLI commands for the new tools, consistent with the existing `tools/call --tool-name list_employees` example style.

### 8. Manual verification pass
- **Files:** none (verification only; may touch `src/hr-mcp-server/hr-data.db` as a side effect of running the app, which is not source-controlled)
- **Depends on:** Task 7
- **Details:** If `src/hr-mcp-server/hr-data.db` already exists from before this change, delete it first so `EnsureCreatedAsync` recreates the schema with the new `Vacancies` table and reseeds both employees and vacancies. Run `dotnet run` from `src/hr-mcp-server`, launch `npx @modelcontextprotocol/inspector --config inspector.config.json --server hr-mcp`, confirm `tools/list` now returns 9 tools, then execute the round trip from Task 7 (add → list → match → close → list) via `--cli ... --method tools/call --tool-name ...` commands and confirm each response matches expectations (correct status transitions, correct matched employees, no exceptions).
- **Acceptance criteria:** All 9 tools listed; `add_vacancy` creates a vacancy with `status: "open"`; `list_vacancies` reflects it; `match_vacancy_candidates` returns only employees with overlapping skills; `close_vacancy` flips status to `"filled"` and a subsequent `list_vacancies` confirms it; no unhandled exceptions or DB errors in server console output.
