# Lessons

## Never relay an interactive auth code through a chat turn

**Pattern:** The Step 5 send needed `Connect-MgGraph`. I started the device-code flow myself in
a background process, read the code out of its output, and posted it in my reply. Graph
PowerShell aborts after 120 seconds of inactivity, so it had expired before the user could act.
The same flow succeeded immediately once the user ran it themselves at the `!` prompt, because
the code and the person were in the same place.

**Rule:** An interactive sign-in is started by the user, never by me on their behalf. Hand them
the command and stop. Device-code windows are short (120s for Graph PowerShell), and a relay
through an assistant turn spends most of it. The same applies to any flow with an inactivity
timeout: browser consent, MFA prompts, `gh auth login`.

## A PowerShell pipe buffers a background job's streaming output

**Pattern:** I ran the device-code login with `... | Select-Object -Last 20` in the background so
I could read the code. The output file stayed empty: `Select-Object -Last N` cannot emit anything
until the upstream pipeline completes, so the code never reached disk and the job died on timeout
with nothing captured. It looked like the process had produced no output at all.

**Rule:** When a background process's value is what it prints *while running*, never pipe it.
Use `*>&1` and read the output file directly. Reserve `Select-Object -Last`/`-First` for
foreground commands whose output you only need after they exit.

## A capability can be gated twice, and the error names only one gate

**Pattern:** `/me/sendMail` was denied through Work IQ. The user granted the `Mail.Send` Graph
consent and it was still denied, because the OAuth scope and Work IQ's server-side path allowlist
are independent gates. `search_paths` returning `fetch` on every path was the real signal and I
had already seen it; I read the fix as "consent the scope" because that is what the denial
mentioned. `workiq policy list` answering `Permission denied` was the confirmation that the second
gate is admin-only.

**Rule:** When a permission fix does not change the error, stop re-applying it. Ask which layer
denied the call before assuming it was the one the message named. A catalogue that lists zero
write operations across every path is a deployment-wide gate, not a missing scope, and no amount
of consenting opens it.

## A prerequisite introduced mid-flow is not "above"

**Pattern:** After the device-code timeout I closed with "Still outstanding: the login above, then
I send." The user answered "what login". The login had only ever appeared as a consequence of a
failure two turns earlier; from their side nothing had established that a second sign-in existed
or why.

**Rule:** A step that appears because something failed is new information, not a back-reference.
Name it, say which system it is against, and say why the obvious alternative does not work,
in the turn that asks for it.

## Verify a guide by running it, not by reading it

**Pattern:** Steps 1 to 4 of the business case read as plausible and were correct. Step 5 read
exactly as plausible and had no tool behind it at all: Work IQ is deployed read-only, so
"use Microsoft Graph to authenticate and send via Outlook" had nothing to call. Only executing it
surfaced that, along with the unindexed-column `$filter` refusal and the GitHub Actions workflow
that cannot authenticate on a runner.

**Rule:** For a demo guide, establish ground truth independently first (query the data directly),
then run the guide's own commands verbatim and compare. Prose that describes a capability is not
evidence the capability is wired up.

## An install command that reports success may have installed nothing

**Pattern:** `uv tool install specify-cli` printed `Installed 1 executable: specify` and exited 0.
It had installed nothing. An older `specify-cli` from a git checkout was already on the machine, so
uv audited the existing environment and kept it. The probed CLI was 0.14.5, the real release is 1.0.9,
and the two generations disagree on every command name. A whole set of verified facts was built on
the wrong binary and had to be thrown away mid-run.

**Rule:** After any install, print the version and compare it against the registry's current release
before treating the tool's behaviour as ground truth. `Audited N packages` in the output means the
install was a no-op; re-run with `--reinstall`. A guide that tells a reader to install a tool needs
the same flag, or readers with a stale copy silently follow instructions for a version they do not have.

## A dirty file outside your scope belongs to a peer session, not to your agents

