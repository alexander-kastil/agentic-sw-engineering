# Declare Azure SQL in Bicep

IaC pattern for an Azure SQL logical server plus a free-tier database. Use when standing up Azure SQL first time or recreating infra. CLI equivalent and the gotchas (provider registration, single-Entra-admin slot, region lock, serverless `-c`): [sql-provision.md](sql-provision.md).

Real values (server name, admin login, password, object IDs): the repo's `credentials.json` / `config.json` (git-ignored).

## Template

```bicep
// Deploy: az deployment group create --resource-group <rg> \
//   --template-file infra/sql.bicep \
//   --parameters administratorLogin=<admin-user> administratorLoginPassword=<password>

@description('Name of the Azure SQL logical server.')
param serverName string = 'sql-<project-name>'

@description('Name of the Azure SQL database.')
param databaseName string = '<db-name>'

@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('SQL administrator login name.')
param administratorLogin string

@description('SQL administrator password.')
@secure()
param administratorLoginPassword string

resource sqlServer 'Microsoft.Sql/servers@2022-05-01-preview' = {
  name: serverName
  location: location
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
  }
}

resource sqlDatabase 'Microsoft.Sql/servers/databases@2022-05-01-preview' = {
  parent: sqlServer
  name: databaseName
  location: location
  sku: {
    name: 'GP_S_Gen5_1'
    tier: 'GeneralPurpose'
  }
}

resource firewallAllowAzureServices 'Microsoft.Sql/servers/firewallRules@2022-05-01-preview' = {
  parent: sqlServer
  name: 'AllowAllAzureIps'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName
output databaseName string = sqlDatabase.name

// Post-deployment: grant App Service managed identity access
// Connect to <databaseName> as SQL admin and run:
//   CREATE USER [<app-service-name>] FROM EXTERNAL PROVIDER;
//   ALTER ROLE db_datareader ADD MEMBER [<app-service-name>];
//   ALTER ROLE db_datawriter ADD MEMBER [<app-service-name>];
//   ALTER ROLE db_ddladmin ADD MEMBER [<app-service-name>];
```

## Free tier

| Property | Value |
| -------- | ----- |
| SKU name | `GP_S_Gen5_1` |
| Tier | General Purpose Serverless, 1 vCore |
| Free offer | 100,000 vCore seconds/month |
| Storage | 32 GB |
| Limit | 10 free databases per subscription |

## Post-deploy

1. Entra ID admin on the logical server:

```bash
az sql server ad-admin create \
  --server-name <name> \
  --resource-group <rg> \
  --display-name "<Name>" \
  --object-id <entra-object-id>
```

2. Store SQL admin credentials in Key Vault:

```bash
az keyvault secret set --vault-name <kv> --name sql-<project>-admin-password --value "<password>"
az keyvault secret set --vault-name <kv> --name sql-<project>-admin-login --value "<login>"
```

3. Apply the EF Core schema over a SQL auth connection string (before Managed Identity is wired up):

```bash
dotnet ef database update --connection "<sql-auth-connection-string>"
```

4. Grant managed identity DB roles with sqlcmd + Azure AD auth (`-G` uses the current `az login` credential, no password). Must be run by the SQL server's Entra ID admin:

```bash
sqlcmd -S "<server>.database.windows.net" -d <database> \
  -G -U "<entra-admin-email>" \
  -Q "CREATE USER [<app-service-name>] FROM EXTERNAL PROVIDER; ALTER ROLE db_datareader ADD MEMBER [<app-service-name>]; ALTER ROLE db_datawriter ADD MEMBER [<app-service-name>]; ALTER ROLE db_ddladmin ADD MEMBER [<app-service-name>];"
```

Verify with SQL auth:

```bash
sqlcmd -S "<server>.database.windows.net" -d <database> \
  -U <sqladmin-user> -P <password> \
  -Q "SELECT name, type_desc FROM sys.database_principals WHERE name = '<app-service-name>'"
```
