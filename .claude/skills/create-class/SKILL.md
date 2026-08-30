---
name: create-class
description: >-
  Master skill for authoring a hands-on course or masterclass repository end to end,
  for any audience (developer, low-code maker, business user). It is the single entry
  point that delegates to reference leaves: module-toc-conception, scaffold,
  create-teaching, create-guide, create-slides, dashboard, run-demo, run-foundry-demo,
  run-guide-browser, verify-by-execution, licensing, and the repo-local brand-voice-* skill. Use when building or
  maintaining any course repo organized as numbered modules under demos/ and labs/.
  Trigger phrases: create a class, build a class, author a course, scaffold a new class,
  bootstrap course layout, generate modules from outline, conceive the toc, order the
  modules, name a topic, engaging titles, restructure demos, write a demo, author a lab,
  create slides, topic to
  slides, enrich module readme, class dashboard, module status, whats missing, run demo,
  verify code demo, run guide in browser, evaluate guide, verify the labs, audit the course,
  does this guide still work, brand voice check, quality
  check, business class, maker class, code class, add a license to the class, license and re-use
  section, code of conduct, proprietary course license, exclude non-profit use, who may teach this,
  free for personal use, commercial training license.
license: CC-BY-NC-SA-4.0
---

# Create Class

One master skill for the full course-authoring lifecycle. It is the entry point that
routes a request to the right leaf. Each leaf lives at `references/<leaf>.md` under this
skill; delegate by READING that file, never by a `Skill` call. Shared assets live under
`templates/`. This master holds no leaf content of its own; it decides which reference to
read and enforces the cross-cutting rules below.

Classes differ by audience: some are code classes, some are for low-code makers, some
are for business users. The authoring engine is the same for all of them. The one
capability that stays per-repo is brand voice, because each audience reads differently.

## How to use this skill

Identify which phase the request belongs to, then read the matching reference. When a
request spans phases (for example "scaffold a class and write the first guide"), walk the
phases in order and read each reference as you reach it. Do not reimplement a leaf's job
here; follow the reference.

## Phases and leaf references

### Phase 1 - Conceive and scaffold the layout

| Task | Leaf reference |
|------|----------------|
| Conceive the module and topic structure: naming, ordering, sizing, one-capability-per-module, and the master-TOC format; also restructuring, retitling, splitting, or reordering an existing course | `references/module-toc-conception.md` |
| Bootstrap a base repo from questions or an outline; create numbered module and topic folders under `demos/` and `labs/` | `references/scaffold.md` |

### Phase 2 - Author content

| Task | Leaf reference |
|------|----------------|
| Enrich a module README with a use-case intro, a topic-specific slash-command table, and key links (audience-adapted) | `references/create-teaching.md` |
| Write a demo or lab guide (`NN-topic/demo-slug.md` / `lab-NN-slug.md`) in the right style: prompt-recipe, guided, or walkthrough | `references/create-guide.md` |
| Turn a demo that is executed into a demo that is presented: a timed `demo-presenter-<slug>.md` cheat sheet whose beats carry `**Open:**` links, a `**Say:**` line, the snippet, a `**Result:**` link to what the run wrote, and a `**Gotcha:**` | `references/create-demo-essentials.md` |
| Turn a topic readme into slides, via the Gamma path or the local pptx path | `references/create-slides.md` |

### Phase 3 - Quality and polish

| Task | Leaf reference |
|------|----------------|
| Audit and fix Markdown for brand voice, including verb-first headings | Repo-local `brand-voice-*` skill (see note below) |
| Author the repo's `LICENSE`, `CODE_OF_CONDUCT.md` and readme `## License & Re-Use` summary: proprietary terms, free for a private individual, licensed for every organization including non-profits, and the giftor-versus-licensor split | `references/licensing.md` |

