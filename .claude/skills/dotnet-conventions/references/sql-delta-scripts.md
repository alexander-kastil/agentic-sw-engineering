# SQL delta scripts instead of EF migrations

Some projects deliberately do not change a database with EF Core migrations. Every schema and data
change ships as a hand-written SQL delta script, authored once and applied identically to each slot.
Where that rule is in force, `dotnet ef migrations add` and `dotnet ef database update` are not part
of the workflow, and a model change means you write the script.

Check the repo before assuming either way: the presence of a `db/deltas/` folder, or a rule in the
project's `CLAUDE.md` or agent definition, decides it. When the rule is in force, the project's own
skill states where the scripts live and what they are named.

The reason is usually a blue/green topology. Two databases behind two slots, with a
`Database.Migrate()` call at container start, applies schema on whichever slot happens to boot first,
at a moment nobody chose. A script is an artifact you can read, dry run, apply in a chosen order, and
verify by counts.

## Where the scripts live

Database artifacts belong in `db/` at the REPOSITORY ROOT, one directory per service, never inside
the .NET project directory:

```
db/<service>/
  readme.md                            the rule and the apply order
  deltas/YYYY-MM-DD-<change-name>.sql  one file per change, named by the date it was authored
  generate-<change-name>.py            optional, when the seed rows come from a data file
```

A delta whose rows come from a JSON or spreadsheet source gets its generator committed beside it, so
the script is regenerated when the source changes rather than hand-patched. That generator is
typically Python, which is the concrete reason the tree sits outside the project: a `.csproj`
directory with a `.py` file and a `__pycache__` in it is wrong on sight, and it was removed from one
repo for exactly that.

## Never reach for `dotnet ef`, including to bootstrap

When a project prohibits migrations, the prohibition covers **generating** them, not only committing
them. `dotnet ef migrations script` to extract the DDL "one last time" before deleting the folder is
still using the banned tool, and it was done in this repository and rejected.

To get `CREATE TABLE` statements for tables that do not exist yet, write them from the
`IEntityTypeConfiguration<T>` classes by hand, or script an existing database with SMO or sqlpackage.

Two traps the model sets that only surface at `CREATE TABLE`, both hit in a real run:

- **A raw check constraint is emitted verbatim**, so any reserved word inside it must be bracketed:
  `t.HasCheckConstraint("CK_X_Trigger", "[Trigger] IS NULL OR [Trigger] IN (...)")`. Unbracketed, the
  script dies with `Incorrect syntax near the keyword 'Trigger'`, and the model builds fine until then.
- **A table mapped `ExcludeFromMigrations` is a read-only mirror of another service's table, and the
  foreign key onto it is real.** Two services that mirror each other cannot both be created first, so
  the create order is its own artifact: one own-tables script per service, then a separate
  cross-service constraints script guarded on the referenced table existing. Those mirrors are also a
  co-location constraint: services whose schemas reference each other share ONE database, whatever
  their names suggest. Grep `ExcludeFromMigrations` and cross-schema `principalSchema` before deciding
  how many databases a stack has.

## What every script contains

1. **A `DB_NAME()` guard, first statement.** `THROW` unless the current database is one this change is
   meant for. A delta applied to the wrong database is the failure this prevents, and it costs two
   lines.
2. **DDL guarded by existence checks.** `IF OBJECT_ID(N'dbo.T') IS NULL CREATE TABLE ...`,
   `IF COL_LENGTH('dbo.T','C') IS NULL ALTER TABLE ...`, indexes behind a `sys.indexes` check. The
   script will be re-run: dev, then each slot, then again after a fix.
3. **No surrogate key the script did not create.** Identity and GUID keys differ per database, so a
   literal id targets a different row on the next slot, or nothing. Resolve existing rows by natural
   key at runtime; for rows the script inserts, capture the generated key with `OUTPUT INSERTED ...
   INTO #Map` and join through that map for the dependent tables.
4. **`THROW` on any unresolved lookup**, selecting the offending rows first so the fix is obvious. A
   half-applied change that inserted NULLs is worse than a script that stopped.
