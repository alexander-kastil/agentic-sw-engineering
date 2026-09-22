# Provision a Shared Azure SQL Logical Server and Free-Tier Databases (CLI)

Logical server is free; the free offer applies **per database**. Works in your own subscription or in a customer tenant accessed as a B2B guest.

Real values (subscription IDs, server names, admin login, password): the repo's `credentials.json` / `config.json` (git-ignored). Never inline them.

Cross-tenant CLI access setup: [tenant-access.md](tenant-access.md). Bicep equivalent: [sql-bicep.md](sql-bicep.md). Auth/connection-string detail: [sql-auth.md](sql-auth.md).

## Cross-tenant rules (subscription in another tenant)

| Rule | Why |
|---|---|
| Pass `--subscription <subscription-id>` on every resource command | `--scope` alone gives `MissingSubscription` |
| `az account set --subscription <subscription-id>` before any `az ad user` / `az ad group` | Graph acts on the **active** subscription's tenant; restore your home default after |
| Use object IDs, never emails, for guest identities | Guest email lookup is unreliable |

## Step 0: register Microsoft.Sql (new subscriptions)

New subscription has no providers registered. First `az sql server create` fails with `MissingSubscriptionRegistration: ... namespace 'Microsoft.Sql'`. Register once, wait for `Registered`.

```bash
SUB="<SUBSCRIPTION_ID>"
az provider register --namespace Microsoft.Sql --subscription "$SUB" --wait
az provider show --namespace Microsoft.Sql --subscription "$SUB" --query registrationState -o tsv
```

Still `Registering`? Poll:

```bash
for i in $(seq 1 20); do
  STATE=$(az provider show --namespace Microsoft.Sql --subscription "$SUB" --query registrationState -o tsv)
  echo "$i: $STATE"; [ "$STATE" = "Registered" ] && break; sleep 15
done
```

## Step 1: resource group + logical server

Admin password: 8-128 chars, three of (upper, lower, digit, symbol), must not contain the login name. Store in a secret store after creation.

```bash
SUB="<SUBSCRIPTION_ID>"; RG="<rg>"; LOC="westeurope"; SERVER="<globally-unique-server-name>"

az group create -n "$RG" -l "$LOC" --subscription "$SUB" -o table

az sql server create -g "$RG" -n "$SERVER" -l "$LOC" \
  --admin-user <admin-user> --admin-password "<password>" \
  --subscription "$SUB" -o table
```

FQDN: `<SERVER>.database.windows.net`. Rotate password:

```bash
az sql server update -g "$RG" -n "$SERVER" --admin-password "<password>" --subscription "$SUB"
```

## Step 2: administrators (single-admin constraint)

A SQL server has exactly **one** Entra administrator slot: one user **or** one group. For multiple admins, set a **security group** and manage membership.

```bash
# Create the group and add members (run with the customer tenant as the active subscription)
GROUP_ID=$(az ad group create --display-name "sql-admins" --mail-nickname "sql-admins" --query id -o tsv)
az ad group member add --group "$GROUP_ID" --member-id "<USER_OID_1>"
az ad group member add --group "$GROUP_ID" --member-id "<USER_OID_2>"

# Set the group as the server's Entra admin (replaces any single-user admin)
az sql server ad-admin create -g "$RG" --server-name "$SERVER" \
  --display-name "sql-admins" --object-id "$GROUP_ID" --subscription "$SUB" -o table
```

Add/remove admins later by editing membership, no server change:

```bash
az ad group member add --group "$GROUP_ID" --member-id "<NEW_OID>" --subscription "$SUB"
```

Do **not** pass `--enable-ad-only-auth`: keeping the SQL login alive gives dual auth (Entra for people, SQL login for tools).

## Step 3: firewall rules

```bash
# Your current client IP (management access)
MYIP="$(curl -s https://api.ipify.org)"
az sql server firewall-rule create -g "$RG" --server "$SERVER" \
  -n "client-$(echo $MYIP | tr '.' '-')" \
  --start-ip-address "$MYIP" --end-ip-address "$MYIP" --subscription "$SUB" -o table

# Allow Azure-hosted services (any Azure resource, any tenant): convenient for dev, broad for prod
az sql server firewall-rule create -g "$RG" --server "$SERVER" \
  -n "AllowAzureServices" --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0 \
  --subscription "$SUB" -o table
```

`0.0.0.0` opens the server to all Azure services across tenants. Dev convenience only; prefer Private Endpoint or per-app outbound IPs in production.

## Step 4: free-tier databases (per database)

Free offer per database: **100,000 vCore-seconds + 32 GB data + 32 GB backup per month, free for the life of the subscription**, max **10 free databases per subscription**. Must be General Purpose, Serverless, Gen5, max 4 vCores / 32 GB.

```bash
az sql db create -g "$RG" -s "$SERVER" -n "<project-db>" \
  -e GeneralPurpose --compute-model Serverless -f Gen5 -c 4 \
  --use-free-limit true --free-limit-exhaustion-behavior AutoPause \
  --subscription "$SUB" -o table
```

- Serverless requires `-c` (capacity). Without it: *"When creating a serverless database, please pass in edition, family, and capacity parameters through -e -f -c"*. Use `-c 4` (free-tier max); serverless auto-scales down and auto-pauses, so headroom is not billed.
- `AutoPause`: pauses the DB until next month when the free limit is hit (stays truly free).
- `BillOverUsage`: stays online, bills overage at standard GP-serverless rates.
- **Region lock:** the first region used for a free database in a subscription applies to all free databases in that subscription and cannot be changed later.

