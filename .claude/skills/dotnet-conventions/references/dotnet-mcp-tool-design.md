# .NET MCP Tools: designing the surface a model calls

What the model sees and chooses from: parameter shape, descriptions, return payloads, tool naming,
and the multi-call patterns. Building and hosting the server is [dotnet-mcp](dotnet-mcp.md); auth is
[dotnet-mcp-auth](dotnet-mcp-auth.md); proving it works is [dotnet-mcp-verify](dotnet-mcp-verify.md).

## A tool parameter takes the natural key, not the surrogate id

The REST controller beside the tool is called by a SPA that already holds the row it is acting on, so
`?listId=2` costs it nothing. The tool is called by a model reading prose, and a surrogate id is a
value it cannot know without a lookup it will sometimes skip, so the same argument has to arrive as
the name a human would say:

```csharp
[McpServerTool(Name = "get_secret")]
[Description("Returns one secret by its exact name within one list.")]
public async Task<SecretDto?> GetSecret(
    [Description("The exact list name as returned by list_secret_lists.")] string list,
    [Description("The exact secret name as returned by list_secrets.")] string name,
    CancellationToken cancellationToken = default) =>
    await repository.GetAsync(
        await lists.RequireIdAsync(list, cancellationToken),
        name,
        version,
        cancellationToken);
```

Three rules make that safe:

- **The repository keeps taking the id.** Resolution lives in one `RequireIdAsync(name, ct)` on the
  lookup repository, and the tool class is the only caller. Do not push name resolution into the
  entity repositories: every method would then carry two ways to say the same thing.
- **An unresolved name throws with the valid set in the message**, `Unknown list 'Web'. The store
  holds: Ext. Resources, Web Accounts.` A model recovers from that in one turn; from
  `ArgumentException: listId` it guesses.
- **Say where the name comes from** in the `[Description]`, naming the tool that returns it. That is
  what makes the id-free chain discoverable: `list_secret_lists` -> `list_secrets` -> `get_secret`.

The same split applies to any lookup whose rows a human names: customer, repo, environment, slot. The
id is an implementation detail of the database, and the tool surface is not the database.

## MCP Apps (`ui://`) tools are not model-callable on every client

A tool that links an interactive form via MCP Apps carries `_meta.ui.resourceUri`:

```csharp
[McpServerTool]
[McpMeta("ui", JsonValue = """{"resourceUri":"ui://myapp/some-form"}""")]
public async Task<string> OpenSomeDraft(...) { ... }
```

**Some clients list such a tool but refuse to let the model invoke it.** claude.ai registers it as an "Interactive UI tool" and answers a direct call with:

```
Tool '<Server>:open_some_draft' not found.
```

while every plain tool on the same server works normally. The tool name showing up in the client's tool list is therefore not evidence that the model can call it.

Rules:

- **Never make a `ui://`-linked tool the only entrance to a capability.** Ship a plain, model-callable tool that completes the job in one call; treat the form as an optional nicety for clients that render it. Otherwise the feature silently does not exist for half your clients.
- **Once the plain path works everywhere, delete the form rather than keeping it as that nicety.** Two entrances to one write mean two `[Description]` contracts telling the model different things, two test surfaces, and docs that drift apart while both look maintained. A form that no client in actual use renders is not a fallback, it is a second specification nobody reads. Removing it is a deletion of the tool, its `ui://` resource and its tests in one pass.
- The plain tool must carry the **full domain shape**, not the demo shape the form happened to collect. A form-backed `save_*` written for a walkthrough tends to hardcode things (a zero VAT rate, a default account, no document reference) that make it wrong for real data.
- "Listed but not found on invoke" is a client-side client-type restriction, never a server fault. Prove the server first — a direct `tools/call` over curl (see *Verifying an HTTP MCP server*) will return the tool's payload happily.

## Human-in-the-loop when the client has no UI

