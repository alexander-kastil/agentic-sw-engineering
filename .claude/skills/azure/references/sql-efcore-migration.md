# Move a .NET EF Core app from SQLite to Azure SQL

Full order of work. Do the steps in sequence.

1. Provision Azure SQL: [sql-provision.md](sql-provision.md) / [sql-bicep.md](sql-bicep.md) (server, database, firewall rule, post-deploy Entra ID admin).
2. Switch the EF Core project: sections 1-4 below.
3. Configure authentication: [sql-auth.md](sql-auth.md).
4. Apply the schema: `dotnet ef database update --connection "<sql-auth-conn-str>"`.
5. Copy existing SQLite data: prefer the standalone migrator (section 6) over the embedded controller (section 5); it truncates first and avoids seeding conflicts.
6. After migration is confirmed: delete the migration controller and the temporary `Microsoft.Data.Sqlite` package reference.

## 1. csproj

| Action | Package |
| --- | --- |
| Remove | `Microsoft.EntityFrameworkCore.Sqlite` |
| Add | `Microsoft.EntityFrameworkCore.SqlServer` (same version as the removed package) |
| Add temporarily | `Microsoft.Data.Sqlite` (needed by the data migration controller; remove after migration is confirmed) |

## 2. Program.cs

- Remove `using Microsoft.Data.Sqlite;`.
- Replace the SQLite registration:

```csharp
options.UseSqlServer(builder.Configuration.GetConnectionString("Family"))
```

- Remove SQLite-specific directory-creation code (anything parsing `DataSource=` out of the connection string and calling `Directory.CreateDirectory`).

## 3. Migrations

Delete the whole `Migrations/` folder. SQLite migrations are not compatible with SQL Server.

Add an `IDesignTimeDbContextFactory` so `dotnet ef` runs without a live Azure SQL connection:

```csharp
public class FamilyDbContextFactory : IDesignTimeDbContextFactory<FamilyDbContext>
{
    public FamilyDbContext CreateDbContext(string[] args)
    {
        var options = new DbContextOptionsBuilder<FamilyDbContext>()
            .UseSqlServer("Server=.;Database=<db>-design;Trusted_Connection=True;")
            .Options;
        return new FamilyDbContext(options);
    }
}
```

```bash
dotnet ef migrations add InitialCreate
```

Verify the generated migration uses SQL Server types: `uniqueidentifier`, `nvarchar`, `datetime2`, `bit`.

## 4. Type mapping (EF Core converts automatically on provider switch)

| SQLite | SQL Server |
| --- | --- |
| TEXT (Guid) | uniqueidentifier |
| TEXT (string) | nvarchar(max) / nvarchar(450) for indexed |
| TEXT (DateTime) | datetime2 |
| INTEGER (bool) | bit |
| REAL (double) | float |
| BLOB (byte[]) | varbinary(max) |
| INTEGER (int) | int |

## 5. Data migration controller (dev-only, remove after)

- Route: `POST /migrate/sqlite-to-sql?sqlitePath=family.db`
- Guard: `Forbid()` when not Development.
- Opens an ADO.NET `SqliteConnection` to the local `family.db`.
- Reads each table row by row, coercing types (`Guid.Parse` for TEXT GUIDs, `reader.GetInt32() == 1` for booleans).
- Inserts via EF Core in a transaction; rolls back entirely on failure.
- Returns `Dictionary<string, int>` of row counts per table.

### Seeding conflict: clear tables first

`EnsureApiModelsSeededAsync` and `EnsureUsersSeededAsync` run at startup and insert rows before the endpoint is ever called. Calling it afterwards throws a duplicate-key error on the `IX_ApiModelSettings_Name` unique index (and potentially on Users).

Fix: truncate all tables with `sqlcmd`, then call the endpoint once.

```powershell
sqlcmd -S "." -d "<db-name>" -Q "DELETE FROM ChatLogs; DELETE FROM TreeVersions; DELETE FROM InvitationCodes; DELETE FROM Edges; DELETE FROM Persons; DELETE FROM Users; DELETE FROM ApiModelSettings;"
Invoke-RestMethod -Method POST "http://localhost:5122/migrate/sqlite-to-sql"
```

