# Verify by Execution

Audit a course's guides by EXECUTING them, not by reading them. Use this when the job is
"verify the labs", "check every guide still works", "audit the course before delivery", or when a
guide ships commands, scripts, config files, or a harness the learner is told to build.

`run-demo.md` prepares and runs one runnable project. `run-guide-browser.md` drives a guide through
a live UI. This leaf owns the layer above both: the classes of defect that execution finds and
review never does, the cheap techniques that make execution affordable, and the honesty rules for
what may be reported as verified.

## Guiding principle

A guide can be internally consistent, well written, brand-voice clean, and still be unrunnable.
Every defect class below was found by running a course's guides end to end, and none of them is
visible to a careful reader. One such pass over 29 lab guides produced 270 findings, 41 of them
blockers, in a repo that had already been reviewed as prose.

Treat "the guide is unchanged since it last worked" as no evidence at all. CLIs rename flags,
frontmatter schemas drop keys, doc hosts move, and SDKs advance underneath a file nobody edited.

## The defect taxonomy

| # | Class | What it looks like | The check |
|---|---|---|---|
| 1 | Invented CLI surface | A command or flag that reads exactly right and does not exist | Every command and flag against `--help` and vendor docs |
| 2 | Unsupported frontmatter | A key the runtime ignores in silence | Every key against the documented field list |
| 3 | Variadic flag eats the positional | The prompt is parsed as another value of the preceding flag | Never put a variadic flag last before a positional |
| 4 | Manifest in the wrong place | The thing never loads and nothing errors | Path of every manifest against the documented location |
| 5 | Exit code lost to a subshell | A gate that can never fail | Run the gate against known-bad input, assert non-zero |
| 6 | Command substitution in a quoted string | CI executes an example instead of quoting it | Grep workflow heredocs for backticks and `$(...)` |
| 7 | Platform assumptions | POSIX-only commands handed to a Windows audience | Classify each: git-bash, needs WSL, or fails |
| 8 | Stale build output | A broken build path masked by a leftover artifact | Verify the starter from a clean copy |
| 9 | Wrong working directory | A harness built where the session cannot discover it | Confirm the launch directory owns the config |
| 10 | Starter ships the deliverable | The learner builds what already exists | `diff -rq <starter> <starter>-solution` |
| 11 | Guide ignores its own starter | Setup scaffolds from scratch beside a shipped project | Every Setup block against the topic folder listing |
| 12 | Fabricated mechanism in teaching prose | A whole feature that does not exist, taught confidently | Every named mechanism against the live vendor docs |
| 13 | Silent-ignore behaviour | Config that parses, never applies, and never errors loudly | Read the startup output, not just the end result |

### 1. Invented CLI surface that looks right

The most expensive defect, because it is the most plausible. Real examples from one pass:
`/plugin reload` where the real command is `/reload-plugins`; `ant whoami` where the real command
is `ant auth status`; `specify init --integration claude` where the real flag is `--ai`. Each reads
like something the tool would obviously support, which is exactly why nobody questioned it.

Check every command and every flag against `--help` output and the vendor documentation, including
the ones that feel too obvious to check. A guide is allowed to use only surfaces that were observed
to exist.

### 2. Unsupported frontmatter that fails silently

`permissions:` with allow and deny lists on a subagent, and `env:` with `inherit` or `pass` for
scoped secrets, are not supported keys. The runtime ignores them without complaint, so the learner
ships a security control that is decoration. Nothing errors, the lab "passes", and the lesson taught
is false.

Validate every frontmatter key in every guide against the documented field list for that artifact
type (agent, skill, command, plugin, hook). An unsupported key is a blocker, not a nit, because the
guide is teaching a capability the product does not have.

### 3. A variadic flag eating the positional argument

`claude -p --add-dir <dir> "prompt"` parses the prompt as a second directory and fails with
`Input must be provided`. The same shape bites `--allowed-tools` and any other flag that accepts a
list. The rule is mechanical: never put a variadic flag last before a positional argument.

```bash
claude -p "prompt" --add-dir ../shared
```

