# Angular A2UI

A2UI is an open protocol for AI agents to emit declarative JSON that an Angular client renders as native UI components, with no arbitrary code execution and no unsafe string evaluation.

## What is A2UI

A2UI separates UI _intent_ (agent JSON) from UI _rendering_ (Angular client). The agent describes which catalog components to show and how to bind them to data. The client renders only components that exist in its pre-approved catalog, making generative UI safe across trust boundaries.

The protocol is stateless on the agent side: agents output a stream of JSON messages; the client owns the local data model and the live DOM. Input fields update the local model immediately; the network round-trip happens only when the user triggers an action.

**Protocol status (as of June 2026):** v0.9.1 is stable/production. v1.0 is release candidate (adds `actionResponse`, action IDs, `surfaceProperties`). Import from `@a2ui/angular/v0_9` until v1.0 is declared stable.

## Message Shape

All messages are JSON objects with a `"version"` key and exactly one operation key. In streaming mode the agent emits JSONL (newline-delimited JSON); in non-streaming mode a JSON array is returned. The client processes each object independently.

### createSurface

Initializes a rendering container. Always send first.

```json
{
  "version": "v0.9",
  "createSurface": {
    "surfaceId": "passenger-card",
    "catalogId": "https://a2ui.org/specification/v0_9/catalogs/basic/catalog.json",
    "sendDataModel": true
  }
}
```

`sendDataModel: true` instructs the renderer to attach the full local data model to every outgoing action message, enabling stateless agents that never track client state themselves.

### updateComponents

Provides a flat adjacency list of components. The renderer builds the tree at render time from ID references.

```json
{
  "version": "v0.9",
  "updateComponents": {
    "surfaceId": "passenger-card",
    "components": [
      { "id": "root",       "component": "Card",   "child": "content" },
      { "id": "content",    "component": "Column",  "children": ["headline", "name-row", "btn"] },
      { "id": "headline",   "component": "Text",    "text": "Passenger", "variant": "h2" },
      { "id": "name-row",   "component": "Row",     "children": ["first-name", "last-name"] },
      {
        "id": "first-name",
        "component": "Text",
        "text": { "path": "/passenger/firstName" },
        "variant": "body"
      },
      {
        "id": "last-name",
        "component": "Text",
        "text": { "path": "/passenger/lastName" },
        "variant": "body"
      },
      {
        "id": "btn",
        "component": "Button",
        "child": "btn-label",
        "action": {
          "event": {
            "name": "increaseMiles",
            "context": { "passenger": { "path": "/passenger" } }
          }
        }
      },
      { "id": "btn-label",  "component": "Text",    "text": "Add Miles", "variant": "body" }
    ]
  }
}
```

Key rules for the component list:

- Every list must contain a component with `"id": "root"`, that is the tree entry point.
- `"child"` (string) holds one child ID; `"children"` (string array) holds an ordered list.
- Literal values are inline strings: `"text": "Hello"`.
- Data-bound values are path objects: `"text": { "path": "/passenger/firstName" }`. Absolute paths (leading `/`) resolve from the data model root. Relative paths resolve within the nearest collection scope during list iteration.
- Function calls embed as: `{ "call": "formatNumber", "args": { "value": { "path": "/count" }, "decimals": 0 }, "returnType": "string" }`.

### updateDataModel

Seeds or patches the surface data model. Bound components re-render automatically. Can arrive before, after, or interleaved with `updateComponents`.

```json
{
  "version": "v0.9",
  "updateDataModel": {
    "surfaceId": "passenger-card",
    "path": "/passenger",
    "value": {
      "id": 42,
      "firstName": "Anna",
      "lastName": "Miller",
      "bonusMiles": 1200
    }
  }
}
```

Send granular patches (only the changed path) rather than replacing the entire model on every turn.

### deleteSurface

Removes a surface and all associated component and data-model state.

```json
{
  "version": "v0.9",
  "deleteSurface": { "surfaceId": "passenger-card" }
}
```

## Angular Client Setup

### Installation

```bash
npm install @a2ui/angular @a2ui/web_core
npm install marked   # required unconditionally — Text always injects MarkdownRenderer, see below
```

### app.config.ts

Register `A2UI_RENDERER_CONFIG` (via `useFactory` so `inject()` works inside the factory) and `A2uiRendererService`.