Deletion order matters when FK constraints are enforced. Safe order: dependents first (ChatLogs, TreeVersions, InvitationCodes, Edges, then Persons, then Users, then ApiModelSettings).

```csharp
[ApiController]
[Route("migrate")]
public class MigrationController : ControllerBase
{
    private readonly FamilyDbContext _db;
    private readonly IWebHostEnvironment _env;

    public MigrationController(FamilyDbContext db, IWebHostEnvironment env)
    {
        _db = db;
        _env = env;
    }

    [HttpPost("sqlite-to-sql")]
    public async Task<IActionResult> MigrateAsync([FromQuery] string sqlitePath)
    {
        if (!_env.IsDevelopment()) return Forbid();

        var counts = new Dictionary<string, int>();

        await using var sqlite = new SqliteConnection($"Data Source={sqlitePath}");
        await sqlite.OpenAsync();

        await using var tx = await _db.Database.BeginTransactionAsync();
        try
        {
            await using (var cmd = sqlite.CreateCommand())
            {
                cmd.CommandText = "SELECT Id, FirstName, LastName, BirthDate, DeathDate, OriginCountry FROM Persons";
                await using var reader = await cmd.ExecuteReaderAsync();
                int n = 0;
                while (await reader.ReadAsync())
                {
                    _db.Persons.Add(new Person
                    {
                        Id = Guid.Parse(reader.GetString(0)),
                        FirstName = reader.IsDBNull(1) ? null : reader.GetString(1),
                        LastName = reader.IsDBNull(2) ? null : reader.GetString(2),
                        BirthDate = reader.IsDBNull(3) ? null : reader.GetString(3),
                        DeathDate = reader.IsDBNull(4) ? null : reader.GetString(4),
                        OriginCountry = reader.IsDBNull(5) ? null : reader.GetString(5),
                    });
                    n++;
                }
                counts["Persons"] = n;
            }

            await _db.SaveChangesAsync();
            await tx.CommitAsync();
        }
        catch
        {
            await tx.RollbackAsync();
            throw;
        }

        return Ok(counts);
    }
}
```

Extend per table (`Edges`, `ApiModelSettings`, ...) by adding more `using` blocks before `SaveChangesAsync`.

## 6. Standalone data migrator (preferred)

Use instead of the controller when startup seeding creates conflicting primary-key GUIDs, or when you want a truncate-first run without starting the app.

Layout, e.g. `.tools/migrator/`:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Data.Sqlite" Version="10.0.0" />
    <PackageReference Include="Microsoft.Data.SqlClient" Version="6.0.2" />
  </ItemGroup>
</Project>
```

Workflow (`Program.cs`, top-level statements):

1. Open `SqliteConnection` to the source db and `SqlConnection` to Azure SQL.
2. Truncate target tables with `DELETE FROM [TableName]` in a transaction (dependents first; with no FK constraints any order works).
3. Read each SQLite table via `SqliteCommand` / `SqliteDataReader`.
4. Insert into Azure SQL via `SqlCommand` with parameterised `INSERT`.
5. Commit per table.

Run: `dotnet run -- path/to/family.db`

Type coercion:

| SQLite storage | C# conversion |
| --- | --- |
| TEXT (Guid) | `Guid.Parse(reader.GetString(i))` |
| TEXT (DateTime) | `DateTime.TryParse(reader.GetString(i), out var d) ? d : DateTime.UnixEpoch` |
| INTEGER (bool) | `reader.GetInt32(i) == 1` |
| BLOB (`byte[]`) | see varbinary note |

### Critical: varbinary(max) columns

`AddWithValue` infers `nvarchar` for `byte[]` / `DBNull.Value` and throws `"Implicit conversion from nvarchar to varbinary(max) is not allowed"`. Declare the parameter explicitly:

```csharp
var p = cmd.Parameters.Add("@photoData", System.Data.SqlDbType.VarBinary, -1);
p.Value = reader.IsDBNull(colIdx) ? DBNull.Value : (object)((byte[])reader[colIdx]);
```

## Siblings

- [sql-publish-bacpac.md](sql-publish-bacpac.md): full-replace copy of a local DB over the online one.
- [cli-conventions.md](cli-conventions.md): az CLI basics.
