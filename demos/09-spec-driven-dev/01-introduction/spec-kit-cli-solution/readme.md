# Solution: Spec Kit CLI, Verified

Every command on [the topic page](../readme.md) was executed on 2026-09-21. This folder records what they actually did, so you can tell a broken install from a changed tool.

Environment: Windows 11, `uv` 0.9.18, Python 3.12.10.

## Install

```bash
uv tool install specify-cli --reinstall
```

```text
Installed 1 executable: specify
```

```bash
specify --version
```

```text
specify 1.0.9
```

The `--reinstall` matters. Without it, `uv tool install specify-cli` on a machine that already carries an older `specify-cli` prints `Audited 16 packages` and installs nothing, leaving you on the previous generation:

```text
Resolved 16 packages in 207ms
Audited 16 packages in 0.44ms
Installed 1 executable: specify
```

That silent no-op is what leaves a reader typing `/speckit.specify` with a dot at a Copilot that only knows `/speckit-specify`.

## Initialize

```bash
specify init meeting-cost --integration copilot --script py
```

```text
Initialize Specify Project
├── ● Check required tools (ok)
├── ● Select coding agent integration (copilot)
├── ● Select script type (py)
├── ● Install integration (GitHub Copilot)
├── ● Install shared infrastructure (scripts (py) + templates)
├── ○ Ensure scripts executable
├── ● Constitution setup (copied from template)
├── ● Install bundled workflow (speckit installed)
└── ● Finalize (project ready)
Project ready.
```

The CLI closes by printing the command names it registered. They carry a hyphen:

```text
2.1 /speckit-constitution - Establish project principles
2.2 /speckit-specify - Create baseline specification
2.3 /speckit-plan - Create implementation plan
2.4 /speckit-tasks - Generate actionable tasks
2.5 /speckit-implement - Execute implementation
2.6 /speckit-converge - Assess the codebase and append remaining work as tasks
```

The separator is not cosmetic. It is written into the generated project:

```bash
cat meeting-cost/.specify/integration.json
```

```json
{
  "integration_settings": {
    "copilot": {
      "script": "py",
      "invoke_separator": "-"
    }
  }
}
```

## What the flags accept

`specify init` takes `--script`, `--ignore-agent-tools`, `--here`, `--force`, `--non-interactive`, `--preset`, `--integration`, `--integration-options`, `--extension` and `--trust-extension-urls`. The top-level subcommands are `init`, `check`, `version`, `self`, `extension`, `integration`, `event`, `preset`, `bundle` and `workflow`.

`init` needs no network. The templates ship inside the package, which is also why the generated project always matches the installed CLI version rather than whatever is on `main`.

## If the version has moved on

Re-run the two commands above. If `specify --version` reports something newer and the closing banner prints different command names, the topic page is the thing to correct, not your install.

[← Back to Why Spec-Driven Development](../readme.md)
