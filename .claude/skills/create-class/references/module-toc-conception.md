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

## Core and Optional tracks keep a long course deliverable

A course that grew to 30 hours of labs is not delivered by deleting content. Mark exactly one lab
per module as Core and every other lab as Optional: the Core path is the spine an instructor can
actually run in a day, and nothing is lost from the repo. One 30-hour course collapsed to a 13-hour
core path this way, with the Optional labs still there for self-study and follow-up.

State prerequisites that sit outside learner effort separately from the lab times. Accounts, API
keys, toolchain downloads, and tenant access are real blockers with real durations, and folding them
into a lab estimate makes every number wrong. Give them their own list with what must be arranged
before the class starts.

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

Before writing or repointing a cross-module link, confirm the target folder's CURRENT name in the
working tree (glob or `ls`), never the name from the session-start git snapshot: that snapshot is
stale, and a parallel restructure of another module may have already renumbered the folder you are
linking to (for example `01-intro/04-licensing-setup` becoming `05-licensing-setup`). Match links to
the live tree. Leave any unrelated in-progress folder renames untouched; scope your edits to your own
module plus the specific inbound links that point into it.

## Splitting one topic into two

A topic covering two capabilities under one number ("Git Worktrees & Agents View") is a split
waiting to happen: the compound title is the tell, and so is a readme whose second half never
appears in the demo. Splitting is cheap; leaving half the references pointing at the old shape is
what breaks the course.

Move the prose first, then sweep every place the old topic was named. All of these go stale
together, and missing one leaves a course that reads correctly in isolation and wrongly as a whole:

| Target | What to change |
|---|---|
| Source topic `readme.md` | Remove the moved section; re-scope the intro, H1, and Key Topics links |
| Source topic slash-command table | Hand the moved topic's commands to the new topic; each table stays distinct |
| New topic `readme.md` | Full teaching prose, its own slash-command table, its own Hands-On links |
| Module opening bullet list | The line that summarised the compound topic |
| Module topic table | Rename the old row, add the new one |
| Module demo table | Same, one row per demo |
| Sibling guides' Related Topics | Link text naming the old compound title |
| Slide specs | Renumber `NN-MM-*.md` into the new topic, and update `topic:`, `slide:`, `order:`, `source:` |

The new topic needs its own demo, not a pointer back to the old one. If the split leaves one half
without enough substance for its own demo and lab, it was not a topic; fold it back.

The new topic's H1 must name the capability, not just describe the benefit. `Supervise Many
Sessions From One Screen` reads well and is unfindable by a learner scanning for the feature;
`Supervise Background Sessions with the Agents View` earns attendance and names the thing. Match
the sibling topics' pattern: verb, then the feature by name.

## Modernizing an outdated course

When the entry point is "this module is outdated" (not a fresh scaffold), the failure mode is
restructuring from memory. Work in this order:

1. Ground before you restructure. Research the CURRENT vendor learning path and each named
   product in parallel, one agent per pillar, each grounding every fact in the authoritative
   source (the MS Learn MCP for Microsoft content) and returning structured facts plus verified
   URLs. Synthesize the proposed TOC from that, never from memory: product taxonomies shift fast
   (renames like Azure AI Foundry to Microsoft Foundry, split tools like the Copilot Studio agent
   builder, frameworks merging like Semantic Kernel and AutoGen into the Agent Framework, and new
   products reaching GA).
2. Migrate runnable assets with `git mv`, do not rebuild. Move existing project folders into the
   new numbered topic folders so rename history survives, then re-point every inbound reference
   (the repo `CLAUDE.md` layout and runnable-project paths, parent indexes, cross-links) and verify
   no stale path remains before reporting done.
3. The repo's `CLAUDE.md` wins over this skill's defaults. Depth (heavy teaching prose vs a
   lightweight link-hub readme), whether a `labs/` tree exists, and brand voice all follow the
   project's established conventions. When an existing repo's style differs from the create-class
   defaults, confirm structure, style, and scope with the author before authoring, and match the
   repo.

## Writing style

No em dashes in anything this subskill produces or in this file itself. Use a colon, comma,
semicolon, or parentheses instead.