Desktop and mobile clients (Claude Desktop, iPhone, iPad) render tool results as text in a chat
bubble. They cannot show an interactive form, and you cannot rely on elicitation or sampling. A
write that deserves confirmation therefore needs a **read-only preview tool** beside the write tool,
not a UI.

Shape that works:

- `preview_x` takes the same arguments as `write_x`, writes nothing, and returns what it *would* do.
- **Array in, array out, always**, in input order, one proposal per input item. A single item is a
  one-element array, so a caller never branches on shape.
- **Essential fields only.** The reader is a human on a phone. If a field would not change their yes
  or no, leave it out. Where a value was *resolved* rather than supplied, name the rule and the
  evidence in one short field.
- An item that cannot be resolved stays in its position carrying its candidates or its error. Never
  drop it: the array length must equal the input length.
- **Stateless.** No preview token, no server-side pending store. The confirm turn may share no state
  with the preview turn; the user types "ok" and the model calls the write tool with the same
  arguments. The write tool must never require a preview to have run.
- Say in the `[Description]` that this is a dry run and the caller is expected to present it for
  confirmation.

### The write tool can be its own preview

When the server has a mode switch (a "human confirms" mode versus an "auto" mode), the cleanest shape
is not a third tool: `write_x` itself returns the proposal as **plain text** in the confirming mode
and writes nothing, ending with the question and naming the follow-up tool literally:

```text
Description: Google
Date: 2026-08-17
Net: 10.00 EUR
VAT: 20%
Gross: 12.00 EUR
Account: 7380 Telefon

Book this? Reply yes to save it, no to cancel. On yes, call save_voucher with exactly these values;
do not call add_voucher again for this booking.
```

Why text and not JSON here: the client renders a tool result verbatim in a chat bubble, so JSON is
shown to a human as JSON. One `Label: value` per line, invariant culture for money, and omit fields
that have no value rather than printing empty ones.

- **The text must carry every identifier the follow-up write tool takes, in the form it takes it.**
  Rendering an account as `7380 Telefon` reads well and is useless to a `save_voucher` that wants the
  GUID, so the model spends a turn re-listing accounts. Print the human label *and* the machine value,
  or accept the extra round trip knowingly.
- The last line is instructions to the model, not to the user, and both read it. Name the exact tool
  and forbid re-calling the proposing tool, or the model loops.
- Failures render as text too, listing the candidates one per line and asking which to use. A mode
  that returns text on success and JSON on failure makes the client show a raw error object.
- Keep the write path single: the confirming mode and the auto mode must land in the same write
  method, so defaults like "mark it paid" or "flag it as AI-booked" cannot diverge between them.

## A tool that mirrors an endpoint shares its implementation, never its rules

When a tool exposes something a controller already does, the validation usually lives inline in the
action method, so the quick path is to restate it in the tool. That produces two copies of the same
rules with no compiler link between them, and they drift on the first change that touches only one.

Extract the logic to the service the tool and the controller both call (validation included), then
make the controller delegate to it. The refactor is behaviour-preserving, so the existing controller
tests are the proof: they must pass untouched.

The same applies to guards. A tool wrapping a state-changing endpoint gets exactly the guards that
endpoint has, no fewer. Adding extra confirmation steps in the tool is a product decision, not a
default: raise it rather than inventing it, and remember the tool surface is reachable by any
connected client, so "the UI asks first" is not a guard.

Where a subset of tools is deliberately withheld from another consumer (an in-app assistant getting
reads but not writes), make the split explicit in code so a newly added tool must choose a side.
A default that silently includes new tools hands out write access nobody reviewed.

## Writing Tool Descriptions for LLM Disambiguation

Once a server has more than a couple of tools that touch related data (e.g. an aggregate total, a per-entity breakdown, and a derived/net figure), a client LLM will regularly pick the wrong one unless each `[Description]` earns its keep. A description that only states what the tool does is not enough once a near-neighbor tool exists — it must also say what it is *not*, so the model can rule out the alternative on the same pass:

