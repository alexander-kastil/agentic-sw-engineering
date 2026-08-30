# dotnet-cli

Quick reference for .NET CLI commands. Use these instead of editing `.csproj` files directly.

## When to Use

- Building or compiling .NET projects and solutions
- Running unit or integration tests with filtering
- Managing NuGet packages (add, remove, update, restore)
- Formatting and linting C# code with `dotnet format`
- Using hot reload / watch mode during development
- Organizing multi-project solutions
- Troubleshooting build failures and dependency issues
- Publishing applications to a target runtime or folder

## Build

| Command | Description |
|---|---|
| `dotnet build` | Build the project or solution in Debug configuration |
| `dotnet build --configuration Release` | Build in Release configuration |

## Run and Watch

| Command | Description |
|---|---|
| `dotnet run` | Build and run the project |
| `dotnet watch run` | Run with hot reload — restarts on file changes |

## Test

| Command | Description |
|---|---|
| `dotnet test` | Run all tests |
| `dotnet test --filter "ClassName=ItemsControllerTests"` | Run tests matching a class name |
| `dotnet test -v n` | Run tests with normal verbosity output |
| `dotnet test --logger "console;verbosity=detailed"` | Show each failure's Error Message and Stack Trace — `-v q`/`-v n` print only the `[FAIL]` names |
| `dotnet test -c Release` | Run the suite while the app is up under `dotnet watch` |

A running app locks `bin/Debug/<tfm>`, so a plain `dotnet test` against a project that references it fails
with `MSB3021`/`MSB3027` while the watch is up. The lock is on that one output directory, not on the
project: `-c Release` builds into `bin/Release/<tfm>` and runs green without touching the watch. Same
trick for a compile check, with `dotnet build <proj> -o <scratch>`. Never stop or kill a watch you did
not start just to get a green run. Neither flag makes the *running* process current, though: a rude
edit is not hot-applied, so a green Release suite says nothing about the code the live app is serving.

## NuGet

| Command | Description |
|---|---|
| `dotnet add package <Name>` | Add a NuGet package reference |
| `dotnet remove package <Name>` | Remove a NuGet package reference |
| `dotnet restore` | Restore all package dependencies |
| `dotnet list package` | List all package references in the project |

## EF Core Migrations

| Command | Description |
|---|---|
| `dotnet ef migrations add <Name>` | Scaffold a new migration |
| `dotnet ef database update` | Apply pending migrations to the database |
| `dotnet ef migrations remove` | Remove the last unapplied migration |

Prefix with `--project <path>` when running from the solution root:

```bash
dotnet ef migrations add AddIndexTable --project src/my-api
dotnet ef database update --project src/my-api
```

Apply against a Release build/output (`--configuration Release`) rather than the `bin/Debug` output a
running API holds locked.

**Some projects prohibit `dotnet ef` outright.** Where schema and data changes ship as hand-written
SQL delta scripts (typically a blue/green topology with a `db/<project>/deltas/` folder), none of
`migrations add`, `migrations script`, `migrations remove`, `database update` or `dbcontext scaffold`
may be run, in any project, for any reason: not even once to extract DDL or to baseline a
database-first schema. Check the repo's `CLAUDE.md` and its own skill before running any of them, and
see [`sql-delta-scripts`](sql-delta-scripts.md).

## Publish

| Command | Description |
|---|---|
| `dotnet publish -c Release -o ./publish` | Publish to the `./publish` folder in Release configuration |

## Format

| Command | Description |
|---|---|
| `dotnet format` | Format all C# files to match `.editorconfig` rules |

## Solution Management

| Command | Description |
|---|---|
| `dotnet new sln` | Create a new solution file |
| `dotnet sln add <project>` | Add a project to the solution |
| `dotnet sln list` | List all projects in the solution |

## A build that fails only on the copy step, on a checkout shared with other sessions

```text
error MSB3027: Could not copy "obj\Debug\net10.0\apphost.exe" to "bin\Debug\net10.0\app.exe".
Exceeded retry count of 10. Failed. The file is locked by: "app (68264)"
```

The compile succeeded. Read the error list before reacting: `MSB3021`, `MSB3026` and `MSB3027` are
the copy step, and a run that reports them and nothing else has already produced a valid assembly.
The lock is a running instance of the app holding its own exe.

**Read the error CODE before the message.** An `MSB3xxx` file-copy lock is a process problem and a
`CSxxxx` is a code problem, and only the second is a reason to open a source file. The failure this
prevents is not a slow diagnosis, it is a false one: the output says "Build FAILED", so a session
that reads the message and not the code edits code that was already correct, or reports the build as
broken and files it as a limitation it cannot fix. The fix is to stop the process, or to build a
project the running app does not lock, or to build to a scratch directory as above.

**Whose instance it is decides what you may do.** On a checkout several sessions share, the pid in
the message is often not yours. Check before killing it:

```bash
# what it is, and since when
powershell -c "Get-Process -Id <pid> | Select-Object Id,ProcessName,@{n='Started';e={\$_.StartTime}}"
netstat -ano | grep LISTENING | grep "\s<pid>\$"
```

A process you started this session is yours to stop. One started hours earlier belongs to someone
else's work: ask before `taskkill //PID <pid> //F`, and say in the report that you killed it.

**To prove the code compiles without touching anyone's process**, build to a scratch output:

```bash
dotnet build <proj>.csproj -p:BaseOutputPath="$TEMP/scratch/"
```

Redirect only the OUTPUT path. Redirecting `BaseIntermediateOutputPath` as well produces
`CS0579: Duplicate 'System.Reflection.AssemblyVersionAttribute'`, because the generated
`AssemblyInfo.cs` is then emitted twice, and that is a false failure of your own making.

Confirm the scratch assembly is the new code rather than a cached copy, by looking for a symbol
that only exists after the change:

```bash
grep -a -o -E "GetDetailBy[A-Za-z]+" "$TEMP/scratch/Debug/net10.0/<app>.dll" | sort -u
```

`strings` is not present in Git Bash on Windows; `grep -a` over the dll does the same job here.

**When all you need is the compiler's verdict, skip the scratch output entirely** and stop before the
copy step that takes the lock:

```bash
dotnet build -t:Compile --no-incremental
```

`-t:Compile` runs `CoreCompile` without the `Build` target's copy-to-`bin`, so a held exe cannot fail
it. Add `--no-incremental` or an unchanged-looking project answers "All projects are up-to-date" and
never recompiles your edit. Judge the run ONLY on lines matching `error CS` or `warning CS`:

```bash
dotnet build -t:Compile --no-incremental 2>&1 | grep -E "(error|warning) CS"
```

An empty result is the pass. `MSB3021`, `MSB3026` and `MSB3027` may still appear in the same output
when MSBuild reaches the copy anyway; they are the lock, not the code. On a project with
`TreatWarningsAsErrors`, this is the check that tells you whether the tree is clean.

Say what this did and did not prove: the code COMPILES; it was not linked, not started, and no
endpoint was exercised. Report that gap rather than letting "build passed" stand in for it.
