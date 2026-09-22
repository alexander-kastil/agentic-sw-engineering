# Angular App Update

Upgrade an Angular workspace to the latest version using an orchestrated, parallel flow.

> **⚠️ `ng update` can commit and sweep the working tree. Verify the index yourself; do not assume either way.**
>
> A `maintenance-planner` upgrade saw `ng update` `git commit` its migration changes and stage **everything** dirty in the tree, not just its own edits, bundling unrelated in-flight work into those commits. That violates the repo's "never commit without explicit request" rule, so keep guarding against it.
>
> **What was actually observed on Angular 22.1.3 (2026-08-10) is narrower, and the difference matters.** `ng update` run with `--allow-dirty` on a dirty tree created no commit (`HEAD` stayed at the pre-update sha and `git reflog` gained no entry) and left every change **unstaged**: column 1 of `git status --porcelain` was a space for all 60 paths, checked repeatedly through the session. The tree *did* later turn up fully staged, 60 entries with `M `/`A ` in column 1 and zero unstaged, including files the update never touched (`CLAUDE.md`, `.claude/skills/**`, `.time/working-time.md`, image assets). But `.git/index` was written about ten minutes after the last `ng` command, in a window where no `ng` and no `git` command ran at all, so **the update did not cause it**. In a checkout shared with other sessions or tooling, assume anything can stage your work at any time, and attribute a state change only when you have a timestamp that supports it.
>
> **Procedure:**
> 1. Record a baseline before starting: `git rev-parse HEAD` and `git status --porcelain`, saved somewhere outside the repo.
> 2. After the update, list what is staged with `git status --porcelain | grep -v '^ '` and confirm `git rev-parse HEAD` still matches the baseline sha. Nothing staged and an unchanged HEAD is the clean outcome.
> 3. If the state changed, check `stat -c '%y' .git/index` against the wall-clock time of your last `ng` command before blaming the update. A gap means another writer.
> 4. `--allow-dirty` only lets the update proceed on a dirty tree. It is not a guard against commits or staging, so do not treat passing it as having handled the risk.
> 5. Undoing any of this (`git reset`, `restore`, `checkout`, `stash`, `clean`) is the user's decision, never the agent's. Report the state and stop.

## Prerequisites

- Workspace path is known (use `list_projects` to confirm)
- Working branch is clean or has uncommitted changes flagged with `--allow-dirty`
- User has granted explicit approval before any refactoring tasks (Tasks H/I) run

## Version Compatibility Gate (run BEFORE bumping anything)

Run it as a script first, then read the rules below for anything it flags:

```bash
node <this-skill>/scripts/angular-update-preflight.mjs --root src
# per workspace: declared/installed/latest core, TypeScript vs the compiler peer range,
# engines.node vs the running node AND the Dockerfile base tag, the MSAL README matrix,
# and every dependency whose @angular/core peer is unmet, with its dist-tags.
# --workspace <dir> (repeatable), --offline, --json; exits 1 if anything is BLOCKED.
```

It only reports; every decision below stays yours. It exists because each of these checks was a separate
manual command, and skipping one is how the MSAL and Node findings below went unnoticed for a whole
portfolio.

"Update everything to latest" is how a workspace breaks. `npm outdated` reports what is newest, never what is *compatible*. Decide what NOT to bump first, and prove each decision from a file on disk or a registry query rather than from memory. Every rule below was established on a real Angular 22.1.1 / CLI 22.1.3 workspace on 2026-08-10.

### 1. TypeScript: read the peer range off the compiler, never take latest

Angular pins a narrow TypeScript window. Read it from the installed compiler:

```bash
node -e "const p=require('./node_modules/@angular/compiler-cli/package.json'); console.log(p.version, JSON.stringify(p.peerDependencies))"
```

On Angular 22.1.1 this prints `22.1.1 {"@angular/compiler":"22.1.1","typescript":">=6.0 <6.1"}`. TypeScript 7.0.2 was available and is **out of range**, so it stays unbumped. The `>=x <y` form is the authority; a green build on an out-of-range TS proves nothing, because the compiler only warns on some mismatches.

### 2. Third-party libraries with an `@angular/core` peer lag the framework

Check the tag before assuming a compatible release exists:

```bash
npm view <pkg> dist-tags --json
npm view <pkg>@<version> peerDependencies --json
```

`@ngrx/signals` was `{"latest":"21.1.1","next":"22.0.0-rc.0"}`, with 21.1.1 peering `@angular/core: ^21.0.0`. So on Angular 22 the choice is stable-with-unmet-peer versus a release candidate.

