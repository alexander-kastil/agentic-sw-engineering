---
name: pitch-brand-voice
description: Subskill of /create-product-pitch. Scrubs the pitch outline and slide-prompt for brand-voice violations BEFORE they are sent to Gamma. Default rule is no em dashes (—). Project-specific rules are loaded from MEMORY.md and feedback_*.md entries. Use as Stage 4 of the pitch pipeline, immediately before [[pitch-gamma]]. Triggers on "scrub voice", "check brand voice", "remove em dashes", or when invoked by [[create-product-pitch]].
metadata:
  version: 1.0.0
---

# Pitch Brand Voice (Subskill)

Stage 4 of [[create-product-pitch]]. Stage gate before Gamma is invoked.

## The rule that exists by default

**No em dashes (—) anywhere in pitch material.** Em dashes feel AI-written; this is the single most common voice failure across pitches.

Replacements (in order of preference):
1. Period — split into two short sentences (best for declarative claims)
2. Colon — when introducing a list or amplification
3. Comma — for tight asides
4. Parentheses — for parenthetical detail
5. " and " or " bis " (DE) — when used as a connector

**Keep:**
- En dashes (`–`) in numeric ranges like `30–100 €` are NOT em dashes. They are technically fine. Even cleaner: write `30 bis 100 €` (DE) or `30 to 100 €` (EN).
- Hyphens in compound words (`Cloud-KI`, `well-tested`).

## Project-specific rules

Before scrubbing, **load the project's voice rules** by reading in parallel:

- The project's `MEMORY.md` (the index)
- Every `feedback_*.md` entry (the actual rules)

A feedback memory tagged `type: feedback` that mentions voice, copy, tone, or phrasing is binding. Apply it after the em-dash scrub.

Common project rules to watch for:
- "no superlatives"
- "no AI tells" (delve, navigate, embark, leverage, …)
- specific banned phrases or required phrases (e.g., always say "in your office" not "on-premises")

## How to scrub

Run in a single message, in parallel:

1. Read `<product>/pitch-outline-<lang>.md`
2. Read `<product>/pitch-slides-prompt-<lang>.md`
3. Read `MEMORY.md` and discovered `feedback_*.md` entries

Then in a single message, in parallel:

4. `Edit` outline with `replace_all: true` to fix em dashes section by section (or `Write` if pervasive)
5. `Edit` slide-prompt with `replace_all: true` similarly

Then verify:

```bash
grep -c "—" <product>/pitch-outline-<lang>.md <product>/pitch-slides-prompt-<lang>.md
```

**Both must return 0.** This is the stage gate.

## When em dashes are pervasive

If a file has more than ~10 em dashes, full rewrite is faster than surgical Edits. Use `Write` with the rewritten content. Be careful to preserve:
- All numbers and prices
- All code snippets and YAML
- All headings and structure
- All italicized money-quotes

## What to return to the caller

A single line: `scrubbed: outline=N1, slides=N2, violations remaining=0`.

If non-zero violations remain (e.g., one quoted phrase legitimately contains an em dash and must stay), surface them explicitly and let the user decide.

## Stage-gate enforcement

**Do not signal completion to [[create-product-pitch]] until `grep -c "—"` returns 0 on both files.** The Gamma call that follows costs 30+ credits per deck. A leaked em dash means burning credits on a violating deck plus a re-run.
