---
name: import-pipeline
description: Automate the import and execution of Azure DevOps pipelines from YAML files using deployment metadata. Use this when users need to import pipelines to Azure DevOps, run them, and fix any errors that occur during execution.
license: MIT
---

# Azure DevOps Pipeline Import and Execution

This skill automates the import of Azure DevOps pipelines from YAML files using deployment metadata, executes them, diagnoses errors, and fixes issues.

## Overview

This skill demonstrates a complete DevOps workflow for importing and running pipelines in Azure DevOps. It uses Azure CLI to interact with Azure DevOps APIs and includes error diagnosis and fixing capabilities.

### Key Benefits

- **Metadata-driven**: Uses deployment metadata (.github/deploy.json) for configuration
- **Automated import**: Imports pipelines using Azure CLI
- **Error handling**: Diagnoses and fixes pipeline execution errors
- **Documentation**: Uses Microsoft Learn MCP to reference official documentation

## Deployment Metadata Format

The skill expects a `deploy.json` file in the skills root with the following structure:

```json
{
    "Service Connection": "wi-az400-dev",
    "Git Repo Url": "https://github.com/alexander-kastil/az-400",
    "GitHub Service Connection ID": "231c44ad-d4a9-4055-bca6-40bab720370f",
    "ADOOrg": "https://dev.azure.com/integrationsonline",
    "ADOProject": "az-400"
}
```

### Metadata Fields

- **Service Connection**: Name of the Azure service connection
- **Git Repo Url**: GitHub repository URL
- **GitHub Service Connection ID**: GUID of the GitHub service connection in Azure DevOps
- **ADOOrg**: Azure DevOps organization URL
- **ADOProject**: Azure DevOps project name

## Importing a Pipeline

### Step 1: Read Deployment Metadata

First, locate and read the deployment metadata file:

```bash
# File location: .github/deploy.json
```

The metadata contains all necessary configuration for pipeline import.

### Step 2: Import Pipeline Using Azure CLI

Use the `az pipelines create` command to import a YAML pipeline:

```bash
az pipelines create \
  --name "03-02-spfx-ci-cd" \
  --repository "https://github.com/alexander-kastil/az-400" \
  --repository-type github \
  --branch main \
  --yml-path ".azdo/spfx-ci-cd.yml" \
  --service-connection "231c44ad-d4a9-4055-bca6-40bab720370f" \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400"
```

**Parameters:**

- `--name`: Display name from the YAML file's `name` attribute
- `--repository`: Git repository URL from deploy.json
- `--repository-type`: Type of repository (github, tfsgit, etc.)
- `--branch`: Branch to use (typically main or master)
- `--yml-path`: Path to the YAML pipeline file
- `--service-connection`: GitHub service connection ID from deploy.json
- `--org`: Azure DevOps organization URL from deploy.json
- `--project`: Project name from deploy.json

**Output:**
The command returns JSON with the pipeline definition including:

- Pipeline ID
- Initial run ID (automatically triggered)
- Pipeline configuration

### Step 3: Monitor Pipeline Execution

After import, the pipeline automatically starts running. Monitor its status:

```bash
az pipelines runs show \
  --id <RUN_ID> \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400"
```

Check the status field:

- `notStarted`: Queued but not yet running
- `inProgress`: Currently executing
- `completed`: Finished execution

Check the result field when completed:

- `succeeded`: All steps passed
- `failed`: One or more steps failed
- `canceled`: Manually cancelled

### Step 4: Manually Run Pipeline

To start a new pipeline run:

```bash
az pipelines run \
  --id <PIPELINE_ID> \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400"
```

## Diagnosing and Fixing Errors

### Common Error: Missing Required Parameters

**Error Type**: Authentication or command syntax errors in pipeline tasks

**Example Case**: CLI Microsoft 365 login command

The pipeline was using:

```bash
m365 login --authType password -u $(username) -p $(password) --tenant $(tenant)
```

**Problem**: Missing required `--appId` parameter for password authentication

### Step 1: Get Pipeline Logs

First, retrieve the pipeline run status to confirm failure:

```bash
az pipelines runs show \
  --id <RUN_ID> \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400" \
  --query "{status: status, result: result, finishTime: finishTime}"
```

### Step 2: Research Official Documentation

Use the Microsoft Learn MCP or web resources to understand the correct command syntax:

```bash
# Example: Fetch CLI Microsoft 365 documentation
# URL: https://pnp.github.io/cli-microsoft365/cmd/login
```

Key findings from documentation:

