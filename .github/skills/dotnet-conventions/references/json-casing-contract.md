## When to use

A field arrives `undefined`/empty in an SPA client after a 200 response, or you're deciding
PascalCase vs camelCase on the wire for a new DTO.

## JSON casing contract with SPA clients

When `PropertyNamingPolicy = null` is set (PascalCase passthrough) but the SPA's TypeScript
models expect camelCase, **every DTO consumed by the client needs explicit
`[JsonPropertyName("camelCase")]` attributes** — and the failure mode when one file misses them
is silent and misleading: the client reads `response.token` from `{"Token": ...}`, gets
`undefined`, and downstream code breaks far from the serialization boundary (here: login
"succeeded" with 200 but the session stored `{}` and the user stayed on the login page). Rules:

- Treat the casing policy as a **contract**: either camelCase globally, or attribute every
  client-facing DTO. Check sibling DTO files for the established attribute precedent before
  adding a new DTO file — the bug enters when a new file skips the pattern its siblings follow.
- When a client-side flow fails with fields mysteriously `undefined`/empty after a 200 response,
  diff the raw response body's key casing against the client interface **first** — before
  debugging the client logic.


## Read the policy before you write it into a contract

Casing is the first thing a coordinator gets wrong when freezing a contract for parallel agents,
because "camelCase, like every other API" is true of most APIs and not of this one. A contract that
names the wrong casing produces properties that are `undefined` at runtime with no compile error and
no failing test, and every gated feature silently reads as off.

Two lines of evidence, before the contract is written, never after:

```bash
grep -rn "PropertyNamingPolicy" src/<api>/Program.cs
sed -n '1,30p' src/<spa>/src/app/<feature>/<feature>.model.ts
```

`PropertyNamingPolicy = null` means the wire carries the C# property names, PascalCase. If the SPA
types its models straight off `HttpClient` with no mapping layer, the client interface is the
contract and new fields are cased like the ones already beside them.

When a delegate flags the conflict instead of quietly picking a side, that is the instruction
working. Answer with the evidence, correct the contract, and tell them to rename rather than keep a
mapping layer: an adapter that exists only to bridge a coordinator's mistake is noise once the
mistake is fixed.