**Rule: prefer the stable version with an unmet peer over an RC**, unless the RC fixes a bug you are actually hitting. An unmet peer is a warning the install already absorbs; an RC is unreleased code in a production dependency. Re-check when the stable major ships.

Check each package separately rather than assuming a family moves together: `@ngrx/operators@21.1.1` declares **no** `@angular/core` peer at all (`{"rxjs":"^6.5.3 || ^7.4.0"}`), so only `@ngrx/signals` was ever unmet. Reporting both as blocked would have been wrong.

### 3. Libraries that declare framework support in prose, which no tool can see

`npm outdated` and peer ranges both missed that the dashboard was running `@azure/msal-angular` v4 on Angular 22, an unsupported pairing. The truth lived in the package README:

```bash
sed -n '/## Version Support/,/## Prerequisites/p' node_modules/@azure/msal-angular/README.md
```

The real table has **three** columns and spells the version out in the first cell, which matters if you
parse it rather than read it:

```text
| MSAL Angular version | MSAL support status | Supported Angular versions |
| -------------------- | ------------------- | -------------------------- |
| MSAL Angular v6      | Active development  | 22                         |
| MSAL Angular v5      | In maintenance      | 19, 20, 21                 |
| MSAL Angular v4      | In maintenance      | 15, 16, 17, 18, 19, 20     |
```

**Rule: for any auth or platform SDK, read the README support matrix and the migration guide, not just the peer range.** A library can install cleanly, typecheck, build and pass tests while being formally unsupported on your framework version. Applies to MSAL, and to anything else that publishes a support table.

### 4. Test-environment majors: gate on the Node floor and on what the tests assert

jsdom 28 to 30 crosses two majors. Both breaking changes were Node engine bumps:

```bash
npm view jsdom@30.0.1 engines --json   # {"node":"^22.22.2 || ^24.15.0 || >=26.0.0"}
node --version                         # must satisfy it, and so must CI and Docker
```

The real risk is not the engine but the behaviour your tests depend on. jsdom 29 replaced the entire CSSOM implementation and 30 changed `getComputedStyle()` to return pixels, so the deciding check was whether anything asserts on computed style:

```bash
grep -rn "getComputedStyle\|computedStyle" src/
```

Zero hits made the bump safe, and the full suite passing on the new version confirmed it. **Rule: for a test-env dependency, identify which behaviour the majors changed, grep for tests that depend on it, then let the suite decide.** Note that raising the floor to `^24.15.0` means a contributor on 24.14 now sees `EBADENGINE`; that is advisory only unless an `.npmrc` sets `engine-strict`, so check for one.

### 5. Caret floors are the deployed version when the image has no lockfile

Check how the image installs before assuming the lockfile governs:

```bash
grep -nE "COPY package|npm (ci|install)" Dockerfile
```

The dashboard `Dockerfile` copies **only** `package.json` and runs `npm install`, no lockfile. A floor of `^22.0.0` therefore ships whatever npm resolves at image build time, not the version the green lockfile pinned; and a floor of `^4.0.15` would have rebuilt the image on MSAL v4 no matter what the lockfile said.

**Rule: after any update, raise the manifest floor to the version you actually tested.** `ng update` does this for the packages it touches; anything you bump by hand needs it done deliberately. It is what makes the manifest a record of a tested combination rather than a wish.

### 6. Repo install convention

Both Dockerfiles install with `--legacy-peer-deps`, so local commands must match or they fail on `ERESOLVE` where the image succeeds:

```bash
npm update --legacy-peer-deps
npm install --save-dev --legacy-peer-deps <pkg>@<version>
```

### 7. The Node floor moves inside a minor line, and it does not live in CI

Angular's `engines.node` is not stable across a major. Angular 22.1.x declares:

```bash
npm view @angular/cli@22.1.4 engines --json
# {"node":"^22.22.3 || ^24.15.0 || >=26.0.0", "npm":"^6.11.0 || ^7.5.6 || >=8.0.0"}
```

A 22.0.x to 22.1.x bump raised that floor **within the same major**. So "we are already on the right
Node major" is not a compatibility answer: read the range off the exact CLI version you land on, every
time, and reconcile it against whatever pins Node in the build.

