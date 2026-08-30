# Angular Wizard / Setup-Flow UI

A wizard turns a store-driven multi-phase flow (e.g. onboarding: `connect → review → deploy`) into a
guided, full-width experience with a persistent step indicator. Use it when a feature spans several
phases and the current one, what's done, and what's next should always be visible.

## Shell: full-width, step rail + content

Two-column grid — a **sticky vertical step rail** plus the content area. Use the app's real width
(don't let the flow sit in a narrow 25%-width card):

```
grid-template-columns: 210px 1fr;  gap: 24px;  max-width: 1280px;  margin: 0 auto;
```

Step cards show `Step N` + label + a short hint. State is **derived from the store phase**, not local:

```ts
protected readonly currentStep = computed(() => {
  if (this.store.phase() === 'deployed') return 2;   // Deploy
  return this.store.hasProposal() ? 1 : 0;           // Review : Connect
});
```

```css
.step-card.active { background: rgba(240,136,62,.08); border-left-color: var(--accent); }
.step-card.active .step-label { color: var(--accent); }
.step-card.done  .step-label { color: var(--success); }
.step-card.done  .step-label::after { content: ' ✓'; }
```

Responsive: below ~860px collapse the rail to a **horizontal** row (`flex-direction: row`, move the
active indicator to `border-top`) and the content to a single column.

## Step body: two columns

Within a step, split a narrow **actions/summary sidebar** (identity, selection summary, primary CTA)
from a wide **content panel** (the list/picker):

```
.connected-grid { display: grid; grid-template-columns: 320px 1fr; gap: 20px; align-items: start; }
@media (max-width: 860px) { .connected-grid { grid-template-columns: 1fr; } }
```

Keep exactly **one primary CTA** per step (the Analyze/Next/Deploy button in the sidebar); secondary
actions (Disconnect, Cancel) are visually subordinate.

## Copy-to-clipboard button

For codes/tokens the user must transcribe (e.g. a device code), pair the value with a copy button that
gives transient confirmation via a signal — no library:

```ts
protected readonly copied = signal(false);
protected async copyCode(code: string): Promise<void> {
  try {
    await navigator.clipboard.writeText(code);
    this.copied.set(true);
    setTimeout(() => this.copied.set(false), 1500);
  } catch { this.copied.set(false); }
}
```

Swap the icon (clipboard ↔ check) on `copied()`, and colour the check with `--success`. Give the button
an `aria-label` that flips between "Copy code" / "Copied".

## Chip filters — real data only

Filter chips must come from **real attributes of the data**, never an invented taxonomy. Owner-based
buckets are legitimate because they derive from the API's `owner.login` vs the signed-in login:

```ts
protected readonly tag = signal<'all' | 'yours' | 'shared'>('all');
protected readonly visibleRepos = computed(() => {
  const login = this.gh.status()?.Login, tag = this.tag(), q = this.query().trim().toLowerCase();
  return this.gh.repos().filter(r => {
    if (tag === 'yours'  && r.OwnerLogin !== login) return false;
    if (tag === 'shared' && r.OwnerLogin === login) return false;
    return !q || r.FullName.toLowerCase().includes(q) || r.Description.toLowerCase().includes(q);
  });
});
```

Show live counts per chip (`All 42 · Yours 30 · Shared 12`). Do **not** synthesize tags a repo doesn't
have (e.g. splitting `dotnet-api` into `dotnet`+`api`) — a repo's stack is unknown until it's analyzed;
tech/kind badges belong on the *result* view where they're actually detected.

## Conventions

- Standalone component, `ChangeDetectionStrategy.OnPush`, `inject()`, `signal()`/`computed()`.
- Style with existing CSS tokens (`--surface`, `--surface2`, `--border`, `--muted`, `--text`,
  `--accent`, `--success`, `--radius`) — no raw hex, so light/dark and theme stay consistent.
- SVG icons only (Lucide/Octicons paths inline), never emoji.
- A richly-styled wizard component can exceed Angular's default `anyComponentStyle` budget (4 kB) —
  raise the budget in `angular.json` (`maximumWarning`/`maximumError`) rather than cramping the design.
