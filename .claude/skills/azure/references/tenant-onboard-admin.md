# First-Time Onboarding: Invite the Guest, Grant Directory Roles, Bootstrap RBAC

Onboard `alexander.kastil@integrations.at` (or any external integrations.at identity) as a privileged admin into a customer's Entra ID + Azure subscription: guest invite, Entra directory roles, Azure RBAC, budget alerts, cleanup.

Real values (tenant IDs, subscription IDs, object IDs, customer emails): the repo's `credentials.json` / `config.json` (git-ignored). Day-to-day operation after onboarding: [tenant-access.md](tenant-access.md).

## Key concepts

Two independent permission planes, both required:

| Plane | Top Role | Controls |
|---|---|---|
| Microsoft Entra ID | Global Administrator | Users, app registrations, identity, tenant settings |
| Azure RBAC | Owner | Subscriptions, resource groups, all Azure resources |

A Global Admin has **zero** Azure resource rights by default.

External identities appear as B2B guests with UPN `alexander.kastil_integrations.at#EXT#@customertenant.onmicrosoft.com`. Always use **object ID**, never email, for CLI role assignments on guests.

## Prerequisites

- Global Administrator access to the customer tenant (or the customer admin performs the invite)
- Azure Cloud Shell or local CLI authenticated to the customer tenant
- Customer's Entra Tenant ID and Subscription ID

## Phase 1: invite external user as guest

Already a guest: skip to Phase 2.

Portal: `https://entra.microsoft.com` -> Identity -> Users -> All users -> New user -> Invite external user. Email `alexander.kastil@integrations.at`, send invite. The user must click **Accept** in the invitation email before roles take effect.

```bash
az ad user invite \
  --invited-user-email-address alexander.kastil@integrations.at \
  --invited-user-display-name "Alexander Kastil" \
  --send-invitation-message true
```

Checkpoint: user appears in All users, type **Guest**, state **Accepted**.

## Phase 2: get guest object ID

Guests cannot be referenced by email in CLI role assignments.

```bash
az ad user list \
  --filter "userPrincipalName eq 'alexander.kastil_integrations.at#EXT#@CUSTOMERTENANT.onmicrosoft.com'" \
  --query "[0].id" \
  --output tsv
```

Replace `CUSTOMERTENANT` with the customer's tenant domain. Save the GUID as `$OID`.

## Phase 3: assign Entra directory roles

Application Administrator (recommended minimum): create/manage app registrations, enterprise apps, managed identities.

```bash
az rest --method POST \
  --url "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments" \
  --headers "Content-Type=application/json" \
  --body "{
    \"principalId\": \"$OID\",
    \"roleDefinitionId\": \"9b895d92-2cd3-44c7-9d02-a6ac2d5ea5c3\",
    \"directoryScopeId\": \"/\"
  }"
```

Global Administrator (only if full directory control is required):

```bash
az rest --method POST \
  --url "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments" \
  --headers "Content-Type=application/json" \
  --body "{
    \"principalId\": \"$OID\",
    \"roleDefinitionId\": \"62e90394-69f5-4237-9190-012177145e10\",
    \"directoryScopeId\": \"/\"
  }"
```

Verify:

```bash
az rest --method GET \
  --url "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments?\$filter=principalId eq '$OID'" \
  --query "value[].roleDefinitionId" \
  --output tsv
```

Role definition IDs:

- `62e90394-69f5-4237-9190-012177145e10` = Global Administrator
- `9b895d92-2cd3-44c7-9d02-a6ac2d5ea5c3` = Application Administrator

## Phase 4: create Azure subscription (if none exists)

Portal: `https://portal.azure.com` -> Subscriptions -> + Add. Subscription name e.g. `customername`, customer's billing account, plan Microsoft Azure Plan, Review + create -> Create. Note the Subscription ID from the overview page.

Not visible after creation: sign out and back in, or go direct to `https://portal.azure.com/TENANT_ID#view/Microsoft_Azure_Billing/SubscriptionsBlade`.

## Phase 5: enable the elevation toggle

Required when you are Global Admin but have no Azure RBAC yet.

Portal: `https://entra.microsoft.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Properties` -> **Access management for Azure resources** -> **Yes** -> Save. Sign out and back in for it to take effect.