5. **Count verification as the closing statements**, one `SELECT` per table with the expected number
   beside the found one. Exit code 0 means the batch parsed, not that the data is right.

## Reconciling a delta with EF migrations already in the tree

This section applies only while a `Migrations/` folder and a `Database.Migrate()` call still exist.
Once they are deleted, a delta owns the schema outright and must NOT write to
`__EFMigrationsHistory`; any surviving copy of that table is read-only history of what was applied
before the rule, and a new script guards on the object it touches instead.

This is the part that is easy to miss and fails loudly at the worst moment. A project that adopts the
rule mid-life still has old migrations on disk and often still calls `ctx.Database.Migrate()` at
startup. If a delta creates tables that a migration also describes, EF finds that `MigrationId`
absent from `__EFMigrationsHistory`, tries to `CREATE TABLE` again, and the application crashes on
boot against a table the script already made.

So a delta that replaces a migration ends by marking that migration applied:

```sql
DECLARE @ProductVersion nvarchar(32) =
    (SELECT TOP 1 h.[ProductVersion] FROM [__EFMigrationsHistory] h ORDER BY h.[MigrationId] DESC);
INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
SELECT N'<the migration id>', @ProductVersion
WHERE NOT EXISTS (SELECT 1 FROM [__EFMigrationsHistory] h WHERE h.[MigrationId] = N'<the migration id>');
```

Read `ProductVersion` from the table at runtime rather than hardcoding it. The value is also written
into every `*.Designer.cs` and into the model snapshot, so those files tell you what it should be,
but a row you read is evidence and a designer file is inference. Confirm against a real row before
applying anywhere.

Guard the whole script with a second check that `__EFMigrationsHistory` exists at all: its absence
means the target is not the database you think it is.

## Overwrite or preserve is a decision, not a default

Delete-and-reinsert is the simpler script and is correct whenever the table is derived from a source
of truth in the repo and carries no user-entered state. Ask which it is. If the rows can be edited
through an application, the script must preserve those edits and idempotence comes from `MERGE` or
`WHERE NOT EXISTS` instead.

Note what overwriting discards. A C# seeder that matched an existing row by a stable key before
falling back to its label was doing so precisely to survive a rename; delete-and-reinsert drops that
behaviour, which is fine while nobody has used the application and wrong the day someone has. Record
that in the script's readme rather than in a commit message.

## Adding rows to a table a generator already owns

The trap is reaching for the generator. A script that regenerates a whole seed deletes every live row
to append yours: on one catalogue that meant dropping and rebuilding 48 rows in production to add 7.
The addition needs its own script, scoped to the new natural keys.

That script is two halves with a clean seam. The **judgement** half is per repo and belongs in the
repo: which keys are being added, which columns they have, which lookup each child row joins by. The
**deterministic** half is the same everywhere, so it lives here:

```bash
python <repo>/db/<project>/generate-<thing>-additions.py <key> [<key> ...] \
  | python ~/.claude/skills/dotnet-conventions/scripts/gen-additive-delta.py \
      --manifest - --out db/<project>/deltas/<date>-<thing>-additions.sql
```

`scripts/gen-additive-delta.py` takes a manifest (databases, parent table with its natural key and
rows, child tables with their foreign key and any natural-key lookups) and emits a script that is
guarded on `DB_NAME()` and on every table existing, transactional, inserts parents whose key is
absent, updates the same keys in place on a re-run, replaces child rows only for those parents,
throws on an unresolved lookup rather than writing `NULL`, and closes with one count `SELECT` per
table **restricted to those keys**. That last restriction is the point: a whole-table count proves the
run happened, a scoped count proves the scope.

Its own `--help` carries the manifest shape. Harvest the manifest from the repo's source of truth,
never by hand: the fields that decide ordering and membership are exactly the ones a hand-typed
manifest gets wrong.

Verify the same way as any delta, plus one extra check that only applies here: the totals of every
touched table must be **unchanged** by a second run, while the scoped counts still match.

