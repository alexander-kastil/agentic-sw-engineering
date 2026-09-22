# Diagnose PostgreSQL Entra auth failures

Connection and auth failures against Azure Database for PostgreSQL with Microsoft Entra ID. Placeholders `<rg>`, `<server>`, `<object-id>`, `<subscription-id>`, `<client-id>`, `<client-secret>`, `<tenant-id>`, `<nsg-name>`: real values live in the repo's credentials.json / config.json (git-ignored).

## Quick diagnostic checklist

| Check | Command | Expected |
|---|---|---|
| Role exists in database | `SELECT * FROM pgaadauth_list_principals(false);` | Your role appears |
| Token is fresh | `az account get-access-token` timestamp | `expiresOn` in the future |
| Username format | Compare with role name in DB | Exact match (case-sensitive) |
| Network connectivity | `nslookup login.microsoftonline.com` | Resolves to IP |
| DNS for Graph API | `nslookup graph.microsoft.com` | Resolves to IP |
| Entra admin exists | `az postgres flexible-server microsoft-entra-admin list` | At least one admin |

## Errors

### `role "user@domain.com" does not exist`

Cause: no PostgreSQL role for that Entra identity.

```bash
export PGPASSWORD=$(az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv)
psql "host=<server>.postgres.database.azure.com user=admin@domain.com dbname=postgres sslmode=require"
```

```sql
SELECT * FROM pgaadauth_create_principal('user@domain.com', false, false);

SELECT * FROM pgaadauth_create_principal_with_oid('my-identity', '<object-id>', 'service', false, false);
```

First form: by name, for users. Second: by object ID, for managed identities / service principals.

### `password authentication failed for user "user@domain.com"`

Cause: token expired, invalid, or wrong format.

```bash
export PGPASSWORD=$(az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv)
```
```powershell
$env:PGPASSWORD = az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv
```
Then verify:
```bash
az account get-access-token --resource-type oss-rdbms --query expiresOn -o tsv
az account show --query user.name -o tsv
```

### `FATAL: password authentication failed` (no username in error)

Cause: username format does not match the database role.

1. `SELECT * FROM pgaadauth_list_principals(false);`
2. Use the exact, case-sensitive role name:
```bash
psql "host=<server>.postgres.database.azure.com user=Developer@Company.com dbname=mydb sslmode=require"
```
3. Guest users need the full UPN with `#EXT#`:
```bash
psql "host=<server>.postgres.database.azure.com user=guest_user_example.com#EXT#@tenant.onmicrosoft.com dbname=mydb sslmode=require"
```

### `could not connect to server: Connection timed out`

Cause: firewall/network block or wrong server name.

```bash
az postgres flexible-server show --resource-group <rg> --name <server> --query fullyQualifiedDomainName -o tsv
az postgres flexible-server firewall-rule list --resource-group <rg> --name <server>
az network nsg rule list --resource-group <rg> --nsg-name <nsg-name>
nslookup <server>.postgres.database.azure.com
nslookup login.microsoftonline.com
nslookup graph.microsoft.com
```

With a private endpoint, the NSG must allow outbound to the `AzureActiveDirectory` service tag.

### `SSL SYSCALL error: Connection reset by peer`

Cause: TLS/SSL issue, usually network.

- `sslmode=require` must be in the connection string.
- Check for a proxy/firewall intercepting TLS.
- Private endpoint: route table needs `AzureActiveDirectory` -> `Internet`.

### Token acquisition fails

Cause: not logged into Azure CLI, or wrong account.

```bash
az login
az account set --subscription <subscription-id>
az account show
az login --service-principal -u <client-id> -p <client-secret> --tenant <tenant-id>
```

### `Cannot validate Microsoft Entra ID user because its name isn't unique`

Cause: multiple Azure AD objects share the display name. Use the OID form:

```sql
SELECT * FROM pgaadauth_create_principal_with_oid('unique-role-name', '<object-id>', 'user', false, false);
```
Get the OID with `az ad user show --id user@domain.com --query id -o tsv`.

### Group member cannot connect (group sync enabled)

Cause: sync has not run yet (every 30 minutes). See [postgres-group-sync.md](postgres-group-sync.md).

```sql
SELECT * FROM pgaadauth_sync_roles_for_group_members();
SELECT * FROM pgaadauth_list_principals(false);
```
```bash
az ad group member list --group "Group Name" --query "[].userPrincipalName" -o tsv
```

### Managed identity cannot connect from an Azure-hosted app

Cause: app not using the Azure Identity SDK correctly.

```bash
az containerapp identity show --name <app> --resource-group <rg>
az webapp identity show --name <app> --resource-group <rg>
```
- Role name must match exactly what was created in PostgreSQL.
- App code must use the Azure Identity SDK (see [postgres-sdk.md](postgres-sdk.md)).
- Compare MI object ID with the DB:
```bash
az identity show --name <identity> --resource-group <rg> --query principalId -o tsv
psql -c "SELECT * FROM pgaadauth_list_principals(false);"
```

## Diagnostic command reference

```bash
az postgres flexible-server microsoft-entra-admin list \
  --resource-group <rg> \
  --server-name <server>
```

```sql
SELECT * FROM pgaadauth_list_principals(false);

\du
\l
\dp

SELECT * FROM information_schema.role_table_grants WHERE grantee = 'user@domain.com';
```

`\du` lists roles, `\l` shows database grants, `\dp` shows table permissions.

```bash
az account get-access-token --resource-type oss-rdbms
```
The accessToken is a JWT; decode at jwt.io to verify claims.

```bash
nslookup <server>.postgres.database.azure.com
nslookup login.microsoftonline.com
nslookup graph.microsoft.com

nc -zv <server>.postgres.database.azure.com 5432
telnet <server>.postgres.database.azure.com 5432
```

```bash
az postgres flexible-server parameter show \
  --resource-group <rg> \
  --server-name <server> \
  --name pgaadauth.enable_group_sync
```

## Still failing

1. Enable diagnostic logging on the PostgreSQL server in the Azure Portal.
2. Check Azure Monitor logs for authentication failures.
3. Verify RBAC: `Contributor` or specific PostgreSQL roles may be required.
4. Contact support with the diagnostic output above.

See also [postgres-passwordless.md](postgres-passwordless.md), [postgres-permissions.md](postgres-permissions.md).
