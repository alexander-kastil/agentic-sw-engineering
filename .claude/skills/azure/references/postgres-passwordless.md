# Passwordless Entra ID auth for Azure Database for PostgreSQL Flexible Server

ALWAYS use passwordless Entra ID auth for production workloads.

Two-layer mapping: **Azure Identity -> PostgreSQL Role -> Database Permissions**.

Real values (tenant/subscription/server names): the repo's `credentials.json` / `config.json` (git-ignored).

## Use when

- Enable Entra ID auth on a PostgreSQL Flexible Server
- Grant a developer access with their Azure identity
- Give an Azure-hosted app (Container Apps, App Service, Functions) managed-identity access
- Manage access via Entra groups
- Migrate password auth -> Entra ID
- Debug Entra auth/connection failures

## Identity types

| Identity type | Use case | SQL function |
|---|---|---|
| User | Developer access, interactive queries | `pgaadauth_create_principal` |
| Group | Team-based access management | `pgaadauth_create_principal_with_oid` |
| Service Principal | Application authentication | `pgaadauth_create_principal_with_oid` |
| Managed Identity | Azure-hosted app passwordless access | `pgaadauth_create_principal_with_oid` |

Object types for `pgaadauth_create_principal_with_oid`: `'user'` (incl. guests), `'group'`, `'service'` (service principals + managed identities).

## Tooling

MCP (preferred, when Azure MCP enabled) via `azure__postgres`:

| Command | Purpose |
|---|---|
| `postgres_server_list` | List PostgreSQL servers in subscription |
| `postgres_database_list` | List databases on a server |
| `postgres_database_query` | Execute SQL (role creation, permissions) |
| `postgres_server_param_get` | Get server parameter (e.g. group sync) |
| `postgres_server_param_set` | Set server parameter |

CLI fallback (`az postgres flexible-server`):

```bash
az postgres flexible-server list --output table
az postgres flexible-server db list --server-name SERVER -g RG
az postgres flexible-server show --name SERVER -g RG
az postgres flexible-server create --name SERVER -g RG --location REGION --admin-user ADMIN --version 16
```

Engine versions: PostgreSQL 11, 12, 13, 14, 15, 16 (16 recommended).

## Helper scripts

Now at `../scripts/postgres/`.

| Script | Usage |
|---|---|
| `az-commands.sh` | Copy/paste reference: token acquisition, identity lookups, Entra admin management |
| `setup-user.sh` | `./setup-user.sh <resource-group> <server-name> <user-upn> <database> <permission-level>` (levels: `readonly`, `readwrite`, `admin`) |
| `setup-managed-identity.sh` | `./setup-managed-identity.sh <resource-group> <server-name> <identity-name> <identity-resource-group> <database> <permission-level>` (levels: `readonly`, `readwrite`, `admin`) |
| `setup-group.sh` | `./setup-group.sh <resource-group> <server-name> <group-name> <database> <permission-level> [enable-sync]` (levels: `readonly`, `readwrite`, `admin`; `enable-sync`: true/false, default false) |
| `migrate-to-entra.sh` | `./migrate-to-entra.sh <resource-group> <server-name>` |

## Core workflow

1. **Check auth status.** List Entra admins; empty output = no Entra admin configured yet.
2. **Add first Entra admin** via Azure CLI. This enables Entra auth.
3. **Connect as Entra admin**: get an access token, pass it to `psql` as the password.
4. **Create PostgreSQL roles** for other identities with the `pgaadauth_*` functions.
5. **Grant permissions** with `GRANT` statements.

Enable auth before creating an admin, otherwise admin create/list fails:

```bash
az postgres flexible-server microsoft-entra-admin list \
  --resource-group <resource-group> \
  --server-name <server-name>

OBJECT_ID=$(az ad signed-in-user show --query id -o tsv)

az postgres flexible-server update \
  --subscription <subscription-id> \
  --resource-group <resource-group> \
  --name <server-name> \
  --microsoft-entra-auth Enabled

az postgres flexible-server microsoft-entra-admin create \
  --resource-group <resource-group> \
  --server-name <server-name> \
  --display-name "admin@domain.com" \
  --object-id $OBJECT_ID \
  --type User

az postgres flexible-server microsoft-entra-admin delete \
  --resource-group <resource-group> \
  --server-name <server-name> \
  --object-id <object-id>
```

Token (valid 5-60 min, acquire fresh per connection):

```bash
az account get-access-token --resource-type oss-rdbms
```