## Adding a column and using it in the same script

SQL Server compiles a whole batch before executing any of it, and deferred name resolution does not
cover a column added earlier in that same batch. So an `ALTER TABLE ... ADD [NewCol]` followed by
anything that names `NewCol` fails to compile, and the script dies on `Msg 207, Invalid column name`
before a single statement runs. This bites the backfill, any `CHECK` constraint over the new column,
any index on it, and any verification `SELECT` that has not been pushed past the final `GO`.

`GO` is not the way out: it ends the explicit transaction the delta is wrapped in. Route every
statement that names the new column through `EXEC sp_executesql`, which compiles at execution time:

```sql
BEGIN TRANSACTION;

IF COL_LENGTH(N'MyTable', N'ApprovalState') IS NULL
BEGIN
    ALTER TABLE [MyTable]
        ADD [ApprovalState] nvarchar(20) NOT NULL
            CONSTRAINT [DF_MyTable_ApprovalState] DEFAULT N'Pending';

    EXEC sp_executesql N'
        UPDATE [MyTable] SET [ApprovalState] = N''Approved'';';
END;

IF NOT EXISTS (SELECT 1 FROM sys.check_constraints WHERE [name] = N'CK_MyTable_ApprovalState')
BEGIN
    EXEC sp_executesql N'
        ALTER TABLE [MyTable]
            ADD CONSTRAINT [CK_MyTable_ApprovalState]
                CHECK ([ApprovalState] IN (N''Pending'', N''Approved'', N''Rejected''));';
END;

COMMIT TRANSACTION;
GO
```

Putting the backfill inside the column-creation branch is deliberate beyond the compile problem: it
runs on the first application only, so a re-run cannot undo a state a person has since changed.

A backfill that marks existing rows as already-approved, already-migrated or already-whatever is how
a new gate is introduced without anything disappearing from a live system. State that in the script's
header comment, because it is the sentence a later reader needs and the one the diff does not carry.

## Extending a delta that has already been applied

The default is a new file: a script that ran is history, and editing it makes the tree disagree with
every database that already took it. The one exception is a migration whose later phase belongs to the
same change as its earlier one (an id column that turns out to need a sibling id turned too), where two
files would leave a half-migrated schema representable. Extend the original only under one condition:

**Each phase carries its own guard, on its own target's real type, so a re-run skips exactly what is
already applied.** Not one guard at the top of the file. A run against a database that took phase 1
prints `Already applied: ... skipping the list id migration.` and proceeds into phase 2, while a fresh
database runs both. That is what makes the extended file honest for the dev box, the test database and
every slot at once.

```sql
IF EXISTS (SELECT 1 FROM sys.columns c
           INNER JOIN sys.types t ON t.user_type_id = c.user_type_id
           WHERE c.object_id = OBJECT_ID(N'dbo.SecretLists') AND c.name = N'ListId'
             AND t.name = N'uniqueidentifier')
BEGIN
    PRINT 'Already applied: dbo.SecretLists.ListId is a uniqueidentifier. Skipping the list id migration.';
    SET NOEXEC ON;
END
GO
```

**Wrap every statement that names a transient column in `sp_executesql`.** A batch is parsed as a whole
before any of it runs, so a statement referencing a column that a *skipped* phase would have created
fails at compile time even though it would never execute. Deferred name resolution covers a missing
table, never a missing column. The string form is what lets one file be correct on both a fresh database
and one mid-migration.

Prove it the way the phases claim: drop and rebuild the test database from the full apply order, and run
the extended file a second time against the already-migrated dev database. Both must be clean, and the
closing `SELECT` must show the same row counts and zero orphans it showed the first time.

## Every environment, including the one with no site

Count the databases before writing the guard. A repo usually has more than the environments it
deploys: the integration-test database the xUnit suite connects to is a real target with no site in
front of it, and it is the one that gets forgotten. A delta can apply cleanly to every deployed slot
and still leave the whole test suite failing on `Invalid column name`, which reads as broken code
rather than as a missing apply.

