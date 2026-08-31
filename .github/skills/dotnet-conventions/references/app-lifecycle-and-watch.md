## When to use

Starting/reusing a running app instance, or diagnosing a `TypeLoadException` after editing code
under a running `dotnet watch`.

## Application Lifecycle

- Before starting the application, check if an instance is already running; if it is running under
  `dotnet watch run`, reuse that instance instead of starting a new one.
- Never start the application as a background process.
- Always dispose of resources properly when the application closes.
- **Hot-reload limits under `dotnet watch`**: structural edits (new methods, added queries/branches
  in controllers or services, signature changes) are rude edits. Hot reload fails with
  `TypeLoadException` and the process then serves that exception for every request while stuck on
  its interactive restart prompt; file touches do not recover it. After any structural edit under a
  running watch, verify with a real HTTP request; if the response is a `TypeLoadException`, ask the
  user to restart the watch (`Ctrl+R` in its terminal). Never kill a watch process you did not start.
- **A red build is the silent case, and it looks like a healthy process.** When the rebuild fails to
  compile, the watch keeps answering from the last good build: no `TypeLoadException`, no error in
  any response, just old behaviour. A `200` proves the process is alive, never that it is running
  your code. After editing under a running watch, build to a scratch directory
  (`dotnet build <proj> -o <scratch>`, because the watch holds `bin/Debug/<tfm>`) and look for a
  symptom only the new code could produce, rather than trusting the endpoint to fail loudly.
- **The route table is snapshotted at startup too, and a stale one 404s in a way that reads as a
  coding error.** Hot reload covers method bodies; a new controller action changes routing, which
  needs a restart. Until then the app answers from the OLD route table, so `GET /api/things/export`
  falls through to `[HttpGet("{name}")]` and returns a well-formed `problem+json` 404 for a thing
  named "export". Every other endpoint stays green and the build is clean, so nothing points at the
  process. Before editing code to chase it, check what is actually listening and how old it is:
  `Get-NetTCPConnection -LocalPort <p>` then the owning process's `StartTime`, compared against the
  source file's mtime. Touching a file does not force the restart. To prove the code without taking
  the user's process, build to a scratch dir and run a second instance on a spare port. Note also
  that a literal segment always outranks a parameter segment, so adding `/export` permanently
  shadows an entity literally named `export` on `/{name}`.
- **The MCP tool catalog is built once at startup and hot reload never rebuilds it.**
  `WithToolsFromAssembly()` snapshots the tool list and its JSON schemas at boot, so a new
  `[McpServerTool]`, a rename, or a parameter that just became optional stays invisible while
  ordinary endpoints reflect the new code. Check `tools/list` for the tool name before debugging its
  behaviour, and expect one restart per tool-surface change. See
  [`dotnet-mcp.md`](dotnet-mcp.md).
- **Restarting the watch is the user's job, and "I will just start my own" is how you take their
  port.** A restart needed for a rude edit gets reported and waited on, never performed. If a kill
  is explicitly approved, kill the whole ancestry, not the listening process: the chain is
  `dotnet watch` (or a `nohup` wrapper) -> `dotnet-watch.dll run` -> `dotnet run` -> the app exe, and
  killing only the app makes the watcher relaunch it within seconds, which reads as "the port freed
  itself and something else grabbed it". Verify the port is actually free
  (`netstat -ano | grep :<port>`) before reporting done. A watcher you started and thought you killed
  will otherwise hold the port and fail the user's own start with
  `AddressInUseException: address already in use`, with the blame pointing at their terminal.