Brand voice is not owned by this master. Discover the repo-local skill with Glob
`.claude/skills/brand-voice-*` and invoke it (for example `brand-voice-copilot` or
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

| Task | Leaf reference |
|------|----------------|
| Set up, evaluate, render, show, update, test, or publish the class progress dashboard | `references/dashboard.md` |

The dashboard is optional per class. Use it only when a class wants a progress board.

### Phase 5 - Run and verify

| Task | Leaf reference |
|------|----------------|
| Run and verify a code demo (.NET, Python, Node), then fold findings back into the guide | `references/run-demo.md` |
| Run and verify a Microsoft Foundry or Agent Framework demo | `references/run-foundry-demo.md` |
| Run a guide as a real user in a live browser or desktop app, then rewrite it from what worked | `references/run-guide-browser.md` |
| Audit guides by executing them: the defect taxonomy execution finds and review never does, cheap verification techniques, and honest not-executed reporting | `references/verify-by-execution.md` |

Guides are run-verified first, then written. Pair `references/create-guide.md` with
`references/run-demo.md` / `references/run-foundry-demo.md` for code, and with
`references/run-guide-browser.md` for prompt-recipe guides. Any guide shipping commands, scripts,
hooks, workflows, or harness config also gets a pass with `references/verify-by-execution.md`.

## Diagrams

Diagrams in guides and slides are authored by the standalone `mermaid-expert` skill.
It is a shared dependency, not part of this master. Invoke it for any flowchart,
sequence diagram, architecture diagram, topic flow, or ERD.

## Cross-cutting rules

These apply across every phase and override any looser guidance in a leaf reference:

- **Settle the subject before the register.** A request to "adjust the language for the audience" carries an unstated premise that the course is about the right thing, and that premise is the expensive one to get wrong: a voice pass over material with the wrong subject makes it fluent and leaves it about the wrong thing. Before any rewrite for an audience, state what the learner should be able to DO at the end and confirm it. The tell is module titles naming the domain job rather than the capability being taught (inventory, crawl, verify describe a pipeline, not a syllabus). When a class uses a real job to teach a tool, the job is the playground: mechanics the tool handles belong in an optional deep-dive or a skill, never in the teaching path.
- **Ask for one real sample before authoring a voice gate.** When the deliverable is a brand voice, register or house style, ask for an example of the target voice first. A transcript of the user actually working (a prompt-history file, a time ledger, an earlier chat in a sibling repo) beats a page of derived principles and costs one question instead of one rewrite.
- No em dashes in prose. Use `,` `;` `:` or `()`.
- Max 4 sentences per paragraph.
- Mermaid node labels use `"quoted<br/>labels"`, never `\n`.
- Slash-command tables are topic-specific, never the same generic set in every module.
- The master TOC is bare keyword links; topic descriptions live in module tables, never in the TOC. A topic title appears in the TOC bullet, the topic H1, and the module table, and must stay in sync. Titles must earn attendance, never `Overview` / `Demos` / a bare noun. See `module-toc-conception`.
- Code fences must declare a language, with no exceptions; prompt blocks are ```text.
- Internal links use relative paths; anchors use `#heading-name`.
- Demos and labs meet the substance bar in `create-guide` (see "What makes a guide worth shipping"): a demo teaches a real capability, a lab is a genuine 20+ minute build, both concept-first with copy-paste inputs and a described Expected result at every step. Setup or navigation is never a demo.
- "Teaching" a topic means both, not either: the topic `readme.md` is developed, concept-first LEARNING prose a student reads under descriptive subheadings (never an instructor "what to teach" bullet outline), AND the topic carries both a Hands-On Demo and a Hands-On Lab. A "learning" is a hands-on lab.
- Validate product names, availability, and version facts against Microsoft Learn (the MS Learn MCP) before authoring slides or prose; never assert a product fact from memory.
- It is "Microsoft Foundry", never "Azure AI Foundry" (the product was renamed). Never write the old name in course content.
- Layout is unified: numbered module folders under `demos/` and `labs/`, with each demo
  guide inside the numbered topic folder it teaches as `demo-<slug>.md`, and its runnable
  starter beside it plus a `<starter>-solution/` sibling.
- After writing or significantly editing any README or guide, invoke the repo-local
  `brand-voice-*` skill to verify.
- Never overwrite existing files during scaffolding; skip and report instead.
- Parallelize all independent work (file reads, searches, subagent tasks).

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