```typescript
// app.config.ts
import { ApplicationConfig, inject, Injector } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import {
  A2UI_RENDERER_CONFIG,
  A2uiRendererService,
  BasicCatalog,
  provideMarkdownRenderer,
} from '@a2ui/angular/v0_9';
import { marked } from 'marked';
import { ChatService } from './chat/chat.service';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    {
      provide: A2UI_RENDERER_CONFIG,
      useFactory: () => {
        const injector = inject(Injector);
        return {
          catalogs: [inject(BasicCatalog)],
          actionHandler: (action) =>
            injector.get(ChatService).handleAction(action),
        };
      },
    },
    provideMarkdownRenderer(
      async (md) => marked.parse(String(md ?? '')),
    ),
    A2uiRendererService,
  ],
};
```

`provideMarkdownRenderer` is required unconditionally, not just when `Text` components use `"variant": "markdown"`. `Text` injects `MarkdownRenderer` regardless of variant, so omitting the provider throws `NG0201: No provider found for MarkdownRenderer` at render time even when no markdown is used anywhere in the app. `marked` (or `@a2ui/markdown-it`, whose peer-dep range is stale against `@a2ui/web_core@0.10.x` and needs `--legacy-peer-deps` to install) is a required dependency, not an optional one.

## Rendering Surfaces

Import `SurfaceComponent` from `@a2ui/angular/v0_9` and render with `<a2ui-v09-surface>`.

```typescript
// chat/chat-panel.ts
import {
  Component, ChangeDetectionStrategy, inject, DestroyRef,
} from '@angular/core';
import {
  A2uiRendererService,
  SurfaceComponent,
} from '@a2ui/angular/v0_9';
import type { A2uiClientAction } from '@a2ui/web_core/v0_9';
import { ChatService } from './chat.service';

@Component({
  selector: 'app-chat-panel',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [SurfaceComponent],
  template: `
    @for (id of chat.activeSurfaceIds(); track id) {
      <a2ui-v09-surface [surfaceId]="id" />
    }
  `,
})
export class ChatPanel {
  private readonly renderer = inject(A2uiRendererService);
  private readonly destroyRef = inject(DestroyRef);
  protected readonly chat = inject(ChatService);

  constructor() {
    const sub = this.renderer.surfaceGroup.onAction.subscribe(
      (action: A2uiClientAction) => this.chat.handleAction(action),
    );
    this.destroyRef.onDestroy(() => sub.unsubscribe());
  }
}
```

`renderer.surfaceGroup.onAction` is not a standard RxJS Observable with `takeUntilDestroyed` support. Unsubscribe manually via `DestroyRef.onDestroy`.

### Feeding messages to the renderer

Call `renderer.processMessages(messages)` whenever the agent responds. The renderer handles progressive rendering internally: components appear as soon as a valid `root` component is available, before all messages arrive.

```typescript
// chat/chat.service.ts
import { Injectable, inject, signal } from '@angular/core';
import { A2uiRendererService } from '@a2ui/angular/v0_9';
import type { A2uiMessage, A2uiClientAction } from '@a2ui/web_core/v0_9';

@Injectable({ providedIn: 'root' })
export class ChatService {
  private readonly renderer = inject(A2uiRendererService);

  readonly activeSurfaceIds = signal<string[]>([]);

  async sendMessage(text: string): Promise<void> {
    const response = await fetch('/api/agent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    const messages = await response.json() as A2uiMessage[];
    this.renderer.processMessages(messages);

    for (const msg of messages) {
      if ('createSurface' in msg) {
        const id = (msg as { createSurface: { surfaceId: string } }).createSurface.surfaceId;
        this.activeSurfaceIds.update((ids) => [...ids, id]);
      }
      if ('deleteSurface' in msg) {
        const id = (msg as { deleteSurface: { surfaceId: string } }).deleteSurface.surfaceId;
        this.activeSurfaceIds.update((ids) => ids.filter((x) => x !== id));
      }
    }
  }

  handleAction(action: A2uiClientAction): void {
    // Forward action context back to agent as a new user turn
    this.sendMessage(JSON.stringify({ action }));
  }
}
```

## Catalogs

### BasicCatalog

`BasicCatalog` provides 15+ general-purpose components. Register it with `inject(BasicCatalog)`, it is an Angular injectable class.

| Category | Components |
|---|---|
| Layout | `Row`, `Column`, `Card`, `Tabs` |
| Content | `Text`, `Image`, `Icon`, `Divider` |
| Input | `Button`, `TextField`, `CheckBox`, `Slider`, `DateTimeInput` |

