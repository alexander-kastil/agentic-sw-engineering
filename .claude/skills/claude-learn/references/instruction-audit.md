# instruction-audit: is the instruction surface still earning its place

A gate, not a loop step. `CLAUDE.md`, its nested per-package files, the hook scripts that
re-inject rules every turn, and the lessons file are all instruction surfaces. They are written
once and then grow, and nothing in the reflect-capture-distribute-close loop ever removes
anything. This leaf is the removal pass, plus the only honest test of whether any of it works.

Run it periodically, and always before adding a rule to a file that has never been audited.

## 1. The universal-applicability test

Every line in a file that loads into **every** session must apply to every session. This is the
single test that separates a rule that gets followed from one that dilutes the rules around it.

- Passes: "run the typechecker after any series of code changes".
- Fails: "when creating a new database schema, follow this naming convention" — relevant to one
  session in twenty, and in the other nineteen it is noise competing with the rules that matter.

Anything narrow, situational, or scoped to one subsystem moves out: to a doc, to the skill that
owns it, or to a nested `CLAUDE.md` in the package it belongs to. A section that begins "if
working in the frontend package" or "only relevant for the API" is naming its own new home.

**Never convert those pointers to `@path` imports to make them feel connected.** An `@` import is
loaded into context, so importing what you just moved out re-inlines it and undoes the work.
Plain relative links are correct: they cost nothing until something actually reads them.

## 2. The contradiction and hotfix sweep

The specific way these files rot: a behaviour goes wrong once, a rule is appended, and nobody
ever revisits it. Six months on the file is twice its useful length and two of its rules
disagree. **When two rules conflict, the conflict is not resolved by the reader, it is resolved
arbitrarily**, which is worse than either rule being followed consistently.

Sweep for, in order:

| Look for | Action |
| --- | --- |
| Two rules that cannot both be followed | Delete the older one. Keep exactly one current standard, do not "reconcile" them into a longer rule |
| A rule that exists because of one incident that never recurred | Delete it. A single occurrence is not a pattern |
| A behaviour already done correctly without the rule present | Delete it. Do not keep rules defensively |
| A rule restating what the harness already injects (skill names, agent rosters, tool lists) | Delete the list, keep the rule |
| A rule that is really a fact | Move it to the doc that owns the fact |

The lessons file gets the same sweep. It is append-only by design, so it accumulates entries whose
rule has since been promoted into a skill, a hook, or `CLAUDE.md`. Once a lesson lives in an
executable surface, the entry is history, not instruction: keep it if the incident explains *why*,
delete it if it only restates a rule now enforced elsewhere.

## 3. The model-upgrade re-simplify pass

Sections 1 and 2 only remove a rule that was always wrong or has been contradicted. They never
catch the largest category: a rule that was right when it was written and stopped being needed
because the model got better. Nothing else in the loop looks for those, so they accumulate as
scar tissue from models that no longer run here, and every one of them spends context and
contrast on a failure that cannot happen any more.

Run this pass after each model release, on the harness as well as the prose:

1. **List what the surface is defending against**, rule by rule: the specific failure each one
   exists to prevent. A rule whose failure mode you cannot name is already a deletion candidate
   under section 1.
2. **Disable one piece at a time**, not the file at once: comment out the rule, or turn off the
   hook, and keep everything else. Changing two things means learning nothing from either.
3. **Run real work under it**, the same standard as the adherence pass in section 5: a genuine
   task, not a prompt written to poke the rule.
4. **Keep what the model still gets wrong. Delete what it now does unprompted.** The deletion is
   the finding; a pass that restores everything has told you the surface is load-bearing, which
   is also a result worth writing down.

Two rules never enter this pass, whatever the model can do: anything protecting a shared working
tree or live system from an irreversible action, and anything encoding a decision that is the
user's to make rather than a capability the model lacks. Those are not compensating for a weak
model, so a stronger one does not retire them.

## 4. Emphasis markers, spent sparingly

`IMPORTANT` and `YOU MUST` are a deliberate adherence signal, not decoration. They work by
contrast, so the budget is a handful per file. **If every rule is marked, none of them are.**

Reserve them for rules where a miss is expensive and irreversible: destructive git operations,
publishing, production data, anything the user must be asked about first. A style preference never
earns one. When auditing, count them: a file whose markers have crept past roughly five has lost
the contrast that made them work, and the fix is removing markers, not adding more.

## 5. Adherence verification: writer and reviewer

Writing the file and hoping is the default, and it is a guess. Close the loop with two sessions:

1. **Writer.** Run one real session under the current instruction surface, on a real task. Not a
   test prompt written to exercise the rules: a genuine piece of work.
2. **Reviewer.** In a separate session, hand the reviewer the first session's transcript and the
   file, and have it walk **each rule individually**: followed / ignored / followed inconsistently
   across similar moments, with the turn where it happened as evidence.

The output is a list of which specific instructions land and which are silently dropped. That is
the only signal that tells you whether a rephrasing, an emphasis marker, or a restructure changed
behaviour, rather than just changing how the file reads to a human skimming it.

Prioritise the `IMPORTANT` / `YOU MUST` lines: those are the rules you have claimed cannot be
skipped. One being ignored anyway means the instruction needs rephrasing, needs to move earlier in
the file, or genuinely conflicts with something else the session is being asked to prioritise. A
marker that does not change behaviour is worse than no marker, because it spends the contrast the
other markers depend on.

Where a repo re-injects rules per turn (a `UserPromptSubmit` hook), audit that text too and on the
same evidence: it decays differently from the file, and it is usually the copy that is actually
being followed.

## 6. Report

Say what was deleted and why, what moved and where to, and which rules the adherence pass found
being dropped. A rule removed is the deliverable here. An audit that only adds is not an audit.
