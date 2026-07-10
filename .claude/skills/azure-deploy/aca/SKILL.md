---
name: azure-deploy/aca
description: Deploy container images from ACR to Azure Container Apps — handles create-or-update, external ingress, environment variables, and managed identity registry authentication. Generates GitHub Actions workflow. Keywords: azure container apps, aca, container app, deploy, ingress, environment variables, managed identity, acr pull.
license: CC-BY-NC-SA-4.0
---

# ACA — Deploy to Azure Container Apps

Deploys each service from ACR to Azure Container Apps. Uses create-or-update pattern — safe to run on first deploy and on every subsequent update.

### Read Configuration

```bash
cfg=.claude/skills/azure-deploy/deploy.json
RG=$(jq -r '.ResourceGroup' $cfg)
CAE=$(jq -r '.ContainerEnv' $cfg)
ACR=$(jq -r '.ACR' $cfg)
WIF=$(jq -r '.WIF' $cfg)
```

### Deploy a Single Service

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

### Attach Managed Identity for ACR Pull

Container Apps cannot pull from ACR without explicit registry authentication. Attach the WIF managed identity once after first deploy:

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

### Environment Variables

Pass environment variables at deploy time:

```bash
az containerapp update \
    --name $name \
    --resource-group $RG \
    --set-env-vars KEY1=value1 KEY2=value2
```

To read another container app's URL dynamically (e.g. UI depends on API):

```bash
API_FQDN=$(az containerapp show \
    --name my-api --resource-group $RG \
    --query "properties.configuration.ingress.fqdn" -o tsv)

az containerapp update \
    --name my-ui \
    --resource-group $RG \
    --set-env-vars API_URL=https://$API_FQDN
```

### GitHub Actions Workflow

Place in `.github/workflows/deploy.yml`. Runs after the ACR build workflow completes:

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

### Get Service URLs

```bash
jq -r '.Services[].Name' $cfg | while read name; do
    fqdn=$(az containerapp show --name $name --resource-group $RG \
        --query "properties.configuration.ingress.fqdn" -o tsv)
    echo "$name → https://$fqdn"
done
```

### Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Container image pull failed` | ACR pull not configured | Run `az containerapp registry set` with managed identity (see above) |
| `Container app already exists` | First `create` succeeds but re-run fails | The `2>/dev/null \|\| update` pattern handles this — verify both commands are present |
| `Environment not found` | Container Apps environment not created | Run the wif subskill first — it creates the environment |
| `ingress fqdn is null` | App deployed without external ingress | Add `--ingress external` to `az containerapp create` |
