---
name: idea-to-pitch
description: Stage 1 of the idea-to-pitch flow. Turns a 3-to-many-line product idea into the structured product brief that /create-product-pitch consumes. Runs a ledger-based discussion loop, asks batched clarifying questions, records every decision to an idea-ledger.md, then writes a product brief (readme.md + usecases.md) under the product's own directory. Use when the user invokes /idea-to-pitch, or says "idea to pitch", "turn my idea into a pitch", "shape this idea", "help me develop a product idea", or "I have an idea for a product".
metadata:
  version: 1.0.0
---

# Idea to Pitch (Stage 1)

Turn a rough idea into a structured product brief that [[create-product-pitch]] can turn into a deck. The user arrives with three to many lines of raw idea. You leave them with a product folder a marketing pipeline can read without further questions.

The job is **a short, ledger-based discussion loop**, not a one-shot guess. You ask the few questions a pitch genuinely needs, record each answer to a durable ledger, and stop the moment the brief is complete enough to draft. Target the whole loop at a couple of ten-minute conversations, not an interrogation.

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

Before drafting the brief, the ledger must answer: problem, audience, value proposition, three capabilities, one differentiator, a pricing or value-capture line, and at least two use cases. Anything still missing becomes an `Assumptions` entry the user can correct in Stage 2.

---

## Output contract

When the checklist is satisfied, confirm with the user, then write two files. These match the shape [[pitch-sources]] reads at the start of [[create-product-pitch]].

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

## Handoff

End the turn by pointing the user to Stage 2:

> Brief ready at `<product>/readme.md`. Run `/create-product-pitch <product>` to generate the outline, slides, and Gamma deck.

[[create-product-pitch]] reads the brief directly, so no copy-paste is needed.

---

## Hard rules

- **One batched question per round.** Never ask questions one at a time.
- **Ledger first.** Write `idea-ledger.md` before the first question and update it after every round.
- **Confirm before drafting.** Show the user the gap summary and get a go-ahead before writing the brief.
- **No em dashes** in any prose you write. Use commas, colons, semicolons, or parentheses. The Stage 2 brand-voice gate will also catch leaks, but author clean.
- **Artifacts under `<product>/` only.** Never write to the repo root.
- **Respect the time budget.** Cap at four to five rounds; convert remaining gaps to `Assumptions` rather than prolonging the loop.
- **Don't re-read freshly written files** to verify. `Write` would have errored if it failed.
