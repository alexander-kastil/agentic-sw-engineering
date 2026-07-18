# Discovery Scripts

Queries used to evaluate module completeness. Replace `<root>` with the module root path (e.g. `demos/04-skills`).

## Theory

Find all topic subfolder readmes:
```
Glob: <root>/*/readme.md
```

Read the first 20 lines of each result. A topic has real content if it contains prose paragraphs or code blocks. A bullet list or empty file does not count.

## Code Demos

Demo guide files may sit at the module root (`<root>/demo-NN-*.md`) or in a `demos/` subfolder (`<root>/demos/demo-NN-*.md`). The evaluator scans both locations.

Find step-by-step guide readmes (topics that contain code blocks):
```
Glob: <root>/*/readme.md
Read: first 20 lines — presence of fenced code blocks (```) indicates a guide
```

Find runnable code projects:
```
Glob: <root>/**/package.json
Glob: <root>/**/*.csproj
Glob: <root>/**/*.sln
Glob: <root>/**/requirements.txt
Glob: <root>/**/go.mod
```

Each matching project root counts as one code demo.

## Labs

Labs live at the repo root under `labs/<module-name>/`, not inside the module's demo folder. The `<module-name>` matches the demo folder slug (e.g. `09-managed-agents`).

Find lab entries:
```
Glob: labs/<module-name>/*/readme.md
Glob: labs/<module-name>/lab-*.md
```

A lab counts if it has a readme or `lab-*.md` file with actual content (not a placeholder). A folder containing only an empty readme does not count.

Threshold: **1 lab required**.

- No lab files at all → **planned**
- Labs folder exists but its `readme.md` declares "No Labs for this Module" (a deliberate none) → **absent** (excluded from the module total, so the module can still reach 100%)
- Lab folder or file exists but content is empty / placeholder → **doing**
- 1 or more labs with real content → **done**

A component marked **absent** is dropped from the module's denominator. A module with one absent component is scored out of 3, not 4. Only the explicit "No X for this Module" marker triggers this; an unmarked empty component stays **planned** and still counts.

## Slides

Slides count only when a real deck exists. Markdown spec files in `pptx/` are preparation, not finished slides:
```
Glob: <root>/pptx/*.pptx
Glob: <root>/pptx/*.md
```

- A `.pptx` deck present → **done**
- No deck, but non-placeholder `.md` slide specs present → **doing**
- Empty pptx folder, or only a placeholder `readme.md` → **planned**
