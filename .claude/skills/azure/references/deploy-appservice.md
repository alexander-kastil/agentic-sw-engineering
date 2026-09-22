# Deploy an API to Azure App Service

Backend API to App Service (Free F1 tier) with passwordless OIDC. Build with `dotnet publish`, deploy via `azure/webapps-deploy@v2`.

Real values (subscription/tenant/client IDs): the repo's `credentials.json` / `config.json` (git-ignored).

## Read configuration

```bash
cfg=.claude/skills/azure-deploy/deploy.json
RG=$(jq -r '.ResourceGroup' $cfg)
APP_NAME=$(jq -r '.AppService.Name' $cfg)
PLAN=$(jq -r '.AppService.Plan' $cfg)
RUNTIME=$(jq -r '.AppService.Runtime' $cfg)
SOURCE=$(jq -r '.AppService.Source' $cfg)
```

## Create plan and web app (one-time)

```bash
az appservice plan create \
    --name $PLAN \
    --resource-group $RG \
    --location $LOC \
    --sku F1 \
    --is-linux

az webapp create \
    --name $APP_NAME \
    --resource-group $RG \
    --plan $PLAN \
    --runtime $RUNTIME
```

## Assign role to WIF identity (one-time)

```bash
WIF=$(jq -r '.WIF' $cfg)
APP_ID=$(az webapp show --name $APP_NAME --resource-group $RG --query id -o tsv)
PRINCIPAL=$(az identity show --name $WIF --resource-group $RG --query principalId -o tsv)

az role assignment create \
    --assignee $PRINCIPAL \
    --role Contributor \
    --scope $APP_ID
```

## GitHub Actions workflow

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

  - name: Setup .NET
    uses: actions/setup-dotnet@v4
    with:
      dotnet-version: '10.x'

  - name: Build and Publish
    run: dotnet publish -c Release -o publish
    working-directory: <source>

  - name: Deploy to App Service
    uses: azure/webapps-deploy@v2
    with:
      app-name: <app-name>
      package: <source>/publish
```

### Full workflow, .NET example

`catalog-service-cs` (.NET 10):

```yaml
name: Deploy API

on:
  push:
    branches: [main]
    paths: ['src/food-app/catalog-api/catalog-service-cs/**']
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Read Config
        id: cfg
        run: |
          echo "app_name=$(jq -r '.AppService.Name' .claude/skills/azure-deploy/deploy.json)" >> $GITHUB_OUTPUT
          echo "source=$(jq -r '.AppService.Source' .claude/skills/azure-deploy/deploy.json)" >> $GITHUB_OUTPUT

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '10.x'

      - name: Build and Publish
        run: dotnet publish -c Release -o publish
        working-directory: ${{ steps.cfg.outputs.source }}

      - name: Deploy to App Service
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ steps.cfg.outputs.app_name }}
          package: ${{ steps.cfg.outputs.source }}/publish
```

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Authorization failed` | WIF identity lacks Contributor on the web app | `az role assignment create --role Contributor` scoped to the web app resource ID |
| `No package found at path` | `dotnet publish` output path mismatch | `-o publish` and `package: <source>/publish` must use the same relative path |
| `Runtime not available on F1` | F1 has limited runtime support | Verify with `az webapp list-runtimes --os linux` |
| `App not reachable after deploy` | F1 cold start, no Always On | F1 does not support Always On; first request after idle is slow, upgrade to B1 for production |

## See also

[oidc-github-actions.md](oidc-github-actions.md), [devops-wif.md](devops-wif.md), [deploy-swa.md](deploy-swa.md), [cli-conventions.md](cli-conventions.md)
