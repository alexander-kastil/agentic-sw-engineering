---
name: create-wi
description: Automate creation of Azure DevOps workload identity federation service connections. Use this when users need to create or delete Azure service connections with workload identity federation.
license: MIT
---

# Azure Workload Identity Federation Automation

This skill automates the creation and deletion of Azure DevOps service connections using workload identity federation (WIF) with managed identities. This enables secure, passwordless authentication from Azure DevOps pipelines to Azure resources.

## Overview

Workload identity federation (WIF) is a secure authentication method that uses OpenID Connect (OIDC) to establish trust between Azure DevOps and Azure managed identities. Instead of managing secrets, this approach uses federated credentials to allow Azure DevOps to authenticate to Azure resources.

### Key Benefits

- **No secrets management**: No keys, certificates, or connection strings to rotate
- **OIDC-based**: Industry-standard OpenID Connect protocol
- **Federated trust**: Direct trust between Azure DevOps and Entra ID
- **Automatic issuer sync**: Scripts automatically detect and sync Azure DevOps generated issuer/subject

## Creating a Workload Identity Service Connection

### Prerequisites

- Azure CLI with `azure-devops` extension installed
- Access to Azure subscription where resources will be created
- Project configured in Azure DevOps

### Available Scripts

Two scripts are provided for maximum flexibility. Scripts are located in the demos folder:

**Script Location**: `demos/03-release-strategy/01-release-pipelines/01-service-connections/`

#### PowerShell Version (Windows)

```powershell
cd demos/03-release-strategy/01-release-pipelines/01-service-connections
.\create-workload-identity.ps1
```

- **Resource Group**: `az400-dev`
- **Managed Identity**: `wi-az400`
- **Best for**: Windows development environments, PowerShell automation workflows

#### Bash Version (Linux/WSL)

```bash
cd demos/03-release-strategy/01-release-pipelines/01-service-connections
bash create-workload-identity.azcli
```

- **Resource Group**: `az400-bash`
- **Managed Identity**: `wi-az400-bash`
- **Best for**: Linux/WSL environments, cross-platform CI/CD pipelines, shell script integration

#### Custom Resource Group

Both scripts support custom resource group names by modifying the script variables or by passing parameters for the PowerShell version.

### What the Scripts Do

1. **Resource Creation**
   - Creates an Azure resource group in West Europe region
   - Creates a managed identity with system-assigned access

2. **Service Principal Propagation**
   - Waits for the service principal backing the managed identity to be available (10 retry attempts, 10-second intervals)
   - Required because Azure resources are eventually consistent

3. **Role Assignment**
   - Assigns the Contributor role to the managed identity at the resource group scope
   - Handles eventual consistency with retry logic (5 retry attempts, 5-second intervals)

4. **Azure DevOps Service Connection Creation**
   - Creates a service connection in Azure DevOps using the REST API (v7.1-preview)
   - Configures workload identity federation with proper authorization scheme
   - Associates the connection with the Azure DevOps project

5. **Automatic Issuer/Subject Detection**
   - Queries the created service connection to retrieve the auto-generated OIDC issuer and subject
   - Azure DevOps generates these values automatically; they cannot be customized via API
   - Issuer format: `https://login.microsoftonline.com/{tenantId}/v2.0`
   - Subject pattern: `/eid1/c/pub/t/.../service-connection-id`

6. **Federated Credential Sync**
   - Creates or updates the federated credential to match the auto-generated Azure DevOps values
   - This establishes the trust between Azure DevOps and the managed identity
   - Critical step: without this, Azure DevOps cannot authenticate

7. **Service Sharing**
   - Shares the service connection with all Azure DevOps pipelines in the project
   - Enables any pipeline to use this connection for Azure authentication

### Important Notes

**Issuer and Subject Handling**: The scripts use a two-step process:

1. Create the service connection (Azure DevOps auto-generates issuer/subject)
2. Query the service connection (get actual values)
3. Create/update federated credential (match to actual values)

This ensures the federated credential always matches what Azure DevOps expects, even if the service generates different values than anticipated.

**Project Reference**: The service connection payload requires both project ID and name in the `serviceEndpointProjectReferences` array. Scripts automatically look up the project ID.

## Deleting a Workload Identity Service Connection

When you need to clean up resources, use the delete scripts. They handle the correct deletion order to avoid dependency errors.

### Available Delete Scripts

