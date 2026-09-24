# HR Current State: Filling Open Positions

Source: `ledger.md` (Process, Excel, Data structure, Implementation findings).

## Inventory

- **Tracking tool**: `vacancies-tracker.xlsx`, two sheets: `Vacancies` (4 rows: 3 vacancies plus headers, of which 2 are Open and 1 is Filled) and `Staff Copy` (6 employee rows, a manual snapshot of staff data) (ledger.md, Excel).
- **Vacancies sheet columns**: Id, Title, Department, Required Skills, Languages, Status, Opened, Days Open (formula `=IF(Fn="Open",TODAY()-Gn,"")`), Internal Candidates, Owner (ledger.md, Excel).
- **Staff Copy sheet columns**: Name, Role, Skills, Languages, Copied On — a static, manually pasted snapshot with no formulas (ledger.md, Excel).
- **Process**: an 8-step manual workflow (add vacancy row → ask Copilot Chat for employees → copy skills into Staff Copy → filter and type candidate names into Vacancies → correct stale rows by hand → email owner → repeat per vacancy → update role and set Status when filled → weekly summary by counting rows) taking roughly 130 minutes total across two vacancies (ledger.md, Process).
- **MCP server**: HR MCP server at `src/hr-mcp-server` exposes 5 tools — `ListEmployees`, `AddEmployee`, `UpdateEmployee`, `RemoveEmployee`, `SearchEmployees` — backed by `EmployeeService` and an EF Core `EmployeeDbContext` over SQLite table `Candidates` in `hr-data.db` (ledger.md, Implementation).
- **Data model**: `Employee` has Id, FirstName, LastName, Email (unique), CurrentRole, SpokenLanguagesData/SpokenLanguages, SkillsData/Skills; no vacancy, position, or department entity exists anywhere in the model (ledger.md, Data structure).
- **Seed data**: 8 restaurant-staff employees are seeded on startup if the table is empty (ledger.md, Implementation).

## How it is used

- HR records a new vacancy by hand-typing a row into the `Vacancies` sheet (title, skills, languages) — 5 minutes (ledger.md, Process).
- To find internal candidates, HR asks the Copilot Chat HR assistant to list all employees, then manually re-types/copies name, role, skills, and languages into `Staff Copy` — 20 minutes per refresh (ledger.md, Process).
- HR filters `Staff Copy` by skill and hand-types matching names into the `Internal Candidates` column of `Vacancies` — 15 minutes (ledger.md, Process).
- When Staff Copy rows are found stale, HR re-queries Copilot Chat and manually fixes the rows — 15 minutes (ledger.md, Process).
- The candidate shortlist is pasted from Excel into an Outlook email to the vacancy owner — 10 minutes (ledger.md, Process).
- The whole Staff Copy re-copy and filter cycle repeats per vacancy (a second vacancy costs another 40 minutes) (ledger.md, Process).
- When a role is filled, HR updates the employee's role through the assistant and manually sets `Status` to `Filled` in Excel — 10 minutes (ledger.md, Process).
- A weekly summary is produced by manually counting open rows and reading the `Days Open` formula column — 15 minutes (ledger.md, Process).
- `Days Open` is the only metric management currently asks for, computed purely inside the spreadsheet with `=IF(Status="Open",TODAY()-Opened,"")` (ledger.md, Excel; ledger.md, Process).

## Limits

- **No vacancy data in the server**: the EF model and SQLite database only contain `Employee`/`Candidates`; there is no vacancy, position, department, or "internal candidates" table or entity anywhere in `Models.cs`, `EmployeeDbContext.cs`, or `hr-data.db` (ledger.md, Data structure).
- **Re-copying is the acknowledged bottleneck**: the process note explicitly states "the biggest cost is re-copying staff into Excel each time because the HR assistant knows the employees but not the vacancies" (ledger.md, Process).
- **Staff Copy drifts from the real employee data** — comparing the `Staff Copy` sheet to the live `Candidates` table in `hr-data.db` shows:
  - `Staff Copy` has only 6 employee rows; `hr-data.db` has 8. **Anna Schmidt** and **Kenji Tanaka** exist in `hr-data.db` (Ids 4 and 6) but are entirely missing from `Staff Copy` (Staff Copy sheet rows 2-7; `hr-data.db` Candidates table, `SELECT * FROM Candidates`).
  - `Staff Copy` row "Olga Petrova" (Copied On 2026-08-01, the oldest/stale timestamp) does not match `hr-data.db` Id 7 "Olga Ivanova": last name differs, role differs (`Waitress` vs `Hostess`), skills differ (`Customer Service` only vs `Hostess; Reservation Management; Multilingual Communication; Conflict Resolution`), and languages differ (missing German) (Staff Copy row 6; `hr-data.db` Candidates Id 7).
  - `Staff Copy` row "Ahmed Khan" does not match `hr-data.db` Id 8 "Ahmed Hassan": last name differs, skills differ (`Grilling; Food Safety` vs `Grill Chef; Meat Preparation; Kitchen Safety; Teamwork`), and languages differ (missing French) (Staff Copy row 7; `hr-data.db` Candidates Id 8). These two rows correspond to the "two Staff Copy names were found to be out of date" step in the process notes (ledger.md, Process, line 10).
  - `Staff Copy` row "Luca Rossi" is close but incomplete versus `hr-data.db` Id 3: missing the "Table Management" skill and missing "Spanish" as a spoken language (Staff Copy row 4; `hr-data.db` Candidates Id 3).
  - Carlos Gomez, Marie Dubois, and Sofia Fernandez match exactly between the sheet and the database (Staff Copy rows 2, 3, 5; `hr-data.db` Candidates Ids 1, 2, 5).