**Pattern:** A verification agent reported `M labs/08-devops/readme.md` as a scope violation and
said "something else in this workflow run did it". Nothing in the run had touched labs 01 to 08.
Another Claude session was working the same repo in parallel and had modified seven lab guides and
added six solution folders while this session ran. Reverting on the agent's word would have
destroyed a peer session's uncommitted work.

**Rule:** When the working tree shows changes outside your scope, read the diff before believing
any explanation of where it came from. A change that matches a different task's shape is a peer
session. Never revert it, never stage it, and say in the report that you left it alone.

## A refutation on "the quote is not in that file" is a re-file, not a dismissal

**Pattern:** Adversarial verifiers correctly refuted four findings because the quoted text lived in
`constitution.md` and `requirements.md` rather than the `readme.md` the finding named. Each
refutation then spelled out that the substance was sound and named the right file. Treating
`refuted: true` as "not a defect" would have shipped four broken commands.

**Rule:** Separate a wrong target from a wrong claim. When a verifier refutes on attribution and
says where the text actually lives, re-file the finding against that file and apply it. Only a
refutation that attacks the claim itself removes work from the list.

## A guide that promises a specific observable failure has to reproduce it

**Pattern:** The spec-driven lab taught that ignoring "money is never a float" shows up as a total
of `239.99999999999997`. It cannot. Every figure in the brief is exactly representable in binary,
so a float implementation returns `240.0` and `45.0` and passes the lab's own verification table.
The promised catch could never fire, and the generated reference solution repeated the same
fabricated number back into its own plan.

**Rule:** Run the failing case before writing the failure into a guide. If the defect is invisible
in the output, say where it IS visible (here, a plan naming the type) rather than inventing an
output that would make it visible.

## A changelog shows deltas; only the docs show the current model

**Pattern:** `demos/06-copilot-app` was written against Copilot app v1.1.14, when the product had
a marketing page and a `github/app` changelog and nothing else. By September 2026 GitHub had
published eight official pages under `docs.github.com/en/copilot/how-tos/github-copilot-app/`.
Refreshing from the changelog alone would have caught every new feature and still left the module
wrong: it taught Autopilot as a *permission* mode, which is a defensible reading of release notes
that mention Autopilot and permission prompts in the same entries, and is flatly wrong against the
docs, where Interactive, Plan and Autopilot are session modes orthogonal to
`/permissions manual|assisted|allow-all`.

**Rule:** When refreshing a module about a fast-moving product, first re-check whether official
docs now exist for it, then read the docs for the model and the changelog for the deltas. A
product that was changelog-only when the module was authored is exactly the one that grows a docs
surface later, so the absence of docs is a fact with an expiry date, not a standing condition.
A conflation like this one survives every review that compares the module against the changelog it
was built from.

## Internal link checking says nothing about external links

**Pattern:** `create-class/scripts/link-check.sh` skips `http(s)` targets by design, so it reports
a clean tree while a documentation URL 404s. Two shipped topic readmes in this module linked
`docs.github.com/en/copilot/concepts/agents/agent-skills`, which had moved to
`.../concepts/agents/about-agent-skills`. It was found only because this pass curled every
external URL in the files it touched, including the ones it had not added.

**Rule:** External links rot on the vendor's schedule, not the repo's, so a course that cites
official docs needs a periodic HTTP check that internal link checking cannot provide. Check every
external URL in a file you touch, not only the ones you wrote:
`bash ~/.claude/skills/create-class/scripts/link-rot.sh --scope demos/<module>`.

## Re-reading a persisted tool result through Bash persists it again

**Pattern:** `cat` of six topic readmes produced 29KB, which the harness saved to a
`tool-results/*.txt` file and showed as a 2KB preview. Running `sed -n '1,400p'` on that saved
file to read the rest produced another 29KB, which was saved to a second file with the same
preview. Two calls, no new information.

**Rule:** A persisted tool result is not readable by piping it back through Bash, because the
output limit applies to the new call as well. Read it with the Read tool, or go back to the
source and read the files one at a time.

## The working tree is the agent's draft, not the baseline you handed it

