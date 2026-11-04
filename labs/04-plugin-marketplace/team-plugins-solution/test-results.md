# Lab 04 test results: team plugin marketplace

Environment: Windows 11, Git Bash and PowerShell 7, `copilot --version` = GitHub Copilot CLI 1.0.105, VS Code 1.144.1, Claude Code 2.1.318, `gh` 2.48.0. Every CLI command ran with `COPILOT_HOME` and `COPILOT_CACHE_HOME` pointed at a scratch folder, and VS Code ran with its own user data folder and a home whose `.copilot` was that same `COPILOT_HOME`, so no real configuration was read or changed.

## What was run and what was not

| Lab step | Result |
|---|---|
| Step 1: copy the starter | Verified in Bash (`cp -r`) and PowerShell (`Copy-Item -Recurse`) |
| Step 2: write both catalogs, try them from the folder | Verified in the Copilot CLI (Bash and PowerShell `"$PWD"`) and in Claude Code with a scratch `CLAUDE_CONFIG_DIR` |
| Step 3: publish on GitHub | `git init`, `git add`, `git commit` verified; `gh repo create --private --source . --push` not executed, because it creates a repository in a real GitHub account. Its flags were checked against `gh repo create --help`. The push went to a local bare repository instead, served as `https://github.com/contoso-team/team-plugins.git` through a scratch git `insteadOf` rule |
| Step 4: install in the CLI | Verified against that repository, with `contoso-team` standing in for `<you>` |
| Step 5: VS Code | Verified in an isolated VS Code: the CLI installs appear under **Plugins**, and **Configure Marketplaces** with `contoso-team/team-plugins` lists both plugins in **Browse** |
| Step 5: GitHub Copilot app | Not executed: adding a marketplace in the app changes the owner's own app configuration, and the app offers no isolated profile. The steps come from GitHub Docs, Customizing the GitHub Copilot app |
| Step 6: ship 1.1.0 | Verified, including `copilot plugin update --all` |
| Cleanup | Verified: `copilot plugin marketplace remove team-plugins --force` left `copilot plugin list` with no installed plugins |

## Step 2

```text
$ copilot plugin marketplace add "$PWD"
Marketplace "team-plugins" added successfully.
$ copilot plugin marketplace browse team-plugins
Plugins in "team-plugins":
  • commit-conventions - Writes a Conventional Commits message for the staged changes.
  • api-review - Reviews HTTP endpoints against the team's API guidelines.

Install with: copilot plugin install <plugin-name>@team-plugins
$ claude plugin marketplace add "$PWD"
Adding marketplace…✔ Successfully added marketplace: team-plugins (declared in user settings)
$ claude plugin marketplace list
Configured marketplaces:

  ❯ anthropic-plugin-directory
    Source: Built in (Anthropic Directory)

  ❯ team-plugins
    Source: Folder (D:\claude-scratch\class-marketplace\lab-run\team-plugins)

$ copilot plugin marketplace remove team-plugins
Marketplace "team-plugins" removed successfully.
$ claude plugin marketplace remove team-plugins
✔ Successfully removed marketplace: team-plugins
```

## Step 4

```text
$ copilot plugin marketplace add contoso-team/team-plugins
Marketplace "team-plugins" added successfully.
$ copilot plugin install commit-conventions@team-plugins
Plugin "commit-conventions" installed successfully. Installed 1 skill.
$ copilot plugin install api-review@team-plugins
Plugin "api-review" installed successfully. Installed 1 skill.
$ copilot plugin list
Built-in plugins:
  • browser-use (v0.0.4) [disabled]

Installed plugins:
  • commit-conventions@team-plugins (v1.0.0)
  • api-review@team-plugins (v1.0.0)
$ ls ~/.copilot/installed-plugins/team-plugins
api-review
commit-conventions
$ copilot skill list
Plugin skills:
  conventional-commit - Write a Conventional Commits message for the staged changes in the current repository. ...
  endpoint-review - Review HTTP endpoints (ASP.NET Core controllers, minimal APIs, Express or FastAPI routes) against the team's API guidelines. ...
```

## Step 5 (VS Code)

**Chat: Open Customizations** > **Plugins** listed `api-review` (`1 agent • 1 skill`) and `commit-conventions` (`1 skill`) under **User**, both marked **Local** with the path `...\.copilot\installed-plugins\team-plugins`. After **Browse** > **All Sources** > **Configure Marketplaces** > **Add Marketplace...** with `contoso-team/team-plugins`, the **All Sources** menu listed `contoso-team/team-plugins`, and **Browse** showed `commit-conventions` and `api-review` from it with **Install**, while the two CLI copies showed **Uninstall**. VS Code stored the entry in `chat.plugins.marketplaces`. The marketplace registered in the CLI did not appear in VS Code's marketplace list before it was added there.

## Step 6

```text
$ git commit -am "api-review 1.1.0: check 201 and Location on create"
$ copilot plugin update api-review@team-plugins
Plugin "api-review@team-plugins" updated successfully (v1.0.0 → v1.1.0). Updated 1 skill.
$ copilot plugin list
Installed plugins:
  • commit-conventions@team-plugins (v1.0.0)
  • api-review@team-plugins (v1.1.0)
$ copilot plugin update --all
Updating 2 installed plugins...
Plugin "commit-conventions@team-plugins" updated successfully (v1.0.0, already at latest). Updated 1 skill.
Plugin "api-review@team-plugins" updated successfully (v1.1.0, already at latest). Updated 1 skill.
```

The installed `SKILL.md` under `installed-plugins/team-plugins/api-review/skills/endpoint-review/` contained rule 6 after the update.
