# Lessons

Self-improvement log for the "Agentic Software Engineering using GitHub Copilot" course-authoring repo. Each entry is a pattern plus a rule that prevents recurrence (see the CLAUDE.md Self-Improvement Loop). Captured and maintained by the `claude-learn` skill.

## Windows git mv fails on .NET project folders (bin/obj lock)

**Pattern:** Restructuring `demos/` with `git mv` failed with "Permission denied" on every folder containing a .NET project, because the C# language server and active builds hold open handles on the compiled DLLs in gitignored `bin`/`obj`. Deleting the artifacts alone did not help when a build immediately regenerated them (14 dotnet and 56 node processes were running).
**Rule:** Do not mass-kill dev processes. Clear the gitignored `bin`/`obj` under the source tree and run the delete plus `git mv` as one atomic command so the rename wins the rebuild race. Folders with no build output (pure markdown) rename without this. Pre-clear before a large restructure.

**Amendment (metro restructure):** one clear-and-rename is not enough. A watcher re-acquires the handle within seconds, so the delete and the move must be a retry loop (5 attempts, 1s apart), with `dotnet build-server shutdown` run once per session first. The same `git mv` failed five times and then succeeded with nothing else changed. To find the real holder, rename every subdirectory to a scratch name and back: the refuser is always `obj/Debug`, which makes every parent above it look locked. All of this is now scripted in `~/.claude/skills/create-class/scripts/renumber-tree.sh`.

## Read tasks/lessons.md before the first structural action

**Pattern:** The bin/obj lock entry above was already in this file, with a working rule, when the metro restructure began. It was not read, so the same lock was re-diagnosed from scratch across six failed `git mv` batches, a process hunt and two lock scans. CLAUDE.md already says to review lessons at session start.
**Rule:** Read `tasks/lessons.md` before the first structural or destructive action in a session, not just at session start in principle. And when any command fails twice with the same error text, grep the lessons file for a distinctive phrase from that error before improvising a diagnosis.

## A bulk rename reads as data loss: lead with the receipt

**Pattern:** After 628 history-preserving renames the owner asked twice whether the demos had been lost ("i have the impression you lost all the demos", "there were no demos in the folders?"). The completion report had listed the new tree but never stated the invariant, and a rename-heavy diff looks exactly like a mass deletion in a file explorer and in most git UIs.
**Rule:** Open the report of any bulk move with the loss receipt, unprompted: identical `git ls-files` count before and after, an identical sorted blob hash against HEAD, and the `git status` breakdown showing renames and zero deletions. Then the old-to-new table. Extracting that proof afterwards, under an accusation, costs far more than stating it first.

## One writer per file when a fan-out verifies its own work

**Pattern:** The verify phase gave two agents fix authority over the same markdown tree. Each saw the other's edits as an unexplained concurrent writer and had to caveat its report: "corrected in the working tree by a concurrent writer during my run, not by me".
**Rule:** In any fan-out, exactly one agent holds write authority over a given file set. A second reviewer is valuable, but it reports and the writer applies. A verification whose report has to disclaim its own findings cannot be quoted as verification.

## A gap in a customer outline is a question, not a guess

**Pattern:** `assets/metro.md` numbered its modules 2, 3, 4, 5, 7, 8, 9. Three defensible readings of the missing 6 produced three different trees. The option chosen by the owner was the one ranked third, so any assumption would have been wrong.
**Rule:** When an outline skips a slot, stop and ask, with the resulting folder tree rendered in each option's preview. A structural choice is read far faster as a tree than as a sentence, and the literal reading is not always the wanted one.

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

## A model name in agent frontmatter is a picker label, not a model id

**Pattern:** Switching every `.github/agents/*.agent.md` to a BYOK DeepSeek model needed the `model:` value, and the model JSON the user supplied carried three plausible candidates: `id` (`deepseek-v4-flash`), `owned_by` (`deepseek`), and `displayName` (`DeepSeek V4 Flash`). None of them is the answer on its own. The field takes the label VS Code shows in the picker, `<displayName> (<vendor id>)`, and the vendor id lives only in the registering extension's `package.json` under `contributes.languageModelChatProviders[].vendor`, which for the OAI Compatible bridge is `oaicopilot`, not `owned_by` and not the provider's own `displayName` ("OAI Compatible").
**Rule:** Resolve the suffix by reading the extension manifest in `~/.vscode/extensions/<publisher>.<ext>-<version>/package.json`, never by inferring it from the model entry. The existing files in this repo were already the corroborating evidence: `(copilot)` for built-in models and `(aitk-foundry)` for the AI Toolkit provider are the same rule with a different vendor id. Full procedure in the global `copilot-model` skill, leaf `references/vscode-chat.md`.

## Judge a delegation test on tool calls, not on the plan it prints

**Pattern:** `DeepSeek V4 Flash (oaicopilot)` was confirmed to drive the `Team Orchestrator` agent team correctly, including real subagent handoffs. The check that matters is not the orchestrator's `## Execution Plan` block, which a model will happily produce while doing nothing: it is whether `agent` tool calls appear in the trace and whether the subagents' files land on disk.
**Rule:** When testing a model behind an OpenAI-compatible bridge for agentic use, give it a task that forces a genuine fan-out (several deliverables splitting across two specialists with no file overlap, scoped to a throwaway folder) and grade it on the tool calls plus the files, never on the narration. Narrating a delegation instead of invoking it is the characteristic shim failure.
