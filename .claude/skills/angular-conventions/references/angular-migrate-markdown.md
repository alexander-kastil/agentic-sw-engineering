# Migrate Markdown Renderer into Split Demo-Container Layout

Move `<app-markdown-renderer>` from individual sample components into the global `demo-container` shell using `angular-split`, so every demo route shares a single split-pane layout.

## Prerequisites

- `angular-split` installed: `npm install angular-split`
- Project has a `db.json` (or equivalent data source) with a `demos` array
- Sample components currently render markdown via `<app-markdown-renderer [md]="'<name>'" />`

## Steps

### 1. Add `md` field to the demo data source

For each demo entry in `db.json`, add `"md": "<markdown-name>"` matching the value currently in `<app-markdown-renderer [md]="'<VALUE>'" />`.

### 2. Update the `DemoItem` model

Add `md: string = ''` to the `DemoItem` class (or interface).

### 3. Convert `SidePanelService` to signal-based toggles

Replace any action-based or Observable-based toggle state with pure signals:

```typescript
@Injectable({ providedIn: 'root' })
export class SidePanelService {
  private _editorVisible = signal(false);
  private _rendererVisible = signal(true);
  editorVisible = this._editorVisible.asReadonly();
  rendererVisible = this._rendererVisible.asReadonly();
  toggleEditor() { this._editorVisible.update(v => !v); }
  toggleRenderer() { this._rendererVisible.update(v => !v); }
}
```

Delete `sidebar.actions.ts` (or equivalent action file) if it exists.

### 4. Update `demo-container` to use `angular-split`

- Import `SplitComponent`, `SplitAreaComponent`, and `MarkdownRendererComponent`.
- Track the current URL with a signal set from `router.events` (`NavigationEnd`) using `takeUntilDestroyed()`.
- Derive `currentMd` as a `computed()` that matches the current URL segment to the `demos()` array `md` field.
- Replace the existing CSS grid layout with `<as-split direction="vertical">` containing three areas:

```html
<as-split direction="vertical">
  <as-split-area [size]="60">
    <router-outlet />
  </as-split-area>

  <as-split-area [size]="20" [visible]="showRenderer() && !!currentMd()">
    <app-markdown-renderer [md]="currentMd()" />
  </as-split-area>

  <as-split-area [size]="20" [visible]="showMdEditor()">
    <app-markdown-editor-container />
  </as-split-area>
</as-split>
```

### 5. Remove `<app-markdown-renderer>` from sample components

Find all usages:

```bash
grep -r "app-markdown-renderer" src/app/demos/samples/
```

For each file found: remove the `<app-markdown-renderer>` HTML tag and its corresponding `MarkdownRendererComponent` import.

### 6. Add PrismJS assets to `angular.json`

```json
"styles": [
  "node_modules/prismjs/themes/prism-okaidia.css",
  "src/styles.scss"
],
"scripts": [
  "node_modules/prismjs/prism.js",
  "node_modules/prismjs/components/prism-typescript.min.js",
  "node_modules/prismjs/components/prism-javascript.min.js"
]
```

## Verification

1. Run `ng build` — confirm no compile errors.
2. Navigate to each demo route — markdown renders in the lower split pane.
3. Toggle pane visibility with the sidebar button — pane shows and hides correctly.
4. Inspect code blocks — dark syntax highlighting renders via PrismJS.