### 4. Manifest in the wrong location

A `plugin.json` at the plugin root instead of `.claude-plugin/plugin.json` means the plugin never
loads, and the failure mode is silence. The learner sees no plugin, no error, and no way to tell
which of the two they got wrong. Check the documented path for every manifest the guide creates.

### 5. Exit codes lost to a subshell

A variable assigned inside a piped `while read` loop lives in a subshell and is discarded when that
subshell exits. A CI gate written this way always exits 0 and can never fail a pull request, which
is the exact opposite of the lesson.

```bash
fail=0
while read -r line; do
  case "$line" in *ERROR*) fail=1 ;; esac
done < <(run_checks)
exit "$fail"
```

Prove a gate by running it against known-bad input and asserting a non-zero exit. A gate that was
only observed passing was not tested.

### 6. Command substitution inside a double-quoted YAML string

Backticks (or `$(...)`) around an example command in a workflow heredoc make the CI runner execute
that command while building the prompt string. The job then fails, or worse, succeeds with a prompt
containing shell output. Use single-quoted heredocs (`<<'EOF'`) and grep every workflow for
backticks inside double-quoted strings.

### 7. Platform assumptions

`crontab`, `nohup`, `xargs -P`, a bare `export VAR=`, `chmod +x`, and `PORT=x cmd` are all fine on
Linux and all questionable in front of a Windows-primary audience. Classify each command in the
guide into one of three buckets and say which in the prose:

| Bucket | Meaning | Guide action |
|---|---|---|
| Works in git-bash | Runs as written on Windows under Git Bash | Ship as is |
| Needs WSL | Requires a real Linux userspace or a scheduler | Say so, give the WSL entry point |
| Fails | No Windows equivalent in this form | Replace with the PowerShell form |

`zip` is the recurring example of the third bucket: it is not on PATH in Git Bash and exits 127.
Use `powershell Compress-Archive`, then verify by unpacking the archive.

`printf` belongs to the same bucket and hides in Setup blocks, where it is used to type a file into
existence. It does not exist in PowerShell. The fix is not a PowerShell twin, it is to ship the
file in the starter so no shell command is needed at all: see "Setup is one command" in
`create-guide.md`. The same reasoning retires most `cp -r`, `rm -rf`, `mkdir`, and `ls -a` from
guides, leaving `git`, `cd`, and the vendor CLI, which are identical in both shells.

### 8. Stale build output masking a broken build path

A leftover `dist/` makes `node dist/index.js` succeed locally while the documented build cannot
complete because a toolchain is missing. The starter looks verified and is not. Verify every starter
from a clean copy, with build output and dependency trees removed, exactly as the learner clones it.

### 9. Skill and harness discovery is project-scoped

`CLAUDE.md`, `.claude/settings.json` hooks, `.claude/agents/`, `.claude/skills/`, `.claude/commands/`
and `.mcp.json` load from the directory the session was launched in. A guide that builds a harness in
one folder while the learner is sitting in another produces no hook, no skill, and no error.

Every guide that creates harness config states the working directory explicitly, and every
verification step confirms discovery (the skill appears, the hook fires) rather than confirming the
file exists on disk.

### 10. The starter already contains the deliverable

A demo whose Part A says "write the policy-gate hook" beside a starter that ships `policy-gate.sh`
teaches nothing, and the guide reads perfectly. It usually enters the repo when someone copies the
solution folder to create the starter, or when one demo's finished state is reused as the next
demo's input.

Audit the whole tree in one pass and rank by fewest differences; a starter/solution pair that
differs by one file is almost always this bug:

```bash
for sol in $(find demos -maxdepth 4 -type d -name "*-solution"); do
  st="${sol%-solution}"
  [ -d "$st" ] || { echo "ORPHAN (no starter): $sol"; continue; }
  echo "$(diff -rq "$st" "$sol" | wc -l) diffs | $st"
done
```

Two adjacent findings fall out of the same sweep: a `-solution` folder with no starter beside it,
and a folder serving as both an earlier demo's solution and a later demo's starter.