**Where Node is pinned is the part that gets looked for in the wrong place.** Asked to upgrade the Node
version "in the workflows", a grep of all 20 workflow files for `setup-node|node-version|NODE_VERSION`
returned zero hits, because every app is built inside its image by `docker/build-push-action@v6` and CI
never installs Node at all. The version was four `FROM node:22` lines in four Dockerfiles. An empty grep
here is the answer, not a failed search: **find where Node enters the build before changing anything**,
and do not add a `setup-node` step to a workflow that builds in Docker, because it is dead configuration
that will later read as the authoritative pin.

A **floating** base tag is not a pin. `FROM node:22` resolved to 22.23.2 that day, which satisfied
`^22.22.3`, so the images built: by luck, since the tag floats and the floor had just moved up inside the
line it floats over. Pin an explicit version that satisfies the range (`FROM node:24.19.0`, keeping each
file's existing `-alpine` or Debian flavour, because `npm rebuild lightningcss` and `--include=optional`
behave differently between them).

**And re-read what the new base image bundles.** Three of the four Dockerfiles carried
`RUN npm install -g npm@11.12.1`. On `node:22` that was an upgrade; on `node:24.19.0`, which bundles npm
11.17.0 (`docker run --rm node:24.19.0 npm -v`), the identical line is now a **downgrade**. That may
still be what you want, since the lockfiles were regenerated with that npm, but it is no longer doing
what its author meant, so decide it deliberately rather than leaving it to read as a no-op.

Verify by building the image, not by building on the host: `npm ci` inside a fresh image is the only
thing that proves the pinned base installs the bumped tree. A green host `ng build` says nothing about
the image's Node.

### 8. Known-benign noise, do not chase

- A clean `npm i -g @angular/cli` still emits an `ERESOLVE` peer warning for `listr2`: CLI 22.1.3 depends on `listr2@10.2.2` while its own `@listr2/prompt-adapter-inquirer@4.2.4` pins `10.2.1`. No version combination resolves it and nothing is broken.
- `npm audit` reports 3 moderate findings via `@angular/cli` to `@modelcontextprotocol/sdk` to `@hono/node-server`. That is the CLI's own MCP server, never in the shipped browser bundle, and `npm audit fix --force` "fixes" it by **downgrading** `@angular/cli` to 21.0.4. Leave it.
- `mcp__angular-cli__search_documentation` may fail with `Cannot find module 'algoliasearch'` from the globally installed CLI. `list_projects` and `get_best_practices` still work; fall back to on-disk peer ranges and the npm registry for version questions.

## Orchestration Flow

Run Tasks A and B in parallel, then C/D/E after the dev server is up, then F/G for analysis. Tasks H and I require explicit user approval before execution.

### Task A: Core Dependencies Upgrade (parallel with B)

1. Read `package.json`: detect Angular version, Material, CDK, NgRx, and other `@angular/*` packages.
2. Run upgrade commands in order:

```bash
ng update @angular/core @angular/cli
ng update @angular/material   # if present
ng update @angular/cdk        # if present
ng update @ngrx/store @ngrx/effects @ngrx/signals  # if present
```

3. Use `--allow-dirty` only if the workspace has uncommitted changes.

### Task B: Dev Environment Setup (parallel with A)

1. Check whether a dev server is already running on port 4200 (or the configured port). Re-use the existing instance; do not kill processes you did not start.
2. If `db.json` exists, run `json-server --watch db.json` in the background.
3. If no server is running and the user has granted permission, run `ng serve` and wait for "Application bundle generation complete".
4. Verify the dev URL is reachable.

### Task C: Runtime Error Audit (after B)

Open the app in the browser via the Chrome DevTools MCP. Capture all console errors and warnings. Categorize: Critical / Warning / Info.

### Task D: Route Testing (after B, parallel with C)

Navigate to key routes. Check for component load errors, signal mismatches, and missing imports.

### Task E: Deprecation Analysis (after C and D)

Cross-reference console warnings with the Angular breaking-changes log. Categorize by severity using the registry below.

**Anti-pattern registry:**

| Anti-pattern | Severity |
|---|---|
| `@Input()` / `@Output()` decorators instead of `input()` / `output()` | Critical |
| `*ngIf` / `*ngFor` / `*ngSwitch` instead of `@if` / `@for` / `@switch` | Critical |
| `standalone: true` explicitly set (redundant in v20+) | High |
| `async pipe + Observable` for HTTP reads instead of `httpResource()` | High |
| `toSignal(http.get(...))` instead of `httpResource()` | High |
| `subscribe()` in component body | High |
| `BehaviorSubject` for local state instead of `signal()` | Medium |
| Constructor injection instead of `inject()` | Medium |
| `ChangeDetectionStrategy.Default` on components | Medium |
| `@HostBinding` / `@HostListener` instead of `host` object | Medium |
| `ngClass` / `ngStyle` instead of `[class.x]` / `[style.x]` bindings | Medium |
| Reactive Forms / `ngModel` where Signal Forms apply | Medium |

