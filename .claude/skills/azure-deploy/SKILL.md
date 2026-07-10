---
name: azure-deploy
description: Deploy a static UI to Azure Static Web Apps and a backend API to Azure App Service using OIDC Workload Identity Federation. Orchestrates three subskills — wif (identity setup), swa (static UI deploy), appservice (API deploy). Use when deploying any service to Azure via GitHub Actions. Keywords: azure static web apps, azure app service, oidc, workload identity, github actions, deploy.
license: CC-BY-NC-SA-4.0
---

# Azure Deploy

Deploy a static UI to Azure Static Web Apps and a backend API to Azure App Service using passwordless OIDC — no long-lived secrets stored in GitHub.

## Configuration

All deployment metadata lives in `.claude/skills/azure-deploy/deploy.json`. Read and customize it before running any subskill.

```json
{
    "ResourceGroup": "rg-myapp",
    "Location": "westeurope",
    "WIF": "wi-myapp",
    "GitHubRepo": "org/repo",
    "SWA": {
        "Name": "swa-myapp",
        "AppLocation": "src/ui",
        "OutputLocation": "dist/my-ui/browser"
    },
    "AppService": {
        "Name": "app-myapi",
        "Plan": "asp-myapp",
        "Sku": "F1",
        "Runtime": "DOTNETCORE:10.0",
        "Source": "src/api"
    }
}
```

## Subskills

Run `wif` once for initial setup. `swa` and `appservice` are used for every deploy.

### wif — Workload Identity Federation

Creates managed identity, assigns Contributor role, and establishes federated trust with GitHub Actions — no secrets needed.

**Trigger:** "set up workload identity", "create WIF", "configure OIDC for GitHub Actions"

See: `.claude/skills/azure-deploy/wif/SKILL.md`

### swa — Azure Static Web Apps

Builds the UI and deploys to Azure Static Web Apps. Retrieves the SWA deployment token via Azure CLI after OIDC login — the deploy action cannot use the OIDC session directly.

**Trigger:** "deploy UI", "deploy to static web apps", "deploy SWA", "deploy Angular"

See: `.claude/skills/azure-deploy/swa/SKILL.md`

### appservice — Azure App Service

Publishes the API with `dotnet publish` and deploys to Azure App Service (F1 free tier) via `azure/webapps-deploy@v2`.

**Trigger:** "deploy API", "deploy to app service", "deploy .NET"

See: `.claude/skills/azure-deploy/appservice/SKILL.md`

## Architecture

```
GitHub Actions (OIDC)
       │
       ▼
WIF Managed Identity
       ├── Contributor → Azure Static Web Apps  ◄── UI build (npm run build)
       └── Contributor → Azure App Service      ◄── API build (dotnet publish)
```

## Required GitHub Secrets

Set once via the `wif` subskill:

| Secret | How to retrieve |
|---|---|
| `AZURE_CLIENT_ID` | `az identity show --name <WIF> --resource-group <RG> --query clientId -o tsv` |
| `AZURE_TENANT_ID` | `az account show --query tenantId -o tsv` |
| `AZURE_SUBSCRIPTION_ID` | `az account show --query id -o tsv` |
