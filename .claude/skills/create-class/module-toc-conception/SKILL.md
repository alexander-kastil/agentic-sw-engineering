---
name: module-toc-conception
description: >-
  Conceive and structure a course's module and topic layout and its master table of contents:
  name topics so they earn attendance, order modules and topics to build knowledge, keep the
  master TOC in the author's bare-keyword-link format, keep each title in sync across the TOC,
  the topic H1, and the module table, size modules so they feel substantial, and keep each
  capability in exactly one module. Peer subskill of create-class, used before and during
  scaffolding and whenever restructuring an existing course. Trigger phrases: conceive the toc,
  design the module structure, order the modules, name a topic, retitle a topic, master toc
  format, toc bullets, module overlap, thin module, split a module, swap modules, agenda,
  course outline, engaging titles, restructure demos.
metadata:
  type: reference
---

# Module & TOC Conception

The information architecture of a course: how the modules and topics are named, ordered, sized,
and surfaced in the master table of contents. This is the conception layer above `scaffold`
(which creates folders) and `create-teaching` (which fills a module README). Reach for it before
scaffolding a new class and whenever restructuring an existing one.

## The master TOC format is a contract

The master TOC (the module list in `demos/readme.md`) is a module heading followed by a `ul` of
BARE keyword links, one per topic. Do not add per-bullet descriptions, a `- ... - prose` suffix,
or any text after the link. Descriptions belong in the module README's topic table, never in the
master TOC. Never change this format; the author's TOC shape is deliberate.

## Titles must earn attendance

Every topic and module title has to make a prospective attendee want that session. Before shipping
a title, ask: "would someone sign up because of this line?" Ban dead titles: `Overview`,
`Introduction`, `Demos`, `Basics`, a bare noun, or a title that just repeats the module name.
Prefer specific, evocative titles that name the capability and its payoff, for example
`Building Agents with Custom Tools` over `SDK Demos`, or `Subagents as Subject-Matter Experts`
over `Subagents`.

## One title, three places, always in sync

A topic's display title appears in three files: the master TOC bullet, the topic's own H1, and the
module README's table row. When a topic's content, framing, or name changes, update all three in
the same pass. Changing the topic body without retitling the TOC is the most common miss; changing
one label and not the others leaves the course inconsistent.

## Order to build knowledge

Sequence modules and topics from foundation to application to administration. Teach how to USE a
capability before how to MANAGE or administer it, and build from the simplest case to the most
advanced. Never open a module with its heaviest or most advanced topic; lead with a gentle,
high-engagement starter (delegating to cloud agents is a poor first topic, a subagent or a
read-only research agent is a better one). When the author asks for an order you would not choose,
their sequencing wins.

## One capability, one home

Each capability belongs to exactly one module. Before adding a topic, confirm it does not overlap
another module's territory. Keep a capability map for the course and respect it, for example CI/CD
and infrastructure as code live in the DevOps module, permissions and cost and bring-your-own-key
model routing live in Governance, framework migration lives in the agentic-coding module, and
defining MCP servers and skills lives in the harness or tools module. A topic that duplicates
another module is a signal to pick a different topic, not to add it.

## Size modules so they feel substantial

A module of three or four thin topics reads as weak and unsellable. Aim for roughly five to six
substantive topics per module, and give each topic real depth. When a topic sits at the bare
mechanic level (for example "Subagents" explaining only the delegation UI), flag it and take it
deeper (subagents as subject-matter experts with their own instructions, tools, and model). When a
module is thin, enrich it by adding genuinely distinct topics or by moving a related topic in.

## Do not invent; confirm additions

Use the repo's established or original module and topic names. Never invent a module name or add a
module or topic the author did not ask for. When adding topics to fill out a thin module, propose
the specific topics and confirm the choice before authoring them, because topic selection is the
author's call.

## Structural changes ripple

Renaming, reordering, splitting, or merging a module is never a one-file edit. It requires: renumber
the affected folders with `git mv` to preserve history, fix every internal link that pointed at a
moved path, update the master TOC and the affected module READMEs, and update the schedule table and
the narrative "story" in `demos/readme.md`. After any structural change, verify zero broken relative
links across the tree before reporting done.

## Writing style

No em dashes in anything this subskill produces or in this file itself. Use a colon, comma,
semicolon, or parentheses instead.
