# React Markdown Editor — Implementation Plan

## Overview

A React + TypeScript markdown editor built with Vite and `@uiw/react-md-editor`, supporting edit/preview toggle and live HTML state capture.

## Stack

- Vite + React + TypeScript
- [`@uiw/react-md-editor`](https://github.com/uiwjs/react-md-editor)

## Phases

### Phase 1 — Scaffold (sequential)

1. Run `npm create vite@latest . -- --template react-ts` inside `react-md-editor/`
2. Run `npm install`
3. Run `npm install @uiw/react-md-editor`

### Phase 2 — File authoring (parallel — no file overlap)

| Task | File | Description |
|------|------|-------------|
| 2A | `src/components/MarkdownEditor.tsx` | Core editor component |
| 2B | `src/index.css` | Design tokens + reset |

#### MarkdownEditor.tsx

- `useState` for `{ markdown, html }` — markdown defaults to `"type markdown here"`
- `useState` for `mode` — `'edit'` or `'preview'`
- `useRef` + `useEffect` to capture rendered HTML from a hidden `MDEditor.Markdown` into state
- Toggle button with `aria-pressed`, controls wrapper with `role="toolbar"`
- `data-color-mode="light"` on root div

#### index.css

- CSS custom properties: `--color-bg`, `--color-text`, `--color-border`, `--color-focus`
- Box-sizing reset, zero body margin
- `button:focus-visible` outline using `--color-focus`

### Phase 3 — Wire up (depends on Phase 2A)

| Task | File | Description |
|------|------|-------------|
| 3A | `src/App.tsx` | Import and render `<MarkdownEditor />` inside `<main>` |
| 3B | `src/App.css` | Cleared (Vite boilerplate removed) |

## File Tree

```
react-md-editor/
├── index.html
├── package.json
├── vite.config.ts
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── App.css
    ├── index.css
    └── components/
        └── MarkdownEditor.tsx
```

## Running Locally

```bash
cd demos/05-capstone/01-planning/01-md-editor/react-md-editor
npm run dev
```

## Accessibility Notes

- `<main>` landmark with `id="maincontent"` and `tabIndex={-1}` for skip-link target
- Single `<h1>` for page topic
- Toggle button uses `aria-pressed` to convey state
- Editor wrapped in `role="toolbar"` controls area
- Focus styles meet 3:1 contrast via `--color-focus`
