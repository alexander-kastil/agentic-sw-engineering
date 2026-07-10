---
name: azure-deploy/swa
description: Deploy a static UI (Angular, React, Vue, Hugo) to Azure Static Web Apps using OIDC Workload Identity Federation. Key insight: azure/static-web-apps-deploy@v1 cannot use the OIDC session directly — the SWA deployment token must be retrieved via Azure CLI after login. Keywords: azure static web apps, swa, oidc, workload identity, angular deploy, static site, github actions.
license: CC-BY-NC-SA-4.0
---

# SWA — Deploy to Azure Static Web Apps

Deploys a static UI to Azure Static Web Apps using passwordless OIDC. No deployment token stored as a GitHub secret.

### Key Insight

`azure/static-web-apps-deploy@v1` **cannot use the OIDC session directly**. After `azure/login@v2` succeeds, the SWA deployment token must be retrieved via Azure CLI and passed explicitly.

### Read Configuration

```bash
cfg=.claude/skills/azure-deploy/deploy.json
RG=$(jq -r '.ResourceGroup' $cfg)
SWA_NAME=$(jq -r '.SWA.Name' $cfg)
APP_LOC=$(jq -r '.SWA.AppLocation' $cfg)
OUT_LOC=$(jq -r '.SWA.OutputLocation' $cfg)
```

### Create Static Web App (one-time)

```bash
az staticwebapp create \
    --name $SWA_NAME \
    --resource-group $RG \
    --location $LOC \
    --sku Free
```

### Assign Role to WIF Identity (one-time)

```bash
WIF=$(jq -r '.WIF' $cfg)
SWA_ID=$(az staticwebapp show --name $SWA_NAME --resource-group $RG --query id -o tsv)
PRINCIPAL=$(az identity show --name $WIF --resource-group $RG --query principalId -o tsv)

az role assignment create \
    --assignee $PRINCIPAL \
    --role Contributor \
    --scope $SWA_ID
```

### Verified GitHub Actions Workflow

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: actions/checkout@v4

  - name: Azure Login (OIDC)
    uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

  - name: Get SWA Deployment Token
    run: |
      SWA_TOKEN=$(az staticwebapp secrets list \
        --name <swa-name> \
        --resource-group <resource-group> \
        --query "properties.apiKey" -o tsv)
      echo "::add-mask::$SWA_TOKEN"
      echo "SWA_DEPLOYMENT_TOKEN=$SWA_TOKEN" >> $GITHUB_ENV

  - name: Build UI
    run: npm ci && npm run build
    working-directory: <app-location>

  - name: Deploy to Static Web Apps
    uses: azure/static-web-apps-deploy@v1
    with:
      azure_static_web_apps_api_token: ${{ env.SWA_DEPLOYMENT_TOKEN }}
      repo_token: ${{ secrets.GITHUB_TOKEN }}
      action: upload
      app_location: <app-location>
      output_location: <output-location>
```

Substitute `<swa-name>`, `<resource-group>`, `<app-location>`, and `<output-location>` from `deploy.json`.

### Full Workflow — Angular Example

For `food-shop-ng` (Angular 21, output at `dist/food-shop-ui/browser`):

```yaml
name: Deploy UI

on:
  push:
    branches: [main]
    paths: ['src/food-app/shop-ui/food-shop-ng/**']
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Get SWA Deployment Token
        run: |
          cfg=.claude/skills/azure-deploy/deploy.json
          SWA_NAME=$(jq -r '.SWA.Name' $cfg)
          RG=$(jq -r '.ResourceGroup' $cfg)
          SWA_TOKEN=$(az staticwebapp secrets list \
            --name $SWA_NAME --resource-group $RG \
            --query "properties.apiKey" -o tsv)
          echo "::add-mask::$SWA_TOKEN"
          echo "SWA_DEPLOYMENT_TOKEN=$SWA_TOKEN" >> $GITHUB_ENV

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Build
        run: npm ci && npm run build
        working-directory: ${{ fromJson(steps.cfg.outputs.cfg).SWA.AppLocation }}

      - name: Deploy
        uses: azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ env.SWA_DEPLOYMENT_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: upload
          app_location: ${{ fromJson(steps.cfg.outputs.cfg).SWA.AppLocation }}
          output_location: ${{ fromJson(steps.cfg.outputs.cfg).SWA.OutputLocation }}
```

### Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `deployment_token was not provided` | Deploy action needs explicit token even with OIDC | Add the "Get SWA Deployment Token" step — this is always required |
| `client-id not supplied` | GitHub secrets not set | Run `gh secret set` for all three AZURE_* secrets (see wif subskill) |
| Output folder not found | Wrong `OutputLocation` in deploy.json | Angular outputs to `dist/<project-name>/browser`; verify in `angular.json` `outputPath` |
| OIDC login fails after secrets set | Federated credential subject mismatch | Verify `--subject repo:<org>/<repo>:ref:refs/heads/main` matches exactly |
