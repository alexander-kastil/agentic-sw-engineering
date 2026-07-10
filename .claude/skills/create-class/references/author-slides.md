---
name: author-slides
description: Analyse one or more module topic readmes and generate structured slide spec files in pptx/, optimised for Gamma AI presentation generation.
---

# Author Slides

Read the target topic readme path(s) from the task passed to create-class.

Analyse one or more topic readme files and write structured slide spec files into the module's `pptx/` folder, ready for Gamma AI presentation generation.

## Inputs

The target path comes from the create-class task. It is a path to either:
- A **topic folder**: `demos/01-cowork/03-permissions` — process that single readme.
- A **module root**: `demos/01-cowork` — process all numbered topic subfolders.

If no path is given, ask for one before proceeding.

## Steps

### 1. Resolve the target

If the path ends with a numbered topic folder (matches `[0-9][0-9]-*`): collect only that folder's `readme.md`.

If the path is a module root: use Glob to find all `[0-9][0-9]-*/readme.md` children directly under that path. Process each in numeric order.

Derive the **module root** and **pptx output folder** from the path:
- Module root = the `demos/NN-*` segment (two path segments under `demos/`)
- Output folder = `{module-root}/pptx/`

### 2. Read each readme

For each topic readme, extract:
- H1 title and all H2 section headings
- All Mermaid code blocks
- The `## In Practice` section if present
- Any JSON or short code blocks

Note the topic folder name (e.g. `03-permissions`) and its numeric prefix (e.g. `03`).

### 3. Plan the slide set

Target **3 to 6 slides per topic**. Do not create one slide per section heading.

| Slide type | When to create | Layout |
|---|---|---|
| Section intro | Always: one per topic, opens the set | `title-only` |
| Core concept | One or two headline ideas worth standalone treatment | `content` |
| Diagram | When a Mermaid block exists and adds visual clarity | `diagram` or `mixed` |
| Practical example | When an `## In Practice` section exists | `content` or `quote` |
| Code or config | When a short JSON/code block is the point | `mixed` |

- `title-only`: 2–3 orientation bullets, atmospheric background visual
- `content`: 3–5 tight bullets, small accent icon
- `diagram`: equal split, mermaid on one side, bullets on the other
- `mixed`: 2–3 bullets beside a code block or annotated image
- `quote`: one impactful sentence centred, photo overlay behind it

Skip a section if it adds no standalone teachable moment beyond adjacent slides.

### 4. Write slide files

**File name:** `{topic-nr}-{order:02d}-{slug}.md`
- `topic-nr`: numeric prefix of the source topic (e.g. `03`)
- `order`: zero-padded position within the topic (01, 02, …)
- `slug`: 2–3 word lowercase hyphen slug from the slide title

**File format:**

    ---
    slide: "{topic-nr}-{order:02d}"
    topic: {topic-folder-name}
    title: "{Slide Title}"
    subtitle: "{One-line subtitle — omit if none}"
    layout: {title-only|content|diagram|mixed|quote}
    visual-weight: {see table below}
    visual-type: {none|mermaid|icon|photo|code}
    visual-prompt: >
      {Required when visual-type is photo or mermaid; omit otherwise.
      Photo: text-to-image prompt for Midjourney/DALL-E/Firefly — subject, mood,
      lighting, composition, style. No text, logos, or UI in the image.
      Mermaid: plain-language diagram description covering node labels, flow
      direction, colour intent, and what concept it illustrates.}
    photo-link: "{relative path e.g. assets/images/foo.jpg — omit if no asset exists}"
    order: {numeric}
    source: {relative path to source readme}
    gamma_prompt: >
      {Self-contained Gamma generation prompt. One paragraph. Describe slide
      purpose, content, and visual clearly. No references to external context.
      Include colour intent, layout preference, and diagram type where relevant.}
    ---

    # {Slide Title}

    ## Content

    {Bullets or one-liners. Max 5 items. Bold one key term per bullet where natural.
    Present for every layout without exception.}

    ## Diagram

    ```mermaid
    {Mermaid block — only present when visual-type is mermaid.}
    ```

    ## Notes

    {1–2 presenter sentences: analogy to use, what to emphasise, what to skip under
    time pressure. Always present.}

**visual-weight values:**