### Task F: Zoneless Migration Analysis (after E, parallel with G)

- Scan components for `ChangeDetectionStrategy.Default`.
- Count `@Input()` / `@Output()` decorators (non-signal inputs/outputs).
- Check for `NgZone` usage that blocks zoneless migration.
- Generate a migration prerequisites list and effort estimate.

### Task G: Optimization Recommendations (parallel with F)

Identify high / medium / low impact improvements. Present findings as a list before making any code changes.

## Key Rules

- Stop and ask the user if `ng serve` fails — do not attempt workarounds and do not proceed.
- Present full findings before touching any source files.
- Tasks H (codebase refactoring) and I (zoneless migration) require explicit user approval before executing.
- Kill dev servers you started when the session ends; never kill servers you did not start.
- Never run `git` commands or commit without explicit user instruction.

## Angular 22 Upgrade (Completed)

`maintenance-planner` `src/ui` was upgraded **21.2.9 → 22.0.5** (all `@angular/*` plus `cli`/`build`/`devkit` packages) via `ng update @angular/core@22 @angular/cli@22`. Non-obvious steps from that run, for the next upgrade:

| Item | Detail |
| --- | --- |
| TypeScript peer bump | Angular 22 requires **TypeScript 6.0.3** (was 5.9.3) — the schematic applied it automatically |
| NgRx stays pinned | `@ngrx/signals` / `@ngrx/operators` remained at **21.1.0** (no v22 build exists yet); the existing `legacy-peer-deps=true` in `.npmrc` absorbed the peer warning with **no `--force` needed**. Do not bump NgRx to a non-existent v22 |
| Automated migration: HTTP testing | `withXhr` added to `provideHttpClient()` in HTTP-testing specs — Angular 22 defaults `HttpClient` to the **Fetch** backend, and `HttpTestingController` needs XHR |
| Automated migration: templates | `$safeNavigationMigration()` wrapper added to templates (stricter optional-chaining/null-propagation); tsconfig `extendedDiagnostics` suppressions added for `nullishCoalescingNotNullable` / `optionalChainNotNullable` |
| Manual fix the schematic missed | Angular 22's `CanMatchFn` gained a required **third `currentSnapshot: PartialMatchRouteSnapshot` argument**. The automated migration does not rewrite direct test invocations of guards — guard `.spec.ts` files calling `canMatchAuth(route, segments)` / `reservationCanMatch(...)` broke compilation; fixed by adding a third `null as any` argument at each test call site. The guard implementations themselves compile fine with fewer params |
| Signal Forms | No API delta in 22 — still `@experimental` (see `angular-forms.md`) |

### Second run: `vouchers-ai` `src/vouchers-ui`, 21.2.15 → 22.1.2 (2026-08-16)

Confirms the `CanMatchFn` third-argument break above (one guard spec, fixed with a third `{} as never`). Four things that run did not:

| Item | Detail |
| --- | --- |
| No `.npmrc` means `--force`, not a warning | `ng update` **hard-refuses** when a stable dependency peers on the previous major: `@a2ui/angular@0.10.5` requires `@angular/common ^21.2.5`, so the run aborted with "Incompatible peer dependencies found". With a `legacy-peer-deps=true` `.npmrc` this is a warning; without one it is a wall, and `--force` is the documented way through. Check for the `.npmrc` before predicting which you will get. Later hand-installs still need `--legacy-peer-deps` explicitly |
| A crash on the first `--force` attempt | The forced run died at "Fetching dependency metadata" with Windows exit `3221226505` (`STATUS_STACK_BUFFER_OVERRUN`). Re-running the identical command succeeded and applied every migration. Retry once before investigating |
| View effects now run inside `detectChanges` | Two specs that passed on v21 broke on **test-environment** gaps the effects had never reached: `scrollIntoView is not a function` (jsdom has never implemented it) and a hand-written A2UI double missing `surfaceGroup.getSurface`. Neither is an app bug. Stub the jsdom gap in a setup file (`Element.prototype.scrollIntoView = () => {}`); complete the double for the path that now executes |
| A setup file is inert until registered twice | `src/test-setup.ts` existed but was in neither `angular.json` nor the spec tsconfig. It needs `setupFiles: ["src/test-setup.ts"]` under the `@angular/build:unit-test` target's `options`, **and** an entry in `tsconfig.spec.json` `include` — without the second it still runs but warns "not found in TypeScript compilation" and is not type-checked |