Both delete scripts are located in the demos folder:

**Script Location**: `demos/03-release-strategy/01-release-pipelines/01-service-connections/`

#### PowerShell Delete Script

```powershell
cd demos/03-release-strategy/01-release-pipelines/01-service-connections
.\delete-workload-identity.ps1
```

#### Bash Delete Script

```bash
cd demos/03-release-strategy/01-release-pipelines/01-service-connections
bash delete-workload-identity.sh
```

### Deletion Order

The scripts follow this critical order to avoid dependency blocks:

1. **Delete Federated Credential** (from managed identity)
   - Must be deleted first; Azure blocks service connection deletion while federated credentials exist
   - Error if skipped: "Cannot delete this service connection while federated credentials exist"

2. **Delete Azure DevOps Service Connection**
   - Removes the connection from the project
   - Must follow federated credential deletion

3. **Delete Role Assignments**
   - Removes the Contributor role from the managed identity
   - Can be done after service connection deletion

4. **Delete Managed Identity**
   - Removes the managed identity resource
   - Safe to delete after role assignments are removed

5. **Optionally Delete Resource Group** (interactive)
   - Scripts prompt for confirmation before deleting the resource group
   - Non-blocking; resource group retained if user declines

## Common Scenarios

### Scenario 1: Set up new Azure DevOps service connection for development

1. Run the create script (PowerShell or Bash)
2. Verify the service connection appears in Azure DevOps Project Settings → Service connections
3. Verify federated credential was created in Entra ID (Azure Portal → Managed Identities → Select identity → Federated credentials)
4. Test the connection by running a sample pipeline

### Scenario 2: Clean up test resources

1. Run the delete script (PowerShell or Bash)
2. Optionally confirm resource group deletion
3. Verify deletion in Azure Portal and Azure DevOps UI

### Scenario 3: Migrate from service principal auth to workload identity federation

1. Create new workload identity service connection using this skill
2. Test it in a new pipeline or test environment
3. Verify authentication works without secrets
4. Delete old service principal-based connections
5. Update all pipelines to use the new workload identity connection

### Scenario 4: Maintain separate connections for different environments (dev/test/prod)

1. Run create script with custom environment suffix: `wi-az400-test`, `wi-az400-prod`
2. Verify each connection is isolated and shared appropriately
3. Use environment-specific connections in respective pipelines

## Troubleshooting

### Service Connection Creation Fails

**Error**: "Following fields in the service connection are not expected: workloadIdentityFederationAudience"

**Cause**: Attempting to set custom issuer/subject values that Azure DevOps doesn't support

**Solution**: The scripts don't set custom values; they query and sync auto-generated ones. Verify script execution completed all steps.

### Service Connection Deletion Blocked

**Error**: "Cannot delete this service connection while federated credentials for app {...} exist in Entra tenant"

**Cause**: Federated credential exists but deletion script was interrupted or only partially executed

**Solution**: Run the delete script again; it will delete the federated credential first, then the service connection.

### Service Principal Not Available

**Warning**: "Waiting for service principal propagation... (10/10)"

**Cause**: Azure service principal hasn't replicated across regions yet (eventual consistency)

**Solution**: Scripts include retry logic with 10-second wait times; usually resolves automatically. If persists, wait 5 minutes and retry script execution.

### Role Assignment Fails

**Warning**: "Retrying role assignment... (5/5)"

**Cause**: Role assignment propagation delay or permission issue

**Solution**: Verify your Azure account has sufficient permissions to assign roles at the subscription level. Scripts retry 5 times with 5-second intervals.

## Environment Variables / Customization

Scripts use hardcoded values for a standard deployment:

- **Subscription ID**: `cd091145-5ea2-4703-ba5d-41063b1d4308`
- **DevOps Organization**: `integrationsonline`
- **Project**: `az-400`
- **Region**: `westeurope`
- **Contributor Role ID**: `b24988ac-6180-42a0-ab88-20f7382dd24c`

To customize for a different environment, edit the script variables at the top before execution.

## Related Documentation

- [Workload Identity Federation on Microsoft Learn](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation)
- [Azure DevOps Service Connections](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/connect-to-azure?view=azure-devops)
- [Azure DevOps CLI Documentation](https://learn.microsoft.com/en-us/azure/devops/cli/service-endpoint?view=azure-devops)
- [Azure Role-Based Access Control (RBAC)](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles)
