---
name: create-wi
description: Automate creation of Azure DevOps workload identity federation service connections with deployment metadata from deploy.json. Use when users need to create or delete Azure service connections with workload identity federation for secure, passwordless authentication.
license: MIT
---

# Azure Workload Identity Federation Automation

This skill automates the creation and deletion of Azure DevOps service connections using workload identity federation (WIF) with managed identities. Scripts automatically read deployment configuration from deploy.json, enabling secure, passwordless authentication from Azure DevOps pipelines to Azure resources.

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
- deploy.json file in .github directory with required deployment metadata

### Available Scripts

Scripts automatically read deployment configuration from deploy.json. Scripts are located in the demos folder:

**Script Location**: `demos/03-release-strategy/01-release-pipelines/01-service-connections/`

**Required deploy.json Fields**:

- ADOOrg: Azure DevOps organization URL
- ADOProject: Azure DevOps project name
- ResourceGroup: Azure resource group name
- WIF: Managed identity name prefix

#### PowerShell Version (Recommended)

```powershell
cd demos/03-release-strategy/01-release-pipelines/01-service-connections
.\create-workload-identity.ps1
```

- Reads ResourceGroup and WIF settings from deploy.json
- Works on Windows, Windows with WSL, and PowerShell 7+ on Linux/macOS
- Recommended default option

#### Bash Version

```bash
cd demos/03-release-strategy/01-release-pipelines/01-service-connections
bash create-workload-identity.sh
```

- Reads ResourceGroup and WIF settings from deploy.json
- Best for: Linux, macOS, and Windows with Git Bash environments

#### Custom Configuration

Scripts read from deploy.json which should be in the repository root. Edit deploy.json to customize:

- ResourceGroup: Azure resource group where managed identity is created
- WIF: Managed identity name prefix
- ADOOrg: Azure DevOps organization URL
- ADOProject: Azure DevOps project name

### What the Scripts Do

1. **Load Configuration from deploy.json**
   - Reads ResourceGroup, WIF, ADOOrg, and ADOProject from .github/deploy.json
   - Ensures deployment metadata is consistent across the project

2. **Create Resource Group**
   - Creates an Azure resource group with name from deploy.json
   - Uses westeurope region (customizable in script)

3. **Create Managed Identity**
   - Creates a managed identity with system-assigned access
   - Uses WIF prefix from deploy.json to name the identity

4. **Wait for Service Principal Propagation**
   - Pauses 15 seconds to allow service principal backing the managed identity to replicate
   - Required because Azure resources are eventually consistent

5. **Assign Contributor Role**
   - Assigns the Contributor role to the managed identity at the resource group scope
   - Enables the identity to deploy and manage resources

6. **Create Azure DevOps Service Connection**
   - Creates a service connection in Azure DevOps using the REST API (v7.1-preview)
   - Uses ADOOrg and ADOProject from deploy.json
   - Configures workload identity federation with proper authorization scheme
   - Associates the connection with the Azure DevOps project

7. **Detect Auto-Generated Issuer and Subject**
   - Queries the created service connection to retrieve the auto-generated OIDC issuer and subject
   - Azure DevOps generates these values automatically; they cannot be customized via API
   - Parses the response to extract workloadIdentityFederationIssuer and workloadIdentityFederationSubject

8. **Create Federated Credential**
   - Creates federated credential in the managed identity
   - Uses the auto-generated issuer and subject from the service connection
   - Establishes trust between Azure DevOps and the managed identity
   - Critical step: without this, Azure DevOps cannot authenticate

9. **Share Service Connection**
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

Delete scripts are located in the demos folder:

**Script Location**: `demos/03-release-strategy/01-release-pipelines/01-service-connections/`

#### Bash Delete Script (Recommended)

```bash
cd demos/03-release-strategy/01-release-pipelines/01-service-connections
bash delete-workload-identity.sh
```

#### PowerShell Delete Script

```powershell
cd demos/03-release-strategy/01-release-pipelines/01-service-connections
.\delete-workload-identity.ps1
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

## Configuration via deploy.json

Scripts automatically read metadata from `.github/deploy.json` in the repository root. This eliminates the need to hardcode values and ensures consistency across the project.

**Required Fields in deploy.json**:

```json
{
    "ResourceGroup": "your-resource-group-name",
    "WIF": "your-managed-identity-name-prefix",
    "ADOOrg": "https://dev.azure.com/your-org",
    "ADOProject": "your-project-name"
}
```

**Example Configuration**:

```json
{
    "ResourceGroup": "rg-agentic-sw-engineering",
    "WIF": "wi-agentic-sw",
    "ADOOrg": "https://dev.azure.com/integrationsonline",
    "ADOProject": "agentic-sw-engineering"
}
```

To customize for a different environment, edit `.github/deploy.json` before running the scripts. The scripts will automatically apply these values during execution.

## Related Documentation

- [Workload Identity Federation on Microsoft Learn](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation)
- [Azure DevOps Service Connections](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/connect-to-azure?view=azure-devops)
- [Azure DevOps CLI Documentation](https://learn.microsoft.com/en-us/azure/devops/cli/service-endpoint?view=azure-devops)
- [Azure Role-Based Access Control (RBAC)](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles)
