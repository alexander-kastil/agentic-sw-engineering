# render-folder — HTML File Explorer Widget Prompt

Use this prompt to generate a self-contained HTML file explorer widget for any folder structure.

## Prompt Template

```
Create an HTML file explorer widget that visualizes the following folder structure.

Style rules:
- Monospace font throughout
- Folder icons in amber/yellow, file icons in muted/secondary color
- Tree connector lines (├─ └─) in tertiary/muted color
- Each row is a flex item with: connector | icon | label | optional inline annotation
- Hover highlight on each row (subtle background)
- Indent levels via padding-left (24px per level)
- Use Tabler outline icon classes for file types:
    - Folder open: ti-folder-open
    - Folder closed: ti-folder
    - CSV: ti-file-spreadsheet
    - DOCX: ti-file-word
    - TXT/MD: ti-file-text
    - Generic: ti-file-description
- Annotations (← note text) in small tertiary color, same row
- No borders, no shadows, no card wrapper — raw tree on transparent background
- Dark mode safe: use CSS variables for all colors

Folder structure to render:
[PASTE YOUR STRUCTURE HERE]
```

## Usage

Replace `[PASTE YOUR STRUCTURE HERE]` with a plain-text folder tree. Annotations are optional; append `← note` after any filename or folder name to render an inline label.

## Example Input

```
demos/
├─ 01-cowork/
│  ├─ readme.md          ← start here
│  └─ labs/
└─ 02-harness/
   └─ readme.md
```