**Pattern:** lab03 reported building "after retargeting all 3 csproj to net10.0". I greped the
scratchpad clone I had handed it, read `net10.0`, and sent a correction telling it the clone
already said that and its report was wrong. It was not: `git show HEAD:...csproj` reads `net8.0`,
the guide tells the reader to update to .NET 10, and what I had greped was the agent's own
uncommitted `sed -i`. My read crossed its write.

**Rule:** In a repository an agent is editing, the working tree is its draft. When challenging a
claim about the baseline, read `git show HEAD:<path>`, and when challenging what it changed, read
`git diff`. Phrase the re-send as a claim about your own evidence ("as of my grep a minute ago X
was still Y, confirm or apply") so it can be refuted for free.

## Fixing a defect silently falsifies every document that describes it

**Pattern:** lab 07's guide carried a "Known repository defect" blockquote and a troubleshooting
row telling students that `npm test` in `src/food-app/food-shop` fails on a clean checkout, and its
solution's `test-results.md` recorded that FAIL baseline with two named failing specs. All of it
was accurate when written. The moment the suite was repaired, every word of it became false, and
nothing in the repair touched those files or could have flagged them.

**Rule:** A defect that was worth documenting is a defect whose fix has a documentation blast
radius. After fixing one, grep for prose describing it, not just for code depending on it, and fix
the description in the same run. Warnings, troubleshooting rows and recorded baselines are the
three shapes it hides in.

## core.longpaths fixes git, not MSBuild

**Pattern:** Two agents independently hit Windows `MAX_PATH` on the same day from deep scratchpad
clones: `MSB3030` on a file copy in lab 03, and the Blazor webcil step in lab 06. Both clones had
`core.longpaths=true` set, which is why the clone and checkout had succeeded in the first place and
why the failure looked unrelated to path length.

**Rule:** `core.longpaths=true` is a git setting and covers git operations only. MSBuild's copy
task uses the Win32 APIs and still stops at 260 characters, so a .NET build under a deep temp path
fails with a path error that never mentions paths. Build from a short root, or redirect the output
path there, and do not read a successful clone as evidence that the path is workable.

## A Windows path through a quoted heredoc is literal; through a Python string it is not

**Pattern:** Writing the text `cd labs\01\03-assisted-coding` into a review file via
`python - <<'PY'` produced `cd labs` followed by two control characters. The quoted heredoc passed
the backslashes through intact, and Python then read them as the escapes `\01` and `\03`. The file
was written successfully, the script printed its success line, and the corruption was invisible
until `cat -A`.

**Rule:** A quoted heredoc protects a string from the shell, not from the interpreter reading it.
Never embed a Windows path in a Python literal inside one: build the separator with `chr(92)`, use a
raw string, or write the text with a tool that does no escape processing. Read the line back after
writing it; a success message says the write happened, not that it wrote what you meant.

## A locked file on Windows names the process through its loaded modules

**Pattern:** Removing the lab 02 venv failed on `venv/Scripts/uvicorn.exe` with "Device or resource
busy" after everything else in the tree had already been deleted. No `uvicorn` process existed, and
the holder turned out to be a bare `python.exe` running `multiprocessing.spawn` whose parent was
already gone: the orphaned reloader child of `uvicorn --reload`, invisible to any search by name or
command line.

**Rule:** When a delete fails on a busy file, find the holder by its loaded modules rather than its
name: `Get-Process | ForEach-Object { $_.Modules | Where-Object FileName -like "*<path fragment>*" }`.
A process that loaded a DLL from the tree is holding it whatever it is called. Any lab that runs a
dev server with a reloader leaves one of these behind.

## A fan-out contract has to name how the new artifact is reached

**Pattern:** Seven parallel agents were briefed to create a `<name>-solution/` folder per lab with a
`test-results.md` inside. Every one of them did exactly that, and not one linked the folder from its
lab guide, because the brief never said to. Correcting it afterwards cost a round trip with each of
the five agents still running, every one of them crossing its report in flight.

**Rule:** Fix the whole contract before fanning out, and "what points at this" is part of it, not a
detail. An omission in one brief is one correction; the same omission in N parallel briefs is N
corrections that all arrive mid-report. When drafting a fan-out brief, walk the new artifact from a
cold reader's entry point and name whatever they would have to already know to find it.

## A reply that hands a step back to the user carries the whole dialog

**Pattern:** Asked to configure BYOK models in the GitHub Copilot desktop app, I found the API key
can only be typed into the app UI, wrote the full field mapping into the reference document, and
ended the reply with the base URLs in prose plus "Want me to?". The next message was a screenshot of
the Add provider dialog and "what do i enter here", and the one after that asked again for the
models that had already been authorized two turns earlier.

**Rule:** When part of an authorized task can only be done by the user in a UI, the reply carries
every field of that screen with its value, not a pointer to a file that describes them, and it never
closes with an offer to do work already asked for. Name the one step that is theirs, hand over the
values, and state what happens next without a question mark.

## An app with no config file keeps its config in a database

**Pattern:** Looking for the Copilot desktop app's BYOK providers, `~/.copilot/settings.json`,
`%APPDATA%\com.github.githubapp` and the install folder all came up empty, which reads as "this app
is UI-only". The providers were in `~/.copilot/data.db`, a SQLite file sitting in the same directory
already searched, in tables `model_providers` and `provider_models`.

**Rule:** Before concluding a desktop app keeps something only behind its UI, enumerate the `.db`
files in its data directory and list their tables. Electron and Tauri apps put structured state in
SQLite and leave JSON for preferences, so an empty JSON search is evidence about JSON, not about the
app. Grep the binary for the table name afterwards to recover the schema and its CHECK constraints.

## A guide is unrunnable in ways no reading finds

**Pattern:** Asked to build the missing `*-solution` folders for `demos/05-cli-sdk/02-sdk`, I wrote
the guides' code out verbatim first and ran it. Four blockers surfaced in one topic, none of which a
careful reader would catch: a custom tool call is denied unless the tool sets `skipPermission` or the
session supplies `onPermissionRequest`, and the agent then reports it could not reach the service, so
the symptom points at the handler rather than at permissions; an unannotated destructured handler
parameter does not compile because `defineTool` defaults its type parameter to `unknown`; a recursive
`rl.question` loop dies with `ERR_USE_AFTER_CLOSE` at end of input; and the runtime's built-in tools
shadow custom ones, so the model called the built-in file reader instead of the tool the demo exists
to demonstrate.

**Rule:** Write the guide's code exactly as printed before improving it, then typecheck and run. `tsx`
does not typecheck, so ship a `tsconfig.json` and run `tsc --noEmit` as its own step: two of those four
were compiler-visible and runtime-invisible. A demo whose lesson is "the agent calls your tool" must
scope the session with `availableTools: ["custom:*"]`, or the lesson is not what the run demonstrates.

## The most confident sentence in a guide is the one to check first

**Pattern:** `03-deploy-azure` opened with "The hosting library handles the protocol, the HTTP server,
health checks, and request and response schemas" and gave three environment variables for
bring-your-own-model. Neither exists. There is no hosting library: you write your own HTTP server and
either let the client spawn the runtime or attach to `copilot --headless` with
`RuntimeConnection.forUri`. Bring-your-own-model is the session's `provider` object, and you choose
the secret variable names yourself. Both claims read as settled fact and had no syntax shown anywhere.

**Rule:** Prose that names a mechanism without ever showing its real syntax is the shape a fabricated
feature takes. Check every such sentence against the installed type definitions and the vendor docs
before writing a line of solution code, because the solution inherits the error otherwise.

## Validate a manifest against its own published schema, never against its example

**Pattern:** The `06-plugins` guide's `plugin.json` declared `skills`, `mcpServers` and a top-level
`com.github.copilot`. Fetching `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` showed it
requires `$schema`, sets `additionalProperties` to false, and permits exactly ten keys, none of them
those three. The example failed validation with two errors. Components are discovered by convention
instead: `skills/`, `mcp.json`, and a `com.github.copilot/` directory.

**Rule:** When a format publishes a schema, fetch it and run a validator; the prose and the examples
both drift from it. Real manifests from the vendor's own marketplace settle what the namespace is
actually used for, which here was metadata such as a logo path, not component lists.

## Verify that a plugin loads, do not verify that its files exist

**Pattern:** `chat.pluginLocations` is a VS Code setting, which looked like it made loading
unverifiable from a terminal. The SDK's session takes `pluginDirectories`, and `session.rpc` exposes
`plugins.list`, `agent.list` and `mcp.list`. Pointing a session at the new plugin returned
`demo-quality` enabled, the agent as `demo-quality:demo-reviewer` sourced from
`com.github.copilot/agents/`, and the MCP server as `topic-index | connected | plugin`. That proved
the directory conventions rather than assuming them.

**Rule:** Before labelling a GUI-only step unverifiable, enumerate the SDK session options and the
`session.rpc` namespaces for a programmatic equivalent. Report honestly what stayed unproven: skill
discovery returned zero skills through that path, which is a limit of the probe and not evidence
about the plugin.

## Bash heredocs are not a reliable way to write a file with quotes in it

**Pattern:** Writing the plugins guide with `cat > file <<'EOF'` failed twice with "unexpected EOF
while looking for matching quote", and an earlier PowerShell heredoc silently turned `'\'` into
`'\'`, producing "The regular expression pattern \ is not valid" at runtime rather than at write
time. The same content went in cleanly through the Write tool.

**Rule:** Content carrying quotes, backslashes or JSON goes through the Write tool, not a heredoc.
The silent variant is the dangerous one: a mangled escape writes successfully and fails later
somewhere that looks unrelated. Test a script that parses stdin by writing its payload to a file
with a JSON serializer, because an inline Windows path in an echoed JSON string loses its
backslashes and the script then correctly does nothing, which looks exactly like a passing check.

## An empty result from an external CLI is a claim about that invocation, not about the tool

**Pattern:** `copilot --help`, `copilot help` and `copilot -h` each returned nothing three times in a
row, in Git Bash and in PowerShell. I concluded the CLI suppresses help when stdout is not a TTY,
wrote that into a solution readme and the task log, told the user, and told a subagent it therefore
had no way to verify CLI flags from help output. The subagent came back saying it had read the
`--fleet` entry out of `copilot --help`, and it was right: the same command emits 13527 bytes when
redirected to a file, piped to `wc -c`, or piped to `head -5`. The early emptiness was transient,
most likely a first-run or update check.

**Rule:** Before turning an empty result into a statement about a tool, probe it a second time with a
different consumer (a file redirect as well as a pipe) and print the byte count rather than eyeballing
the output. Never hand a subagent a negative capability claim as an established fact in its brief:
that one propagated into the brief, into a readme and into a reply before the delegate falsified it.
The related rule about an empty search result already existed and did not fire here, because this
looked like a tool behaviour rather than a failed search.

## Counts given to a delegate as facts are exactly what it will not re-check

**Pattern:** My brief stated `.github/prompts/` has 9 files and `.github/skills/` has 24 skills, both
from `ls -1 | wc -l`. Both were wrong: each directory contains a `readme.md`, so the real numbers are
8 prompt files and 22 skills with a `SKILL.md`. The delegate measured them itself, used the correct
values, and flagged the discrepancy. Had it trusted the brief, two wrong counts would have shipped
into a teaching guide as verified facts.

**Rule:** Count what you actually mean. `ls | wc -l` counts directory entries, not artifacts of a
type, so use `find -name '<pattern>' -type f | wc -l` when the number will be written down. Tell a
delegate to re-measure anything numeric even when the brief supplies it, and treat a delegate that
corrects your facts as the run working rather than as noise.

## A harness layout is a fact on disk, not something to derive from a schema

**Pattern:** Asked to build the `02-mcp-skills` solution folder, I guessed the Copilot harness layout
four times: `.mcp.json` at the folder root, then an Agent Plugin with `plugin.json` and `mcp.json` at
its root, then `.github/plugin/plugin.json` plus `.mcp.json` copied from the installed `workiq`
plugin, then `.github/mcp.json`. Each guess had a plausible source, and `workiq` was the worst of them
because it ships `.claude-plugin/` and `.codex-plugin/` too, so its `.mcp.json` is another agent's
convention wearing a Copilot plugin's clothes. The owner had to say "gh copilot does not use
.mcp.json" twice before I stopped. The answer was sitting in this repository the whole time:
`.github/skills/`, `.github/agents/`, `.github/instructions/`, `.github/prompts/`, `.github/hooks/`
and `.vscode/mcp.json`, whose top-level key is `servers`, not `mcpServers`.

**Rule:** When a demo must reproduce a product's harness, read the harness this repository already
runs before reading any schema, any vendor doc, or any installed third-party package. A repo that
uses the product daily is primary evidence; a package that targets three agents at once is not.
`copilot mcp --help` listing `.mcp.json` as a workspace source did not make it true, and four
executed probes all failed to surface a server from a file, which was the signal to stop and look
rather than to try a fifth path. The answer was in this course, one module away:
`demos/02-agentic-harness/03-mcp/01-basics/readme.md` line 35 names `.vscode/mcp.json` in the
workspace root. I was editing a sibling module and never opened the topic called "MCP basics".

## The CLI and the editor do not share an MCP registry

**Pattern:** I read `.vscode/mcp.json` as "the repo's MCP config" and expected `copilot mcp list` to
show its servers. It never does. The CLI reads `~/.copilot/mcp-config.json`, which is what
`copilot mcp add` writes; VS Code reads `.vscode/mcp.json`. Skills, agents, instructions and prompts
under `.github/` are shared by both hosts. MCP servers are not, and that asymmetry is the actual
lesson of this topic.

**Rule:** State which host reads a config file before teaching it. A server checked into
`.vscode/mcp.json` reaches every teammate who opens the repo in the editor and nobody on the command
line, so a class that teaches one and demonstrates the other teaches a bug.

## Do not write into a folder a subagent is still working in

**Pattern:** `sdk-multiagent` went idle and its report never arrived, so I read its deliverables off
disk, found the solution readme had no verified-versus-not-executed table, and wrote one myself with
my own evidence. Its report then arrived: it had replaced my rows, correctly, because it could not
vouch for evidence it had not produced, and it asked who had written them since they read as its own.
Two of my three rows were real observations, one was a wrong inference, and none of that was the
problem. The problem was two writers in one folder.

**Rule:** Reading a delegate's output on disk is always allowed; writing into its working folder is
not, until it has reported or been stopped. When a report is missing, ask for it or stop the agent
first. My own delegation rules already said "stop the agent before editing the files yourself", and
it did not fire because the trigger felt like absence of information rather than a live conflict.

## An idle notice is not the absence of a report, it is the absence of a report YET

**Pattern:** Both delegates showed `idle` in `ListAgents` with nothing delivered. I treated that as
"finished, report lost", verified their work myself, wrote a reply to the user, and then both full
reports arrived afterwards carrying evidence stronger than mine, including two corrections to facts
I had asserted.

**Rule:** Idle plus no report means wait or ask, not substitute. Verifying the deliverables on disk
is the right first move and it does not license replacing the delegate's evidence with your own.
When a reply to the user is due before the report lands, say the report is outstanding rather than
presenting your own spot-checks as the final account.

## A blocker inside the user's security product is a hand-back, not a retry

**Pattern:** The Copilot CLI would not run, so I spent roughly fifteen tool calls on installs,
reinstalls, `--force`, the platform optional dependency, and a direct launch of the binary. The user
interrupted twice, the second time with "what the fuck are you doing?". Everything needed to stop
was visible by the second attempt: the 150 MB exe existed and then did not, the direct launch said
`Access is denied` rather than naming a missing dependency, and `Add-MpPreference` failed with
`0x800106ba`, which means Defender is off because another product owns the machine. It was
Kaspersky deleting the binary on sight.

**Rule:** Diagnose an endpoint-protection blocker once, then hand it over. Name the product with
`Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct`, list every path
needing an exclusion, give the exact reinstall command and its ORDER, and stop. Expect the exclusion
list to be wrong the first time, because a CLI unpacks its runtime somewhere other than where npm
put it: three separate roots needed excluding here and each surfaced only after the previous was
cleared. Say up front which error means one is still missing. Related and separate: `npm install -g`
silently skipped the platform optional dependency, and installing the platform package first and the
parent second prunes it again, so the order is part of the instruction.

## An empty MCP search is a broken server, not an empty corpus

**Pattern:** Told to use the MS Learn MCP to settle a question, its `search` returned
`{"results":[]}` for every query including a certain-hit control (`Azure Storage GRS RPO`), while
`fetch` on a known URL returned the full page. Had I read the empty results as an answer, I would
have reported that Microsoft documents nothing about the topic.

**Rule:** Probe a search tool with a query you know must hit before believing any empty result, and
probe a second verb on the same server before blaming the server. Then ask whether the source could
answer at all: MS Learn does not document GitHub products, so it was the wrong source for a Copilot
CLI question no matter which verb worked.

## The repo's own validator agent existed and went unused

**Pattern:** I wrote and rewrote two demo guides entirely on the main thread. `.claude/agents/`
carries `guide-validator`, described as "Validates and fixes a single demo or lab guide against the
brand-voice and create-guide rules ... Invoke once per file", which is exactly the work I did by
hand across several passes.

The same thing happened with a script. I hand-rolled a relative-link checker twice, as
`grep -o '](\.[^)]*)' | sed | test -e`, and got it wrong the first time by leaving the trailing
paren on. `create-class/scripts/link-check.sh` already resolves every internal link in a tree and
prints an assertable summary; run properly afterwards it reported `files=20 links=48 broken=0`.

**Rule:** List `.claude/agents/` and the active skill's `scripts/` before starting, not after. A
guide rewrite is one `guide-validator` invocation per file, and a link check is one `link-check.sh`
run. The global delegation rule already says the roster on disk is the roster, and the skill already
ships the script, but neither fires unless the directory and the scripts folder are actually opened
at the start of the task. A hand-rolled check is also an untested check: mine had a bug that a
shipped script did not.

## The pre-flight inventory rule did not hold, and hand-rolled checks replaced shipped scripts again

**Pattern:** The entry directly above this one was written to stop exactly this, and one session later
every half of it repeated. `create-class` was invoked through `/create-class`, so its scripts folder
was one `ls` away. `probe-cli-surface.sh` exists to snapshot a CLI's version and `--help` so a guide
can be diffed against it, which is verbatim the task; I hand-rolled `gh aw --help` and eyeballed the
command table against it. `link-rot.sh` exists and the master's own cross-cutting rules name it by
command; I wrote a `curl -o /dev/null -w "%{http_code}"` loop instead. `.claude/agents/` carries
`guide-validator`, described as validating a single guide against the brand-voice rules; I checked em
dashes, counted `> Note:` callouts and ran the fence check by hand, and only caught the callout-cap
breach after writing the note that broke it.

One rule did fire: `fence-lang.py`, because the cross-cutting rule spells out the command to run
rather than describing the capability. The rules that named a command got run; the rules that named
a capability got re-implemented from scratch.

**Rule:** A lessons entry is not a fix. Nothing loads `tasks/lessons.md`, so a rule written only
there cannot fire, and writing the same rule a second time will not make it fire either. Put it where
the harness reads it: the skill's own cross-cutting rules, as an imperative naming the exact command.
When a rule names a shipped script, run that script rather than something equivalent, because the
hand-rolled version is also the untested version. And when a task is "verify a guide", the first two
commands are `ls .claude/agents/` and `ls <active-skill>/scripts/`, before any work.

## A vendor's own migration tool reports clean while the product rejects the file

**Pattern:** After upgrading `gh aw` from v0.84.3 to v0.88.8, `gh aw fix` (the codemod pass that
exists to repair deprecated fields) printed `✓ No workflow fixes needed`. `gh aw validate` on the
same tree then failed with `Unknown property: chrome-devtools`: the release had retired the
`chrome-devtools: {}` shorthand under `tools:` in favour of a separate `mcp-servers:` key, and the
vendor's own codemod did not cover its own breaking change. Reading the codemod as the upgrade
receipt would have shipped a workflow that cannot compile.

The same CLI then disagreed with itself. `gh aw compile` accepted `schedule: daily on weekdays` and
scattered it into `cron: "38 22 * * 1-5"`, while `gh aw mcp inspect` rejected the identical file with
`fuzzy cron expression requires a workflow identifier`.

**Rule:** The migration tool is a claim; the validator is the evidence. After any upgrade run the
command that REJECTS bad input, never the one that offers to fix it, and treat a clean codemod as
untested. Then run every command the guide actually tells a learner to run, because "it compiles" is
a statement about one subcommand, not about the CLI.

## Write to a path without checking it exists and you silently destroy what was there

**Pattern:** I harvested a procedure into `~/.claude/skills/claude-learn/scripts/fix-skill-frontmatter.py`
with the Write tool. A proven script authored in another repo's session was already at that exact path,
and Write replaced it with no warning, no diff and no prompt, because the file was not in my context.
I only noticed when the harvest registry already had a row for the procedure, describing capabilities my
version did not have.

**Rule:** Before Write, check whether the path exists, and if it does, read it and Edit instead. A Write
to an unread path is an overwrite waiting to happen, and outside a git repo there is nothing to diff
against afterwards. The tell that it already went wrong: an index, registry or doc that documents the
thing you think you just created.

## "Not a git repo" does not mean "no backup"

**Pattern:** Having overwritten that file, I checked `git rev-parse` in `~/.claude`, found no repository,
searched once for copies, and concluded it was unrecoverable. A peer session reached the same conclusion
independently. Eight intact copies existed: four timestamped snapshots under
`~/.claude/skills/.skill-sync-backups/<skill>/<YYYYMMDD-HHMMSS>/`, written by the sync procedure we are
both supposed to run, and four more in repo-local copies of the same skill in other repos.

**Rule:** Enumerate the recovery paths before declaring a loss: the sync snapshot directories, every
repo-local copy of that skill on disk, then `Write` tool inputs in the session transcripts under
`~/.claude/projects/`, which record file contents verbatim. Absence of version control is not absence of
copies, and a mechanism documented in the very skill you are editing is the one you are most likely to
forget exists.

## Grepping for a behaviour is not testing it

**Pattern:** A peer recovered that script and vouched for all four of its documented behaviours, having
confirmed each was present in the source and that the file compiled. The first fixture I ran against it
found a corrupting bug: when `description:` is the last frontmatter key, the continuation scan eats the
trailing blank line and the closing `---` is joined onto the folded value, destroying the frontmatter
boundary and the body. It printed `1 repaired` while doing it. The peer's own words afterwards:
"presence is not behaviour, and the one case I did not construct is the one that breaks it."

**Rule:** A behaviour is verified by a fixture that exercises it, never by a grep proving the code for it
exists. Construct the boundary case specifically: first element, last element, empty, one item. For a
script that rewrites files, the last-key and only-key cases are where the off-by-one lives, and a script
that reports success while corrupting its input is worse than one that crashes.

## Slide photography shows the class topic, modern and bright

**Pattern:** Nano Banana prompts for the module 02 deck were written as abstract metaphors (climbing
harness, letterpress stamps, canal locks, a dusty binder in a server room) with dusk light and weathered,
retro settings. The user rejected them twice: first as unrelated to the class, then as "70ies and 80ies
sceneries, dark and dirty".

**Rule:** Photos for this class show software engineers and their work, each scene carrying the slide's
idea. Default register is modern, light, bright and friendly: high-key daylight, white and light-oak 2020s
interiors, pastel accents, plants, screens as soft blurred colour. Add "dark or moody lighting, vintage or
retro decor, grime" to the Avoid list.
