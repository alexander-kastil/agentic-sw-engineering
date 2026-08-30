# offering-harvest: capture the mechanism while the session still knows it

Task 4b of claude-learn, written in the same breath as the time-ledger row (task 4,
[session-closeout](session-closeout.md)). One JSON object per ledger row, in `.time/working-time.json`
beside `.time/working-time.md`.

The consumer is [`productize-delivered-work`](../../productize-delivered-work/SKILL.md), whose order of
work opens with "mine the ledgers and repositories into service records". This leaf front-loads that
mining to the moment it is cheap.

## Why the ledger alone cannot feed the catalogue

The two artifacts answer different questions and the difference is by design, not by neglect.

The ledger's `Work` cell is a **billing** sentence: customer-facing plain language, no internal jargon,
no file paths, no components. `track-time` enforces that, and it is right to. The catalogue needs the
opposite: the **mechanism**, what it takes in, what it does, what comes out.

One row from a real ledger:

> AI assistant now presents vouchers for confirmation instead of booking them itself, with an optional
> automatic mode whose bookings are marked in the list

Correct for an invoice. Useless for a catalogue. Nothing in it recovers *in-chat submit-back form
rendered by the assistant host, per-item confirm, server-side resolution against booking history* -
which is the part a second buyer would purchase, and the part that ports to any approval workflow that
is not bookkeeping at all.

So the mechanism has to be written down by the session that built it. A later mining pass reading the
ledger reconstructs the invoice, not the engine, and a mining pass reading the repository finds the
code without knowing which parts were the point. **The window closes when the session ends.**

## The rule this exists to enforce

`productize-delivered-work` opens with the failure it is built against: *do not judge the instance,
name the mechanism*. A session is the worst possible judge of whether its own work is sellable, because
it is looking straight at the instance: this customer, this schema, this afternoon's bug.

So the sidecar records the mechanism and **does not decide**. `catalogue.action` may be `none`, and
that is a fine answer; what is not fine is omitting the entry because the work "was just a fix". The
audit that produced the parent skill dismissed its owner's two strongest assets as "a personal scanner"
and "a private family app". Capture, then let the catalogue pass judge with every repo in view.

## Schema

```json
{
  "repo": "vouchers-ai",
  "origin": "https://github.com/acme/vouchers-ai",
  "sessions": [
    {
      "date": "2026-08-16",
      "from": "22:28",
      "to": "23:22",
      "sessionId": "912d379a-8b32-46ce-93b3-e6faa2df02fa",
      "branch": "master",
      "commits": [],
      "surfaces": ["vouchers-ai"],
      "files": ["src/vouchers-ai/Tools/VoucherUiResources.cs"],
      "mechanism": {
        "takes": "free-text booking requests from a chat client",
        "does": "resolves each against booking history, renders them as a read-only card per item in an in-chat form, writes only what the user confirms",
        "returns": "per-item write results with the confirmed row marked as agent-booked"
      },
      "portsAsIs": ["the in-chat confirm form and its host protocol", "per-item confirm with independent failure"],
      "perCustomer": ["the domain the rows describe", "the history the resolver learns from"],
      "evidence": [".claude/experiments/mcp-add-voucher-form/harness-readonly.html"],
      "toolchain": {
        "skills": ["mcp-claude", "claude-orchestration", "track-time"],
        "mcpServers": ["chrome-devtools"],
        "agents": ["dotnet-expert"]
      },
      "industry": "professional services, single-operator bookkeeping",
      "status": "Built and running in-house",
      "catalogue": { "action": "extends", "item": "bookkeeping-and-tax-platform" }
    }
  ]
}
```

| Field | Rule |
|---|---|
| `date` / `from` / `to` / `sessionId` | Copied verbatim from the ledger row, so the two files join on the window. Never re-derived, or they drift |
| `branch` / `commits` | `commits` is the hashes this session produced, often empty; an empty array is the honest value, never a guess |
| `surfaces` | Which app in a multi-app repo, matching the ledger's surface prefix |
| `files` | The handful that carry the mechanism, not the full diff. A later reader opens these to see the engine |
| `mechanism` | Three fields, always all three. If you cannot fill `takes`/`returns`, the session did not build a mechanism and this is a maintenance entry: say so with `catalogue.action: "none"` |
| `portsAsIs` / `perCustomer` | Candidates, not conclusions. Lists, never sentences |
| `evidence` | An **array of strings**, always: repo-relative paths to what proves it works, plus test counts or verification notes written as strings (`"tests: 289 backend, 318 frontend"`). Never a nested object; the importer deserializes this as a list and one malformed entry throws away the whole file's harvest, not just its own. **Private**; the parent skill strips these at render, so keep them here |
| `toolchain` | `skills`, `mcpServers` and `agents` the session actually used, including inside subagents. See below |
| `industry` | The proof line, already stripped: industry only, no differentiator, no counts, no stack |
| `status` | Exactly one of `Live`, `Built and running in-house`, `Designed, not built`. A session that shipped nothing to a buyer never writes `Live` |
| `catalogue.action` | `new`, `extends` or `none`. With `extends`, `item` is the existing catalogue slug, **read from the live catalogue in the same breath, never from memory of what the item is called**. A key that resolves to nothing reads as a decision already taken and survives until a catalogue pass tries to apply it |

