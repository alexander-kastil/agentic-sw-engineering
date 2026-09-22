# Publish a local SQL Server database over its online counterpart via .bacpac

Make the online database an exact copy of the local dev database. No per-table patching: export local to `.bacpac`, import as staging, swap.

Project-agnostic. All project values are parameters resolved in Stage 0.

Real values: the repo's `credentials.json` / config JSON (git-ignored). Never copy a connection string with a password into a doc, prompt, or commit.

## Config discovery order

1. `.claude/skills/azure/config/publish-db-online.json` (consolidated location, preferred).
2. `.claude/skills/publish-db-online/config.json` (legacy, per-project skill folder).

First file found wins; any parameter present in it is authoritative. Missing parameters are discovered (Stage 0) and written back to the same file. Both files are git-ignored and may hold a real password, so read values only into the running command, never into output. Template: `templates/publish-db-online.config.json`.

## Config contract

| Key | Meaning | Placeholder |
| --- | --- | --- |
| `localConnectionString` | Local SQL Server connection string | `Server=.;Database=<db-name>-dev;Trusted_Connection=True;TrustServerCertificate=True;` |
| `database` | Online database name | `<db-name>` |
| `target` | Where the online DB lives | `azure` or `hetzner` |
| `authMode` | How the online DB is reached | `ActiveDirectoryDefault` or `SqlLogin` |
| `targetServer` | Online server host/FQDN | `<server-fqdn>` |
| `targetConnectionString` | Full online connection string; holds `<password>` when `authMode=SqlLogin` | see below |
| `sqlServer` | Azure SQL logical server FQDN (Azure target) | `<server-fqdn>` |
| `serverResourceGroup` | Resource group of the SQL server | `rg-sql` |
| `subscription` | Azure subscription id | `<subscription-id>` |
| `managedIdentityUsers` | Contained external users to recreate after restore, with roles | `[{ "name": "<app-name>-api", "roles": ["db_owner"] }]` |
| `serviceObjective` / `autoPauseDelay` / `minCapacity` / `maxSizeGb` | Serverless SKU settings to re-apply | `GP_S_Gen5_1` / `60` / `0.5` / `2` |
| `deployedApiBaseUrl` | Optional, end-to-end verification | `https://<app-name>-api.azurewebsites.net` |
| `backupDir` | Where bacpacs go; MUST be gitignored (bacpacs can contain secrets) | `.tools/db-backups` |

Azure target, passwordless (preferred):

```
Server=tcp:<server-fqdn>,1433;Initial Catalog=<db-name>;Authentication=Active Directory Default;Encrypt=True;Connect Timeout=60
```

Locally this resolves through the Azure CLI credential; the logged-in `az` user must be Entra admin of the server (required to create/drop/rename databases and recreate users).

`authMode=SqlLogin` (non-Azure host, e.g. a self-managed SQL box) uses a login and password from `targetConnectionString`; Stage 2/6 Azure-only steps (SKU capture, `az sql db update`, external users) do not apply.

## Stage 0: resolve configuration

1. Load the config file per the discovery order above.
2. Discover what is missing, then WRITE resolved values back so the next run skips discovery:
   - `localConnectionString`: API project's `appsettings.Development.json` connection string.
   - `sqlServer` + `database`: API's production `appsettings.json` connection string, or the App Service connection-string settings.
   - `serverResourceGroup` + `subscription`: `az sql server list --query "[?contains(fullyQualifiedDomainName, '<sqlServer>')].{rg:resourceGroup}"` across the user's subscriptions.
   - SKU settings + `managedIdentityUsers`: captured live in Stage 2 (first run: write what Stage 2 finds).
3. Confirm `backupDir` is gitignored: `git check-ignore <backupDir>` after creating it; add an ignore rule at the REPO ROOT if not.

## Stage 1: preflight

```powershell
az account show --query user.name -o tsv
az account get-access-token --resource https://database.windows.net --query expiresOn -o tsv
sqlpackage /Version
Invoke-Sqlcmd -ConnectionString "<localConnectionString>" -Query "SELECT COUNT(*) FROM __EFMigrationsHistory"
```

All must succeed.

| Failure | Action |
| --- | --- |
| Token acquisition fails | Ask the user to run `az login` themselves (interactive) |
| sqlpackage missing | `dotnet tool install -g microsoft.sqlpackage` |
| SQL error 40613 on first online connect | Serverless auto-pause resume, up to 60 s; retry up to 2 more times |

