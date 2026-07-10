---
name: idea-to-pitch
description: Stage 0 (optional) of /create-product-pitch. Turns a 3-to-many-line product idea into the structured product brief the pitch pipeline consumes. Runs a ledger-based discussion loop, asks batched clarifying questions, records every decision to an idea-ledger.md, then writes a product brief (readme.md + usecases.md) under the product's own directory. Use when the user arrives with a raw idea rather than existing product docs, or says "idea to pitch", "turn my idea into a pitch", "shape this idea", "help me develop a product idea", or "I have an idea for a product".
metadata:
  version: 1.0.0
---

# Idea to Pitch (Stage 0 Subskill)

Optional front-end of [[create-product-pitch]]. Run this when the user has only a rough idea, not the `readme.md` + `usecases.md` brief that [[pitch-sources]] expects. The user arrives with three to many lines of raw idea. You leave them with a product folder the pitch pipeline can read without further questions, then continue straight into Stage 1.

The job is **a short, ledger-based discussion loop**, not a one-shot guess. You ask the few questions a pitch genuinely needs, record each answer to a durable ledger, and stop the moment the brief is complete enough to draft. Target the whole loop at a couple of ten-minute conversations, not an interrogation.

---

## When to run this stage

- The user invoked /create-product-pitch with only a raw idea (no product folder, no `readme.md`).
- The user explicitly asked to "shape an idea" or "turn my idea into a pitch".

Skip straight to Stage 1 ([[pitch-sources]]) when a product brief already exists.

---

## Input

One of:
- A 3-to-many-line idea pasted directly into the prompt.
- A path to a rough notes file (`.md`, `.txt`, `.docx`).

First action: derive a short product slug from the idea (kebab-case, e.g. `fleet-inspector`). Confirm the slug and the target directory with the user in the first question batch if it is ambiguous. All artifacts live under `<product>/`, never in the repo root.

---

## The ledger

Create `<product>/idea-ledger.md` immediately, before the first question. It is the single source of truth for the conversation and survives across sessions.

```markdown
# Idea Ledger: <product>

## Idea
<the user's raw seed, verbatim>

## Decisions
<append-only. one bullet per confirmed answer, tagged with the gap it closes>

## Open questions
<the gaps not yet closed, in priority order>

## Assumptions
<anything you inferred and are proceeding on without asking>
```

Update the ledger after **every** question round: move answered items from `Open questions` to `Decisions`, and record any inference in `Assumptions`. The ledger is what makes the loop resumable and what feeds the brief.

---

## Discussion loop

Each round: read the ledger, pick the highest-priority unanswered gaps, ask **one** batched `AskUserQuestion` (1 to 4 questions), then write the answers back to the ledger. Never ask one question at a time.

Close the gaps a pitch needs, in this priority order:

1. **Problem and who has it** which pain, and whose.
2. **Target audience or personas** end customers, resellers, internal teams, investors.
3. **Core value proposition** the one-sentence promise.
4. **How it works** the three or so capabilities or components.
5. **Differentiation** why this and not the obvious alternative.
6. **Business model** pricing tiers or how value is captured.
7. **Use cases** two or three concrete persona stories.

Always include a low-friction escape option such as "That is enough, draft the brief" so the user can cut the loop short. Cap the loop at four to five rounds; if gaps remain, fill them with explicit `Assumptions` rather than another round.

---

## Coverage checklist

Before drafting the brief, the ledger must answer: problem, audience, value proposition, three capabilities, one differentiator, a pricing or value-capture line, and at least two use cases. Anything still missing becomes an `Assumptions` entry the user can correct later.

---

## Output contract

When the checklist is satisfied, confirm with the user, then write two files. These match the shape [[pitch-sources]] reads at the start of Stage 1.

`<product>/readme.md`:

```markdown
# <Product Name>

<one-sentence summary>

## Problem
<the pain and who feels it>

## Solution
<what it is + the three named components or capabilities>

## How it works
<the short mechanism>

## Differentiation
<why this over the obvious alternative>

## Audience
<the personas, one line each>

## Pricing
<tiers: name + price + one-line use case, or the value-capture model>

## Next step
<the concrete first move, e.g. a 30-day pilot>
```

`<product>/assets/usecases.md`:

```markdown
# Use Cases

## <Persona 1>
<3 to 5 sentences. End on one quotable line.>

## <Persona 2>
<3 to 5 sentences. End on one quotable line.>
```

Keep `idea-ledger.md` as the decision trail. Do not delete it.

---

## Handoff into Stage 1

Once the brief is written, do not stop. Continue directly into Stage 1 ([[pitch-sources]]) of [[create-product-pitch]] using the freshly written `<product>/readme.md` and `<product>/assets/usecases.md` as the source materials. No copy-paste and no second invocation are needed.

---

## Hard rules

- **One batched question per round.** Never ask questions one at a time.
- **Ledger first.** Write `idea-ledger.md` before the first question and update it after every round.
- **Confirm before drafting.** Show the user the gap summary and get a go-ahead before writing the brief.
- **No em dashes** in any prose you write. Use commas, colons, semicolons, or parentheses. The Stage 4 brand-voice gate will also catch leaks, but author clean.
- **Artifacts under `<product>/` only.** Never write to the repo root.
- **Respect the time budget.** Cap at four to five rounds; convert remaining gaps to `Assumptions` rather than prolonging the loop.
- **Don't re-read freshly written files** to verify. `Write` would have errored if it failed.
