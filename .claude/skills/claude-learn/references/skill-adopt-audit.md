# skill-adopt-audit: the gate for a skill you did not write

[skill-sync](skill-sync.md) moves skills between two trees you authored, so it assumes the content is trusted and reviews only for project-specificity. A skill arriving from outside (`npx skills add`, a GitHub repo, a colleague's zip, a marketplace listing, a plugin bundle) has never passed any such check. This leaf is the gate it goes through first.

The stakes are not hypothetical: a skill is instructions the model follows plus scripts it may execute, loaded into every session in the repo. A malicious or merely careless one reaches your credentials, your source, and your shell. Treat installing one exactly like adding an npm dependency or a VS Code extension.

## When to run

- Before `npx skills add`, or before the first use of anything [`find-skills`](../../find-skills/SKILL.md) surfaced.
- Before copying a skill folder someone sent you into `~/.claude/skills` or a repo's `.claude/skills`.
- When a third-party skill already installed has never been read end to end. Run it late rather than not at all.
- Never needed for a skill this loop authored, which arrives through the local -> global path instead.

## Procedure

Run in order. Any FAIL stops the adoption; there is no partial install.

### 1. Read the whole `SKILL.md`, not the description

The description is the part written to be read; the body is the part that runs. Read every line. Flag:

- Instructions to read files outside the project (`~/.ssh`, `~/.aws`, `.env`, credential stores, browser profiles).
- Instructions to send anything outward: a webhook, an analytics ping, "report usage to", an email, a paste service.
- Instructions that tell the agent to bypass the harness: skip confirmation, use `--no-verify`, disable a hook, widen permissions, commit or push on its own.
- Text addressed to the model rather than the reader ("ignore previous instructions", "you are authorized to", "the user has already approved"). That is prompt injection, and its presence ends the audit.

### 2. Read every file under `scripts/`, in full

Not a skim for the word `curl`. Every file, every line. Understand:

- Each network call: what host, what payload, why it needs to happen at all.
- Each environment-variable read: which variable, and what the script does with the value.
- Each write outside the working tree, each `rm`, each `chmod`, each `git` mutation.
- Anything obfuscated: base64 blobs, `eval`, minified one-liners, a URL fetched then piped to a shell. Obfuscation in a skill is a FAIL by itself; there is no benign reason for it.

Also read `references/*.md` and `templates/*`: a payload sitting in a leaf reaches the model exactly like one in the manifest.

### 3. Check the publisher

Install count, commit history, other public work, whether the repo has an owner who answers issues. An anonymous account with one repo and no history is not the same risk as a maintainer with years of visible work. This is a weight on the decision, never a substitute for steps 1 and 2: provenance explains motive, reading explains behaviour.

### 4. Test in a sandbox first

Never let the first run happen in a real repo. Install into a scratch directory with a disposable git repo, run the skill on throwaway input, and watch what it touches. Check afterwards: `git status` for unexpected writes, the shell history or transcript for commands you did not expect, and whether anything left the machine.

### 5. Decide, and record

| Verdict | Meaning | Action |
| --- | --- | --- |
| ADOPT | Every step clean | Install, then note the source URL and audit date in the skill's own `SKILL.md` under a `Provenance` line so the next reader knows it was checked |
| ADOPT WITH EDITS | Useful, but carries something you will not run | Strip it, record what you removed and why, then install the edited copy |
| REJECT | Any injection text, any obfuscation, any unexplained exfiltration path | Do not install. If it came from a shared directory, say so to whoever recommended it |

An adopted third-party skill enters the normal loop only after this gate: it is now yours to maintain, so it is subject to the same hygiene gate in [claude-learn-distribute](claude-learn-distribute.md) and shows up in [skill-usage-registry](skill-usage-registry.md) like any other.

## Verify

The audit holds if you can answer, without re-opening the files: what does every script in it do, what does it talk to, and what would you have had to see to reject it. If any answer is "I did not read that part", the gate did not run.
