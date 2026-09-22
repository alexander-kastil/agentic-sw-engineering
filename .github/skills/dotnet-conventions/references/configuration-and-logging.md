## When to use

Binding strongly-typed settings from `IConfiguration`/`appsettings.json`, or adding structured
logging and exception handling around a new code path.

## Configuration & Settings

- Use strongly-typed configuration classes with data annotations.
- Implement validation attributes (`Required`, `NotEmptyOrWhitespace`).
- Use `IConfiguration` binding for settings.
- Support `appsettings.json` configuration files.

### An omitted section inherits production

`appsettings.{Environment}.json` layers over `appsettings.json` key by key, so a section the
environment file simply does not mention is inherited whole. A `Development` file with no
`Storage` / `ConnectionStrings` / external-endpoint section points local runs at **production**
resources, and the first write-side test writes there for real.

- Before the first write-side test in any environment, read the **effective** config back from
  the running app (an existing settings/diagnostics endpoint), never from the file you just
  edited. Only that proves which storage account, container, bucket or queue is live.
- Override only what the environment writes to. Read-mostly resources (templates, reference
  data) can and usually should keep pointing at the real ones.
- A value bound once at startup (`builder.Configuration.Get<AppConfig>()`, singleton options)
  needs a **full process restart**. `dotnet watch` does not restart on an `appsettings.*.json`
  change, so the edit is inert and the test silently repeats against the old target — verify the
  restart took before re-running the test that depends on it.

### A non-empty array default is appended to, never replaced

`ConfigurationBinder` binds arrays by index onto whatever the target property already holds. A C#
property initializer that is not empty therefore survives every override: with
`public string[] ServedFolders { get; set; } = ["video-assets"];`, setting
`Media__ServedFolders__0=renders-only` yields `["video-assets", "renders-only"]`, not
`["renders-only"]`. Nothing errors, the override reads as applied, and for an allow-list the
original value stays in force.

- Give every bound array or collection an **empty** C# default (`= []`), and put the real default
  in `appsettings.json`. A fresh clone still gets the intended value, and an override replaces it.
- Prove it with a layered-source test rather than a single source: bind two
  `AddInMemoryCollection` layers, which is what `appsettings.json` followed by environment
  variables actually does. A one-source test passes either way and proves nothing.
- The same append applies to `List<T>`. Scalars and complex objects replace normally; only
  collections accumulate.
- If append is genuinely what you want, say so in the property's own name (`ExtraMounts`,
  `AdditionalOrigins`) so the accumulation is a documented feature rather than a surprise.

### Do not auto-create a directory the configuration points at

`Directory.CreateDirectory(resolvedRoot)` at startup looks defensive and is the opposite: it
cannot distinguish "the path is missing" from "the path is wrong", so a mistyped or wrongly
resolved root silently becomes a new empty directory and the app serves nothing rather than
failing. The symptom surfaces much later as an empty library or a 404 nobody can explain.

- Check `Directory.Exists` and throw, naming the config key, its double-underscore environment
  form, and **the resolved absolute path**. The resolved path is what makes a wrong relative value
  obvious; the key alone does not.
- Before removing an existing auto-create, confirm the directory is guaranteed present: tracked
  content in the repo, or a container bind mount. Both are checkable, and neither is an assumption.
- Extract the guard into a testable unit rather than leaving it inline in `Program.cs`, or it can
  only ever be exercised by a manual run.

## Error Handling & Logging

- Use structured logging with `Microsoft.Extensions.Logging`.
- Include scoped logging with meaningful context.
- Throw specific exceptions with descriptive messages.
- Use `try`-`catch` blocks for expected failure scenarios.
