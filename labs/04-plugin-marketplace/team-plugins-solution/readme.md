# Lab 04 solution: team plugin marketplace

The `team-plugins` repository as [Lab 04](../readme.md) leaves it after Step 6, without its `.git` folder: both catalogs and both plugins, with `api-review` at 1.1.0. See [test-results.md](test-results.md) for the commands that were run against it and their output.

## File map

| File in this folder | Lab step | What it is |
|---|---|---|
| `.github/plugin/marketplace.json` | Step 2, Step 6 | The Copilot catalog: marketplace `team-plugins`, two plugin entries, `api-review` at 1.1.0 |
| `.claude-plugin/marketplace.json` | Step 2, Step 6 | The Claude Code catalog listing the same two plugin folders |
| `plugins/commit-conventions/` | Step 1 | Unchanged starter plugin: `plugin.json` and the `conventional-commit` skill |
| `plugins/api-review/plugin.json` | Step 6 | Version bumped to 1.1.0 |
| `plugins/api-review/skills/endpoint-review/SKILL.md` | Step 6 | Rule 6 added: `201` with a `Location` header on create |
| `plugins/api-review/com.github.copilot/agents/api-reviewer.agent.md` | Step 1 | Unchanged Copilot agent that applies the `endpoint-review` skill |

## Links & Resources

- [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) - the `marketplace.json` fields these two catalogs use
