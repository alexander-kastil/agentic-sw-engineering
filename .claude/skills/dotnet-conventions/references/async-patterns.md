## When to use

Writing or reviewing any `async`/`await` code: I/O calls, `Task`-returning methods, `ConfigureAwait`,
or async exception handling.

## Async/Await Patterns

- Use `async`/`await` for all I/O operations and long-running tasks.
- Return `Task` or `Task<T>` from async methods.
- Use `ConfigureAwait(false)` where appropriate.
- Handle async exceptions properly.