> **Verify:** The official client-setup guide also exports a `minimalCatalog` object constant (used without `inject()`). Check which export is present in the installed package version; `inject(BasicCatalog)` is preferred in Angular 22 for DI consistency.

### Custom Catalog

Extend `BasicCatalogBase` when you need domain-specific components. The catalog is an Angular injectable, so it participates in the DI graph.

```typescript
// catalog/custom-catalog.ts
import { Injectable, inject } from '@angular/core';
import { BasicCatalogBase } from '@a2ui/angular/v0_9';
import { BASIC_FUNCTIONS } from '@a2ui/web_core/v0_9';  // verify export name
import { chartEntry } from './chart/chart';

@Injectable({ providedIn: 'root' })
export class CustomCatalog extends BasicCatalogBase {
  constructor() {
    super({
      // URI is the catalogId agents must reference in createSurface.catalogId
      id: 'https://yourapp.example.com/catalogs/v1/catalog.json',
      extraComponents: [chartEntry],
      functions: [...BASIC_FUNCTIONS],
    });
  }
}
```

Register in `app.config.ts`:

```typescript
{
  provide: A2UI_RENDERER_CONFIG,
  useFactory: () => ({
    catalogs: [inject(CustomCatalog)],
    actionHandler: (action) => inject(ChatService).handleAction(action),
  }),
},
```

### Defining a custom component

Each custom component needs three files: a Zod schema, an Angular component, and a catalog entry object.

**Schema**, defines valid JSON the agent can emit for this component:

```typescript
// chart/chart-schema.ts
import { z } from 'zod';
import { DynamicStringSchema } from '@a2ui/web_core/v0_9';

export const chartSchema = z.object({
  title:     DynamicStringSchema,
  dataPath:  z.string(),
  chartType: z.enum(['bar', 'line', 'pie']).optional(),
}).strict();

export type ChartSchema = z.infer<typeof chartSchema>;
```

`DynamicStringSchema` (confirmed export from `@a2ui/web_core/v0_9`, defined in `schema/common-types.d.ts`) is a Zod union of a literal string, a `{ path: string }` binding, and a `{ call, args, returnType }` function call. It is the real mechanism for "this field accepts either a literal or a data-model path reference" — there is no `binding()` helper in the package. Matching `DynamicNumberSchema` / `DynamicBooleanSchema` / `DynamicStringListSchema` exist for the other primitive shapes.

**Angular component**, receives props via signal inputs:

```typescript
// chart/chart.ts
import {
  Component, ChangeDetectionStrategy,
  input, computed,
} from '@angular/core';
import type { BoundProperty } from '@a2ui/web_core/v0_9';

interface ChartProps {
  title:     BoundProperty<string>;
  dataPath:  string;
  chartType?: 'bar' | 'line' | 'pie';
}

const initialProps: ChartProps = {
  title:    { value: () => '' },
  dataPath: '',
};

@Component({
  selector: 'app-chart',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <figure>
      <figcaption>{{ title() }}</figcaption>
      <!-- chart canvas wired here -->
    </figure>
  `,
})
export class ChartComponent {
  // Provided by the A2UI renderer; default needed for initial render pass
  readonly props          = input<ChartProps>(initialProps);
  readonly surfaceId      = input.required<string>();
  readonly componentId    = input.required<string>();
  readonly dataContextPath = input('/');

  // BoundProperty<T>.value() is a signal accessor, use computed() to derive
  protected readonly title = computed(() => this.props().title.value());
}
```

**Catalog entry:**

```typescript
// chart/chart.ts (continued)
import type { AngularComponentImplementation } from '@a2ui/angular/v0_9';
import { chartSchema } from './chart-schema';

