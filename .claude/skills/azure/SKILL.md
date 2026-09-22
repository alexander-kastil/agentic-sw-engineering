---
name: azure
description: >
  Everything Azure from the CLI and from CI/CD: provision resources with `az`/Bicep, wire
  passwordless identity (GitHub Actions OIDC, Azure DevOps WIF, Entra app registrations in
  Bicep), deploy Static Web Apps / App Service / Container Apps / ACR, run Azure SQL (provision,
  free tier, Managed Identity auth, EF Core SQLite-to-SQL migration, .bacpac publish) and Azure
  Database for PostgreSQL Flexible Server (Entra passwordless auth, roles, group sync,
  troubleshooting, SDK), and operate a customer's Entra tenant and subscription as a B2B guest.
  Read the ONE matching reference under `references/`; never load them all.
  Triggers on: azure cli, az command, azcli script, provision azure resources, tear down azure,
  key vault, role assignment, MissingSubscription, MissingSubscriptionRegistration Microsoft.Sql,
  deploy to azure, setup ci/cd, azure deploy, github actions deploy, passwordless github actions
  deploy, github oidc azure, azure/login workload identity, oidc, workload identity, federated
  credential bicep, app registration bicep, graph bicep extension, azd app registration, set azure
  github secrets, create wif, azure devops service connection, workload identity federation,
  service connection delete, deploy.json, 2-tier deployment, static web app, azure static web apps,
  swa cli, swa init, staticwebapp.config.json, swa local development, azure functions api in swa,
  deploy static web app from github actions, swa deployment token, app service deploy, azure app
  service, azure container apps, container apps deploy, azure container registry, acr build push,
  azure sql, provision azure sql, add sql server, create azure sql, free tier sql, free sql tier, free sql
  database, shared sql server, sql admin group, sql firewall rule, azure sql migration, sqlite to
  azure sql, migrate to azure sql, migrate sqlite, switch ef core provider, EF Core SQL Server,
  UseSqlServer, sql server, sqlserver, GP_S_Gen5_1, data migration, sqlite data, varbinary, cors
  override, standalone migrator, managed identity sql, deploy migrated backend, publish db online,
  update online db, sync database to azure, restore db online, online db is stale, bacpac,
  passwordless for postgres, entra id postgres, azure ad postgres authentication, postgres managed
  identity, migrate postgres to passwordless, pgaadauth, postgres group sync, postgres permissions,
  postgres connection fails, manage customer tenant, access customer azure from cli, switch azure
  tenant, cross-tenant az cli, manage another tenant, guest admin azure cli, global administrator, global admin elevation, elevate access, keep
  my default subscription, invite guest admin, customer tenant onboarding, budget alert.
---

# Azure

Router. Pick the ONE leaf that matches the task, read it, work from it. Do not read the whole set.

Replaces the retired skills `azure-cli`, `azure-deploy`, `azure-postgres`, `azure-sql`,
`azure-static-web-apps`, `azure-github-oidc-bicep`, `create-wif`, `setup-deploy-2-tier`,
`manage-customer-tenant`, `add-sql-server`, `publish-db-online`.

Real values (subscription IDs, tenant IDs, client IDs, passwords, connection strings): the repo's
`credentials.json` / `config.json` (git-ignored). Never inline them.

## Task -> leaf

