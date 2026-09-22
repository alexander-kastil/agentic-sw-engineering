# .NET Testing Patterns

Reference for xUnit, FluentAssertions, and NSubstitute. Target 80%+ behavior-focused coverage.

## Test Class Structure

```csharp
public class ItemsControllerTests
{
    private readonly AppDbContext _db = Substitute.For<AppDbContext>();

    [Fact]
    public async Task GetAll_ReturnsAllItems()
    {
        // Arrange
        var items = new List<Item> { new() { Id = 1, Name = "Widget" } }.AsQueryable();
        _db.Items.Returns(items);

        // Act
        var controller = new ItemsController(_db);
        var result = await controller.GetAll();

        // Assert
        result.Should().NotBeNull();
    }

    [Theory]
    [InlineData(1, true)]
    [InlineData(99, false)]
    public async Task GetById_ReturnsExpectedResult(int id, bool exists)
    {
        // Arrange / Act / Assert as needed
    }
}
```

## xUnit Attributes

| Attribute | When to use |
|---|---|
| `[Fact]` | Single, parameterless test case |
| `[Theory]` | Parameterized test with multiple inputs |
| `[InlineData(...)]` | Inline parameters for a `[Theory]` |

## FluentAssertions

| Assertion | Example |
|---|---|
| Equality | `result.Should().Be(expected)` |
| Null check | `result.Should().NotBeNull()` |
| Deep equality | `result.Should().BeEquivalentTo(expected)` |
| Collection not empty | `result.Should().NotBeEmpty()` |
| Type check | `result.Should().BeOfType<OkObjectResult>()` |

## NSubstitute

| Operation | Example |
|---|---|
| Create substitute | `var svc = Substitute.For<IMyService>()` |
| Stub return value | `svc.GetAsync(1).Returns(person)` |
| Verify call | `await svc.Received(1).SaveAsync(Arg.Any<Item>())` |
| Argument matcher | `Arg.Is<Item>(i => i.Name == "Widget")` |

## Controller Test with Mocked DbContext

```csharp
public class ItemsControllerServiceTests
{
    private readonly IAppDbContext _db = Substitute.For<IAppDbContext>();

    [Fact]
    public async Task GetAll_ReturnsItems()
    {
        _db.Items.Returns(new List<Item> { new() { Id = 1, Name = "Widget" } }.AsQueryable());
        var controller = new ItemsController(_db);
        var result = await controller.GetAll();
        result.Should().NotBeNull();
    }
}
```

## Coverage Goal

- 80%+ behavior-focused coverage.
- Test behavior, not implementation details.
- Cover both success paths and failure/not-found paths.

## Diagnosing a Failing Suite

### Get the actual error first

`dotnet test -v q` prints only the `[FAIL]` test names, and `-v n` buries the detail. Neither shows you
the assertion message. Use the console logger explicitly:

```bash
dotnet test <project> --nologo --logger "console;verbosity=detailed"
```

Package-audit and analyzer warnings (`NU1903`, `EF1002`) can flood the output to the point that the
failures scroll away. Filter them, then pull the failure blocks:

```bash
dotnet test <project> --nologo --logger "console;verbosity=detailed" 2>&1 \
  | grep -v "NU1903\|EF1002" | grep -B2 -A 14 "Error Message"
```

### Establish which side is wrong before editing either

A failing test means the test and the production code disagree. It does **not** say which one is right.
Decide per failure, and state the verdict:

| Symptom | Likely wrong side | How to confirm |
|---|---|---|
| Test asserts a field/table the code no longer writes | **Test** — a migration moved the data and the tests were not swept | Find the migration; check whether producers and consumers both moved |
| A sibling test on the adjacent path passes | **Test fixture** — the mock/stub for this path is broken, not the service | Read the fixture's branching, not just the service |
| FK / constraint violation on an in-memory DB | **Production** — a write persists a row referencing something that does not exist | Check whether the caller guards it; an unreachable path is still a defect |
| Library throws on a degenerate input the test deliberately passes | **Production** — the builder does not handle the empty/zero case | Read the library's precondition in the stack trace |

**Never weaken an assertion to reach green.** Relaxing `NotBeNull()`, widening a matcher, or deleting a
case converts a real signal into a silent one. Change an assertion only after establishing that it
encodes an expectation the system deliberately abandoned, and say so explicitly when reporting.

### A permanently-red suite has stopped reporting

Failures that are known, tolerated, and labelled "pre-existing" stop being read. A genuine new regression
in the same area lands in the same red block and is invisible. Treat a standing red count as a defect in
its own right, not as background noise: the cost is not the red rows, it is every future regression they
will hide.

### Delegating a "make the tests pass" task

The cheap path to green is weakening assertions, and an agent optimizing for a passing suite will find it.
Any delegation prompt for test failures must carry:

- Do not weaken an assertion unless you establish that the assertion, not the production code, encodes
  the wrong expectation, and say so explicitly in your report.
- Group the failures by root cause before editing; N failures in one area are frequently not one bug.
- Report per group which side was wrong (test or production) and why.

## A green suite proves only what its environment can express

The in-memory provider **has no schema**. It accepts any model the code declares, so a suite can be
fully green while the model expects a column, table or index that no real database has. The failure
then appears at runtime on the first query, with the build and the tests both reporting healthy.

This is not hypothetical. A session shipped a new `bool` property plus its fluent mapping, ran 626
green tests, and the running API would have failed on **every** query against that entity — the DDL
had never been applied. A second, worse case: two tables the code queried on every page load did not
exist in the target database at all, and nothing in the test suite could notice.

