# Azure SQL authentication: Managed Identity over passwords

Connect to Azure SQL with `Authentication=Active Directory Default`. No username, no password, in any connection string. Guard the JWT key at startup. No secrets in committed files.

Real values: the repo's `credentials.json` / `config.json` (git-ignored).

## How `Authentication=Active Directory Default` resolves

| Environment | Identity used |
| --- | --- |
| Local dev | `az login` credential |
| App Service (production) | System-assigned managed identity |

After deployment the SQL server's Entra ID admin must grant the managed identity (or the developer account) database roles. Nothing else is required.

## appsettings.json (committed, zero secrets)

```json
{
  "ConnectionStrings": {
    "Family": "Server=tcp:<server-fqdn>;Authentication=Active Directory Default;Database=<db-name>;Encrypt=True;"
  },
  "Jwt": {
    "Issuer": "<app-name>",
    "Audience": "<audience>",
    "Key": ""
  }
}
```

## appsettings.Development.json (committed, dev-only values OK)

Option A: Azure SQL from local dev. Requires `az login` with an account holding DB roles, and the Azure SQL firewall must allow the local IP.

```json
{
  "Jwt": {
    "Key": "dev-only-change-in-prod-via-user-secrets-or-keyvault-32chars"
  },
  "ConnectionStrings": {
    "Family": "Server=tcp:<server-fqdn>;Authentication=Active Directory Default;Database=<db-name>;Encrypt=True;"
  }
}
```

Option B: local SQL Server, fully offline. Use when Azure SQL is not yet deployed or unreachable.

```json
{
  "Jwt": {
    "Key": "dev-only-change-in-prod-via-user-secrets-or-keyvault-32chars"
  },
  "ConnectionStrings": {
    "Family": "Server=.;Database=<db-name>-dev;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

Local SQL Server uses Windows auth, no credentials. `dotnet run` auto-applies EF migrations and creates the DB on first startup.

## JWT key startup guard

`Program.cs`, before `builder.Build()`. Fail fast instead of starting with broken auth.

```csharp
var rawKey = jwtSection["Key"];
if (string.IsNullOrEmpty(rawKey))
    throw new InvalidOperationException("Jwt:Key must be set via user-secrets or environment variable.");
var jwtKey = Encoding.UTF8.GetBytes(rawKey);
```

## Production App Service settings

Set in the App Service configuration blade or via CLI. Never in committed files.

| Setting | Value |
| --- | --- |
| `ConnectionStrings__Family` | `Server=tcp:<server-fqdn>;Authentication=Active Directory Default;Database=<db-name>;Encrypt=True;` |
| `Jwt__Key` | 32+ character secret |

## Key Vault: SQL admin credentials

Store immediately after Bicep deployment.

```bash
az keyvault secret set --vault-name <kv-name> --name sql-<project>-admin-password --value "<password>"
az keyvault secret set --vault-name <kv-name> --name sql-<project>-admin-login --value "<login>"
```

## Siblings

- [sql-provision.md](sql-provision.md), [sql-bicep.md](sql-bicep.md): create the server and DB, set the Entra admin.
- [sql-efcore-migration.md](sql-efcore-migration.md): provider switch and schema apply.
- [postgres-passwordless.md](postgres-passwordless.md): same principle on PostgreSQL.
