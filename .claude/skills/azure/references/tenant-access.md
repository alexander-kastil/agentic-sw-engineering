# Operate a Customer's Entra Tenant and Subscription as an External Identity

Run a customer's Entra tenant + Azure subscription from your CLI as an external `alexander.kastil@integrations.at` identity (B2B guest), without disturbing your home tenant (`integrations.at`) or its default subscription.

Real values (tenant IDs, subscription IDs, object IDs): the repo's `credentials.json` / `config.json` (git-ignored).

First-time onboarding (guest invite, directory roles, RBAC bootstrap, budget): [tenant-onboard-admin.md](tenant-onboard-admin.md). This file covers running and managing access **after** the identity exists.

## Two permission planes

Both matter; Global Admin covers only one.

| Plane | Top Role | Controls |
|---|---|---|
| Microsoft Entra ID | Global Administrator | Users, groups, app registrations, tenant settings |
| Azure RBAC | Owner / Contributor | Subscriptions, resource groups, all Azure resources |

A guest who is Global Administrator has **zero** Azure resource rights until an Azure RBAC role is assigned at subscription (or higher) scope.

A guest has a **different object ID** in the customer tenant than your home object ID. UPN shape: `alexander.kastil_integrations.at#EXT#@<customer>.onmicrosoft.com`. Use the customer-tenant **object ID** for CLI role assignments, never the email.

Role definition IDs worth recognizing:

- `b24988ac-6180-42a0-ab88-20f7382dd24c` = Contributor
- `18d7d88d-d35e-4fb5-a5c3-7773c20a72d9` = User Access Administrator
- `8e3af657-a8ff-443c-a75c-2fe8c4bcb635` = Owner
- `62e90394-69f5-4237-9190-012177145e10` = Global Administrator (directory role)

## The MissingSubscription gotcha

Most cross-tenant CLI failures are **not** permission gaps. `az role assignment list --scope /subscriptions/<id>` fails `MissingSubscription` when the CLI has no ARM token context for that tenant.

- Pass `--subscription <id>` so the CLI selects the right tenant token.
- Required even for listing/reading; `--scope` alone is not enough.
- Tenant-root scope (`/`) cannot be read by `az role assignment list` at all. Use the ARM REST API (see Cleanup).

## Step 1: sign into the customer tenant

Does not log you out of home; the CLI caches tokens for both.

```bash
az login --tenant <tenant-id>
```

Resolve the guest object ID and UPN as the customer tenant sees you:

```bash
az ad signed-in-user show --query "{name:displayName, id:id, upn:userPrincipalName}" -o json
```

## Step 2: restore your home default subscription

`az login --tenant` flips the default to a customer subscription. You do not need it as default to manage the customer.

```bash
az account set --subscription <home-subscription-id>
```

Then target the customer per command with `--subscription <subscription-id>`.

## Step 3: verify your access

```bash
az rest --method GET \
  --url "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments?\$filter=principalId eq '<guest-oid>'" \
  --query "value[].roleDefinitionId" -o tsv

az role assignment list \
  --subscription <subscription-id> \
  --assignee <guest-oid> \
  --query "[].{Role:roleDefinitionName, Scope:scope}" -o table
```

RBAC present (typically `Contributor` + `User Access Administrator`) means done: go to Day-to-Day. RBAC missing: use [tenant-onboard-admin.md](tenant-onboard-admin.md) or the elevation path below.

## Step 4: elevation (only when you have Global Admin but no RBAC)

Global Administrator can self-grant `User Access Administrator` at root `/`, then assign a real subscription role. High severity: run deliberately, clean up after.

```bash
az rest --method post \
  --url "https://management.azure.com/providers/Microsoft.Authorization/elevateAccess?api-version=2016-07-01"

az login --tenant <tenant-id>

az role assignment create --assignee-object-id <guest-oid> --assignee-principal-type User \
  --role "Contributor" --scope /subscriptions/<subscription-id>
az role assignment create --assignee-object-id <guest-oid> --assignee-principal-type User \
  --role "User Access Administrator" --scope /subscriptions/<subscription-id>
```

Step 2 (`az login --tenant`) is a token refresh so the new root role is picked up.

## Step 5: clean up the root elevation

Root `/` is unreadable via `az role assignment list`; find and delete through ARM REST.

```bash
az rest --method get \
  --url "https://management.azure.com/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01&\$filter=principalId+eq+'<guest-oid>'" \
  --query "value[?properties.scope=='/'].id" -o tsv

az rest --method delete \
  --url "https://management.azure.com<root-assignment-id>?api-version=2022-04-01"
```