### 11. The guide ignores the starter shipped beside it

`mkdir cli-utils && cd cli-utils && claude` in a topic folder that already contains a complete
`cli-utils` project. The learner spends the first third of the demo having the model re-create
shipped assets, and the shipped assets rot because nobody runs them.

Read every Setup block against the actual topic folder listing. The related shapes are a Setup that
copies from a sibling topic, and one that presents live scaffolding as the primary path with the
starter mentioned only in the intro. Scaffolding-live is a legitimate classroom option; it belongs
under an explicit "Optional: scaffold it live instead" heading, never as the default path.

### 12. A fabricated mechanism taught as fact

Worse than an invented command, because it is a whole feature. One course readme taught permission
policy through `include` and `exclude` settings in `CLAUDE.md`, complete with a copy-paste template
and `/include` and `/exclude` slash commands. None of it exists. The real mechanism lives in a
different file with different syntax, and the demo built on top of it inherited the error.

Class 1 checks commands. This checks the concept: for every mechanism a readme names, confirm
against the live vendor docs that it exists, lives where the prose says, and is enforced the way
the prose claims. The highest-risk sentences are the ones that sound most reasonable, and the tell
is prose that explains a mechanism without ever showing its real syntax.

### 13. Configuration that is silently ignored

Distinct from class 2 (an unsupported key) because here the key is supported and still does
nothing. Both examples below were invisible until a real run:

- Project `allow` rules are ignored entirely until the workspace is trusted. The policy looks
  inert, the rules are syntactically perfect, and a startup line nobody reads says why.
- A path rule written for a tool the file checks never consult parses fine, protects nothing, and
  emits a startup warning that scrolls past before the prompt appears.

Verify by reading the FIRST lines a session prints, not the last. Capture startup output
deliberately and treat any warning there as a finding, then re-run to confirm a clean start.

### 14. A real flag whose enforcement runs the other way

Distinct from class 12, where the mechanism was invented outright. Here the flag exists, the syntax
is right, and only the direction is inverted. One course readme taught that limiting a run to
`--allowed-tools "Read,Glob,Grep"` "prevents any write operation no matter what the prompt says";
the flag is an allow list that waives permission prompts and removes nothing, and the restrictive
flag is `--tools`, which the module never mentioned. Three topics and two shipped scripts were built
on the inverted claim.

Enforcement claims fail open, which is what makes them the highest-value thing to execute: the
wrongly-scoped run still returns a correct-looking answer and nothing errors. Verify one by asking
the agent to do the forbidden thing and then checking the filesystem, never by reasoning from the
flag's name. When the vendor docs describe a flag, read the clause saying what it is *not* for; here
the answer was one line under the very flag the readme cited, naming the other flag.

### Script and setup defects that recur

These belong to the same family and are worth a dedicated pass over any guide that ships a script:

- Command substitution missing, so a `grep` runs against an empty string and the gate always passes.
- A hook script that never blocks: feed it the real stdin payload and assert the exit code (exit 2
  blocks).
- Steps that depend on git history in a course repo that already has it. The course repo IS a git
  repo, so a demo needing branches or worktrees uses it directly: no `git init`, no copy out to a
  scratch directory, no nested repo. Gitignore `.claude/worktrees/`, and have the guide review and
  discard rather than merge into the default branch.
- `git clean -fd` refusing to remove anything that is its own repository. It prints
  `Skipping repository` and exits 0, so a cleanup step that was never checked leaves worktrees
  behind. `-ff` is required, and it still will not delete a nested `.git`.
- Docs links to `docs.anthropic.com/en/docs/agents-and-tools/claude-code/*`, which now 404. The
  current host is `code.claude.com/docs/en/*`.
- A table titled "slash commands" that actually lists `claude -p` shell invocations.
- A scoping fix that silently rebudgets the run. Restricting the tool set also removes the shell, so
  an audit that used to read a project in a few calls now spends a turn per file and blows an
  unchanged `--max-turns`, exiting indeterminate instead of gating. A permission change is also a
  performance change: re-run every artifact that consumes a flag you changed, and treat the numbers
  around it (`--max-turns`, timeouts, retries) as calibrated against the old tool set.