Turn it off again after Phase 6 (Phase 8).

## Phase 6: assign Azure RBAC roles

Recommended split: customer owner = **Owner**; external consultant = **Contributor** + **User Access Administrator**. Consultant gets full resource creation and managed-identity role assignment; customer keeps sole Owner (billing control, subscription cancellation).

```bash
SUB_ID="<subscription-id>"
OID="<guest-object-id>"

az role assignment create \
  --assignee-object-id "$OID" \
  --assignee-principal-type User \
  --role "Contributor" \
  --scope /subscriptions/$SUB_ID

az role assignment create \
  --assignee-object-id "$OID" \
  --assignee-principal-type User \
  --role "User Access Administrator" \
  --scope /subscriptions/$SUB_ID
```

Owner to the customer admin:

```bash
CUSTOMER_OID="<customer-admin-object-id>"

az role assignment create \
  --assignee-object-id "$CUSTOMER_OID" \
  --assignee-principal-type User \
  --role "Owner" \
  --scope /subscriptions/$SUB_ID
```

Get the customer admin object ID:

```bash
az ad user list \
  --filter "userPrincipalName eq '<customer-admin-upn>'" \
  --query "[0].id" \
  --output tsv
```

Verify:

```bash
az role assignment list \
  --scope /subscriptions/$SUB_ID \
  --output json \
  --query "[].{Principal:principalName, Role:roleDefinitionName}"
```

Expected: customer admin -> Owner; Alexander -> Contributor; Alexander -> User Access Administrator.

## Phase 7: set budget alert

Cost alerts go to the customer only, not the consultant.

```bash
az rest --method PUT \
  --url "https://management.azure.com/subscriptions/$SUB_ID/providers/Microsoft.Consumption/budgets/monthly-budget?api-version=2021-10-01" \
  --headers "Content-Type=application/json" \
  --body "{
    \"properties\": {
      \"category\": \"Cost\",
      \"amount\": 25,
      \"timeGrain\": \"Monthly\",
      \"timePeriod\": {
        \"startDate\": \"$(date +%Y-%m-01)\",
        \"endDate\": \"$(date -d '+1 year' +%Y-%m-01)\"
      },
      \"notifications\": {
        \"actual_GreaterThan_80_Percent\": {
          \"enabled\": true,
          \"operator\": \"GreaterThan\",
          \"threshold\": 80,
          \"contactEmails\": [\"CUSTOMER_EMAIL\"],
          \"thresholdType\": \"Actual\"
        },
        \"actual_GreaterThan_100_Percent\": {
          \"enabled\": true,
          \"operator\": \"GreaterThan\",
          \"threshold\": 100,
          \"contactEmails\": [\"CUSTOMER_EMAIL\"],
          \"thresholdType\": \"Actual\"
        }
      }
    }
  }"
```

Replace `CUSTOMER_EMAIL`; adjust `amount` as agreed with the customer.

## Phase 8: cleanup

Remove the accidental Owner role from the consultant (the Phase 5 elevation toggle may have auto-assigned it):

```bash
az role assignment delete \
  --assignee-object-id "$OID" \
  --role "Owner" \
  --scope /subscriptions/$SUB_ID
```

Turn off the elevation toggle: `https://entra.microsoft.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Properties` -> **Access management for Azure resources** -> **No** -> Save.

## Final state checklist

| Item | Expected |
|---|---|
| Alexander, Entra | Application Administrator (minimum) or Global Administrator |
| Alexander, Azure | Contributor + User Access Administrator |
| Customer admin, Azure | Owner |
| Elevation toggle | Off (No) |
| Budget | Set, alerts to customer email |
| Alexander Owner role | Removed |

## Common issues

| Symptom | Fix |
|---|---|
| `Cannot find user or service principal in graph database for email` | guests must be referenced by object ID, not email: Phase 2 |
| "No subscriptions found" after login | sign out and back in, or the subscription does not exist yet: Phase 4 |
| Elevation toggle shows the customer admin's name, not yours | normal: it shows who currently has elevation. Flip to Yes to grant yourself the temporary root-scope access needed to assign roles |
| `az consumption budget create` fails with unrecognized arguments | the `az consumption` group is preview with limited parameters: use `az rest` against the Management API (Phase 7) |
