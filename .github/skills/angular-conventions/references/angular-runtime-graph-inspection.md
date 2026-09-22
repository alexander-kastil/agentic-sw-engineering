# Runtime DI and Signal Graph Inspection

Angular ships two in-page debugging tools that expose framework internals to an agent.
Use them to answer questions about the *running* app that the source does not settle:
which providers actually resolved, in what injector, and which signals an effect reads.

## What ships, and where

`@angular/core` 22.1.1 defines `angular:di_graph` and `angular:signal_graph` in
`fesm2022/core.mjs`. `registerAiTools()` runs inside `createPlatform()` and answers a
`devtoolstooldiscovery` window event with `{name: 'Angular', tools: [...]}`.

Nothing is needed in application code: no provider, no import, no flag. Verified on
`admin.integrations.at` (Angular 22.1.1) with an unmodified `ng serve`.

Upstream: angular/angular#68030, merged 2026-04-14.

## Reaching the tools

### Path A: `evaluate_script` (works with our default MCP config)

Dispatch the discovery event yourself and call `execute` in the page:

```js
async () => {
  let payload = null;
  const ev = new CustomEvent('devtoolstooldiscovery');
  ev.respondWith = (p) => { payload = p; };
  window.dispatchEvent(ev);
  const tool = payload.tools.find(t => t.name === 'angular:di_graph');
  const r = await tool.execute({}, {});
  return r.environmentInjectorRoot.children[0].providers.map(
    p => typeof p.token === 'function' ? p.token.name : String(p.token)
  );
}
```

**The raw result is not JSON-serializable.** Provider `value`s and `hostElement` are live
objects and the LView `blueprint` is circular, so returning `r` (or stringifying it)
fails with `Converting circular structure to JSON`. Always map to primitives inside the
page function: token names, `tagName`, counts.

### Path B: the MCP's own bridge (needs a config change)

`chrome-devtools-mcp` 1.7.0 carries `list_3p_developer_tools` and
`execute_3p_developer_tool`, but their category `experimentalThirdParty` is in
`OFF_BY_DEFAULT_CATEGORIES`. Enable with `--categoryExperimentalThirdParty=true` in the
server args. Without it the tools are not in the session tool list at all.

The parallel WebMCP route (`navigator.modelContext`, `provideExperimentalWebMcpTools`,
`--categoryExperimentalWebmcp=true`) needs Chrome 150+ launched with
`--enable-features=WebMCP`; `navigator.modelContext` was `undefined` in our profile, so
Angular's `declareExperimentalWebMcpTool` returns early and registers nothing.

## `angular:di_graph`

Takes no arguments. Returns `elementInjectorRoots` (array) and `environmentInjectorRoot`.

**The environment half is the useful half.** On the admin app it returned 5 nodes and 95
providers, with 87 of them on the application environment injector: `ROUTES`,
`HTTP_INTERCEPTOR_FNS`, `HTTP_INTERCEPTORS`, `MSAL_INSTANCE`, `MSAL_GUARD_CONFIG`,
`MSAL_INTERCEPTOR_CONFIG`, `ErrorHandler`, `Zoneless enabled`. That answers the questions
worth asking a live app: is the interceptor registered, in what order, did the MSAL config
token resolve, is zoneless actually on, is a provider registered twice.

**The element half is close to noise.** 18 nodes and 108 providers on one route, and every
node is named `NodeInjector` carrying the identical six built-ins (`Injector`,
`DestroyRef`, `ElementRef`, `Renderer2`, `ViewContainerRef`, `ChangeDetectorRef`). The
only identifying data on a node is `hostElement`, so read `hostElement.tagName` to
recover the component tree and ignore `name`. Component-level `providers: [...]` show up
here as extra entries beyond those six.

Known gaps, stated by the author: there is no component to environment-injector edge, so
the graph cannot tell you *which* environment injector serves a component; multiple apps
on one page are unsupported; components inside i18n messages are skipped.

## `angular:signal_graph`

Takes `{target: HTMLElement}`, which must be a component host element. Returns `nodes`
(`kind`: signal / computed / effect / template, plus `label`, `value`, `epoch`) and
`edges` (`{consumer, producer}` as indices into `nodes`).

**It walks the effects of that element and nothing else.** A component with no `effect()`
returns `{nodes: [], edges: []}`. Measured on the admin app: `app-editor-pane`,
`app-activity-bar` and `app-site-header` all returned 0 nodes; `app-chat-page` returned
2 nodes and 1 edge, being its single effect and the `slug` signal that effect reads.

So an empty result means "this component runs no effects", never "this component has no
reactive state". Signals consumed only by the template do not appear. Reach for this tool
when an `effect()` fires too often, too rarely, or reads something unexpected, and do not
use it to survey a component's state.

## Choosing

| Question | Tool |
| --- | --- |
| Is my interceptor / MSAL token / route config actually provided, and once? | `di_graph`, environment half |
| What is the live component tree under this root? | `di_graph`, element half, read `hostElement.tagName` |
| Why does this effect re-run, and what does it depend on? | `signal_graph` on that component's host |
| What signals does this component hold? | Neither; read the source |
