## When to use

Injecting a dependency into a class, choosing a service lifetime (`Singleton`/`Scoped`/`Transient`),
or disposing a resource (`IDisposable`/`IAsyncDisposable`).

## Primary constructors

- Use .NET primary constructors with no private backing fields unless additional logic is required;
  migrate existing classes to primary constructors where feasible.
- Use primary constructor syntax for dependency injection (e.g., `public class MyClass(IDependency dependency)`).

## Dependency injection & service lifetimes

- Use constructor dependency injection with null checks via `ArgumentNullException`.
- Use `Microsoft.Extensions.DependencyInjection` patterns.
- Implement service interfaces for testability.

### The lifetime follows the state the class holds

Not how stateless it looks, and not how expensive it seems to construct.

- A class with a settable `DbContext` property, a mutable results collection, or any other
  per-request field is **`Scoped`**. `Singleton` is for classes that hold nothing a request can write.
- A `Singleton` that resolves or is handed a `Scoped` dependency is a **captive dependency**: the
  scoped object outlives its scope and is shared by every concurrent request.

The failure this produces, and why it hides:

```
System.InvalidOperationException: A second operation was started on this context instance
before a previous operation completed.
```

- It is **timing-dependent**. It appears only once a second concurrent caller exists, so it surfaces
  as "the page broke when I added a widget", long after the registration was written.
- The same URL returns **200 when curled alone**. A single sequential request is not evidence the
  endpoint is healthy; reproduce with two callers in flight.
- Adding a second consumer of an existing endpoint (a second component, a header KPI, a polling
  panel) is therefore a concurrency change, not only a UI change.

Seen in `vouchers-ai`: `AddSingleton<IBalanceEngine, BalanceEngine>()` where `BalanceEngine` exposes
`public VouchersDBContext Data { get; set; }`, plus the `ICalcConfig` it mutates. Both became
`AddScoped`. Audit for it with a grep rather than by reading `Program.cs` top to bottom:

```bash
grep -rn "AddSingleton" --include=*.cs .            # then open each type
grep -rn "public .*DbContext .* { get; set; }" --include=*.cs .
```

- **A `Program.cs` registration change needs a real restart.** `dotnet watch` cannot hot-reload a DI
  registration, and `dotnet build` fails with `MSB3027 ... file is locked by` while the app runs from
  `bin/<config>/<tfm>/<app>.exe`. Stop the process first; see
  [app-lifecycle-and-watch.md](app-lifecycle-and-watch.md).

## Disposal

- Implement proper disposal patterns (`IDisposable` / `IAsyncDisposable`) for all resources.
