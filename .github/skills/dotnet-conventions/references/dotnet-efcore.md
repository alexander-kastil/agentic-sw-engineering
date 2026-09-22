# EF Core Patterns

Reference for EF Core 10 usage: configuration, context registration, migrations, and query patterns.

## Hard Rules — Seeding and Migrations

**NEVER add seed data unless explicitly requested by the user.**
Seeding is only valid at initial project setup. Do not add `HasData()` calls, seed methods, or any startup data insertion on your own initiative. Do not add `EnsureMigratedAsync()` or `db.Database.MigrateAsync()` to `Program.cs`.

**NEVER use migrations to insert data.**
Migrations are strictly for schema changes (DDL: tables, columns, indexes, constraints). Do not embed `INSERT`, `UPDATE`, or any DML inside migration `Up()`/`Down()` methods. Data belongs in dedicated seed scripts, delta scripts or import tools — never in migrations and never in application startup.

## When the project prohibits migrations altogether

Some projects ship every schema and data change as a hand-written SQL delta script instead (see
[`sql-delta-scripts`](sql-delta-scripts.md)). Where that rule is in force it is absolute: never
scaffold, generate, script or apply an EF Core migration, and do not reintroduce a `Migrations/`
folder, a `Microsoft.EntityFrameworkCore.Design` package reference, an
`IDesignTimeDbContextFactory<T>`, or a `Database.Migrate()` / `EnsureCreated()` call, including "just
once" to extract DDL or to baseline a database-first schema. Deltas live under the repository's delta
folder, which belongs at the REPOSITORY ROOT and not inside the .NET project (typically
`db/<service>/deltas/`, named `YYYY-MM-DD-<change>.sql`; a Python generator beside a `.csproj` is the
smell that says the tree is in the wrong place).

To get `CREATE TABLE` statements for tables that do not exist yet in such a project, write them by
hand from the `IEntityTypeConfiguration<T>` classes, or script an existing database with SMO or
sqlpackage. Never `dotnet ef`. Everything else in this file (model configuration, context
registration, query patterns, splitting a model across services) still applies unchanged; only the
migration workflow is replaced.

## Entity Configuration

Use `IEntityTypeConfiguration<T>` for all model configuration. Never place data annotations on domain model classes.

```csharp
public class ItemConfiguration : IEntityTypeConfiguration<Item>
{
    public void Configure(EntityTypeBuilder<Item> builder)
    {
        builder.HasKey(i => i.Id);
        builder.Property(i => i.Name).IsRequired().HasMaxLength(200);
    }
}
```

A one-to-one where the dependent's primary key *is* the foreign key needs `WithOne()` and
`HasForeignKey<TDependent>(...)`, not the `WithMany()` every other configuration in the model uses:
see [`sql-stored-files`](sql-stored-files.md).

Apply in `OnModelCreating`:

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
}
```

## Context Registration

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("App")));
```

Connection string in `appsettings.json`:

```json
"ConnectionStrings": {
  "App": "Server=localhost;Database=mydb;Trusted_Connection=True;"
}
```

## Migrations

See `dotnet-cli` for the full command reference. Typical workflow:

```bash
dotnet ef migrations add <Name> --project src/my-api
dotnet ef database update --project src/my-api
```

A running app locks its build output exe, so `dotnet build` / `dotnet ef` can fail with
`MSB3027`/`MSB3021` while it is up. When that app is the user's own `dotnet watch run` session, the
lock is not yours to break. It is also not yours to work around by force: the lock covers
`bin/Debug/<tfm>` only, so `-c Release` or `-o <scratch>` builds past it without disturbing anything
(see [`dotnet-cli`](dotnet-cli.md)). Never `taskkill` a watch process you did not start just to get a
green build.

### Adding migrations to a database-first schema (baseline trick)

When a context maps a **pre-existing, database-first** schema (the DB already exists, was never `ef migrations`-managed, and has no `__EFMigrationsHistory` table), you cannot just `migrations add MyChange` — EF diffs against an *empty* model snapshot and emits `CreateTable` for **every** existing table, which would fail against the live DB. To add only the new tables:

1. **`migrations add InitialBaseline`** first — this captures the entire current model in the snapshot/`Designer`. Then **manually empty its `Up()` and `Down()` bodies** (make it a no-op). It exists only to give the next migration a correct diff baseline; applying it just writes a history row.
2. **`migrations add AddMyTables`** next — now diffed against the baseline snapshot, so it contains `CreateTable` for **only** the genuinely new entities.
3. **`database update`** applies InitialBaseline as a no-op history row, then `AddMyTables`' real DDL.

Never remove, reorder, or hand-edit `InitialBaseline` afterward — every future migration must come *after* it. Verify the migration by generating migrations against a throwaway copy of the source tree if the live API/DB must not be disturbed (`ef` builds the project and needs the DLL unlocked).

### Condensing many migrations into one

Squashing an accumulated migration chain back to a single file is safe **only if the consolidated
migration inherits the id of a migration the deployed databases have already applied** — normally the
first one. Regenerating with a fresh timestamp instead makes every existing database treat it as
pending, so the next `Database.Migrate()` runs `CreateTable` for every table against a populated
schema and the application fails to start.

