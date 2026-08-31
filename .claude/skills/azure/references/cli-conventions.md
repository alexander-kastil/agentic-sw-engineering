# Azure CLI conventions

House style for `az` automation scripts: file shape, naming, capture patterns, RBAC, Key Vault, teardown.

Real values (subscription IDs, tenant IDs, passwords): the repo's `credentials.json` / `config.json` (git-ignored).

## File extension

New Azure CLI files: `.azcli`, never `.sh`. Same bash, but `.azcli` signals intent and activates run-line tooling in the Azure CLI Tools VS Code extension. Existing `.sh` Azure scripts: leave the extension alone unless asked.

## Shell

Bash + `az`. No PowerShell wrappers unless the task is Windows-specific and Bash cannot do it.

## Naming

| Rule | Detail |
|---|---|
| Case | camelCase for env, resource group, location, resource identifiers |
| Length | short: `grp`, `loc`, `vault`, not `resourceGroup`, `location`, `keyVaultName` |
| Composition | interpolate off a shared `$env` suffix |
| Validation | check target resource constraints first (storage: lowercase, 3-24 chars, no specials; same for ACR, key vaults, other restricted types) |

Resource-group prefix for course/demo scripts: `<course>-<module>-<topic>-$env`.

## Script structure

- All variables declared at the top.
- `az` order: resource group, then extensions, then dependent resources.
- Explicit names and parameters over defaults or inferred values.
- `$(...)` for command substitution.
- Teardown at the bottom, guarded by a `# Do not execute` marker so the file can be sourced safely.

## Style

- No inline comments narrating single commands.
- One-line section markers allowed between logically distinct stages (role assignments, secret seeding, teardown). Max ~8 words.
- No error handling unless requested.
- No extra documentation inside the script.

## Variable block

```bash
env=prod
grp=az204-m07-secure-solutions-$env
loc=westeurope
vault=foodvault-$env
server=foodserver-$env
```

## Flag style

Short flags: `-n` name, `-g` resource group, `-l` location, `-o` output.

```bash
az group create -n $grp -l $loc
az keyvault create -l $loc -n $vault -g $grp --sku Standard
```

Long flags (`--vault-name`, `--name`, `--value`, `--query`, `--scope`) only when no short form exists or the short form hurts readability on compound flags.

## Capturing output

`$(...)` + `--query` + `-o tsv` for a single value. Always pair `--query` with `-o tsv` when feeding another command.

```bash
userId=$(az ad signed-in-user show --query id -o tsv)
miObjectId=$(az identity show -g $grp -n $miName --query principalId -o tsv)
user=$(az keyvault secret show --vault-name $vault --name "DBUser" --query value -o tsv)
pwd=$(az keyvault secret show --vault-name $vault --name "DBPassword" --query value -o tsv)
```

`-o table` for human inspection only; never capture table output into a variable.

```bash
az keyvault secret list --vault-name $vault -o table
```

## Role assignments

Capture the principal first, assign with explicit `--scope`, break long commands with `\`.

```bash
az role assignment create \
  --role "Key Vault Secrets Officer" \
  --assignee-object-id $userId \
  --scope $kvId
```

- Prefer `--assignee-object-id` over `--assignee`: avoids Graph lookups and ambiguity.
- Quote role names (they contain spaces).
- `--scope` = full resource ID, captured earlier via `az keyvault show --query id -o tsv` or equivalent.

## Key Vault secrets

```bash
az keyvault secret set --vault-name $vault --name "conSQLite"   --value "Data Source=./food.db"
az keyvault secret set --vault-name $vault --name "DBUser"      --value "azlabadmin"
az keyvault secret set --vault-name $vault --name "DBPassword"  --value "<password>"
```

Composed values: capture each secret into a variable, then assemble.

```bash
user=$(az keyvault secret show --vault-name $vault --name "DBUser" --query value -o tsv)
pwd=$(az keyvault secret show --vault-name $vault --name "DBPassword" --query value -o tsv)
az keyvault secret set --vault-name $vault --name "conSQLServer" \
  --value "Server=tcp:$server.database.windows.net,1433;Database=$db;User ID=$user;Password='$pwd';Encrypt=true;Connection Timeout=30;"
```

- Single-quote passwords inside a composed string to survive special characters.
- Quote secret names even without spaces.

## Teardown

```bash
# Do not execute
az keyvault delete -n $vault
az keyvault purge -n $vault
```

Key Vault needs both `delete` and `purge` for permanent removal (soft-delete default).

## Provisioning lessons

| Situation | Rule |
|---|---|
| Shared stateful resources (SQL server, storage account, key vault) | Check existing subscriptions for one to reuse before provisioning. Databases go on `integrations-sql.database.windows.net`, VS Enterprise sub `<subscription-id>`, rg `rg-integrations-sql` (see [sql-provision.md](sql-provision.md)). Create databases, not servers. Ask if unsure. |
| `az role assignment create` fails `MissingSubscription` (even with correct context) | Fall back to `az rest --method PUT` against `https://management.azure.com/{scope}/providers/Microsoft.Authorization/roleAssignments/{newGuid}?api-version=2022-04-01` |
| Resource group deleted | Role assignments die with their scope; after recreating an RG, re-grant and verify with `az role assignment list --assignee <appId>` |
| Serverless Azure SQL auto-pause | First connection after idle takes up to ~60 s to resume; retry once on timeout |
| SPA redirect URIs | No `az ad app` flag; PATCH `spa.redirectUris` via `az rest` and always send the FULL list (the call replaces it) |
| GUID needed in a script | `uuidgen` is missing in git bash on Windows; use `python -c "import uuid; print(uuid.uuid4())"` |

## Pitfalls

- Referencing an undeclared variable (`$miName`, `$kvId`, `$db` appear unset in the source Key Vault demo). Grep `$varName` against the declaration block before running.
- Missing `-o tsv` in command substitution yields JSON and breaks downstream consumers.
- `--assignee` with a UPN containing `#` (guest accounts) fails silently. Resolve to object ID first.
- Reusing a deleted Key Vault name inside the soft-delete retention window without `purge` fails with a name conflict.

## Worked example

```bash
env=prod
grp=az204-m07-secure-solutions-$env
loc=westeurope
vault=foodvault-$env

az group create -n $grp -l $loc
az keyvault create -l $loc -n $vault -g $grp --sku Standard

kvId=$(az keyvault show -n $vault -g $grp --query id -o tsv)
userId=$(az ad signed-in-user show --query id -o tsv)

# Assign Key Vault Secrets Officer role to yourself
az role assignment create \
  --role "Key Vault Secrets Officer" \
  --assignee-object-id $userId \
  --scope $kvId

az keyvault secret set --vault-name $vault --name "DBUser"     --value "azlabadmin"
az keyvault secret set --vault-name $vault --name "DBPassword" --value "<password>"

az keyvault secret list --vault-name $vault -o table

# Do not execute
az keyvault delete -n $vault
az keyvault purge -n $vault
```

## See also

[oidc-github-actions.md](oidc-github-actions.md), [tenant-access.md](tenant-access.md), [sql-provision.md](sql-provision.md)