**Add a model-versus-schema check and run it before trusting a suite.** Walk
`dc.Model.GetEntityTypes()` for mapped tables, columns, CLR types and nullability, diff against
`INFORMATION_SCHEMA.COLUMNS` for the target database, and report both directions. Model-expects-but-
missing is a runtime failure waiting to happen; database-has-but-unmapped is harmless drift worth
knowing. Compare case-insensitively — SQL Server does not care and a casing difference is a false
positive.

Generalise the habit. For each suite, name how its environment differs from production and ask
whether that difference could conceal the bug class under test:

| Environment | Hides |
|---|---|
| In-memory EF provider | Schema drift, real FK and constraint behaviour, provider-specific SQL translation |
| The developer's own machine timezone | Anything reading `TimeZoneInfo.Local` or converting `DateTime` implicitly; a container with no `TZ` runs UTC |
| A `date` column read back as `DateTime` | Time-of-day precision, and a `Kind` mismatch between the write echo and a fresh read |
| A `WebApplicationFactory` whose test scheme authenticates every request | Every authorization decision under test: an "anonymous caller" assertion runs authenticated |

Where the difference is load-bearing, add one check that runs in the production shape rather than
broadening the unit suite: a schema diff, or a container run with the real `TZ` set.

## A shared test factory that authenticates everything cannot test authorization

The usual `WebApplicationFactory` override replaces the default scheme with a handler returning
`AuthenticateResult.Success`, so controller tests need no token. Every suite sharing that factory
then runs as an authenticated user, including the one asserting what an **un**authenticated caller
may see. Such a test passes before the feature works and after, and the green tick is about nothing.

Seen on an MCP tool list: the assertion "an anonymous `tools/list` returns exactly the five public
tools" was green while an anonymous caller could both list and call the two private ones.

- Give the auth-sensitive suite a factory that leaves authentication alone. A
  `protected virtual bool UseTestAuthentication => true` on the shared factory, overridden to `false`
  in a subclass, costs three lines and no duplication of the config.
- Assert both directions: what the anonymous caller sees, and that the authenticated caller sees
  strictly more. Only the pair distinguishes "filtered correctly" from "not filtered at all".
- Prove it by removing one `[Authorize]`, watching the suite go red, and restoring it.

## Verifying while another process holds bin/

A running dev instance (`dotnet run` in another terminal or another session) locks
`bin/Debug/net10.0/<app>.exe`, and every build fails with MSB3021/MSB3027 on the file copy. That is
an environment lock, not a compile error, and killing the other process is not yours to do.

Redirect the output instead, and keep the redirect **inside the project**:

```bash
dotnet test --nologo -p:BaseOutputPath="<project>/bin-verify/" -p:NuGetAudit=false
```

A path outside the project (a temp folder) builds and runs, but silently breaks anything deriving a
repo path from `AppContext.BaseDirectory`: a `MemberData` source walking up five levels lands
somewhere else, finds no files, and xUnit reports `No data found for <test>` — which reads exactly
like a real failure. The tell is the **total**: 49 tests instead of 60. Compare test counts between
runs, not only pass/fail, and delete the redirect folder afterwards.

**Keeping the redirect inside the project is the workaround; `[CallerFilePath]` is the fix.** A test
that reads a repo file (a SQL delta, a fixture, a schema) should not know where its own binary ended
up. The compiler bakes the source file's absolute path in at build time, so this survives any output
redirect, a container copy, and single-file publish:

```csharp
private static string RepositoryRoot([CallerFilePath] string callerFilePath = "") =>
    Path.GetFullPath(Path.Combine(Path.GetDirectoryName(callerFilePath)!, "..", ".."));

private static string ScriptPath => Path.Combine(RepositoryRoot(), "db", "myproj", "deltas", "x.sql");
```

The `..` count is now relative to the source file, which moves only when someone moves the file, and
it needs `using System.Runtime.CompilerServices;`. Prove it by running the suite once with
`-p:BaseOutputPath` pointed at a temp folder outside the repo: the counts must match the normal run.
Five tests in one repo passed for weeks and failed the moment the output moved, because they were
never wrong about the repo, only about where they were standing.

## An endpoint that reports success for work it did not do

A handler shaped `if (entity != null) { ...mutate... } return Ok(new Result { Success = true });`
reports success when the lookup matched nothing. The caller cannot distinguish "applied" from "I
found nothing and gave up", and every layer above inherits the lie — in one codebase this shape
existed on four write endpoints at once, including the delete that every test teardown called, which
is why fixtures accumulated for weeks while cleanup reported success.

Return an explicit refusal instead, reusing the result type the endpoint already returns for its
other rejections rather than inventing a second shape:

```csharp
var es = await dc.EmployeeSchedules.FirstOrDefaultAsync(s => s.ID == param.ID);
if (es == null)
{
    return Ok(new MoveAssignmentResult
    {
        Success = false,
        Reason = param.ID == Guid.Empty ? "Kein Termin übergeben." : "Termin nicht gefunden."
    });
}
```

Distinguish "the caller sent nothing" (`Guid.Empty`, an unbound or absent body) from "a real id that
matched no row" — they have different causes and different fixes. Cover both with tests asserting
the reason **and** that nothing was written. And when auditing, check the siblings: this shape
travels in families, because the handlers were written by copying each other.

## A passing unit test is not a receipt for what a running system does

A fix reported "done" on a passing unit test asserting the calculation, plus reasoning that the
change was config-only, can still be unverified: the test was correct, the config was correct and
present, and the process actually answering the request was a stale build the fix never reached. The
unit test proves a pure function computes correctly in isolation. It says nothing about which process
is deployed, wired, or listening behind the port the caller actually hits.

When a fix is meant to change what a running system records or returns, hold it to a receipt the
test did not produce: the value in the live response, the row in the database, or the service's own
log line for that operation. Three independent sources agreeing is the bar, not a green `dotnet
test`.