Query Azure SQL via PowerShell `Invoke-Sqlcmd -AccessToken`. ODBC sqlcmd v16 does NOT support Azure CLI auth.

## Stage 2: capture online state

Record everything the restore destroys and must be re-applied. Compare with the config file; update it if drifted.

```powershell
az sql db show -g <serverResourceGroup> -s <serverName> -n <database> --subscription <subscription> --query "{objective:currentServiceObjectiveName, autoPause:autoPauseDelay, minCapacity:minCapacity, maxBytes:maxSizeBytes}" -o json
```

```sql
SELECT dp.name, dp.type_desc, STRING_AGG(r.name, ', ') AS roles
FROM sys.database_principals dp
LEFT JOIN sys.database_role_members rm ON rm.member_principal_id = dp.principal_id
LEFT JOIN sys.database_principals r ON r.principal_id = rm.role_principal_id
WHERE dp.type IN ('E','X','S','U') AND dp.name NOT IN ('dbo','guest','INFORMATION_SCHEMA','sys')
GROUP BY dp.name, dp.type_desc;
```

## Stage 3: backup both sides

ABSOLUTE paths for `/tf:` (the shell working directory drifts between calls).

```powershell
$ts = Get-Date -Format yyyyMMdd-HHmmss
sqlpackage /a:Export /scs:"<localConnectionString>" /tf:"<repoRoot>/<backupDir>/<localDb>-$ts.bacpac"
sqlpackage /a:Export /scs:"Server=tcp:<sqlServer>,1433;Initial Catalog=<database>;Authentication=Active Directory Default;Encrypt=True;Connect Timeout=60" /tf:"<repoRoot>/<backupDir>/<database>-online-$ts.bacpac"
```

Local bacpac = restore source. Online bacpac = rollback safety net.

## Stage 4: restore to staging, verify before swapping

Import as a NEW database `<database>-staging`; sqlpackage Import requires the target not to exist.

```powershell
sqlpackage /a:Import /sf:"<repoRoot>/<backupDir>/<localDb>-$ts.bacpac" /tcs:"Server=tcp:<sqlServer>,1433;Initial Catalog=<database>-staging;Authentication=Active Directory Default;Encrypt=True;Connect Timeout=120" /p:DatabaseEdition=GeneralPurpose /p:DatabaseServiceObjective=<serviceObjective> /p:DatabaseMaximumSize=<maxSizeGb>
```

Verify staging: latest `__EFMigrationsHistory` entry matches the newest local migration file, and row counts of all user tables match local.

## Stage 5: swap (destructive)

State explicitly that this drops the production DB, then run against `master`:

```sql
DROP DATABASE [<database>];
ALTER DATABASE [<database>-staging] MODIFY NAME = [<database>];
```

## Stage 6: post-restore fixes (MANDATORY)

The new database has neither the contained external users nor the serverless settings.

```powershell
az sql db update -g <serverResourceGroup> -s <serverName> -n <database> --subscription <subscription> --auto-pause-delay <autoPauseDelay> --min-capacity <minCapacity>
```

For each entry in `managedIdentityUsers` (and anything else captured in Stage 2):

```sql
CREATE USER [<name>] FROM EXTERNAL PROVIDER;
ALTER ROLE <role> ADD MEMBER [<name>];
```

## Stage 7: verify

Never declare success without checking final state:

- `__EFMigrationsHistory`: newest entry matches newest local migration.
- Row counts of all user tables equal local.
- Contained users exist with their roles (Stage 2 query again).
- `az sql db show` reports the configured objective and auto-pause.
- If `deployedApiBaseUrl` is set: curl a data-serving endpoint, expect HTTP 200 (proves the recreated identity works).

## Cautions

- REPLACES the production database wholesale, with a short outage (drop + rename, typically well under a minute). Announce the swap before Stage 5; invoking this procedure is the authorization to perform the full replace.
- Failure after the drop: import the online safety bacpac as `<database>` with the same Import command, then re-run Stage 6.
- The local DB must not receive schema changes during export (a running local API is fine).
- Bacpacs may contain secrets stored in tables. Keep them in the gitignored `backupDir` only; never commit or upload them.
- Do not store passwords anywhere. On Azure all access paths are passwordless (Azure CLI credential locally, managed identity in Azure); `authMode=SqlLogin` is the exception and its password lives only in the git-ignored config file.

## Siblings

- [sql-auth.md](sql-auth.md): passwordless connection strings and Entra admin.
- [sql-efcore-migration.md](sql-efcore-migration.md): schema apply and row-level data copy.