- `--appId` is required when using password authentication
- Full parameter names (`--userName`, `--password`) are recommended over short forms
- Tenant parameter is optional but recommended

### Step 3: Fix the Pipeline YAML

Update the pipeline YAML file with the correct syntax:

**Before:**

```yaml
- script: m365 login --authType password -u $(username) -p $(password) --tenant $(tenant)
  displayName: "Connect to M365"
```

**After:**

```yaml
- script: m365 login --authType password --userName $(username) --password $(password) --appId 31359c7f-bd7e-475c-86db-fdb8c937548e --tenant $(tenant)
  displayName: "Connect to M365"
```

### Step 4: Commit and Push Changes

```bash
git add .azdo/spfx-ci-cd.yml
git commit -m "Fix m365 login command - add required --appId parameter and use full parameter names"
git push
```

### Step 5: Run Pipeline Again

After pushing the fix, run the pipeline again:

```bash
az pipelines run \
  --id <PIPELINE_ID> \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400"
```

## Complete Workflow Example

Here's the complete workflow from import to successful execution:

```bash
# 1. Read deployment metadata
cat .github/deploy.json

# 2. Import pipeline
az pipelines create \
  --name "03-02-spfx-ci-cd" \
  --repository "https://github.com/alexander-kastil/az-400" \
  --repository-type github \
  --branch main \
  --yml-path ".azdo/spfx-ci-cd.yml" \
  --service-connection "231c44ad-d4a9-4055-bca6-40bab720370f" \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400"

# 3. Monitor initial run (automatically started)
az pipelines runs show --id 99 \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400"

# 4. If failed, diagnose and fix
# - Review logs
# - Research documentation using Microsoft Learn MCP
# - Fix YAML file
# - Commit and push changes

# 5. Run again with fixes
az pipelines run --id 34 \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400"

# 6. Verify success
az pipelines runs show --id 102 \
  --org "https://dev.azure.com/integrationsonline" \
  --project "az-400" \
  --query "{status: status, result: result}"
```

## Best Practices

### 1. Use Deployment Metadata

Always maintain a `deploy.json` file in the skills root with environment-specific configuration. This enables:

- Environment consistency
- Easy pipeline migration between projects
- Configuration documentation

### 2. Reference Official Documentation

When fixing errors:

- Use Microsoft Learn MCP to search for official documentation
- Reference vendor documentation (e.g., PnP CLI Microsoft 365)
- Verify command syntax and required parameters

### 3. Use Full Parameter Names

Prefer full parameter names over shortcuts for clarity:

- `--userName` instead of `-u`
- `--password` instead of `-p`
- `--appId` instead of relying on environment variables

### 4. Monitor Pipeline Runs

Always verify pipeline execution:

- Check status immediately after import
- Monitor long-running pipelines
- Review logs for any warnings or errors

### 5. Version Control Pipeline Changes

Commit pipeline fixes with descriptive messages:

```bash
git commit -m "Fix m365 login command - add required --appId parameter"
```

## Prerequisites

- Azure CLI installed with `azure-devops` extension
- Access to Azure DevOps organization and project
- GitHub service connection configured in Azure DevOps
- Repository with YAML pipeline files
- Deployment metadata file (.github/deploy.json)

## Required Permissions

- **Azure DevOps**: Build Administrator or Project Administrator
- **GitHub**: Read access to repository
- **Service Connection**: Permission to use the GitHub service connection

## Troubleshooting

### Pipeline Import Fails

**Issue**: Service connection not found

**Solution**: Verify the GitHub Service Connection ID in deploy.json matches an existing connection in Azure DevOps.

### Pipeline Run Immediately Fails

**Issue**: Missing pipeline variables (e.g., username, password)

**Solution**: Configure pipeline variables in Azure DevOps before running:

1. Navigate to the pipeline in Azure DevOps
2. Edit the pipeline
3. Go to Variables tab
4. Add required variables (mark sensitive ones as secret)

### Authentication Errors in Tasks

**Issue**: Commands fail with authentication errors

**Solution**:

1. Use Microsoft Learn MCP to research correct command syntax
2. Verify all required parameters are provided
3. Check if authentication method requires additional setup (e.g., app registration)

## Related Skills

- [get-pipeline-logs](../get-pipeline-logs/SKILL.md)

## References

- [Azure DevOps CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/pipelines)
- [Azure Pipelines YAML Schema](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema)
- [CLI Microsoft 365 Documentation](https://pnp.github.io/cli-microsoft365/)
- [Microsoft Learn MCP Server](https://github.com/microsoft/mcp-microsoft-learn)

## License

MIT
