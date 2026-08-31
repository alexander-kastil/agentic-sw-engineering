# CI/CD with GitHub Actions

GitHub Actions is where the infrastructure from the previous topic gets deployed on every push. The [GitHub Actions agent](/.github/agents/github-actions.agent.md) writes and maintains those workflows using Microsoft Learn best practices, covering authoring, optimization, troubleshooting, and security posture. It creates production-ready YAML for single and multi-job workflows, manages environments and secrets, and integrates third-party marketplace actions securely.

The agent designs workflows that match your repository structure, evaluates and locks down action dependencies, and diagnoses failures with detailed root cause analysis. It enforces least-privilege token scopes and helps you adopt reusable workflows and OpenID Connect federation for cloud deployments.

## Setting Repository Secrets with the GitHub CLI

A workflow reads its credentials from repository secrets, and the GitHub CLI sets them without anyone opening the settings UI. That matters for a class and for a real team: the setup becomes a script you can rerun, review, and hand to the next person, instead of a sequence of clicks nobody wrote down.

The [set-repo-secrets.sh](set-repo-secrets.sh) script shows every form `gh secret set` accepts. A literal value is fine for a throwaway token, but piping from stdin keeps the value out of shell history, and reading from a file is the only workable option for multi-line values such as certificates.

```bash
gh secret set API_KEY --repo <org>/<repo> --body "<value>"
echo -n "<value>" | gh secret set DB_PASSWORD --repo <org>/<repo>
gh secret set SIGNING_KEY --repo <org>/<repo> < ./signing-key.pem
gh secret set --repo <org>/<repo> --env-file ./.env.ci
```

Secrets are write-only once set, so `gh secret list` shows names and update times but never values. Anything you need to read back later belongs in a variable instead, which is why resource group and region go in as variables while credentials go in as secrets.

> Note: Dependabot cannot see repository secrets. A private feed token that Dependabot needs must be set again with `--app dependabot`, or its update runs fail while your workflows keep passing.

```mermaid
flowchart LR
    A["gh secret set"] --> B["Repository secret"]
    B --> C["Workflow job"]
    C --> D["secrets.API_KEY"]
```

## Consuming Secrets in a Workflow

Secrets reach a job through the `secrets` context, and variables through `vars`. Reference them only where they are needed, because a secret passed into a step's environment is available to everything that step runs, including its dependencies.

```yaml
permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: ./deploy.sh --group ${{ vars.AZURE_RESOURCE_GROUP }}
```

Actions masks a secret's value in the log, but only when it appears verbatim. A secret that gets base64-encoded, JSON-embedded, or split across lines prints in the clear, so never echo one even to debug a failing run.

Scoping a job to an `environment` gates it behind that environment's protection rules and gives it access to that environment's secrets. This is how a production credential stays unavailable to a workflow running from a pull request branch.

## Demo: Generate a Deployment Workflow

Ask the GitHub Actions agent to build the workflow that provisions and deploys the food-app infrastructure created in the IaC topic:

```prompt
Create a GitHub Actions workflow that deploys src/food-app to Azure.

Requirements:
- Trigger on push to main and on workflow_dispatch
- Separate build and deploy jobs, deploy depends on build
- Authenticate with azure/login using the AZURE_CREDENTIALS secret set by set-repo-secrets.sh
- Read the resource group and location from repository variables, not from literals
- Provision infrastructure with azd using the Bicep templates in infra/
- Pin every marketplace action to a full commit SHA
- Set the minimum permissions each job needs

Read demos/07-agentic-devops/01-iac-configuration for the infrastructure layout before writing the YAML.
```

## Demo: Troubleshoot a Failing Run

Point the agent at a failed run and let it work the logs rather than reading them yourself:

```prompt
The latest run of .github/workflows/deploy-food-app.yml failed.
Fetch the run, identify the failing job and step, explain the root cause, and propose a diff that fixes it.
```

## Links & Resources

[GitHub Actions documentation](https://docs.github.com/en/actions)

[Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

[gh secret manual](https://cli.github.com/manual/gh_secret) - every flag the `gh secret set` and `gh secret list` commands accept

[Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
