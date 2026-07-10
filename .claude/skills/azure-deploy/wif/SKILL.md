---
name: azure-deploy/wif
description: One-time setup of Azure Workload Identity Federation for GitHub Actions — creates managed identity, assigns AcrPush and Contributor roles, creates federated credential. Run before any deployment. Keywords: workload identity federation, WIF, OIDC, managed identity, federated credential, github actions azure auth, passwordless.
license: CC-BY-NC-SA-4.0
---

# WIF — Workload Identity Federation Setup

One-time setup. Creates the managed identity and federated credential that lets GitHub Actions authenticate to Azure without storing any secrets.

### Read Configuration

```powershell
$cfg  = Get-Content .claude/skills/azure-deploy/deploy.json | ConvertFrom-Json
$rg   = $cfg.ResourceGroup
$loc  = $cfg.Location
$acr  = $cfg.ACR
$wif  = $cfg.WIF
$repo = $cfg.GitHubRepo
```

```bash
cfg=.claude/skills/azure-deploy/deploy.json
RG=$(jq -r '.ResourceGroup' $cfg)
LOC=$(jq -r '.Location' $cfg)
ACR=$(jq -r '.ACR' $cfg)
WIF=$(jq -r '.WIF' $cfg)
REPO=$(jq -r '.GitHubRepo' $cfg)
```

### Create Resources

```powershell
az group create --name $rg --location $loc
az acr create --name $acr --resource-group $rg --sku Basic --admin-enabled false
az containerapp env create `
    --name $cfg.ContainerEnv --resource-group $rg --location $loc
az identity create --name $wif --resource-group $rg
Start-Sleep -Seconds 15
```

```bash
az group create --name $RG --location $LOC
az acr create --name $ACR --resource-group $RG --sku Basic --admin-enabled false
az containerapp env create \
    --name $(jq -r '.ContainerEnv' $cfg) --resource-group $RG --location $LOC
az identity create --name $WIF --resource-group $RG
sleep 15
```

### Assign Roles

```powershell
$principal = az identity show --name $wif --resource-group $rg --query principalId -o tsv
$subId     = az account show --query id -o tsv
$acrId     = az acr show --name $acr --resource-group $rg --query id -o tsv

az role assignment create --assignee $principal --role AcrPush --scope $acrId
az role assignment create --assignee $principal --role Contributor `
    --scope /subscriptions/$subId/resourceGroups/$rg
```

```bash
PRINCIPAL=$(az identity show --name $WIF --resource-group $RG --query principalId -o tsv)
SUB_ID=$(az account show --query id -o tsv)
ACR_ID=$(az acr show --name $ACR --resource-group $RG --query id -o tsv)

az role assignment create --assignee $PRINCIPAL --role AcrPush --scope $ACR_ID
az role assignment create --assignee $PRINCIPAL --role Contributor \
    --scope /subscriptions/$SUB_ID/resourceGroups/$RG
```

### Create Federated Credential

```powershell
az identity federated-credential create `
    --name fc-github-main `
    --identity-name $wif `
    --resource-group $rg `
    --issuer https://token.actions.githubusercontent.com `
    --subject "repo:${repo}:ref:refs/heads/main" `
    --audience api://AzureADTokenExchange
```

```bash
az identity federated-credential create \
    --name fc-github-main \
    --identity-name $WIF \
    --resource-group $RG \
    --issuer https://token.actions.githubusercontent.com \
    --subject "repo:${REPO}:ref:refs/heads/main" \
    --audience api://AzureADTokenExchange
```

### Set GitHub Secrets

```bash
CLIENT_ID=$(az identity show --name $WIF --resource-group $RG --query clientId -o tsv)
TENANT_ID=$(az account show --query tenantId -o tsv)
SUB_ID=$(az account show --query id -o tsv)

gh secret set AZURE_CLIENT_ID       --body "$CLIENT_ID" --repo $REPO
gh secret set AZURE_TENANT_ID       --body "$TENANT_ID" --repo $REPO
gh secret set AZURE_SUBSCRIPTION_ID --body "$SUB_ID"    --repo $REPO
```

> Use `az identity show` to retrieve the client ID — never guess it.

### Teardown

Federated credential must be deleted before the managed identity, otherwise deletion is blocked.

```bash
az identity federated-credential delete \
    --name fc-github-main --identity-name $WIF --resource-group $RG
az identity delete --name $WIF --resource-group $RG
```

### Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `OIDC login fails` | Subject mismatch in federated credential | Verify `--subject repo:<org>/<repo>:ref:refs/heads/main` matches exactly |
| Role assignment retry (5/5) | Service principal not yet propagated | Wait 30s and rerun — the 15s sleep is a minimum |
| `Cannot delete identity` | Federated credential still exists | Delete federated credential first, then identity |