## Step 5: passwordless app access via the admin group (zero T-SQL)

Normal path is a contained user (`CREATE USER ... FROM EXTERNAL PROVIDER`), which needs a T-SQL connection as Entra admin: painful non-interactively (classic `sqlcmd -G` opens a browser; token auth needs go-sqlcmd or `Invoke-Sqlcmd -AccessToken`).

Shortcut: add the app's managed identity to the SQL **admin group** from Step 2. Any member, including a managed identity, then authenticates as admin, passwordlessly.

```bash
# Prefer a USER-assigned identity so its principalId is known before SQL setup
APP_MI_PRINCIPAL_ID=$(az identity show -g "$APP_RG" -n "<id-app>" --query principalId -o tsv --subscription "$SUB")
az ad group member add --group "$GROUP_ID" --member-id "$APP_MI_PRINCIPAL_ID"
# Verify (MIs/service principals do not render in the member-list table, use check):
az ad group member check --group "$GROUP_ID" --member-id "$APP_MI_PRINCIPAL_ID" --query value -o tsv
```

Connection string (user-assigned identity named explicitly):

```text
Server=tcp:<server>.database.windows.net,1433;Initial Catalog=<db>;Authentication=Active Directory Managed Identity;User Id=<MI_CLIENT_ID>;Encrypt=True;TrustServerCertificate=False;
```

- On App Service set it as a **connection string** of type `SQLAzure`; it overrides any password-bearing value in `appsettings.json` at runtime.
- EF Core apps that migrate/seed on startup create and populate the schema on first connect; a `200` from a data endpoint proves the whole passwordless chain.
- Tradeoff: group membership grants the identity server-admin. For least privilege, drop it from the group and use Step 6.

## Step 6: least-privilege contained user (T-SQL over an access token)

Old ODBC `sqlcmd` cannot do token auth. Use PowerShell `System.Data.SqlClient` with `.AccessToken` (works in pwsh out of the box, cross-subscription fine).

```bash
TOKEN=$(az account get-access-token --resource https://database.windows.net/ --query accessToken -o tsv)
pwsh -NoProfile -Command "
  \$c = New-Object System.Data.SqlClient.SqlConnection
  \$c.ConnectionString = 'Server=tcp:<server>.database.windows.net,1433;Database=<db>;Encrypt=True'
  \$c.AccessToken = '$TOKEN'
  \$c.Open()
  \$cmd = \$c.CreateCommand()
  \$cmd.CommandText = @'
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = '<app-name>')
  CREATE USER [<app-name>] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [<app-name>];
ALTER ROLE db_datawriter ADD MEMBER [<app-name>];
'@
  \$cmd.ExecuteNonQuery(); \$c.Close()"
```

- User name = the app's **resource name** (identity display name), not the principalId GUID.
- `db_datareader` + `db_datawriter` cover normal CRUD. `db_owner` only if the app runs EF Core **migrations** on startup (needs schema-create rights); see [sql-efcore-migration.md](sql-efcore-migration.md).

### `Active Directory Default` connection string

```text
Server=tcp:<server>.database.windows.net,1433;Initial Catalog=<db>;Authentication=Active Directory Default;Encrypt=True;
```

`Microsoft.Data.SqlClient` resolves `Active Directory Default` to the managed identity on App Service and to the Azure CLI login locally, so one string works in both places (local dev usually keeps a local SQL Server `Trusted_Connection` string instead). For a user-assigned identity prefer the explicit `Authentication=Active Directory Managed Identity;User Id=<MI_CLIENT_ID>` form from Step 5.

## Verification

```bash
az sql server show -g "$RG" -n "$SERVER" --subscription "$SUB" --query fullyQualifiedDomainName -o tsv
az sql server ad-admin list -g "$RG" --server-name "$SERVER" --subscription "$SUB" -o table
az sql server firewall-rule list -g "$RG" --server "$SERVER" --subscription "$SUB" \
  --query "[].{Name:name, Start:startIpAddress, End:endIpAddress}" -o table
az sql db list -g "$RG" -s "$SERVER" --subscription "$SUB" --query "[].{Name:name, Sku:currentSku.name}" -o table
```

## Common issues

| Symptom | Cause / Fix |
|---|---|
| `MissingSubscriptionRegistration ... Microsoft.Sql` | New subscription: Step 0, wait for `Registered`. |
| `MissingSubscription` on list/read | Pass `--subscription <id>`, not `--scope` alone. |
| `When creating a serverless database, please pass in ... -e -f -c` | Add `-c 4` to `az sql db create`. |
| App can't get a passwordless token | Add the app's MI principalId to the SQL admin **group** (Step 5); verify with `az ad group member check`. |
| `Login failed for user '<token-identified principal>'` | Contained MSI user missing in the DB: run Step 6 against the app's resource name. |
| `CREATE USER ... FROM EXTERNAL PROVIDER` fails | T-SQL connection not authenticated as the server's Entra admin (check token identity). |
| Works locally, fails deployed | Local `az login` resolved `Active Directory Default`; the MSI has no DB user: run Step 6. |
| First request times out after idle | Serverless auto-pause resume (~60 s on free tier): retry once. |
| Cannot resolve a guest user by email | Use object ID: `az ad user list --filter "mail eq '<email>'" --query "[0].id" -o tsv`. |
| Only one of two admins keeps access | Single Entra admin slot: set a **group** (Step 2), not individual users. |
| Group create / lookup hits the wrong directory | `az ad` uses the active subscription's tenant: `az account set` to the customer subscription first. |