Find them by reading the connection strings, not by listing the environments: the test factory's
constant, `appsettings*.json`, and the deploy env files. Then name all of them in the `DB_NAME()`
guard, and apply to the test database first: it is the cheapest place for the script to be wrong.

## Apply order

Per slot, never in parallel: apply the script, verify the counts, deploy the application, verify the
application. Schema lands before the build that depends on it, or every query against the new table
throws for the length of the deploy. Prove idempotence for real by running it twice on the first slot
and confirming no count moves.

Applying to a live database is a main-thread action. A subagent authors the script and never runs it.
That names who applies it, not whether it happens. On a local development database the coordinator
applies it on the main thread as the last step of the same run, before reporting, and quotes the
verification counts. A delta left authored while the application that queries the new table keeps
running does not read as a missing apply: it reads as broken code, because the next request throws
`Invalid object name` from inside the feature that was just delivered. A delta that only adds a COLUMN
throws `Invalid column name '<X>'` instead, from a table that plainly exists, which reads even less
like a missing apply. Where the apply genuinely belongs to the user (a deployed slot), it is the single
next action line of the reply, never a clause inside a summary of what went well.

**The split at the permission boundary is what loses the apply.** "A subagent authors the script and
never runs it" is a correct rule that leaves the apply owned by nobody unless the coordinator writes it
into its own task list at the moment it writes the brief. The failure mode is not forgetting the rule;
it is briefing "write it, do not run it", getting a clean report back, and treating that report as the
end of the task. Add the apply and its verification query to the coordinator's own list before the
subagent is dispatched.

Neither a compiler nor a unit test can fail on an unapplied delta: the build validates C# against the
entity, the component tests validate against fixtures, and both are blind to the schema. The only check
that can fail is a live query. If no live query ran, the change is unverified however green the run was.

On a local Windows dev instance the invocation is `sqlcmd -S localhost -E -C -b -W -d "<database>" -i
"<backslash Windows path>"`. `-C` is required for the self-signed certificate. Where an agent harness
classifies shell commands, a `sqlcmd -i` against a live database may be blocked in the POSIX shell and
permitted through the PowerShell tool; try the other interpreter before treating the denial as a wall.

## Proving this still holds

Run the script a second time against the slot you applied it to first. Every `RowsFound` must equal
the `RowsExpected` beside it and must not have moved from the first run. Where the project still has
migrations in the tree, `SELECT COUNT(*) FROM __EFMigrationsHistory WHERE MigrationId = N'<the
migration id>'` must return 1, not 2. If the counts move or the history row duplicates, the script is
not idempotent and the guards described above are missing or misplaced.

Prove the prohibition itself the same way, from the repository root:

```bash
grep -rn "Database\.Migrate\|EnsureCreated\|EntityFrameworkCore\.Design\|IDesignTimeDbContextFactory"   --include="*.cs" --include="*.csproj" src/ | grep -v "/obj/\|/bin/"
find src -type d -name Migrations | grep -v "/obj/\|/bin/"
```

Both must return nothing. A project that prohibits migrations but still carries the Design package or
a design-time factory is one `dotnet ef` away from a violation, and the artifact reads to the next
session as permission.

## Related

- `~/.claude/skills/sql-server/references/portable-multi-env-migration.md`: the environment-agnostic
  scripting technique in depth, including generator-side injective-mapping asserts for scripts whose
  seed rows come from a data file.
- `~/.claude/skills/sql-server/references/sqlcmd-safe-execution.md`: sqlcmd invocation on Windows,
  UTF-8 fidelity, and COMMIT-to-ROLLBACK dry runs. Two traps bite this kind of script specifically:
  `-b` is load-bearing, because without it a `THROW` in an early batch does not stop the run and
  execution falls through into the DDL, and `-i` needs a backslash path on Windows while piping the
  file on stdin runs and prints nothing.
- [`dotnet-efcore`](dotnet-efcore.md): model and `IEntityTypeConfiguration` conventions, which still
  apply unchanged. Only the migration workflow is replaced.