| Value | Proportion | Use when |
|---|---|---|
| `none` | Text only | Dense concept or bullet slides |
| `1/3` | Small accent | Icon or tiny diagram alongside text |
| `1/2` | Equal split | Mermaid diagram, side-by-side comparison |
| `2/3` | Visual dominant | Strong diagram, annotated screenshot |
| `full` | Visual IS the slide | Minimal text, image speaks for itself |
| `bg` | Subtle background | Atmospheric opener, mood-setting |
| `grid` | 2–4 small visuals | Three concepts, icon-per-point rows |
| `strip` | Thin top or bottom band | Wide timelines, step sequences |
| `overlay` | Photo with frosted text layer | Quotes, closing slides, dramatic statements |

### 5. Field rules

- No em dashes in any field. Use `,` `;` `:` or `()` instead.
- `title` and `subtitle`: sentence case, no trailing period.
- `gamma_prompt`: self-contained, no phrases like "as described above" or "see source".
- `visual-prompt`: required when `visual-type` is `photo` or `mermaid`; omit for all other types.
- `photo-link`: optional. When both `photo-link` and `visual-prompt` are present, `photo-link` is the preferred asset and `visual-prompt` is the fallback generation instruction.
- `## Diagram` section: present only when `visual-type` is `mermaid`.
- `## Content` section: present for every layout without exception.
- `# {Slide Title}` heading: present in every file, matches the `title` frontmatter field exactly.

### 6. Print summary

    CREATED: demos/01-cowork/pptx/03-01-permissions-intro.md  [title-only]
    CREATED: demos/01-cowork/pptx/03-02-three-tiers.md        [diagram]
    CREATED: demos/01-cowork/pptx/03-03-approval-prompts.md   [content]
    CREATED: demos/01-cowork/pptx/03-04-allow-list.md         [mixed]
    CREATED: demos/01-cowork/pptx/03-05-in-practice.md        [quote]

    SUMMARY: 5 slides written for 03-permissions → demos/01-cowork/pptx/

## Example Output File

`demos/01-cowork/pptx/03-02-three-tiers.md`:

```markdown
---
slide: "03-02"
topic: 03-permissions
title: "Three types of action"
subtitle: "How Claude classifies everything it might do"
layout: diagram
visual-weight: 1/2
visual-type: mermaid
visual-prompt: >
  Top-down flowchart. Entry node "Claude plans an action" connects to a diamond
  "What type?". Three branches: left labelled "Read / search / list" to a green
  rounded rectangle "Runs automatically"; centre labelled "Create / modify / delete /
  run" to an amber rounded rectangle "Pauses for your approval"; right labelled
  "Outside workspace or internet" to a red rounded rectangle "Always blocked".
  White background, clean sans-serif font, no drop shadows.
order: 2
source: demos/01-cowork/03-permissions/readme.md
gamma_prompt: >
  Slide titled "Three types of action", subtitle "How Claude classifies everything
  it might do". Left half contains three short bullet points. Right half shows a
  top-down decision flowchart with three colour-coded outcome branches: green for
  auto-allowed, amber for approval-required, red for always-blocked. Clean minimal
  style, white background.
---

# Three types of action

## Content

- Every action Claude plans falls into one of three categories
- **Auto-allowed**: read, search, list files — no prompt, no pause
- **Approval required**: create, modify, delete, or run a command
- **Always blocked**: outside the workspace, internet access

## Diagram

```mermaid
flowchart TD
    A["Claude plans an action"] --> B{What type?}
    B -->|"Read / search / list"| C["Runs automatically"]
    B -->|"Create / modify / delete / run"| D["Pauses for your approval"]
    B -->|"Outside workspace or internet"| E["Always blocked"]
```

## Notes

Use the signing-authority analogy: like employee approval levels in any company.
Green, amber, red maps directly to the colour convention audiences already know.
```

## Subskill: merge-slides

**Gamma caps at 10 items per generation call.** When a module produces more than 10 slide spec files, the user must generate multiple PPTX exports and then merge them.

Invoke `references/merge-slides.md` when:
- The user asks to merge PPTX files after Gamma export
- A module has more than 10 slide spec files (flag this proactively after step 4)
- The user says "combine the parts", "merge the pptx", or similar

The subskill contains a self-contained Python script and verification step. Read it and execute the merge inline, do not ask the user to run it manually.