- **State the disambiguation explicitly, by tool name.** "Returns the single aggregate total (not per-customer) — for a per-entity breakdown use `GetXByCategory` instead" beats two descriptions that both independently say "returns totals" and leave the model to guess which one is the aggregate.
- **Include the natural user question verbatim**, not just the technical operation. Users ask "how much was my revenue in 2022," not "aggregate income query" — echo the former in the description so embedding/keyword matching on the tool list actually surfaces it.
- **Name domain near-synonyms that map to different fields.** Many business domains have two or more terms that sound interchangeable to a general model but are computed differently server-side (e.g. gross turnover vs. net income; a domain's internal jargon vs. the everyday word a user would type, possibly in a different language than the codebase). If the underlying query already returns both, say so explicitly (`GrossX is the turnover figure, NetX is the income figure`) instead of leaving the model to infer which field answers which phrasing.
- **Verify the semantic claim against the query/service implementation before writing it** — don't guess which field maps to which business term; open the underlying `*Query`/`*Service` method and confirm what it actually aggregates. A confidently wrong disambiguation is worse than a vague one.
- **Prefer fixing descriptions over adding a new tool.** A new tool is only justified when the underlying data genuinely isn't computable from an existing tool's return shape — if two "different" questions already resolve to the same query with different wording, that's a description gap, not a coverage gap.

## Returning Structured Data

```csharp
public class ItemCollection
{
    public List<Item> Items { get; set; } = [];
}

public class Item
{
    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("name")]
    public string Name { get; set; } = string.Empty;
}

[McpServerTool]
[Description("Returns all items")]
public async Task<ItemCollection> ListItems()
{
    var items = await _service.GetAllAsync();
    return new ItemCollection { Items = items };
}
```

MCP tools can return plain strings or any JSON-serializable type. Use DTOs whenever the response has more than one field.

## Propose/confirm tool pairs: the confirming leg never recomputes

A server that writes on the model's behalf usually ships two tools: one that proposes (returns a
plain-text description and asks for a yes) and one that confirms and writes. The trap is running the
same resolver on both legs.

A private receipt of 57.90 gross was proposed correctly as `Net 57.90 / VAT 0%`. The confirming tool
took `netAmount` plus the VAT the model had read off the receipt, ran the same
`net * (1 + vat/100)` derivation, and wrote 63.69. Nothing errored, the suite was green, and the
ledger was 5.79 over the receipt.

Rules:

- **The confirming leg takes the proposal verbatim.** Make it explicit at the call site rather than
  implicit in a number: an `amountMode: Final | Recompute` argument on the shared resolver, where
  `Final` means the amount supplied is already the total.
- **Require, do not default, the fields the proposal already decided.** A confirming input that
  defaults VAT is guessing: `0` silently destroys an input-tax deduction and `20` invents one. Refuse
  the row with a message naming the proposal instead, and refuse only that row, not the batch.
- **Both legs must round-trip.** Feed the proposal's own printed values back into the confirming tool
  in a test and assert the written amounts equal the proposed ones.
- Descriptions on the two tools must not contradict each other. "The VAT printed on the receipt"
  belongs on the proposing tool; the confirming tool's field is "the VAT shown in the proposal".

## Let the resolved entity decide the derived fields, not the caller

When a tool's arguments could contradict each other, derive from the one the server can verify. An
expense-booking tool took `account`, `vatPercentage` and a voucher type; a private account can never
carry input tax, so VAT and voucher type are properties of the resolved account, not of the caller's
arguments. Deriving them server-side made an invalid combination unrepresentable and reduced the
model's job to a single account choice.

The matching risk: once accounts of both kinds share one candidate list, a name-fragment match can
silently cross the boundary. Require an exact id for the sensitive kind on any path that writes
without human confirmation, and let the fragment match stand where a human confirms first.

## Tool names are snake_case on the wire

`WithToolsFromAssembly()` exposes `GetPeriodSummary` as `get_period_summary`. Scripting `/mcp` with
the C# method name fails at the JSON-RPC layer, not in your code. Read the names off `tools/list`.
