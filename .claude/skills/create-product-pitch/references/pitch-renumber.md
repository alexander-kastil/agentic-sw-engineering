---
name: pitch-renumber
description: Subskill of /create-product-pitch. Atomically renumbers slide files when inserting, removing, or reordering. Renames `<NN>-<slug>.{md,png}` pairs AND updates each `.md`'s `slide:` and `order:` frontmatter fields in lockstep. Verifies no gaps remain in the resulting sequence. Use when slides need shifting after an insertion or deletion. Triggers on "renumber slides", "shift slides", "fix slide numbers", or when invoked by [[pitch-add-slide]] or [[create-product-pitch]].
metadata:
  version: 1.0.0
---

# Pitch Renumber (Subskill)

Single responsibility: keep filename numeric prefixes, `slide:` frontmatter fields, and `order:` frontmatter fields in perfect sync after any slide insertion, removal, or reorder.

## Inputs

One of:

- **insertion mode** — slides folder + insertion position N. Shifts all slides at positions ≥ N upward by 1.
- **removal mode** — slides folder + position N to remove. Shifts all slides at positions > N downward by 1.
- **explicit moves** — slides folder + a map of `old_NN → new_NN`.

## Algorithm (insertion mode, the common case)

1. List all `<NN>-<slug>.md` files in the slides folder, sorted by numeric prefix.
2. Determine the set that needs to shift (everything at position ≥ N).
3. **Shift highest-first** to avoid name collisions:
   - For each pair to shift, in descending numeric order:
     - `mv <old_NN>-<slug>.md <new_NN>-<slug>.md`
     - `mv <old_NN>-<slug>.png <new_NN>-<slug>.png` (if PNG exists)
     - `Edit` the `.md` to update `slide: "TT-<old_NN>"` → `slide: "TT-<new_NN>"`
     - `Edit` the `.md` to update `order: <old>` → `order: <new>`

Batch the `mv` operations in one bash chain. Batch the `Edit` operations across files in one message.

## Algorithm (removal mode)

1. Delete the target `.md` and `.png` (after confirming with user — `pitch-add-slide` does not call this).
2. **Shift lowest-first** (so highest doesn't collide with the deleted-then-shifted neighbor):
   - For each pair at position > N, in ascending numeric order: same rename + frontmatter edit.

## Verification

After the renumber, verify:

```bash
# every .md has a matching .png (or document the gap)
ls *.md *.png | awk -F. '{ print $1 }' | sort | uniq -c | grep -v "^   *2 "
# numeric prefixes are contiguous from 01 (or whatever start) with no gaps
ls *.md | sed 's/-.*//' | sort -n | uniq -c
# every .md's slide: field matches its filename prefix
grep -H "^slide:" *.md
# every .md's order: field matches its filename prefix
grep -H "^order:" *.md
```

If any check fails, surface the discrepancy. Do not auto-correct silently.

## What to return to the caller

```
shifted: [<old> → <new>, ...]
verified: ok | <list of discrepancies>
```

## What NOT to do

- Don't rename one file at a time across many tool calls. Batch the moves in a single bash chain.
- Don't update `.md` content with `replace_all: true` on `order:` — multiple `.md` files may share patterns. Use file-scoped Edits.
- Don't reorder by changing only `order:` without renaming the file. The filename prefix is the authoritative sort key for downstream tools (Gamma, the bundle script).
- Don't touch `topic:` during renumber. Topic stays constant; only the slide-within-topic number changes.