SQL role functions and `SECURITY LABEL` syntax: [postgres-permissions.md](postgres-permissions.md).
GRANT templates: [postgres-permissions.md](postgres-permissions.md).

## Patterns

### Pattern 1: developer user access

Need: developer UPN (e.g. `developer@company.com`), target database, permission level (read-only / read-write / admin). Script: `../scripts/postgres/setup-user.sh`.

### Pattern 2: managed identity for applications

Need: managed identity name + resource group, target database, permission level.

1. Get managed identity object ID.
2. Create PostgreSQL role with `pgaadauth_create_principal_with_oid`.
3. Grant permissions.
4. Configure the app to use the Azure Identity SDK ([postgres-sdk.md](postgres-sdk.md)).

Script: `../scripts/postgres/setup-managed-identity.sh`.

### Pattern 3: group-based access control

Need: group display name + object ID, group-sync decision (`pgaadauth.enable_group_sync`), permission level.

| Mode | Behavior | Use case |
|---|---|---|
| OFF (default) | Members use group name as username | Simple setup, no individual tracking |
| ON | Individual member roles auto-created | Audit trails, per-user permissions |

Script: `../scripts/postgres/setup-group.sh`. Details: [postgres-group-sync.md](postgres-group-sync.md).

### Pattern 4: troubleshooting connection failures

Errors: `role "user@domain.com" does not exist` (role not created), `password authentication failed` (token expired/invalid), `FATAL: password authentication failed` (wrong username format), `could not connect to server` (network/firewall). See [postgres-troubleshooting.md](postgres-troubleshooting.md).

### Pattern 5: migration from password auth

1. Enable "PostgreSQL and Microsoft Entra authentication" mode (parallel auth).
2. Map existing roles to Entra identities with `SECURITY LABEL`.
3. Test Entra auth for each migrated role.
4. Disable passwords: `ALTER ROLE "username" PASSWORD NULL`.
5. Switch to "Microsoft Entra authentication only" mode.

Script: `../scripts/postgres/migrate-to-entra.sh`.

## Service tiers

| Tier | vCores | Memory | Use case |
|---|---|---|---|
| Burstable | 1-20 | 0.5-4 GB/vCore | Dev/test, low traffic |
| General Purpose | 2-64 | 4 GB/vCore | Most production workloads |
| Memory Optimized | 2-64 | 8 GB/vCore | High-memory workloads |

Start Burstable for dev/test, scale up as needed.

## Security best practices

| Practice | Recommendation |
|---|---|
| Least privilege | Minimum required permissions; no admin roles for apps |
| Use groups | Manage access via Entra groups |
| Managed identity | Always for Azure-hosted apps |
| MFA for admins | Set `isMfa=true` on admin roles if tenant supports optional MFA |
| Token handling | Never store tokens; acquire fresh before each connection |
| Audit access | `pgaadauth_list_principals` to review who has access |
| Private endpoint | Production: private endpoint + NSG rule for the `AzureActiveDirectory` service tag |

## Common issues

| Issue | Cause | Solution |
|---|---|---|
| `role does not exist` | Role not created in database | Run `pgaadauth_create_principal` or `pgaadauth_create_principal_with_oid` |
| `password authentication failed` | Token expired (5-60 min validity) | `az account get-access-token --resource-type oss-rdbms` |
| `permission denied` | Role exists, lacks permissions | Run `GRANT` statements: [postgres-permissions.md](postgres-permissions.md) |
| Connection timeout | Firewall blocking access | `az postgres flexible-server firewall-rule create` |
| Network timeout | Private endpoint missing NSG rule | Add outbound rule for `AzureActiveDirectory` service tag |
| Username case mismatch | Entra names are case-sensitive | Use exact case from Azure AD |
| Guest user login fails | Wrong UPN format | Full UPN with the `#EXT#` tag from Azure AD |

## Portal link format

```
https://portal.azure.com/#@{tenant-domain}/resource/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.DBforPostgreSQL/flexibleServers/{server-name}/overview
```

## Siblings

- [postgres-permissions.md](postgres-permissions.md) - role functions + GRANT/REVOKE templates
- [postgres-group-sync.md](postgres-group-sync.md) - group sync configuration
- [postgres-troubleshooting.md](postgres-troubleshooting.md) - connection and auth diagnostics
- [postgres-sdk.md](postgres-sdk.md) - PostgreSQL client + Azure Identity SDK snippets
- [cli-conventions.md](cli-conventions.md) - general `az` CLI conventions
