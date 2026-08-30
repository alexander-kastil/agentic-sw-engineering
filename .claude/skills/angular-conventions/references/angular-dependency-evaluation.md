# Evaluating a Frontend Dependency Before Adopting It

Answer "is library X worth adding" with measured numbers, before a line of integration code is
written. Complements [`angular-bundle-optimization`](angular-bundle-optimization.md), which fixes a
budget that a dependency has *already* broken; this reference stops that from happening.

Four gates, in order. Any one of them can kill the candidate on its own, so run them cheapest
first.

## Gate 1 — Health, from the registry API and not the website

`WebFetch` on `npmjs.com/package/<name>` returns **HTTP 403**. Do not conclude the package is
missing; use the registry and downloads APIs, which are open:

```bash
for p in "@milkdown/crepe" "@toast-ui/editor" "@codemirror/lang-markdown"; do
  enc=$(echo "$p" | sed 's|/|%2F|')
  echo -n "$p :: "
  curl -s "https://registry.npmjs.org/$enc" \
    | python -c "import sys,json;d=json.load(sys.stdin);v=d['dist-tags']['latest'];print(v,d['time'][v],d['versions'][v].get('license'))"
  echo -n "   weekly :: "
  curl -s "https://api.npmjs.org/downloads/point/last-week/$enc" \
    | python -c "import sys,json;print(json.load(sys.stdin).get('downloads'))"
done
```

Read three fields and stop: **latest version**, **publish date of that version**, **weekly
downloads**. Publish date is the maintenance signal; downloads alone are not, because a dead
package coasts on transitive installs for years (`@toast-ui/editor`: 227k downloads a week, last
release February 2023).

Also check `dist-tags`: a package whose `latest` is stale but which has a newer `beta` is a
project that stalled mid-rewrite, not a maintained one.

Never report health from a blog post, an aggregator score, or a search summary. Those lag and
they average across a scope you did not choose. Query the registry.

## Gate 2 — The Angular wrapper trap

Most `ngx-*` / `ng-*` wrappers around a popular framework-agnostic library are one person's
side project and are dead years before the library they wrap. Measured on 2026-08-16:

| wrapper | latest | published | weekly |
| --- | --- | --- | --- |
| `ng-milkdown` | 0.0.3 | 2024-06 | 68 |
| `@ctrl/ngx-codemirror` | 7.0.0 | 2023-05 | negligible |
| `@ks89/ngx-codemirror6` | 4.0.0 | 2026-05 | 190 |
| `@mdefy/ngx-markdown-editor` | 11.1.0 | 2021-01 | negligible |

**Run gate 1 against the wrapper separately from the library.** A healthy library behind a dead
wrapper is a healthy library, and the right move is to drop the wrapper: instantiate the
framework-agnostic library directly in a component. That is usually 40 to 80 lines and it is also
the zoneless-correct pattern:

```ts
export class EditorPane {
  private readonly host = viewChild.required<ElementRef<HTMLElement>>('host');
  private view: EditorView | null = null;

  constructor() {
    afterNextRender(async () => {
      const { EditorView, basicSetup } = await import('codemirror');
      this.view = new EditorView({ parent: this.host().nativeElement, /* ... */ });
    });
    inject(DestroyRef).onDestroy(() => this.view?.destroy());
  }
}
```

A wrapper is worth keeping only when it earns its own maintenance risk: `ControlValueAccessor`
plumbing you would otherwise write, or an SSR story. Convenience alone does not.

## Gate 3 — Weight, measured, not estimated

Never quote a size from memory or from bundlephobia. Bundle the candidate in the scratchpad and
gzip it, which takes about a minute:

```bash
cd "$SCRATCHPAD" && mkdir cand && cd cand && npm init -y
npm i --no-audit --no-fund codemirror @codemirror/lang-markdown @milkdown/crepe esbuild

cat > cm.js <<'EOF'
import { EditorView, basicSetup } from 'codemirror'
import { markdown } from '@codemirror/lang-markdown'
export { EditorView, basicSetup, markdown }
EOF

npx esbuild cm.js --bundle --minify --format=esm --outfile=out.js
node -e "const z=require('zlib'),f=require('fs');const b=f.readFileSync('out.js');
console.log('min',(b.length/1024).toFixed(0),'kB  gzip',(z.gzipSync(b).length/1024).toFixed(0),'kB')"
```