| Task | Leaf |
|---|---|
| Write or review an `az` automation script: `.azcli` file shape, naming, capture patterns, RBAC, Key Vault, teardown | [cli-conventions.md](references/cli-conventions.md) |
| Stand up a full Angular SWA + .NET App Service free-tier app end to end (sequence, topology, both workflows) | [deploy-2tier.md](references/deploy-2tier.md) |
| Deploy a static UI to Azure Static Web Apps: provision, `swa init`/`staticwebapp.config.json`, local emulation, Functions API, OIDC CI/CD + the mandatory deployment-token step | [deploy-swa.md](references/deploy-swa.md) |
| Deploy a .NET API to App Service Free (F1) with `dotnet publish` + `azure/webapps-deploy@v2` | [deploy-appservice.md](references/deploy-appservice.md) |
| Deploy a container from ACR to Azure Container Apps (create-or-update, re-run safe) | [deploy-aca.md](references/deploy-aca.md) |
| Build and push a per-service Docker image to Azure Container Registry | [deploy-acr.md](references/deploy-acr.md) |
| Passwordless GitHub Actions deploy via `az` CLI: user-assigned managed identity, federated credential, RBAC, `azure/login@v2`, subject claims | [oidc-github-actions.md](references/oidc-github-actions.md) |
| Same, declared as code: Entra app registration + service principal + federated credential in Bicep via the Microsoft Graph extension, `bicepconfig.json` | [oidc-bicep.md](references/oidc-bicep.md) |
| Create or delete an **Azure DevOps** service connection using WIF with a user-assigned managed identity (auto-generated issuer/subject sync) | [devops-wif.md](references/devops-wif.md) |
| Provision a shared Azure SQL logical server and free-tier databases from the CLI (provider registration, `--use-free-limit`, single-Entra-admin, firewall) | [sql-provision.md](references/sql-provision.md) |
| Declare an Azure SQL server + free-tier database in Bicep | [sql-bicep.md](references/sql-bicep.md) |
| Connect to Azure SQL with `Authentication=Active Directory Default` (Managed Identity, no passwords) and grant DB roles | [sql-auth.md](references/sql-auth.md) |
| Move a .NET EF Core app from SQLite to Azure SQL: csproj, provider switch, migrations, type mapping, data copy, standalone migrator | [sql-efcore-migration.md](references/sql-efcore-migration.md) |
| Publish the local SQL Server DB over its online counterpart via `.bacpac` (export, staging import, swap) | [sql-publish-bacpac.md](references/sql-publish-bacpac.md) |
| Enable Entra ID passwordless auth on PostgreSQL Flexible Server: developer access, managed identities, migration off passwords | [postgres-passwordless.md](references/postgres-passwordless.md) |
| Grant/template PostgreSQL permissions for Entra principals (`pgaadauth_create_principal`, readonly/readwrite/admin SQL) | [postgres-permissions.md](references/postgres-permissions.md) |
| Map Entra groups to PostgreSQL roles, `pgaadauth.enable_group_sync` ON vs OFF | [postgres-group-sync.md](references/postgres-group-sync.md) |
| Diagnose PostgreSQL Entra auth/connection failures (role missing, stale token, username mismatch, DNS, NSG) | [postgres-troubleshooting.md](references/postgres-troubleshooting.md) |
| Connect to PostgreSQL with an Entra token from app code (Python / TS / .NET, `DefaultAzureCredential`) | [postgres-sdk.md](references/postgres-sdk.md) |
| Operate an existing customer tenant + subscription from the CLI as a B2B guest: cross-tenant login, two permission planes, `MissingSubscription`, Global Admin elevation | [tenant-access.md](references/tenant-access.md) |
| First-time customer onboarding: guest invite, Entra directory roles, Azure RBAC bootstrap, budget alerts, cleanup | [tenant-onboard-admin.md](references/tenant-onboard-admin.md) |

## Pick the identity path

| Consumer | Path | Leaf |
|---|---|---|
| GitHub Actions, set up with `az` | user-assigned managed identity + federated credential, `azure/login@v2` | [oidc-github-actions.md](references/oidc-github-actions.md) |
| GitHub Actions, declared as code | Entra app registration + federated credential in Bicep (Graph extension) | [oidc-bicep.md](references/oidc-bicep.md) |
| Azure DevOps pipelines | service connection with WIF; issuer/subject are generated by ADO and must be synced back | [devops-wif.md](references/devops-wif.md) |

## Scripts

| Script | Does |
|---|---|
| `scripts/postgres/az-commands.sh` | Copy/paste `az postgres flexible-server` command bank (Entra admin management and friends) |
| `scripts/postgres/setup-user.sh` | `<resource-group> <server-name> <user-upn> <database> <permission-level>` (readonly\|readwrite\|admin): Entra user access |
| `scripts/postgres/setup-group.sh` | `<resource-group> <server-name> <group-name> <database> <permission-level> [enable-sync]`: group access, `enable-sync` default `false` |
| `scripts/postgres/setup-managed-identity.sh` | `<resource-group> <server-name> <identity-name> <identity-resource-group> <database> <permission-level>`: managed-identity access |
| `scripts/postgres/migrate-to-entra.sh` | `<resource-group> <server-name>`: migrate existing roles from password auth to Entra ID |

## Templates

| Template | Used by |
|---|---|
| `templates/deploy.json` | Deployment metadata (ResourceGroup, Location, WIF, GitHubRepo, SWA, AppService) read by [deploy-2tier.md](references/deploy-2tier.md), [deploy-swa.md](references/deploy-swa.md), [deploy-appservice.md](references/deploy-appservice.md), [deploy-aca.md](references/deploy-aca.md), [deploy-acr.md](references/deploy-acr.md), [devops-wif.md](references/devops-wif.md) |
| `templates/publish-db-online.config.json` | Per-project parameters for [sql-publish-bacpac.md](references/sql-publish-bacpac.md); copy to `.claude/skills/azure/config/publish-db-online.json` (git-ignored, may hold a password) |
