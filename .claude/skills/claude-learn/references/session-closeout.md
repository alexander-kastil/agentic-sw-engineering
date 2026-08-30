# session-closeout: log the session to the time ledger

Task 4 of claude-learn. **Mandatory final step of every claude-learn run.** claude-learn runs at the end of a chat; before finishing, append this session to the repo's time ledger.

Mechanics (discovery, sessionizing, append logic, billing sheet) belong to the **`track-time`** skill. Invoke it; do not reimplement it here.

## Target

- File: `.time/working-time.md` at the repo root
- Columns: `Date | Hours | From | To | Work`
- Update the `**Total**` line

## Rules

**Window from evidence, never from a guess.** Derive `From`/`To` from actual file-modification evidence: working-tree mtimes of files this session touched, commit/reflog timestamps, Claude Code session transcripts. Never a "first request -> now" estimate. Evidence is one shared clock across all concurrent chats, so it dedupes overlap automatically; conversation estimates do not, and get tiled end-to-end to look sequential when the work was concurrent. (`track-time` principles 1 and 5.)

**Split rows at midnight.** A session crossing midnight becomes one row per date, so every row belongs to exactly one Date cell.

**Never bill the same wall-clock minute twice, never hide a delivered task.** Concurrent chats each close with their own append. Append **one row per task** with its own true `[From, To]`; set `Hours` to only the portion not already covered by rows recorded earlier for that date. A task that ran entirely inside an already-billed window gets `0.00` and `(parallel, not billed)` in the Work cell. **Never merge or rewrite another session's rows**: that destroys its record of what it delivered. Order the day's rows by `From`. (`track-time` principle 5 and Procedure step 1.)

**Invariant on every write:** a day's summed `Hours` never exceeds the union of its wall-clock intervals. Rows may overlap in `From`/`To`; Hours must not.

**Work cell = ONE short customer-facing headline.** Plain language, what was delivered. No internal jargon (no store/feature/agent/workflow/slot terms), no file paths, no paragraph, no multi-sentence recap, no semicolon laundry list. Length target: `track-time` Procedure step 3.

**Leave the edit uncommitted.**

## Then the offering sidecar

Every ledger row gets one object appended to `.time/working-time.json`, in the same step, per
[offering-harvest](offering-harvest.md). The ledger's `Work` cell is a billing sentence and is
deliberately stripped of the mechanism, so it cannot feed the services catalogue on its own; the
sidecar carries what the session built, in mechanism terms, plus the repo, branch, commits and the
files that hold it. It is knowable now and unrecoverable later. Report both lines together.

## Then the import

The two files are the source of truth, but every later consumer (billing, the catalogue pass, the
worklog UI) reads the **worktime service**, so a row that was written and never imported is invisible
work. The import is part of the close-out, not a separate errand someone remembers.

**The endpoint lives in the repo's config, never in this skill.** Read the `work-time` entry in the
repo's `.mcp.json`: its `url` is the service (today `http://localhost:5211`) and its `headers` carry
the key. A repo with no `work-time` entry is not registered, and this step is a no-op for it. When the
service moves to a hosted URL, that one `url` changes and nothing here does.

**Import with the `import_ledger` MCP tool on the `work-time` server.**

```text
import_ledger(repoName: "<this-repo-name>")
```

`repoName` is required, so the tool has no unscoped form to reach for. That is why it is the primary
path: the scoping is structural, not a matter of remembering to type a flag.

The container reads the ledgers directly. `src/worktime-mcp/docker-compose.yml` mounts
`D:/git-customers` and `D:/git-projects` read-only at `/repos/git-customers` and `/repos/git-projects`,
and a configured prefix map (`Ledger__PathMap__N__From` / `__To`) translates a stored `D:/...`
`LedgerPath` into its container path. The resolver returns the stored path unchanged whenever it
exists on disk, so the host-side path still behaves exactly as it did.

**If the service is down, start it.** Do not reach for the CLI fallback because the endpoint did not
answer: the container is meant to be running, and leaving it down means the next session hits the same
wall. This is the one server the no-start-servers rule does not cover, because it is infrastructure for
the ledger rather than someone's dev instance.

```bash
cd <repo>/src/worktime-mcp && docker compose up -d
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5211/health   # expect 200
```

`/mcp` answering `405` to a GET is correct: it takes POST. Note that MCP connections are established at
session start, so a server started mid-session stays unavailable as a *tool* until the next session even
once it is healthy: use the CLI import for this run, and the container is then up for the next one.

**Fallback**, for a run where the container genuinely cannot be started, or where MCP tools are
unavailable because the server came up mid-session, run from the project that serves the configured
`url` (today `src/worktime-mcp` in `integrations.at`), and only ever in this scoped form:

```bash
dotnet run -- --import --repo <this-repo-name>
```

**Scope the run to this repo.** One `WorkTime` instance is shared by every tracked repo, most of them
different paying customers. A bare import walks all of them and writes to all of their rows, and a
verification run is still a write. The hole was never carelessness, it lived in the CLI's argument
parser: a `--repo` that was dangling or misspelt fell through to the unscoped all-customers run while
still reading like a scoped command. That degradation is now refused (`--repo=<value>` is accepted,
and any near-miss `--repo*` flag is rejected outright), but the tool is the safe path because it has
no such surface to get wrong, not because the parser was patched.

**What a good run returns.** The stored `ledgerPath` alongside the `resolvedLedgerPath` actually
opened, `ledgerFound` and `sidecarFound`, the counts `parsed / inserted / updated / unchanged /
skipped / orphaned`, the orphaned session windows, and a nested `harvest` block with its own counts.
Read the rows back through the `work-time` MCP tools rather than through SQL, because that is the path
every consumer uses. `unmatched` must be `0`: anything else means the sidecar and the ledger disagree
about a window. Report the session counts and the harvest counts in the run's closing summary
alongside the ledger row.

**A second run over an unchanged ledger must report `inserted` 0 and `updated` 0**, with every row
`unchanged`. That is the idempotency proof, and it is cheap. An `updated` count that is non-zero and
repeats on every run is the never-converging bug `track-time` already warns about, not noise.

**Import once, at the real end. A row is immutable the moment it is imported.** The importer keys a
session on (date, from, to), so widening an already-imported row's window does not update it: it
inserts a second row, the original becomes an orphan, and the overlap is billed twice. Nothing in the
importer deletes, so no re-run repairs it. On 2026-08-22 a 00:45-01:04 row was widened to 00:45-01:15
after its import and the day carried thirty-two duplicated minutes while the ledger file itself read
perfectly. If more work lands on the same task after an import, append a NEW row covering only the
new minutes. If a window was already widened and imported, say so: removing the superseded row is a
write to shared billing data and the user's decision, never a quiet cleanup.

**Read the orphan lines, every time.** The report lists them "for the operator to decide", which makes
them easy to scroll past. An orphan whose window overlaps a row the same run just inserted is a
double-bill; an orphan that overlaps nothing is a genuine leftover.

One standing case is neither, and it looks alarming. A repo that deliberately archives invoiced rows
out of the active ledger (bauer-sport moves them into `.time/billed/`) reports a large orphan count on
every import, 75 of them there, because the importer never deletes and those rows are no longer in the
file it reads. That is correct, and trying to "fix" it would delete billed history. Tell the two apart
before acting: look for an archive beside the ledger (`.time/billed/` or the same convention under
another name) and check whether the orphan windows are the old dated rows sitting in it. Archived
orphans are historic, are present in the archive file, and their count stays flat across consecutive
runs; a real leftover is recent, appears in no archive, and turns up newly after a ledger edit.
