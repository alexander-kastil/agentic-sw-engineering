# Licensing a class repo: proprietary terms, free for the individual

Author the three files that decide who may use and who may teach a course: the `LICENSE`, the
`CODE_OF_CONDUCT.md`, and the readme's `## License & Re-Use` summary. The default posture for these
class repos is **proprietary, free for a private individual, paid for every organization**, which is
neither open source nor Creative Commons and must never be described as either.

Not legal advice. This leaf produces the structure and the wording that has been used across these
repos; a lawyer confirms it before anything external depends on it.

## The file set

| File | Holds | Rule |
| --- | --- | --- |
| `LICENSE` | The binding terms: definitions, grant, prohibitions, contact, termination, penalty, warranty, liability, governing law, jurisdiction, severability | The only authority. Everything else points at it |
| `CODE_OF_CONDUCT.md` | Contributor Covenant, unmodified except the enforcement contact | Swap the contact to this repo's owner. A copied file carrying the previous repo's reporting address is a real defect: complaints route to someone with no authority here |
| `readme.md` `## License & Re-Use` | A five-bullet convenience summary plus the contact | Must state in the same breath that it is for convenience and does not modify the `LICENSE`, or the summary becomes a competing licence |

Reuse an existing repo's `LICENSE` as the base rather than drafting from scratch, then run the checks
below over the copy. Copying carries two defects forward every time: the previous enforcement contact
in the conduct file, and a first line naming the previous course ("These workshop materials").

## The section order, when there is no base copy to reuse

Twelve numbered sections, in this order, after a title line, the copyright line, an
intellectual-property paragraph naming the governing copyright act, and the free-initiative preamble:

1. Definitions (`You`, `Personal Use`, `Organization`, `Commercial Use`)
2. Grant of Permission
3. Prohibited Without a Paid Written License (lettered clauses a to g)
4. Commercial, Non-Profit, and Training Licenses (the contact block)
5. Reservation of Rights
6. Term and Termination
7. Contractual Penalty (Vertragsstrafe, with the court's right to review the amount)
8. No Warranty
9. Limitation of Liability (intent and gross negligence only; mandatory statutory liability unaffected)
10. Governing Law (substantive law only, excluding conflict-of-law rules and the CISG)
11. Place of Jurisdiction (name the city; consumer protections unaffected)
12. Severability

Sections 7 and 9 to 11 are the Austrian-specific ones. For another jurisdiction, keep the slots and
have counsel replace the content rather than dropping the sections.

## Free for the individual, licensed for the organization

The structure that expresses this without contradiction:

1. **Definitions.** `Personal Use` = a natural person, purely private capacity, own self-study, no
   direct or indirect organizational benefit. `Organization` = the widest possible list. `Commercial
   Use` = anything that is not Personal Use.
2. **Grant.** One limited, personal, non-exclusive, non-transferable, revocable permission, for
   Personal Use, free of charge.
3. **Prohibitions.** Everything else, each as its own lettered clause.

Say "free of charge" inside the grant clause itself. A reader who has been told the materials are a
gift and then reads a wall of prohibitions needs the permission to be as concrete as the bans.

## Excluding non-profit use takes three edits, not one

"Also exclude non-profit use" reads like one word in one definition. It is three independent edits,
because a reader arrives directly at a clause and never reads the definitions above it:

1. **The `Organization` definition** names them explicitly: non-profit organization, charity, NGO,
   volunteer initiative, community group, association, foundation, school, university, public body.
   Close it with "whether or not it pursues profit".
2. **The `Commercial Use` definition** states the consequence: "Use is Commercial Use regardless of
   the user's legal form, tax status, or funding model, and the absence of profit, of a fee, or of
   commercial intent does not make a use permitted."
3. **Each prohibition clause** repeats it in its own terms: the by-or-for-an-organization clause ends
   "even where the delivery is described as internal, educational, charitable, or non-profit", and the
   delivery clause ends "whether for profit or not for profit".

The readme summary then repeats it a fourth time, because most readers never open the `LICENSE`.

Generalize the shape: **an exclusion belongs in every clause a reader can stop at, not only in the
definition it logically modifies.** After adding one, read each prohibition alone and ask whether that
sentence by itself answers the question.

## Giftor, author, licensor: three roles, one casual word

When a second organization joins as a sponsor or co-giftor of a free initiative, it belongs in the
sentences describing the gift: the readme intro, the readme licence paragraph, and the `LICENSE`
preamble. It does **not** automatically belong in the copyright line or the defined term `Licensor`,
which decide who owns the rights and who may grant them.

Change only the role that was actually named, then say plainly what you left alone and offer the
other change. Widening the rights holder is invisible in a diff review and expensive to unwind.

## The free-initiative framing

Where the course is published as a free contribution, put that in the `LICENSE` preamble too, next to
the "this is not open source" sentence, and bound it in the same paragraph:

> The Materials are published as part of a free initiative of <giftors> to help <audience>. Free of
> charge for an individual learner is exactly the permission granted in Section 2, and nothing more.

The bound sentence is what stops the generous framing from being read as a general grant.

## Verify

- Every prohibition clause, read in isolation, answers "may a non-profit deliver this?" with no.
- `grep -n "non-profit\|not for profit" LICENSE` returns hits in the definitions **and** in the
  prohibitions, not only in the definitions.
- The conduct file's enforcement email is this repo's owner: `grep -n "@" CODE_OF_CONDUCT.md`.
- The readme summary carries the "does not modify it" disclaimer and links `LICENSE` and
  `CODE_OF_CONDUCT.md` with paths that resolve.
- The copyright line and every `Licensor` mention name exactly the party the user said owns the
  rights, and no one added along the way as a sponsor.
- No em dashes anywhere in the three files.
