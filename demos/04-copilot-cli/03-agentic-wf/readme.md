# GitHub Agentic Workflows

[GitHub Agentic Workflows](https://github.github.com/gh-aw/)

## Demo

### Installation and Requirements

> Note: [GitHub CLI](https://github.com/cli/cli/releases/download/v2.87.2/gh_2.87.2_windows_amd64.msi) is a required dependency for this demo.

Login to GitHub CLI:

```
gh auth login
```

Installation:

```
gh extension install github/gh-aw
```

### Add the sample workflow and trigger a run:

```
gh aw add-wizard githubnext/agentics/daily-repo-status
```