```bash
# 0. back up the folder, and stop the app (it locks the output exe)
cp -r src/my-api/Migrations <scratch>/migrations-backup
taskkill //F //IM my-api.exe

# 1. clear the folder — migration files AND the model snapshot
rm -f src/my-api/Migrations/*.cs

# 2. regenerate the whole model as one migration (gets a new timestamp)
dotnet ef migrations add InitialBaseline --project src/my-api

# 3. retag it with the id the live databases already have
cd src/my-api/Migrations
mv <new>_InitialBaseline.cs          <old>_InitialBaseline.cs
mv <new>_InitialBaseline.Designer.cs <old>_InitialBaseline.Designer.cs
sed -i 's/\[Migration("<new>_InitialBaseline")\]/[Migration("<old>_InitialBaseline")]/' <old>_InitialBaseline.Designer.cs
```

Then verify, in this order, and do not trust the change until all three pass:

| Check | Expected |
| --- | --- |
| `dotnet ef migrations list` | one entry, **not** marked `(Pending)` |
| `dotnet ef migrations has-pending-model-changes` | "No changes have been made to the model since the last migration." |
| Application startup log | `No migrations were applied. The database is already up to date.` |

Notes that matter:

- **Leave the orphaned history rows alone.** Deployed databases keep a `__EFMigrationsHistory` row per
  squashed migration. EF computes pending as (migrations in the assembly) minus (rows in history), so
  rows with no matching migration are ignored. Deleting them is a write against a live database and
  needs the user's say-so; it buys tidiness, nothing else.
- **A hard-coded baseline id in startup code must still resolve.** If an initializer stamps a constant
  `BaselineMigrationId` onto out-of-band databases, reusing that same id is what keeps it valid.
  Reusing a *different* id silently breaks the stamp.
- **Classify each migration before dropping it.** Schema DDL and `HasData` seeds are regenerated from
  the model. Hand-written DML in `migrationBuilder.Sql()` / `InsertData` is genuinely lost, which is
  fine only when it repairs rows a new database will not have. Grep the regenerated migration for the
  `InsertData` calls you expect.
- This is the one sanctioned exception to "never hand-edit `InitialBaseline`" above: the id is
  preserved precisely so the ordering guarantee still holds.

### Hand-creating a table an EF migration owns

Sometimes one environment's database needs a table before that environment's API image ships — for
example a blue/green pair where the candidate slot has the migration applied and the live slot does
not yet. If you create the table with raw DDL, you **must write the `__EFMigrationsHistory` row in the
same transaction**:

```sql
IF NOT EXISTS (SELECT 1 FROM dbo.__EFMigrationsHistory WHERE MigrationId = '<stamp>_<Name>')
    INSERT INTO dbo.__EFMigrationsHistory (MigrationId, ProductVersion)
    VALUES ('<stamp>_<Name>', '<version copied from the database that already has it>');
```

Without that row, the next `Database.Migrate()` re-runs `CreateTable` against a table that already
exists and **the application fails to start**. Rules:

- Transcribe the DDL from the migration's `Up()` verbatim: identity seed, column types *and* lengths,
  PK name, FK name, cascade behaviour, index name. A table that differs from what EF would have built
  is a silent model/schema mismatch later.
- Copy `ProductVersion` from the database that already has the migration; do not invent it.
- Guard the script with `IF DB_NAME() <> '<target>' RAISERROR(...)` so it cannot hit the wrong database.
- Verify parity afterwards by diffing `sys.columns` / `sys.indexes` / `sys.foreign_keys` between the two
  databases, not by reading the script back.

An extra history row is harmless for an older image whose assembly does not contain that migration —
EF only compares history against the migrations present in the assembly. For the sqlcmd mechanics
(dry runs, guards, structure diffing) see the `sql-server` skill, `sqlcmd-safe-execution` reference.

## Query Patterns

| Pattern | Code |
|---|---|
| Read all (no tracking) | `await db.Items.AsNoTracking().ToListAsync()` |
| Read by primary key | `await db.Items.FindAsync(id)` |
| Filtered read | `await db.Items.AsNoTracking().Where(i => i.Name == name).ToListAsync()` |
| Add and save | `db.Items.Add(entity); await db.SaveChangesAsync()` |
| Remove and save | `db.Items.Remove(entity); await db.SaveChangesAsync()` |

Always use `AsNoTracking()` for read-only queries to reduce memory overhead and avoid unintended change tracking.

## Splitting one EF model across services

When a single entity model has to become two or three services (one database, several owners), the
boundary is already written down: it is the set of `HasOne<T>()` calls that cross the areas you want
to separate. Find them before moving a file:

```bash
for f in Configuration/*Configuration.cs; do
  echo -n "$f: "; grep -o "HasOne<[A-Za-z]*>" "$f" | sort -u | tr '\n' ' '; echo
done
```

An area whose configurations only reference their own types moves cleanly. Every reference that
points outside becomes one of two things, and never a deleted relationship:

- **A read-only mirror.** Declare the principal entity in the borrowing service with just the key and
  identifying columns, and map it `ToTable("X", "schema", t => t.ExcludeFromMigrations())`. The
  foreign key stays expressed, the table stays owned by one service, and no migration in the
  borrower tries to create it.
- **A soft link.** Keep the column, drop the constraint, and say so in writing. Only where the
  services will genuinely not share a database.

Guard the partition in the context rather than in review: override `OnModelCreating`, call
`ApplyConfigurationsFromAssembly`, then walk `modelBuilder.Model.GetEntityTypes()` and throw if any
entity is neither the tenant marker interface (`ITenantOwned`) nor on a short reviewed allow-list of
genuinely global tables. A model that cannot build is a partition that cannot silently regress.

Order of operations when the code moves between repositories: copy excluding `bin`/`obj`,
`diff -rq` the copy against the source, build the copy, and only then delete the source. Check
`git ls-files` on the source first: an untracked project has no history to fall back on, and that is
exactly the kind that turns out to hold the only copy of a schema.
