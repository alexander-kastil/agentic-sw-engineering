# Deploy a container to Azure Container Apps

Deploy each service from ACR to Container Apps. Create-or-update pattern: safe on first deploy and every re-run. Build/push first: [deploy-acr.md](deploy-acr.md).

## Read config

```bash
cfg=.claude/skills/azure-deploy/deploy.json
RG=$(jq -r '.ResourceGroup' $cfg)
CAE=$(jq -r '.ContainerEnv' $cfg)
ACR=$(jq -r '.ACR' $cfg)
WIF=$(jq -r '.WIF' $cfg)
```

## Deploy one service

```bash
name=<service-name>
port=<port>
sha=<image-tag>

az containerapp create \
    --name $name \
    --resource-group $RG \
    --environment $CAE \
    --image $ACR.azurecr.io/$name:$sha \
    --registry-server $ACR.azurecr.io \
    --target-port $port \
    --ingress external \
    --min-replicas 1 --max-replicas 3 \
    2>/dev/null || \
az containerapp update \
    --name $name \
    --resource-group $RG \
    --image $ACR.azurecr.io/$name:$sha
```

## Managed identity for ACR pull

Container Apps cannot pull from ACR without explicit registry auth. Attach the WIF managed identity once after first deploy.

```bash
MI_ID=$(az identity show --name $WIF --resource-group $RG --query id -o tsv)

jq -r '.Services[].Name' $cfg | while read name; do
    az containerapp registry set \
        --name $name \
        --resource-group $RG \
        --server $ACR.azurecr.io \
        --identity $MI_ID
done
```

## Environment variables

```bash
az containerapp update \
    --name $name \
    --resource-group $RG \
    --set-env-vars KEY1=value1 KEY2=value2
```

Read another app's URL dynamically (UI depends on API):

```bash
API_FQDN=$(az containerapp show \
    --name my-api --resource-group $RG \
    --query "properties.configuration.ingress.fqdn" -o tsv)

az containerapp update \
    --name my-ui \
    --resource-group $RG \
    --set-env-vars API_URL=https://$API_FQDN
```

## GitHub Actions workflow

`.github/workflows/deploy.yml`. Runs after the ACR build workflow completes. Secrets hold real values (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`); OIDC setup: [oidc-github-actions.md](oidc-github-actions.md).

```yaml
name: Deploy to Container Apps

on:
  workflow_run:
    workflows: ["Build and Push Images"]
    types: [completed]
    branches: [main]
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'workflow_dispatch' }}

    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy Services
        run: |
          cfg=.claude/skills/azure-deploy/deploy.json
          RG=$(jq -r '.ResourceGroup' $cfg)
          CAE=$(jq -r '.ContainerEnv' $cfg)
          ACR=$(jq -r '.ACR' $cfg)

          jq -c '.Services[]' $cfg | while read svc; do
            name=$(echo $svc | jq -r '.Name')
            port=$(echo $svc | jq -r '.Port')

            az containerapp create \
                --name $name \
                --resource-group $RG \
                --environment $CAE \
                --image $ACR.azurecr.io/$name:${{ github.sha }} \
                --registry-server $ACR.azurecr.io \
                --target-port $port \
                --ingress external \
                --min-replicas 1 --max-replicas 3 \
                2>/dev/null || \
            az containerapp update \
                --name $name \
                --resource-group $RG \
                --image $ACR.azurecr.io/$name:${{ github.sha }}
          done
```

## Get service URLs

```bash
jq -r '.Services[].Name' $cfg | while read name; do
    fqdn=$(az containerapp show --name $name --resource-group $RG \
        --query "properties.configuration.ingress.fqdn" -o tsv)
    echo "$name → https://$fqdn"
done
```

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Container image pull failed` | ACR pull not configured | `az containerapp registry set` with managed identity (above) |
| `Container app already exists` | First `create` succeeds, re-run fails | `2>/dev/null \|\| update` pattern handles it: verify both commands present |
| `Environment not found` | Container Apps environment not created | Run the WIF setup first, it creates the environment ([oidc-github-actions.md](oidc-github-actions.md)) |
| `ingress fqdn is null` | Deployed without external ingress | Add `--ingress external` to `az containerapp create` |
