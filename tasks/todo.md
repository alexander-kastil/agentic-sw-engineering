# Solution implementations for demos/05-cli-sdk/02-sdk (topics 02-04)

Topics 02-sdk-demos, 03-deploy-azure and 04-multi-agent ship guides with no runnable
reference. Build a `*-solution` folder per topic by executing the guide, then fold every
defect found back into the guide.

## Groundwork

- [x] Confirm the `*-solution` sibling convention (spec-kit-cli-solution, sample-case-solution)
- [x] Probe the real `@github/copilot-sdk` API surface (1.0.14) against the guide snippets
- [x] Confirm Copilot CLI 1.0.87 is installed and authenticated

## 02-sdk-demos

- [x] Create `sdk-demos-solution/` with the weather agent, the interactive assistant and the security analyzer
- [x] Pin dependencies, add tsconfig, .gitignore and a solution readme
- [x] Typecheck, then run every non-interactive program end to end
- [x] Fix the guide against what actually ran

## 03-deploy-azure

- [x] Create `deploy-azure-solution/` wrapping an SDK agent in an HTTP service with a health check
- [x] Add the container and Container Apps deployment assets
- [x] Run the service locally and verify health plus a real agent call
- [x] Replace the guide's three-bullet demo with the executed steps

## 04-multi-agent

- [x] Create `multi-agent-solution/` with a coordinator and specialist agents
- [x] Verify the guide's `defineFactory` and fleet-mode claims against the SDK and the CLI
- [x] Run the coordinator end to end
- [x] Replace the guide's four-bullet demo with the executed steps

## Added mid-session

- [x] Rework `demos/02-agentic-harness/06-plugins` around a real, runnable plugin
- [x] Reframe `demos/02-agentic-harness/09-agent-interop` as Copilot and Claude Code interop
- [x] Renumber `demos/05-cli-sdk/02-sdk` after 03-mcp-apps moved to module 02

## Close

- [x] Name each solution folder once in its topic readme and in the module readme
- [x] Run the brand-voice-gh-copilot skill over every edited readme
- [x] Review section below

## Review

Every solution folder was built by executing its guide. The guides now describe what ran.

### Blockers found by running, all folded back into the guides

02-sdk-demos, four blockers, none visible to a reader:

1. A custom tool call is denied at runtime unless the tool sets `skipPermission: true` or the
   session supplies `onPermissionRequest`. The agent reports it could not reach the service, so
   it reads as a broken handler rather than a missing permission.
2. `handler: async ({ city }) => ...` does not compile. `defineTool` defaults its type parameter
   to `unknown`, so `tsc` reports TS2322. Invisible under `tsx`, which does not typecheck.
3. The recursive `rl.question` loop dies with `ERR_USE_AFTER_CLOSE` at end of input.
4. Built-in tools shadow custom ones: asked to read a file the model calls the built-in reader,
   not `read_code_file`. Fixed with `availableTools: ["custom:*"]`.

03-deploy-azure, two fabricated mechanisms:

1. "The hosting library handles the protocol, the HTTP server, health checks, and request and
   response schemas." There is no hosting library. You write your own HTTP server and either let
   the client spawn the runtime or attach to `copilot --headless` with `RuntimeConnection.forUri`.
2. `COPILOT_PROVIDER_TYPE`, `COPILOT_PROVIDER_BASE_URL` and `COPILOT_PROVIDER_API_KEY` are not
   real. Bring-your-own-model is the session's `provider` object, and you name the secret
   variables yourself.

06-plugins, the manifest example was schema-invalid:

The published schema requires `$schema` and sets `additionalProperties` to false. The guide's
example declared `skills`, `mcpServers` and a top-level `com.github.copilot`, none of which are
permitted keys, so it fails validation with exactly two errors. Components are discovered by
convention instead: `skills/`, `mcp.json`, and a `com.github.copilot/` directory. The guide also
never mentioned `chat.pluginLocations`, which is the only way to load a plugin you are editing.

### Verification notes

`copilot --help` DOES work and emits 13527 bytes, including the `--fleet` entry. Three early
attempts in this session returned nothing and I wrongly concluded the CLI suppresses help when
stdout is not a TTY. It does not: the same command piped to `wc -c`, to `head -5`, and redirected
to a file all produce the full text. The early emptiness was transient, most likely a first-run
or update check. The lesson is that an empty result from an external CLI is a claim about that
one invocation, and it needs a second probe with a different consumer before it becomes a fact
about the tool.

Separately and still true: the `copilot` on the PowerShell PATH is a VS Code-managed wrapper whose
1.0.88-0 install is broken (missing native addon, and it tries to prompt for a reinstall). The
Git Bash one is 1.0.87-0 and works.

Azure deployment was deliberately not run: it creates billable resources in the owner's
subscription.

### Left alone

The repo-wide brand-voice backlog: 111 demo readmes, 112 violations, almost all rule 6 (no
mermaid diagram) and rule 10 (no Links & Resources section) on index pages. Four of those sit in
files touched this session, in `03-mcp/readme.md` and `02-sdk/readme.md`, both of which are index
pages that were already non-compliant. Not expanded into a repo-wide sweep.

## 2026-09-23: Python variant of the harness solution

- [x] Port `.github/` customization files to Python in `labs/03-harness/harness-solution/product-inventory-py/.github/`
- [x] Build a runnable FastAPI ContosoInventory API (auth, categories baseline, Product feature) with SQL delta scripts
- [x] Write `labs/03-harness/harness-solution/readme-py.md`
- [x] Run every command in `readme-py.md` from a clean venv and fix what fails
- [x] Validate the guide (fence languages, links, guide-validator)

### Review

All 8 Run and verify blocks in `readme-py.md` executed from a clean venv and database; outputs match every Expected line. Fixed during the run: responses pasted as one block printed blank rows until each call was piped to `Format-List`.

## 2026-09-24: Module 08 consolidation (cost + BYOK, enterprise control)

- [x] Move `02-cost` to `02-cost-byok`, nest the two BYOK guides under it, renumber `06-compliance` to `05-compliance`
- [x] Repair nav links, module table, master TOC, schedule row, module 9 and lab 09 references
- [x] Merge the old topic 05 readme into `02-cost-byok/readme.md`, reframed to bring your own key
- [x] Retitle and reframe the two BYOK guides; add `03-byok-copilot-app` from the local app config, keys excluded
- [ ] Reframe `03-enterprise-control/readme.md` to Business and Enterprise controls, architect view
- [x] Link check, fence check, brand voice
- [x] Slides: specs renumbered, three cards rewritten, two diagrams redrawn, deck patched in place, dividers, clean, notes

### Review

link-check demos: no broken link under module 08 (24 pre-existing elsewhere); labs clean. Fences 0 untagged. Brand voice clean on new and rewritten files; pre-existing rule 5/6/10 hits left in untouched files. Deck: 27 slides, clean `removed=0 bullets=0`, notes `unmatched=0 missing=0`. Not delivered to OneDrive.