Write the entry file to import **exactly what the integration would import**, not the package
root, or the number is meaningless for a tree-shakeable library.

Then measure the headroom you are spending it against, from the app's own production build:

```bash
npx ng build --configuration production
cd dist/<app>/browser && node -e "
const fs=require('fs'),z=require('zlib');
const idx=fs.readFileSync('index.html','utf8');
let raw=0,gz=0;
for (const f of fs.readdirSync('.').filter(f=>f.endsWith('.js')))
  if (idx.includes(f)) { const b=fs.readFileSync(f); raw+=b.length; gz+=z.gzipSync(b).length }
console.log('initial raw',(raw/1024).toFixed(0),'kB  gzip',(gz/1024).toFixed(0),'kB')"
```

`index.html` referencing the file is what makes a chunk part of the eager graph, which is what the
`initial` budget in `angular.json` measures. Angular budgets are on **raw** bytes, so compare
minified-raw against the budget and quote gzip only as the wire cost.

Decide from the two numbers together. A candidate larger than the remaining headroom is not
automatically rejected: it is rejected *as an eager import*, and the question becomes whether a
dynamic `import()` behind `afterNextRender` is acceptable for that feature. If the library must
run before first paint or before a route guard resolves, lazy loading is not available and the
weight is a hard no.

## Gate 4 — Format fidelity, for anything that parses or serializes

An editor, formatter, or converter that round-trips content through its own AST will silently
rewrite everything its AST cannot model. Before adopting one, inventory what the stored format
actually contains beyond the standard:

- non-standard block syntax (Hugo shortcodes `{{< media-block >}}`, MDX, Liquid, Jinja)
- raw HTML embedded in markdown
- front matter
- whitespace or line endings that another system asserts on

Every ProseMirror-based markdown editor (Milkdown/Crepe, Tiptap, Toast UI) fails this gate for
such content unless you write a custom node spec per construct. A **source** editor
(CodeMirror 6) does not have the failure mode at all: the document is the text.

Second half of the gate: who else writes the document? If an AI agent or a sibling editor replaces
the whole document, a WYSIWYG's internal state and undo history fight that write path, and the
guard you need (apply an external change only when the incoming text differs from the current doc)
is far easier to get right on a text editor than on an AST editor.

## Verdict shape

Report a decision, not a survey: **the call, the reason it beat the runner-up, the two measured
numbers, and the cost in hours.** Put the maintenance table and the size table in the reply only
because they are the evidence for the call, and put the task breakdown in the repo's todo file
rather than the reply.

## Worked example (2026-08-16, `src/admin.integrations.at`)

Question: replace the article editor's `<textarea>` with a good maintained markdown editor?

- Gate 1: `@codemirror/lang-markdown` 6.5.2 published 12 days prior, 4.2M/week. `@toast-ui/editor`
  last published 2023-02-17, dead despite 227k/week. `easymde` alive but still CodeMirror **5**.
- Gate 2: every Angular wrapper dead (table above), so CodeMirror 6 used directly.
- Gate 3: app initial bundle 419 kB raw / 109 kB gzip against a 500 kB warning. CodeMirror +
  markdown = 526 kB raw / 181 kB gzip, so it must be lazy. Crepe = 2675 kB raw / 898 kB gzip,
  unaffordable either way.
- Gate 4: the source carries YAML front matter, raw `<figure class="blog-img--hero">` HTML, and
  Hugo `{{< split-block >}}` / `{{< media-block >}}` shortcodes, and a chat agent rewrites the
  whole document each turn. Every WYSIWYG candidate eliminated here.

Verdict: adopt CodeMirror 6 as a source editor behind a dynamic `import()`, reject the WYSIWYG
class entirely. Half a day to a day.

## Checklist

- [ ] Health read from `registry.npmjs.org` + `api.npmjs.org`, not from npmjs.com or a summary.
- [ ] Latest publish date checked, not just download count.
- [ ] Any framework wrapper health-checked separately from the library it wraps.
- [ ] Size measured with esbuild + gzip on the real import surface, not estimated.
- [ ] App's current initial bundle measured as the headroom baseline.
- [ ] Eager-vs-lazy decided explicitly; heavy libs put behind `import()`.
- [ ] Format-fidelity gate run for anything that parses or serializes stored content.
- [ ] Verdict reported with numbers; task breakdown written to the repo's todo file.
