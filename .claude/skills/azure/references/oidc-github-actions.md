# Passwordless GitHub Actions deploys with OIDC (az CLI path)

One-time identity setup with `az`: a user-assigned managed identity, a federated credential trusting the repo, RBAC on the target scope. GitHub Actions then authenticates with no stored secret.

Same thing declared in Bicep (Entra app registration via the Microsoft Graph extension): [oidc-bicep.md](oidc-bicep.md).

Placeholders below (`<tenant-id>`, `<subscription-id>`, `<client-id>`, `<box-ip>`, ...) are never literal. Real values: the repo's `credentials.json` / `config.json` (git-ignored).

## Order

| Step | When | Leaf |
|---|---|---|
| identity + federated credential + RBAC | once | this file |
| static UI deploy | every deploy | [deploy-swa.md](deploy-swa.md) |
| API deploy | every deploy | [deploy-appservice.md](deploy-appservice.md) |

Shape: GitHub Actions (OIDC) -> WIF managed identity -> Contributor on the RG -> SWA (npm build) + App Service (dotnet publish).

## Configuration

All deployment metadata in `.claude/skills/azure-deploy/deploy.json`. Customize before running anything.

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

`ACR` / `ContainerEnv` keys are only needed for the container path ([deploy-acr.md](deploy-acr.md), [deploy-aca.md](deploy-aca.md)).

### Read it

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

## Create resources

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

The 15s sleep is a minimum for SP propagation. Drop the `acr` / `containerapp env` lines for a SWA + App Service topology.

## Assign roles

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

Explicit-id variant (avoids name resolution and principal-type guessing):

```bash
az role assignment create --assignee-object-id $principalId --assignee-principal-type ServicePrincipal \
  --role b24988ac-6180-42a0-ab88-20f7382dd24c \
  --scope "/subscriptions/$subscriptionId/resourcegroups/$grp"
```

Contributor role id `b24988ac-6180-42a0-ab88-20f7382dd24c`, scoped to the resource group. Contributor on the RG is enough to deploy SWA / App Service and to read SWA deployment tokens.

On Git Bash / MSYS, prefix with `MSYS_NO_PATHCONV=1` or the `/subscriptions/...` scope is rewritten to a Windows path and the call fails `MissingSubscription`.

As a B2B guest in a customer tenant, `az role assignment create` often fails `MissingSubscription` regardless: assign the role in Bicep instead ([oidc-bicep.md](oidc-bicep.md), [tenant-access.md](tenant-access.md)).

## Create the federated credential

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

Audience flag: sources disagree, `--audience` (above) and `--audiences api://AzureADTokenExchange`. `--audiences` is the documented plural parameter of `az identity federated-credential create`; if one spelling is rejected by the installed CLI, use the other. Value is identical either way.

## Subject-claim rules

The `subject` must match the OIDC token's `sub` claim EXACTLY. One credential per subject; add more for more branches / environments.

| Trigger | Subject |
|---|---|
| branch push | `repo:<org>/<repo>:ref:refs/heads/<branch>` |
| tag push | `repo:<org>/<repo>:ref:refs/tags/<tag>` |
| job with `environment: <env>` | `repo:<org>/<repo>:environment:<env>` |
| pull request | `repo:<org>/<repo>:pull_request` |

- A job that declares `environment:` emits the **environment** subject, NOT the branch subject, even on a branch push. Mismatch here is the most common `AADSTS70021`.
- `master` is not `main`: match the repo's actual default branch (`refs/heads/master` where that is the deploying branch).
- Audience is always `api://AzureADTokenExchange`.
- Issuer is always `https://token.actions.githubusercontent.com`.

## Set the GitHub secrets

```bash
CLIENT_ID=$(az identity show --name $WIF --resource-group $RG --query clientId -o tsv)
TENANT_ID=$(az account show --query tenantId -o tsv)
SUB_ID=$(az account show --query id -o tsv)

gh secret set AZURE_CLIENT_ID       --body "$CLIENT_ID" --repo $REPO
gh secret set AZURE_TENANT_ID       --body "$TENANT_ID" --repo $REPO
gh secret set AZURE_SUBSCRIPTION_ID --body "$SUB_ID"    --repo $REPO
```

Retrieve the client id with `az identity show`, never guess it.

| Secret | How to retrieve |
|---|---|
| `AZURE_CLIENT_ID` | `az identity show --name <WIF> --resource-group <RG> --query clientId -o tsv` |
| `AZURE_TENANT_ID` | `az account show --query tenantId -o tsv` |
| `AZURE_SUBSCRIPTION_ID` | `az account show --query id -o tsv` |

## Use it in a workflow

Every job needs `permissions: { id-token: write, contents: read }`.

```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

The SWA deploy action cannot use the OIDC session: pull the deployment token with `az` after `azure/login`, then pass it to the action ([deploy-swa.md](deploy-swa.md)).

## Teardown

Delete the federated credential BEFORE the identity, otherwise deletion is blocked.

```bash
az identity federated-credential delete \
    --name fc-github-main --identity-name $WIF --resource-group $RG
az identity delete --name $WIF --resource-group $RG
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| OIDC login fails / `AADSTS70021` | Subject mismatch in the federated credential | Verify `--subject repo:<org>/<repo>:ref:refs/heads/<branch>` matches exactly; check whether the job declares `environment:` (different subject form) |
| Role assignment retry (5/5) | Service principal not yet propagated | Wait 30s and rerun; the 15s sleep is a minimum |
| `MissingSubscription` on `az role assignment create` (Git Bash) | MSYS rewrites `/subscriptions/...` to a Windows path | Prefix `MSYS_NO_PATHCONV=1` |
| `MissingSubscription` on `az role assignment create` (B2B guest) | Guest lacks tenant context for the write | Assign the role in Bicep: [oidc-bicep.md](oidc-bicep.md) |
| `Cannot delete identity` | Federated credential still exists | Delete the federated credential first, then the identity |