export const chartEntry = {
  name:      'Chart',          // must match the string agents use in "component"
  component: ChartComponent,
  schema:    chartSchema,
} as unknown as AngularComponentImplementation;
```

### Schema-to-component correspondence

The catalog schema is the contract. Every property the schema defines must be handled by the Angular component, and vice versa.

| Zod schema field | Angular component usage | Agent JSON |
|---|---|---|
| `title: DynamicStringSchema` | `computed(() => props().title.value())` | `"title": {"path": "/report/name"}` |
| `chartType: z.enum([...])` | `props().chartType` (direct, not bound) | `"chartType": "bar"` |
| `dataPath: z.string()` | `props().dataPath` | `"dataPath": "/sales/2026"` |

## Large Option Sets Need a Custom Compact Component

`ChoicePicker` from `BasicCatalog` has no dropdown or compact variant. Confirmed from the shipped `.d.ts` (`ChoicePickerApi` in `@a2ui/web_core/src/v0_9/basic_catalog/components/basic_components.d.ts`): `variant` only accepts `"multipleSelection" | "mutuallyExclusive"`, both of which render as a full vertical list of checkboxes or radio buttons. There is no schema option that collapses it into a `<select>`.

**Rule of thumb:** for any bound field where the option count is unbounded or plausibly large (contact lists, account/category lists, anything sourced from a DB query rather than a fixed small enum), do not reach for `ChoicePicker`. Build a small custom catalog component wrapping a native `<select>` (or similar compact control) from the start, rather than discovering the UX problem after a real user scrolls past 30 radio buttons to find the Save button.

### Worked example: `Select`

vouchers-ai hit this with an "Account" picker driven by ~30 expense accounts pulled from the DB.

- **Schema** — `src/vouchers-ui/src/app/assistant/catalog/select/select-schema.ts`:

  ```typescript
  import { z } from 'zod';
  import { DynamicStringSchema } from '@a2ui/web_core/v0_9';

  export const selectSchema = z.object({
    label: DynamicStringSchema.optional(),
    value: DynamicStringSchema,
    options: z.array(
      z.object({
        value: z.string(),
        label: DynamicStringSchema,
      }),
    ),
  }).strict();
  ```

  The `options` shape (`{ value: string; label: DynamicString }[]`) deliberately matches `ChoicePickerApi.options`, confirmed from the same `.d.ts`, so swapping a `ChoicePicker` prompt template over to `Select` is a one-word change in the agent system prompt (see below).

- **Component** — `src/vouchers-ui/src/app/assistant/catalog/select/select.ts` (+ separate `select.html` / `select.css`, this project never inlines templates/styles): extends `CatalogComponent` from `@a2ui/angular/v0_9`, reads `props()['value']?.value()` / `props()['options']?.value()` the same way `TextFieldComponent` and `ChoicePickerComponent` do internally, and writes back via `props()['value']?.onUpdate(newValue)` on the native `<select>`'s `(change)` event.

- **Catalog registration** — `src/vouchers-ui/src/app/assistant/catalog/custom-catalog.ts`: a `CustomCatalog extends BasicCatalogBase` with `extraComponents: [selectEntry]`, wired into `A2UI_RENDERER_CONFIG` in `app.config.ts` in place of a plain `inject(BasicCatalog)`. This keeps every default BasicCatalog component (`Card`, `Column`, `Text`, `TextField`, `DateTimeInput`, `Button`, …) available — `BasicCatalogBase` merges `DEFAULT_COMPONENT_IMPLEMENTATIONS` with `extraComponents`, it does not replace them.

### Gotcha: two `zod` installs do not type-check against each other

The app's own top-level `zod` and the `zod` nested inside `@a2ui/web_core/node_modules/zod` can be different major versions (v4 vs v3 in this project). A schema built with `z.object(...)` imported from the app's `zod` fails `CatalogComponent<typeof YourApi>`'s generic constraint and the `AngularComponentImplementation` assignment with a `TS2344`/`TS2322` error whose message oddly claims your `ZodObject` is "missing" properties like `_type`, `_parse`, `_getType` — that is two different `ZodType` classes, not a real schema mistake.

Symptom in dev: the Angular CLI build fails on the incremental rebuild, but the dev server keeps serving the last good bundle with no visible error in the browser — the page looks unchanged, and the browser console reports the *old* code's behavior (here, `A2uiRendererService` logged `Component type "Select" not found in catalog` because the catalog registration was never actually rebuilt). Check the terminal running `ng serve` for `✘ [ERROR] TS2344`/`TS2322` before assuming the browser or the DI wiring is wrong.

Fix: extend `CatalogComponent<any>` instead of `CatalogComponent<typeof YourApi>`, and cast the catalog entry with `... as unknown as AngularComponentImplementation` — exactly the cast this doc's "Defining a custom component" example already uses; now you know precisely why it is there.

### Prompt-template lesson: literal fill-in-the-blank beats prose

The agent system prompt that emits this component's JSON (`src/vouchers-ai/Services/A2uiAgentService.cs`) builds the `updateComponents` message as a literal fill-in-the-blank JSON template in the system prompt string, not a prose description of the shape. This is deliberate: prose lets the LLM invent or rename keys (for example emitting `"type"` instead of `"component"`) even at temperature 0. Swapping `ChoicePicker` for a new custom component in that prompt is a one-line change to the template (`"component":"Select"` instead of `"component":"ChoicePicker"`) — keep it that way for any future custom component; do not refactor the template into a descriptive paragraph.

## Action Handling

### How actions flow

1. Agent includes `"action": { "event": { "name": "...", "context": { ... } } }` on a Button or other interactive component.
2. User triggers the component.
3. Renderer resolves `context` path bindings from the local data model.
4. `renderer.surfaceGroup.onAction` emits an `A2uiClientAction`.
5. Your handler receives it and forwards to the agent (or handles locally).

### A2uiClientAction shape

```typescript
interface A2uiClientAction {
  name:              string;       // stable identifier set by the agent
  surfaceId:         string;
  sourceComponentId: string;
  timestamp:         string;       // ISO 8601
  context:           Record<string, unknown>;  // resolved from data-model paths
}
```

### Forwarding actions back to the agent

```typescript
handleAction(action: A2uiClientAction): void {
  // The agent receives action.name and action.context
  // and responds with new A2UI messages
  this.sendMessage(JSON.stringify({ action }));
}
```

### Optimistic local updates

Update the local data model immediately before the agent round-trip:

```typescript
handleAction(action: A2uiClientAction): void {
  if (action.name === 'increaseMiles') {
    const passenger = action.context['passenger'] as Passenger;
    this.renderer.processMessages([
      {
        version: 'v0.9',
        updateDataModel: {
          surfaceId: action.surfaceId,
          path: '/passenger',
          value: { ...passenger, bonusMiles: passenger.bonusMiles + 300 },
        },
      },
    ]);
  }
  this.sendMessage(JSON.stringify({ action }));
}
```

### functionCall actions (renderer-local)

Some actions never reach the agent. The renderer evaluates them from catalog-registered functions:

```json
{
  "id": "external-link",
  "component": "Button",
  "child": "link-label",
  "action": {
    "functionCall": {
      "call": "openUrl",
      "args": { "url": "https://example.com" }
    }
  }
}
```

## Theming

The BasicCatalog injects a default stylesheet using `:where(:root)` selectors (minimal specificity). Override tokens in your global `styles.css`:

```css
:root {
  /* Primary brand color */
  --a2ui-color-primary: #86efac;

  /* Typography */
  --a2ui-font-family-title:     'Inter', sans-serif;
  --a2ui-font-family-monospace: 'Fira Code', monospace;

  /* Component tokens */
  --a2ui-card-background: #0f3d20;
}

