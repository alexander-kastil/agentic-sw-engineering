# Test Results

Run on Windows 11, Git Bash, Node v24.15.0, npm 11.12.1, git 2.53.0.windows.1. Working directory was a scratch copy of this folder, not `src/scratch/session-lab/`.

## Commands run

```bash
node --version
```

```text
v24.15.0
```

```bash
npm test
```

```text
> session-lab@1.0.0 test
> node --test

✔ slugifies an ordinary title (0.9108ms)
✔ collapses runs of non-alphanumeric characters into one hyphen (0.0803ms)
✔ strips leading and trailing hyphens (0.1048ms)
✔ returns an empty string for the empty string (0.067ms)
✔ returns an empty string for non-string input (0.0929ms)
✔ returns an empty string when the input is only punctuation (0.0624ms)
✔ folds accented Latin characters to their ASCII base (0.0844ms)
✔ treats a letter with no ASCII decomposition as a separator (0.0496ms)
✔ returns an empty string for scripts with no ASCII equivalent (0.1147ms)
ℹ tests 9
ℹ suites 0
ℹ pass 9
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 85.2985
```

## Per test case

| Test | Input | Result |
|------|-------|--------|
| slugifies an ordinary title | `'Hello World'` | pass, `hello-world` |
| collapses runs of non-alphanumeric characters into one hyphen | `'Agent   Sessions --- Lab #5!'` | pass, `agent-sessions-lab-5` |
| strips leading and trailing hyphens | `'  ...Trimmed Title...  '` | pass, `trimmed-title` |
| returns an empty string for the empty string | `''` | pass, `''` |
| returns an empty string for non-string input | `null`, `undefined`, `42`, `{}`, `['a']` | pass, `''` for all five |
| returns an empty string when the input is only punctuation | `'---'`, `'!!! ??? ...'` | pass, `''` for both |
| folds accented Latin characters to their ASCII base | `'Café Über'` | pass, `cafe-uber` |
| treats a letter with no ASCII decomposition as a separator | `'Straße Zwei'` | pass, `stra-e-zwei` |
| returns an empty string for scripts with no ASCII equivalent | `'日本語'` | pass, `''` |

One test failed on the first run and the expectation was wrong, not the implementation: `'Café Über Straße'` was expected to produce `cafe-uber-strae`, and it produced `cafe-uber-stra-e`. `ß` has no NFKD decomposition, so it is not a letter in the `a-z0-9` set and becomes a separator like any other character. The case was split into the two accent tests above so the real behaviour is asserted rather than smoothed over.

## Shell commands in the lab guide

Checked as written, on Windows.

| Command | Where | Result |
|---------|-------|--------|
| `mkdir -p src/scratch/session-lab` | Step 2 | Works in Git Bash. Also works in PowerShell 7, where `mkdir` is a wrapper over `New-Item` and `-p` binds as a prefix of `-Path`, which creates intermediate folders anyway. Verified by creating a two-level path in both shells. |
| `git worktree list` | Step 3, Cleanup | Runs. Output on this checkout is one line, `D:/git-classes/agentic-sw-engineering 7f52432 [master]`, so the branch name the Cleanup step needs is in the listing. |
| `git status --short -- src/scratch/` | Step 3, Cleanup | Runs. Two behaviours the guide's Expected lines did not match, both fixed in the guide: an entirely untracked folder is reported collapsed as `?? src/scratch/` rather than per file, and after the folder is deleted the command prints `warning: could not open directory 'src/scratch/': No such file or directory` and still exits 0. |
| `git worktree remove --force <path>` | Cleanup | Not run. This checkout is shared with other sessions and the command is destructive. Syntax and ordering checked against `git worktree list`, which shows the path the command needs. |
| `git branch -D <branch>` | Cleanup | Not run, same reason. The order in the guide is correct: a branch checked out by a worktree cannot be deleted until that worktree is gone. |

## Steps that could not be executed

Every one of these is driven from the VS Code Agents window and has no command-line equivalent.

| Step | Why |
|------|-----|
| Step 1, open the Agents window and confirm the host | Requires the VS Code companion window and its settings UI |
| Step 2, the `/research` session | Slash command inside an agent session; the report content was produced by doing the research directly, and every path in `research.md` was checked on disk |
| Step 3, the worktree checkbox | The isolation checkbox is a session UI control, and creating a worktree in this shared checkout was out of bounds for this run |
| Step 4, side-by-side layout and background send | Window layout and session lifecycle |
| Step 5, `/btw` side chat | Slash command inside a session |
| Step 6, window reload and session survival | Requires a live agent host to survive |
| Step 7, `/troubleshoot` | Reads the session record, which exists only for a real session. The failure it diagnoses was reproduced instead: the folder has no manifest until `package.json` is added |
| Step 8, `/rubber-duck` | Hands the session to a complementary model. The three findings the step predicts were implemented and tested instead |
| Step 9, diff stats, prompt timeline, Find in Chat | All three are session detail pane surfaces |
| Step 10, `/chronicle` | Queries the account-scoped session record |
