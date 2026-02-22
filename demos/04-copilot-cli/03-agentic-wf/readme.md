# GitHub Agentic Workflows

[GitHub Agentic Workflows](https://github.github.com/gh-aw/)

## Demo

### Installation and Requirements

> Note: [GitHub CLI](https://github.com/cli/cli/releases/download/v2.87.2/gh_2.87.2_windows_amd64.msi) is a required dependency for this demo.

Login to GitHub CLI:

```bash
gh auth login
```

Installation:

```bash
gh extension install github/gh-aw
```

### Add the sample workflow and trigger a run:

```bash
gh aw add-wizard githubnext/agentics/daily-repo-status
```

> Note: Before adding the workflow, make sure your repo is clean and you have committed all your changes. The workflow will be added to a new branch and a pull-request wil be issued.

Create the token:

![images](./_images/token.jpg)

Add the demo workflow:

![images](./_images/add-wf.jpg)
