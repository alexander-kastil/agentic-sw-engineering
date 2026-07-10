---
name: create-class
description: >-
  Master skill for authoring a hands-on course or masterclass repository end to end:
  scaffold the module/topic/lab layout, write demo and lab guides, generate slide specs,
  enrich module READMEs, enforce brand voice, polish headings, track completeness on a
  live dashboard, evaluate guides by running them, and propose business enhancements.
  Delegates to task-oriented leaf references. Use when building or maintaining any course
  repo organized as numbered modules under demos/ and labs/. Trigger phrases: scaffold a
  new class, bootstrap course layout, generate modules from outline, scaffold module,
  create a guide, write a demo, author a lab, create slides, topic to slides, pptx from
  readme, enrich module readme, helpful slash commands table, brand voice check, quality
  check, fix em dashes, polish slugs, verb-first headings, class planning, module status,
  what's missing, setup dashboard, show status, update class status, test dashboard,
  publish class dashboard, github pages dashboard, evaluate guide, run guide, test guide,
  enhance for business owner, business demos.
license: CC-BY-NC-SA-4.0
---

# Create Class

One master skill for the full course-authoring lifecycle. It replaces a sprawl of
single-purpose skills (`scaffold-class`, `scaffold-module`, `create-guide`, `create-slides`,
`create-learning`/`create-teaching`, `polish-slug`, `class-planning`,
`setup-dashboard`, `show-status`, `update-class-status`, `test-dashboard`,
`publish-class-dashboard`, `evaluate-guide`, `enhance-for-business-owner`) with one entry point
that delegates to leaf references under `references/`.

This skill is intentionally generic and audience-neutral, so it can live at the personal
(global) level and be reused across different classes. Brand voice is the one capability it
does NOT bundle: a GitHub Copilot class and a Cowork class write for different audiences, so brand
voice stays a repo-local skill. The master discovers it at run time by globbing
`.claude/skills/brand-voice-*` in the current repo and invokes that skill. Never globalize brand
voice and never fold it back into this master.

## How to use this skill

Identify which phase the request belongs to, then read and follow the matching leaf reference.
Each leaf is self-contained; load only the one(s) the task needs. Do not load every reference up
front. When a request spans phases (for example "scaffold a class and write the first guide"),
walk the phases in order, loading each leaf as you reach it.

## Phases and leaves

### Phase 1 - Scaffold the layout

| Task                                                                                        | Leaf                                             |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Bootstrap a whole course from an outline file; create numbered topic folders under a module | [references/scaffold.md](references/scaffold.md) |

### Phase 2 - Author content

| Task                                                                                              | Leaf                                                       |
| ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Write a demo or lab guide file (`demo-NN-slug.md` / `lab-NN-slug.md`) with companion assets       | [references/author-guide.md](references/author-guide.md)   |
| Turn a topic readme into Gamma-ready slide spec files in `pptx/`                                  | [references/author-slides.md](references/author-slides.md) |
| Enrich a module README with a use-case intro, a topic-specific slash-command table, and key links | [references/enrich-module.md](references/enrich-module.md) |

### Phase 3 - Quality and polish

| Task                                                                                               | Leaf                                                   |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Audit and fix Markdown for brand voice (em dashes, Mermaid labels, paragraph length, slash tables) | Repo-local `brand-voice-*` skill (see note below)      |
| Rewrite H1 headings across `demos/` to be verb-first                                               | [references/polish-slug.md](references/polish-slug.md) |

Brand voice is not a leaf of this skill. Discover the repo-local skill with Glob
`.claude/skills/brand-voice-*` and invoke it (in this repo, `brand-voice-gh-copilot`). If no
`brand-voice-*` skill exists in the repo, report that and skip the brand-voice step rather than
applying a generic ruleset.

### Phase 4 - Track completeness

| Task                                                                          | Leaf                                               |
| ----------------------------------------------------------------------------- | -------------------------------------------------- |
| Set up, evaluate, render, show, test, or publish the class progress dashboard | [references/dashboard.md](references/dashboard.md) |

### Phase 5 - Evaluate and enhance

| Task                                                                                                | Leaf                                                             |
| --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Run a demo guide as a real user in the live Claude Desktop app and fix it from what actually worked | [references/evaluate-guide.md](references/evaluate-guide.md)     |
| Audit all demos, rank business enhancements by wow-factor, and implement the top picks              | [references/enhance-business.md](references/enhance-business.md) |

## Templates

Shared template assets live under `templates/`:

| Path                                   | Used by                                                                         |
| -------------------------------------- | ------------------------------------------------------------------------------- |
| `templates/scaffold/`                  | scaffold leaf (module, topic, lab, labs-index, CLAUDE.md, dashboard.json stubs) |
| `templates/dashboard/`                 | dashboard leaf (static web app + evaluator/render/test scripts)                 |
| `templates/update-class-dashboard.yml` | dashboard leaf (GitHub Pages workflow)                                          |

## Cross-cutting rules

These apply across every phase and override any looser guidance in a leaf:

- No em dashes in prose. Use `,` `;` `:` or `()`.
- Max 4 sentences per paragraph.
- Mermaid node labels use `"quoted<br/>labels"`, never `\n`.
- Slash-command tables are topic-specific, never the same generic set in every module.
- Code fences must declare a language.
- Internal links use relative paths; anchors use `#heading-name`.
- After writing or significantly editing any README or guide, invoke the repo-local `brand-voice-*` skill to verify.
- Never overwrite existing files during scaffolding; skip and report instead.
- Parallelize all independent work (file reads, searches, subagent tasks).