MSAL moved 5 → 6 in the same pass (v6 is the only major supporting Angular 22, see `msal-angular.md`). Where the wiring already matches the v5+ shape — `navigateToLoginRequestUrl` on the `handleRedirectObservable()` call, `logoutRedirect()`, `/*`-suffixed `protectedResourceMap` keys, auth state written into signals — the bump is `npm install --legacy-peer-deps @azure/msal-angular@^6.0.3 @azure/msal-browser@^5.18.0` and **no code change at all**. Verify each of those four before assuming work is needed.

### Third run: four workspaces in one monorepo, 22.0.1 → 22.1.2 (2026-08-17)

A whole portfolio on one framework version, updated as two parallel agents (three admin apps, one
customer portal). Every app was install-only: zero source edits across all four, 776 unit tests green,
and all four images rebuilt. What that run changed in the guidance above:

| Item | Detail |
| --- | --- |
| The hard-refusal is **not** deterministic | The second-run note above says `ng update` hard-refuses without an `.npmrc` when a dependency peers on the previous major. Two of these four apps have no `.npmrc` and `@ngrx/signals` peering `^21.0.0`, and both updated cleanly with no `--force` and no refusal. **Try without `--force` first** and let the tool decide; predicting the wall from the absent `.npmrc` cost nothing here but would have applied `--force` needlessly |
| The Windows crash reproduced a third time | `3221226505` (`STATUS_STACK_BUFFER_OVERRUN`) at "Fetching dependency metadata", identical command succeeded on retry. Three occurrences across three repos: treat one retry as part of the procedure, not as a symptom |
| An unsupported auth SDK drifts silently across a **whole portfolio** | All four apps ran `@azure/msal-angular@^5.x` on Angular 22, which the README matrix says is unsupported (v6 is the only major supporting 22). Nothing surfaced it: `npm outdated` is quiet because 5.x had newer 5.x releases, and the peer range installs fine. When a framework major lands, sweep **every** app's auth SDK support matrix, not just the app you were sent to. All four already had the v5+ call shape, so the fix was `npm install --legacy-peer-deps @azure/msal-angular@^6.0.3 @azure/msal-browser@^5.18.0` and no code change |
| `@ngrx/signals` still has no stable v22 | `{"latest":"21.1.1","next":"22.0.0-rc.0"}`, unchanged from the first run. Rule 2 above holds: stable with an unmet peer, never the RC |
| `CanMatchFn` did not bite | None of the four apps has a `CanMatchFn` guard, so the documented third-argument break never triggered. Grep for it (`grep -rn "CanMatchFn\|canMatch" src/`) rather than assuming the fix is needed |
| `list_projects` under-reports | It gives `frameworkVersion: "22"`, the major only, so it cannot confirm you landed on 22.1.2: read `node_modules/@angular/core/package.json`. It also omitted `unitTestFramework` entirely for these workspaces; read the `test` target's builder out of `angular.json` instead (`@angular/build:unit-test` means Vitest) |
| The generic best-practices guide can contradict a repo hard rule | The v22 guide returned by `get_best_practices` says not to set `changeDetection: ChangeDetectionStrategy.OnPush` explicitly because it is the v22 default, and prefers a new `@Service` decorator over `@Injectable({providedIn: 'root'})`. That repo's agent file mandates explicit OnPush on every component, 88 files' worth. **The repo convention wins and the divergence gets recorded**, so a later session does not "fix" it as an anti-pattern. Report what the guide flagged; do not act on it inside an update task |

### After the upgrade: a red e2e suite is usually not the upgrade

A 23-failure Playwright suite straight after this upgrade contained **zero** upgrade regressions. The causes were app changes made weeks earlier that no one had re-run the suite against: selectors targeting a `title` attribute that a custom tooltip directive had replaced, specs asserting a server call the app now does client-side, fixtures sitting exactly on a `PAGE_SIZE` boundary, and reads racing an async form load.

Attribute before fixing: `git show HEAD:<file>` at the pre-upgrade commit answers "did this ever work?" in one command. Budget the triage, not the upgrade.