## Verification techniques

### Stub the model, not the script

Put a stub `claude` earlier on `PATH` that writes a sentinel and exits with a chosen code. That
proves exit-code propagation, sentinel tokens, JSON parsing, backgrounding and polling at zero model
cost, and it proves them deterministically, which a live model never does.

```bash
mkdir -p /tmp/stub
cat > /tmp/stub/claude <<'EOF'
#!/usr/bin/env bash
echo '{"type":"result","subtype":"success","result":"STUB_OK"}'
exit 0
EOF
chmod +x /tmp/stub/claude
export PATH="$(cygpath -u /tmp/stub):$PATH"
which claude
```

On Windows Git Bash, convert the path with `cygpath -u` and then assert that `which claude` resolves
to the stub. A Windows-style path prepended to `PATH` silently no-ops, the real binary is found, and
a billed live call runs while you believe you are testing plumbing. This failure is silent and
expensive when the script backgrounds its agents: the live calls run in parallel and the log is the
only place the substitution shows up, after the money is spent.

Skip `PATH` entirely when the script under test runs under `bash`. An exported shell function cannot
be outranked by path resolution, so it needs no `cygpath` and no `which` assertion:

```bash
claude() {
  echo '{"type":"result","subtype":"success","result":"STUB_OK"}'
  return 0
}
export -f claude
bash scripts/run.sh
```

Read the stub's arguments positionally with care: a script calling `claude -p "$PROMPT" --max-turns 8`
puts `-p` in `$1`, so a stub that branches on `$1` branches on the flag and every task takes the same
path. Branch on the prompt (`$2`), or scan all arguments.

### Drive MCP servers over the protocol

Do not trust a guide's claimed tool list. Speak JSON-RPC to the server directly over stdio or HTTP
(`initialize`, then `tools/list`, then `tools/call`) and capture the REAL tool names and responses.
Guides routinely name tools that the server renamed or never exposed.

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"audit","version":"1.0"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | node server.js
```

### Feed hooks their real stdin payload

A hook is verified by its exit code against the actual `PreToolUse` JSON, not by reading its source.
Include the Windows case: an absolute path with backslashes breaks naive `*/src/*` case patterns
that match happily on POSIX paths.

```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"D:\\repo\\src\\app.ts"}}' | bash .claude/hooks/guard.sh; echo "exit=$?"
```

### "I cannot find it" is not "it does not exist"

A negative search result is evidence about the search, not about the world. Before calling guide
content fabricated, check the vendor documentation for the exact surface. Report the honest form:
"could not confirm X against source Y", never "X does not exist".

### Never report as verified what was not run

Steps that need a live authenticated session, a paid account, a browser, or a CI runner get labelled
not-executed with the reason. Verify their preconditions instead (the file exists, the schema is
valid, the endpoint resolves, the credential is present) and say precisely that.

| Claim | Only allowed when |
|---|---|
| Verified | The step was executed and its observable result was seen |
| Preconditions verified | The inputs were checked, the step itself was not run |
| Not executed | Named blocker: needs a live session, an account, a browser, a runner |

Keep "the payload was correct" separate from "the process exited cleanly". A tool can print a
correct result and then die in teardown, and a learner who is not warned reads the crash dump as a
failed demo and debugs working code.

## Reporting

Report per guide, one line per finding, severity first. A blocker is anything that stops the learner
from completing the step: an invented command, a silently ignored key, a gate that cannot fail, a
manifest that never loads. Everything else is a finding.

```text
lab-04-ci-gate.md: 11 findings, 2 blockers
  BLOCKER Step 6: `while read` subshell discards $fail, gate always exits 0
  BLOCKER Step 3: permissions: frontmatter is not a supported subagent key
  finding Step 8: crontab needs WSL on Windows, no note in the guide
  not-executed Step 9: GitHub Actions job, verified workflow syntax only
```

Fold every confirmed finding back into the guide, then re-run the affected steps. A finding that was
fixed but not re-executed is still open.