/* Override color scheme in a subtree */
.a2ui-light { color-scheme: light; }
.a2ui-dark  { color-scheme: dark; }
```

Dark mode is auto-detected via `prefers-color-scheme`. Apply `.a2ui-light` or `.a2ui-dark` to an ancestor element to override for a subtree.

The renderer controls _how_ components look. Agents control _what_ to show. Agents must use semantic hints (`"variant": "h1"`) rather than pixel values or color literals.

## Single Source of Truth

Schema drift, the catalog Zod schema, the agent system prompt, and the Angular component out of sync, is the most common production failure. Derive all three from one definition:

```text
catalog/chart-schema.ts        ← Zod schema (ground truth for valid JSON)
        ↓ imported by
catalog/custom-catalog.ts      ← registers ChartComponent + chartSchema
        ↓ same Zod schema exported as JSON Schema
agent system prompt            ← includes the JSON Schema so the LLM knows Chart fields
```

Use `register-catalogs.js` (A2UI repo `scripts/`) to resolve `$ref` imports in JSON Schema catalog files before shipping, producing a self-contained `catalog.json`. The `catalogId` URI does not require runtime fetching; catalogs must be known at compile/deploy time.

### Catalog versioning

- **Minor/patch** (same URI): add optional leaf components, add optional properties, remove properties, update metadata.
- **Major** (new URI): add/remove required properties, change property types, add container components.

Support old agents during transition by registering both catalog versions in order:

```typescript
catalogs: [inject(CustomCatalogV2), inject(CustomCatalogV1)],
```

Agents pick the best match from the ordered list.

## When to Use / When Not to Use

**Use A2UI when:**

- An AI agent must present data in a structured, interactive UI at runtime (variable form fields, dynamic layouts).
- The exact UI shape is not known at build time.
- You want the same agent to drive multiple render targets (Angular, Flutter, React) without changing agent code.
- You need to compose many small data-driven surfaces inside a chat-like conversation.

**Do not use A2UI when:**

- The UI is fully known at build time, build a regular Angular component.
- The agent only produces text or markdown, use an async pipe with a markdown renderer.
- You need pixel-perfect custom layouts with complex animations, custom catalogs help but complex designs belong in dedicated components.

## Anti-patterns and Gotchas

**Schema drift.** If the Angular component and catalog Zod schema diverge, the renderer silently drops or misrenders components. Keep schema and component inputs in lockstep; bump the `catalogId` URI on any breaking change.

**Using `useValue` for `A2UI_RENDERER_CONFIG`.** `inject()` only works inside a factory or constructor context. Using `useValue: { catalogs: [inject(BasicCatalog)] }` throws at bootstrap. Always use `useFactory`.

**Forgetting `DestroyRef` cleanup.** `renderer.surfaceGroup.onAction` does not support `takeUntilDestroyed`. Always store the subscription and call `sub.unsubscribe()` inside `DestroyRef.onDestroy`.

**Hallucinated component names.** The agent can only use component types registered in the active catalog. Unknown type names produce `VALIDATION_FAILED` errors. Always include the full catalog schema (or a JSON Schema rendering of it) in the agent system prompt.

**`sendCatalogDescription: true` in production.** This flag sends the full catalog schema in every outgoing message. Useful for development; disable in production to reduce payload size and prevent prompt-injection attacks that exploit the schema description.

**Mixing version import paths.** `@a2ui/angular/v0_9` and `@a2ui/angular/v1_0` export differently-shaped types and token values. Never import from both in the same app until you are intentionally migrating.

**Arbitrary values in component properties.** A2UI is declarative. Never place raw HTML strings, JavaScript, or `<script>` tags in component property values. Agents must stay within catalog-defined primitives.

**Progressive rendering ordering.** Components start rendering as soon as a valid `root` component arrives, before all sibling `updateComponents` messages have been processed. Avoid sibling components that visually depend on each other's final dimensions when streaming is enabled.

## Verify Before Use

These APIs were drawn from community samples (ANGULARarchitects) and may differ in the installed package version. Confirm against the actual `@a2ui/angular` / `@a2ui/web_core` build:

- `minimalCatalog` vs `inject(BasicCatalog)` export form.
- `BASIC_FUNCTIONS` export name.

Confirmed against the installed package (no longer "verify," these are facts as of this project's `@a2ui/angular`/`@a2ui/web_core` versions):

- There is no `binding()` helper. Use `DynamicStringSchema` / `DynamicNumberSchema` / `DynamicBooleanSchema` / `DynamicStringListSchema`, exported directly from `@a2ui/web_core/v0_9` (`schema/common-types.d.ts`).
- `BasicCatalogBase` exists and is the correct class for custom catalog extension; its constructor merges `DEFAULT_COMPONENT_IMPLEMENTATIONS` with `options.extraComponents`, it does not replace the defaults.
- `AngularComponentImplementation` type exists and is exported from `@a2ui/angular/v0_9`. The `as unknown as AngularComponentImplementation` cast is still commonly required in practice — not because the type itself is wrong, but because a custom Zod schema built with the app's own `zod` install can structurally mismatch the `zod` nested inside `@a2ui/web_core` (see "Large Option Sets Need a Custom Compact Component" above).

## Sources

- A2UI home and spec: <https://a2ui.org/> , <https://a2ui.org/specification/v0.9-a2ui/>
- Client setup, catalogs, actions, theming guides: <https://a2ui.org/guides/client-setup/> , <https://a2ui.org/concepts/catalogs/> , <https://a2ui.org/concepts/actions/> , <https://a2ui.org/guides/theming/>
- GitHub: <https://github.com/a2ui-project/a2ui>
- Google Developers Blog: <https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/>
- Angular Blog (Devin Chasanoff): <https://blog.angular.dev/demystifying-a2ui-how-to-make-ai-agents-speak-ui-in-your-app-e1ffea2303bd>
- ANGULARarchitects A2UI series: <https://www.angulararchitects.io/en/blog/a2ui-how-ai-generates-dynamic-uis-at-runtime/>
