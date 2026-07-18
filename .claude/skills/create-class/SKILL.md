---
name: create-class
description: >-
  Master skill for authoring a hands-on course or masterclass repository end to end,
  for any audience (developer, low-code maker, business user). It is the single entry
  point that delegates to standalone peer skills: scaffold, create-teaching,
  create-guide, create-slides, dashboard, run-demo, run-foundry-demo, run-guide-browser,
  and the repo-local brand-voice-* skill. Use when building or maintaining any course
  repo organized as numbered modules under demos/ and labs/. Trigger phrases: create a
  class, build a class, author a course, scaffold a new class, bootstrap course layout,
  generate modules from outline, write a demo, author a lab, create slides, topic to
  slides, enrich module readme, class dashboard, module status, whats missing, run demo,
  verify code demo, run guide in browser, evaluate guide, brand voice check, quality
  check, business class, maker class, code class.
disable-model-invocation: true
license: CC-BY-NC-SA-4.0
---

# Create Class

One master skill for the full course-authoring lifecycle. It is the entry point that
routes a request to the right standalone peer skill. Each peer is a real skill in its
own folder under `.claude/skills/`, independently invocable and also delegated to from
here by name. This master holds no leaf content of its own; it decides which skill to
invoke and enforces the cross-cutting rules below.

Classes differ by audience: some are code classes, some are for low-code makers, some
are for business users. The authoring engine is the same for all of them. The one
capability that stays per-repo is brand voice, because each audience reads differently.

## How to use this skill

Identify which phase the request belongs to, then invoke the matching peer skill. When
a request spans phases (for example "scaffold a class and write the first guide"), walk
the phases in order and invoke each peer as you reach it. Do not reimplement a peer's
job here; delegate to it.

## Phases and peer skills

### Phase 1 - Scaffold the layout

| Task | Peer skill |
|------|-----------|
| Bootstrap a base repo from questions or an outline; create numbered module and topic folders under `demos/` and `labs/` | `scaffold` |

### Phase 2 - Author content

| Task | Peer skill |
|------|-----------|
| Enrich a module README with a use-case intro, a topic-specific slash-command table, and key links (audience-adapted) | `create-teaching` |
| Write a demo or lab guide (`demo-NN-slug.md` / `lab-NN-slug.md`) in the right style: prompt-recipe, guided, or walkthrough | `create-guide` |
| Turn a topic readme into slides, via the Gamma path or the local pptx path | `create-slides` |

### Phase 3 - Quality and polish

| Task | Peer skill |
|------|-----------|
| Audit and fix Markdown for brand voice, including verb-first headings | Repo-local `brand-voice-*` skill (see note below) |

Brand voice is not owned by this master. Discover the repo-local skill with Glob
`.claude/skills/brand-voice-*` and invoke it (for example `brand-voice-cowork` or
`brand-voice-code`).

If no `brand-voice-*` skill exists in the repo, bootstrap one before writing content.
Ask the user 3 to 4 short questions:

1. Who is the audience (developer, low-code maker, business user, or a specific role)?
2. What tone fits (hands-on and technical, plain and outcome-focused, formal)?
3. Any hard rules to enforce (for example no em dashes, quoted Mermaid labels, sentence
   case headings, paragraph length cap)?
4. What short suffix names the skill (for example `code`, `cowork`, `sales`)?

Then create `.claude/skills/brand-voice-<suffix>/` with a `SKILL.md` (non-empty `name`
and `description` carrying trigger phrases) and a `references/rules.md` holding the
agreed rules. Keep it repo-local. Never globalize brand voice and never fold it into
this master.

### Phase 4 - Track completeness

| Task | Peer skill |
|------|-----------|
| Set up, evaluate, render, show, update, test, or publish the class progress dashboard | `dashboard` |

The dashboard is optional per class. Use it only when a class wants a progress board.

### Phase 5 - Run and verify

| Task | Peer skill |
|------|-----------|
| Run and verify a code demo (.NET, Python, Node), then fold findings back into the guide | `run-demo` |
| Run and verify an Azure AI Foundry or Agent Framework demo | `run-foundry-demo` |
| Run a guide as a real user in a live browser or desktop app, then rewrite it from what worked | `run-guide-browser` |

Guides are run-verified first, then written. Pair `create-guide` with `run-demo` /
`run-foundry-demo` for code, and with `run-guide-browser` for prompt-recipe guides.

## Diagrams

Diagrams in guides and slides are authored by the standalone `mermaid-expert` skill.
It is a shared dependency, not part of this master. Invoke it for any flowchart,
sequence diagram, architecture diagram, topic flow, or ERD.

## Cross-cutting rules

These apply across every phase and override any looser guidance in a peer skill:

- No em dashes in prose. Use `,` `;` `:` or `()`.
- Max 4 sentences per paragraph.
- Mermaid node labels use `"quoted<br/>labels"`, never `\n`.
- Slash-command tables are topic-specific, never the same generic set in every module.
- Code fences must declare a language.
- Internal links use relative paths; anchors use `#heading-name`.
- Demos and labs meet the substance bar in `create-guide` (see "What makes a guide worth shipping"): a demo teaches a real capability, a lab is a genuine 20+ minute build, both concept-first with copy-paste inputs and a described Expected result at every step. Setup or navigation is never a demo.
- Layout is unified: numbered module folders under `demos/` and `labs/`.
- After writing or significantly editing any README or guide, invoke the repo-local
  `brand-voice-*` skill to verify.
- Never overwrite existing files during scaffolding; skip and report instead.
- Parallelize all independent work (file reads, searches, subagent tasks).
