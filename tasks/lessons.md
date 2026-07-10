# Lessons

Self-improvement log for the "Agentic Software Engineering using GitHub Copilot" course-authoring repo. Each entry is a pattern plus a rule that prevents recurrence (see the CLAUDE.md Self-Improvement Loop). Captured and maintained by the `claude-learn` skill.

## Windows git mv fails on .NET project folders (bin/obj lock)

**Pattern:** Restructuring `demos/` with `git mv` failed with "Permission denied" on every folder containing a .NET project, because the C# language server and active builds hold open handles on the compiled DLLs in gitignored `bin`/`obj`. Deleting the artifacts alone did not help when a build immediately regenerated them (14 dotnet and 56 node processes were running).
**Rule:** Do not mass-kill dev processes. Clear the gitignored `bin`/`obj` under the source tree and run the delete plus `git mv` as one atomic command so the rename wins the rebuild race. Folders with no build output (pure markdown) rename without this. Pre-clear before a large restructure.

## A user-invocable master skill must not disable model invocation

**Pattern:** `/create-class` errored with "cannot be used with Skill tool due to disable-model-invocation" because its `SKILL.md` frontmatter set `disable-model-invocation: true`.
**Rule:** For any skill the user invokes by slash command, do not set `disable-model-invocation: true` (remove it or set false). Keep the flag only for skills that must never be model-invoked or user-invoked.

## demos/readme.md TOC drifts from the actual folders

**Pattern:** The course readme TOC referenced paths that did not exist on disk (Module 2 numbering off from 06 onward, a dangling `10-debug-panel`, a Module 5 `01-azd-agentic` that actually lived under `02-IaC/01-azd`). The drift predated the modernization.
**Rule:** After any edit to `demos/` structure or the readme TOC, verify every TOC link resolves to a real directory and that no parent has a duplicate numeric prefix. Update `.inventory/target-structure.md` when the structure moves.

## Run brand voice at author time, not after

**Pattern:** Brand-voice fixes are cheap to fold in while writing but expensive to sweep later across many files.
**Rule:** After writing or significantly editing any `demos/` README, invoke `brand-voice-gh-copilot` before considering the file done. Authoring agents must apply the rules as they write (no em dashes, at most 4 sentences per paragraph, quoted Mermaid `<br/>` labels).

## Ground authored content in the sources; never invent specifics

**Pattern:** The pre-existing `02-models` readme contained invented, internally inconsistent model names and versions.
**Rule:** Constrain authoring to the source anchors in `.inventory/` and the modernization brief (VS Code release notes, product pages). Where the source lacks depth, explain the concept generally rather than fabricating settings, versions, or model names.

## Parallelize inventory and authoring with self-sufficient module agents

**Pattern:** Fanning out one agent per module (inventory first, then authoring) with the source anchors, repo style exemplars, and brand-voice rules baked into each prompt produced consistent, on-spec output quickly.
**Rule:** For multi-module sweeps, delegate one scoped agent per module and make each self-sufficient: name the exemplars to read, the sources to ground in, and the hard constraints. Verify centrally afterward (em dash, Mermaid labels, link resolution).
