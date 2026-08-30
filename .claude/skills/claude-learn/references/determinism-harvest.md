# determinism-harvest: turn what the model just improvised into a script it only parameterizes

Task 2b of claude-learn, run right after [claude-learn-distribute](claude-learn-distribute.md) has
decided a learning is worth keeping.

A session that solved something by reasoning through twenty tool calls has produced two artifacts,
not one: the answer, and a procedure. The answer goes in the lessons file. The procedure is worth
more, because the next run should not re-derive it: the model should call it and pass arguments.

**The goal is to shrink the model's job from "work out the steps" to "supply the parameters".**
Every step moved into a script is a step that cannot drift, cannot be half-remembered, and can be
tested later without a model in the loop.

## What qualifies

A procedure is harvestable when all four hold:

| Check | Fails when |
|---|---|
| The steps are fixed; only the inputs change between runs | Each run needs a different judgement call about what to do next |
| The output is checkable without a model reading it | "Looks right" is the only success criterion |
| It ran at least once end to end in this session | It is a plan, not a proven procedure |
| It will recur: monthly, per release, per customer, per incident | One-off |

Judgement steps do not disqualify a procedure. **Split it**: the deterministic half becomes the
script, the judgement stays with the model. A script that fetches, parses and emits a manifest,
with the model deciding what to do with the rows, is the normal shape.

## How to harvest

1. **Name the parameters first.** Everything the session hardcoded (a date range, a subscription,
   a hostname, an account id) is an argument. If you cannot name them, the procedure was not
   deterministic.
2. **Write it as a CLI with explicit flags**, not positional arguments: the caller is a model, and
   `--from 2026-01-01 --out ./x` survives being reordered or partially remembered where `$1 $2` does not.
3. **Give it a dry-run** whenever it writes anything, and make re-runs idempotent (skip what is
   already done rather than duplicating it).
4. **Print a summary line the caller can assert on**: counts and totals, not prose.
5. **Store it beside the skill that owns the procedure**, in `scripts/`, and reference it from that
   skill's SKILL.md so it is discoverable at the same moment the topic is.
6. **Run it once against the real case** and confirm it reproduces what the session did by hand.
   An unproven script is worse than no script: it will be trusted.
7. **Register it** in [harvest-registry.md](../harvest-registry.md) with status `scripted`.

## The registry, and what "marked" means

[`~/.claude/skills/claude-learn/harvest-registry.md`](../harvest-registry.md) is a flat table of
harvested and harvestable procedures, one row each:

```
| Procedure | Skill | Script | Status | Proven on | Test |
```

Status is one of:

- `candidate`: the session showed the procedure is deterministic, but nothing was scripted yet.
  Write the row anyway; it is the backlog.
- `scripted`: a parameterized script exists and reproduced the manual result at least once.
- `tested`: an automated check runs it against a known input and asserts the summary line.

`scripted` is the loop's normal exit state. Promoting to `tested` is separate work: it needs a
fixture or a safe target, and it is what the registry exists to queue up. **Never claim `tested`
because the script ran successfully once** — that is `scripted`, and the `Proven on` column records
the case it ran against.

Review the `candidate` rows when a related topic comes up again: a procedure that surfaces twice is
one that should have been scripted the first time.