## Day-to-day management

Default stays on your home subscription; target the customer per command.

```bash
az group list --subscription <subscription-id> -o table
az group create -n rg-example -l westeurope --subscription <subscription-id>
az role assignment list --subscription <subscription-id> --assignee <guest-oid> -o table
```

Two rules that prevent every cross-tenant error:

1. Always pass `--subscription <subscription-id>` (not `--scope` alone).
2. Stale token: re-run `az login --tenant <tenant-id>`.

## Graph API in a non-default tenant

`az ad *` commands (and `az rest` against Graph) always run in the **active account's** tenant; there is no `--tenant` flag on them. To read or mutate another tenant's directory without flipping the default subscription, mint a tenant-scoped Graph token and call Graph directly:

```bash
TOKEN=$(az account get-access-token --tenant <tenant-id> --resource-type ms-graph \
  --query accessToken -o tsv)

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/applications(appId='<client-id>')"

curl -s -X DELETE -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/applications/<objectId>"
```

App lookup is by **appId**; a 404 means the app lives in a different tenant. Delete is by **object id**, and it also removes the enterprise app (service principal); `204` = done.

Two practical uses: locating which tenant actually hosts a given clientId (probe tenants until the 404s stop), and cleaning up an app registration created in the wrong tenant (2026-07 incident: an admin-SPA app registration landed in integrations.at instead of the customer tenant; see `add-mixed-auth` -> "Incident pattern: app registration in the wrong tenant").

## Role-assignment writes: the harder gotcha

Listing cross-tenant is the documented `MissingSubscription` case. **Writing** as a guest is worse: `az role assignment create --scope /subscriptions/<sub>/resourceGroups/<rg>` can fail `MissingSubscription` **even with the customer subscription active and `--subscription` passed**, while plain ARM writes in the same shell (`az group create`, `az sql server create`) succeed. The guest's ARM token works for resource writes but not always for the Authorization plane. (Off purely cached tokens, many resource writes instead fail `SubscriptionNotFound` until an interactive login: next section.)

Fixes, preferred first:

1. **Do the role assignment in Bicep.** A subscription-scoped `az deployment sub create` runs in the correct customer-tenant ARM context, so a `Microsoft.Authorization/roleAssignments` resource (RG or sub scope, `principalType: 'ServicePrincipal' | 'User'`) applies cleanly where the CLI refuses. Reliable path for granting an app-registration SP or guest a role.
2. CLI fallback: `az login --tenant <tenant-id>` to refresh, then retry.

**Listing without a Graph lookup:** `az role assignment list --assignee <oid>` resolves `<oid>` in the *active* tenant's directory and errors `Cannot find user or service principal in graph database` when your home tenant is default. List by scope and filter on the raw id instead, no Graph call:

```bash
az role assignment list --scope "/subscriptions/<subscription-id>/resourceGroups/<rg>" \
  --query "[?principalId=='<guest-oid>'].{role:roleDefinitionName, scope:scope}" -o table
```

## Resource writes off cached tokens: SubscriptionNotFound

Repeatable trap: customer subscription **active** but **without** running `az login --tenant <tenant-id>` this session (relying on cached tokens from an earlier sign-in), direct `az` resource **writes** fail with **`SubscriptionNotFound`**: `az storage account create`, `az sql db update`, `az storage account check-name`. Everything else off the same cached tokens works:

| Off cached tokens | Works? |
|---|---|
| reads (`az group list`, `az sql db show`) | yes |
| Graph writes (`az ad app create`, `az ad group member add`, `oauth2PermissionGrant`) | yes: cached refresh token mints the Graph token silently (`az account get-access-token --tenant <t> --resource https://graph.microsoft.com` succeeds without a prompt) |
| SQL data plane (pyodbc / sqlpackage with an `az account get-access-token` token, when in the SQL admin group) | yes |
| ARM **deployments** (`azd provision`, `az deployment sub/group create`) | yes: they run in the correct customer ARM context |
| direct `az ...create/update` on a resource | no: `SubscriptionNotFound` |

Fix: one interactive `az login --tenant <tenant-id>`, then direct CLI writes succeed (restore your home default with `az account set` afterwards). When running unattended, prefer IaC (`azd` / `az deployment`) over direct CLI writes to avoid it.

## Related

- [tenant-onboard-admin.md](tenant-onboard-admin.md): first-time onboarding, guest invite, directory roles, RBAC bootstrap, budget alerts, cleanup.
- [cli-conventions.md](cli-conventions.md)
- [oidc-bicep.md](oidc-bicep.md): role assignments via Bicep.
