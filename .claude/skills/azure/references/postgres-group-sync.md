# Sync Entra groups to PostgreSQL roles

Group-based access control with Entra ID on Azure Database for PostgreSQL Flexible Server. Placeholders `<rg>`, `<server>`, `<group-id>`, `<object-id>`, `<subscription-id>`: real values live in the repo's credentials.json / config.json (git-ignored).

## Two modes

| Mode | Setting | Behavior | Best for |
|---|---|---|---|
| Sync disabled (default) | `pgaadauth.enable_group_sync=OFF` | Members use group name as username | Simple setups, shared audit trail |
| Sync enabled | `pgaadauth.enable_group_sync=ON` | Individual member roles auto-created | Per-user auditing, fine-grained permissions |

## Mode 1: sync disabled

Flow: create group role -> grant permissions to group -> members sign in with the **group name** -> all members share one PostgreSQL role.

```bash
GROUP_ID=$(az ad group show --group "Database Readers" --query id -o tsv)

export PGPASSWORD=$(az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv)
psql "host=<server>.postgres.database.azure.com user=admin@domain.com dbname=postgres sslmode=require"
```

```sql
SELECT * FROM pgaadauth_create_principal_with_oid('Database Readers', '<group-id>', 'group', false, false);

GRANT CONNECT ON DATABASE mydb TO "Database Readers";
GRANT USAGE ON SCHEMA public TO "Database Readers";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "Database Readers";
```

Member connection (username = group name):

```bash
export PGPASSWORD=$(az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv)
psql "host=<server>.postgres.database.azure.com user='Database Readers' dbname=mydb sslmode=require"
```

```powershell
$env:PGPASSWORD = az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv
psql "host=<server>.postgres.database.azure.com user='Database Readers' dbname=mydb sslmode=require"
```

Group names with spaces must be escaped or quoted: `user='Database Readers'` or `user=Database\ Readers`.

| Pros | Cons |
|---|---|
| Simple setup | Cannot distinguish users in audit logs |
| Instant membership effect | Cannot grant per-user permissions |
| Single role to manage | Username is the group name, not intuitive |

## Mode 2: sync enabled

Flow: create group role -> enable sync parameter -> individual roles auto-created per member -> sync runs every 30 minutes -> members sign in with their own UPN.

```bash
az postgres flexible-server parameter set \
  --resource-group <rg> \
  --server-name <server> \
  --name pgaadauth.enable_group_sync \
  --value ON

GROUP_ID=$(az ad group show --group "Database Readers" --query id -o tsv)

export PGPASSWORD=$(az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv)
psql "host=<server>.postgres.database.azure.com user=admin@domain.com dbname=postgres sslmode=require"
```

```sql
SELECT * FROM pgaadauth_create_principal_with_oid('Database Readers', '<group-id>', 'group', false, false);

GRANT CONNECT ON DATABASE mydb TO "Database Readers";
GRANT USAGE ON SCHEMA public TO "Database Readers";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "Database Readers";

SELECT * FROM pgaadauth_sync_roles_for_group_members();
```

The last statement forces sync now; otherwise wait 30 min.

Member connection (username = own UPN):

```bash
export PGPASSWORD=$(az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv)
psql "host=<server>.postgres.database.azure.com user=developer@company.com dbname=mydb sslmode=require"
```

```powershell
$env:PGPASSWORD = az account get-access-token --resource-type oss-rdbms --query accessToken -o tsv
psql "host=<server>.postgres.database.azure.com user=developer@company.com dbname=mydb sslmode=require"
```

| Pros | Cons |
|---|---|
| Individual audit trails | 30-min sync delay for new members |
| Per-user permissions possible | More roles to manage |
| Users sign in with their own name | Group role must NOT be deleted |

## Rules and limits

**Never drop the group role while sync is enabled**: it carries the member-group relationship.

```sql
DROP ROLE "Database Readers";
ALTER ROLE "Database Readers" NOLOGIN;
```

First statement breaks sync. Use the second instead when login must be blocked.

- Manual sync: `SELECT * FROM pgaadauth_sync_roles_for_group_members();`
- List synced roles: `SELECT * FROM pgaadauth_list_principals(false);`
- Permission inheritance: group grants are inherited by member roles; extra grants can go on individual member roles; revoking from the group affects all synced members.
- Nested groups are **not** supported. Only direct members sync. For hierarchy, create separate group roles.

## Switching modes

```bash
az postgres flexible-server parameter set \
  --resource-group <rg> \
  --server-name <server> \
  --name pgaadauth.enable_group_sync \
  --value ON
```

Then `SELECT * FROM pgaadauth_sync_roles_for_group_members();`

```bash
az postgres flexible-server parameter set \
  --resource-group <rg> \
  --server-name <server> \
  --name pgaadauth.enable_group_sync \
  --value OFF
```

Turning sync OFF leaves existing synced member roles in place; they are not deleted automatically.

## Troubleshooting

New group member cannot connect (sync ON):
1. Wait up to 30 min or run `SELECT * FROM pgaadauth_sync_roles_for_group_members();`
2. `az ad group member list --group "Database Readers" --query "[].userPrincipalName"`
3. `SELECT * FROM pgaadauth_list_principals(false) WHERE rolename = 'user@domain.com';`

Group login fails (sync OFF):
1. Username must be the **group name**, not an individual UPN.
2. Escape spaces: `user='Group Name'` or `user=Group\ Name`.
3. `SELECT * FROM pgaadauth_list_principals(false) WHERE principaltype = 'group';`

Membership changes not reflected:
```bash
az postgres flexible-server parameter show \
  --resource-group <rg> \
  --server-name <server> \
  --name pgaadauth.enable_group_sync
```
Sync OFF: changes are immediate (members use the group name). Sync ON: wait 30 min or run manual sync.

See also [postgres-passwordless.md](postgres-passwordless.md), [postgres-permissions.md](postgres-permissions.md), [postgres-troubleshooting.md](postgres-troubleshooting.md).
