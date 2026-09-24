# Solution: The Generated Project, Verified

[The topic page](../readme.md) draws the project structure and lists the commands. This folder is the same information taken from a real `specify init` on 2026-09-21, so the tree can be checked rather than trusted.

Environment: Windows 11, `specify` 1.0.9, `uv` 0.9.18, Python 3.12.10.

## Every file init wrote

```bash
specify init meeting-cost --integration copilot --script py
cd meeting-cost
find . -type f | sort
```

```text
.github/skills/speckit-analyze/SKILL.md
.github/skills/speckit-checklist/SKILL.md
.github/skills/speckit-clarify/SKILL.md
.github/skills/speckit-constitution/SKILL.md
.github/skills/speckit-converge/SKILL.md
.github/skills/speckit-implement/SKILL.md
.github/skills/speckit-plan/SKILL.md
.github/skills/speckit-specify/SKILL.md
.github/skills/speckit-tasks/SKILL.md
.github/skills/speckit-taskstoissues/SKILL.md
.specify/.gitignore
.specify/init-options.json
.specify/integration.json
.specify/integrations/copilot.manifest.json
.specify/integrations/speckit.manifest.json
.specify/memory/.constitution-template.json
.specify/memory/constitution.md
.specify/scripts/powershell/check-prerequisites.ps1
.specify/scripts/powershell/common.ps1
.specify/scripts/powershell/create-new-feature.ps1
.specify/scripts/powershell/resolve-template.ps1
.specify/scripts/powershell/setup-plan.ps1
.specify/scripts/powershell/setup-tasks.ps1
.specify/scripts/python/check_prerequisites.py
.specify/scripts/python/common.py
.specify/scripts/python/create_new_feature.py
.specify/scripts/python/resolve_template.py
.specify/scripts/python/setup_plan.py
.specify/scripts/python/setup_tasks.py
.specify/templates/checklist-template.md
.specify/templates/constitution-template.md
.specify/templates/plan-template.md
.specify/templates/spec-template.md
.specify/templates/tasks-template.md
.specify/workflows/speckit/workflow.yml
.specify/workflows/workflow-registry.json
```

Three things to read out of that listing:

There is no `specs/` directory and no `src/`. The topic page's tree shows both because they appear later, `specs/` on the first `/speckit-specify` run and `src/` when you implement.

There is no `git init`. The generated folder is not a repository until you make it one.

`.specify/memory/constitution.md` exists already, as a template full of placeholders. `/speckit-constitution` fills it in; it does not create it.

## The ten commands

One directory per command under `.github/skills/`, each holding a `SKILL.md`. The name in its front matter is the name you type:

```bash
head -3 .github/skills/speckit-specify/SKILL.md
```

```text
---
name: "speckit-specify"
description: "Create or update the feature specification from a natural language feature description."
```

## Script flavour

`--script` decides which directory appears under `.specify/scripts/`. Three runs, three outcomes:

| `--script` | Directories written |
| --- | --- |
| `sh` | `.specify/scripts/bash/` |
| `ps` | `.specify/scripts/powershell/` |
| `py` | `.specify/scripts/powershell/` and `.specify/scripts/python/` |

`py` writes two, which is why the topic page's tree annotation names all three outcomes rather than presenting a choice between two.

## If the version has moved on

Re-run the three commands at the top. A changed listing means the topic page needs correcting; the listing here is what 1.0.9 produced.

[← Back to The Spec-Driven Workflow](../readme.md)