## The toolchain block, and its two readers

`toolchain` is the only field with a consumer outside the catalogue, which is why it is worth the
extra lines.

**For the catalogue**, how the thing was built is part of what ports. A buyer asking why the estimate
is small gets a sourced answer rather than a claim: the verification harness came from a skill, the
browser proof came from a named MCP server, the domain work went to a named expert. It also keeps the
`portsAsIs` list honest, because a capability that only exists when a particular MCP server is
connected is a dependency, not a portable asset, and this is where that shows up.

**For [skill-usage-registry](skill-usage-registry.md)**, which asks which installed skills never fire.
Today that answer is scraped from transcripts, and transcripts expire. A per-session record does not,
so a skill that has never appeared in any repo's sidecar is a deprecation candidate with evidence
behind it.

Derive it from the transcript, not from memory, in the same project directory `track-time` already
reads. Skills and subagents come out of this session's file:

```bash
f=~/.claude/projects/<project-dir>/<sessionId>.jsonl
grep -oh '"skill":"[^"]*"' "$f" | cut -d'"' -f4 | sort -u
grep -oh '"subagent_type":"[^"]*"' "$f" | cut -d'"' -f4 | sort -u
grep -oh '"name":"mcp__[^"]*"' "$f" | cut -d'"' -f4 | sed 's/^mcp__//;s/__.*//' | sort -u
```

Three cautions, all of which produce a wrong list if ignored:

- **A skill read in place is still a skill used.** Only the `Skill` tool leaves a `"skill":` record;
  a leaf opened with `Read` because the tool could not launch it leaves none. Add those by hand.
- **The MCP grep matches tool *calls* only.** A bare mention of a server name in prompt or hook text
  will not match that pattern, and should not: mentioning `chrome-devtools` in a routing rule is not
  using it.
- **Subagent tool calls belong to the session.** They land in the subagent's own context, so the
  parent transcript shows the dispatch and not the calls. Take them from the agent's report and record
  them, or the field will under-count exactly the work that was delegated.

## Procedure

1. Write the ledger row first (task 4). It fixes the window and the session identity.
2. Append one sidecar object per ledger row, reusing that window verbatim. A `0.00` parallel row still
   gets a sidecar: it was billed at zero, not delivered at zero.
3. Fill `mechanism` from what the session actually built, in the vocabulary of a second buyer who is
   not in this industry. If the sentence only makes sense to someone who knows this customer, it is
   still the instance.
4. Set `status` from evidence, not intention.
5. Re-read the file as JSON before finishing (`python -c "import json;json.load(open(...))"`) and confirm every
   `evidence` is a list. The file is parsed as a whole, so a single bad entry is a total loss, and the
   failure surfaces days later in an importer stack trace rather than here.
5. Report the sidecar with the ledger line in the run's closing summary.

Create the file with `{"repo": ..., "origin": ..., "sessions": []}` on first use. Append only: an entry
is corrected in place if it was wrong, never rewritten to match a later opinion of what the work was.
Leave it uncommitted, like the ledger.

## Verify

- Every row in `.time/working-time.md` written **since the sidecar existed in this repo** has exactly
  one object in `.time/working-time.json` with the same `date`, `from` and `to`. A newer ledger row
  with no sidecar is a session whose mechanism is gone.
- Older rows are **not backfilled**. Reconstructing a mechanism from a billing sentence produces a
  confident guess, which is worse in a catalogue than an absence: mine those the slow way, from the
  repository, on the next catalogue pass.
- No `mechanism.does` reuses the ledger's `Work` sentence. If they match, the mechanism was not
  captured, only copied.
- No `status: "Live"` on a repo with no external buyer.
- `industry` names no company, count, hostname or stack.
- `toolchain.mcpServers` lists servers whose tools were **called**, not servers that were connected or
  named in a rule. A list that matches the session's MCP config rather than its tool calls was copied,
  not derived.