- **No relational link between vacancies and employees**: `Internal Candidates` in the `Vacancies` sheet is a free-text semicolon-separated name string, not a foreign key or lookup against any employee table (ledger.md, Excel).
- **No search-by-skill capability server-side for vacancies**: `SearchEmployeesAsync` matches a free-text term against employee fields only; it has no notion of "required skills for vacancy X" or department/language matching combined (ledger.md, Implementation).
- **No days-open, status, or vacancy-count logic in the server**: these are pure Excel formulas/manual counts with no equivalent MCP tool or stored field (ledger.md, Excel; ledger.md, Implementation).
- **Configuration dead code**: `HRMCPServerConfiguration.EmployeesPath` is defined but unused; actual storage is the SQLite connection string, so any future file-based vacancy config should not assume this setting is wired up (ledger.md, Implementation).

## Gap list

Capability ratings are **exists**, **partly exists**, or **missing** in the HR MCP server, each against what HR actually does in the workbook today.

| Capability (used in workbook) | Rating | Ledger evidence |
| --- | --- | --- |
| Record a vacancy | **Missing** | No vacancy/position entity, DbSet, or MCP tool exists; only `Employee`/`Candidates` is modeled (ledger.md, Data structure: "Models.cs defines Employee and EmployeeCollection only"; ledger.md, Implementation: 5 tools listed, none vacancy-related). Today this is a manual row typed into `Vacancies` sheet A2:J2 (ledger.md, Process, line 7; ledger.md, Excel, sheet Vacancies). |
| List and close vacancies | **Missing** | No tool lists vacancies or sets a Status/Filled state; `Status` is a plain Excel cell HR edits by hand (ledger.md, Process, line 13; ledger.md, Excel, column F "Status"). The server's only list-type tool, `ListEmployees`, returns employees, not vacancies (ledger.md, Implementation: "ListEmployees() -> Task<EmployeeCollection>"). |
| Find matching employees for a vacancy | **Partly exists** | `SearchEmployees(searchTerm)` can already search employees by skill/role/language text server-side (ledger.md, Implementation: "SearchEmployeesAsync... filters in memory for case-insensitive matches across FirstName, LastName, Email, CurrentRole, any Skills, or any SpokenLanguages"), which is exactly the data HR currently re-copies into `Staff Copy` to filter by hand (ledger.md, Process, line 8-9). What's missing is any concept of "required skills of vacancy X" to drive that search automatically, and a way to record the resulting `Internal Candidates` list against a vacancy (ledger.md, Data structure: no vacancy entity; ledger.md, Excel, column I "Internal Candidates" is free text). |
| Days open (per-vacancy age / weekly summary) | **Missing** | `Days Open` is purely an Excel formula (`=IF(Status="Open",TODAY()-Opened,"")`) with no `Opened` date, `Status`, or computed-age field anywhere in `Models.cs`, `EmployeeDbContext.cs`, or `hr-data.db` (ledger.md, Excel, column H; ledger.md, Data structure: only Employee fields listed). The weekly summary is produced by HR manually counting open rows and reading this column (ledger.md, Process, line 14). |

**Net finding**: the server already solves the piece HR repeatedly re-copies by hand — querying and filtering employee skills/languages (`SearchEmployees`) — but has zero notion of a vacancy as a first-class entity, so nothing about recording, listing, closing, or aging vacancies is available yet; a vacancies feature needs a new `Vacancy` entity/table plus tools that reuse the existing employee search instead of duplicating it.
