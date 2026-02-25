# Copilot Skills

Documented automation patterns that solve specific DevOps tasks with validated, reusable workflows. Each skill is self-documenting and regularly tested to ensure reliability.

## Skills Overview

| Skill                                            | Purpose                                                                                                                                                                                                           |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Create Workload Identity](create-wif/)**     | Automate Azure DevOps service connection creation with workload identity federation. Enables secure OIDC-based authentication between Azure DevOps pipelines and Azure managed identities without storing secrets |
| **[Get Pipeline Logs](get-pipeline-logs/)**     | Retrieve logs from Azure DevOps pipeline runs using Azure CLI. Always works with the latest run to ensure logs are available and provides structured access to build step outputs                                 |
| **[Import Pipeline](import-pipeline/)**         | Import and execute Azure DevOps pipelines from YAML files using deployment metadata. Includes automatic error diagnosis and fixing with Microsoft Learn guidance                                                  |
| **[Visualize Conversation](visualize-conversation/)** | Generate markdown documentation with Mermaid diagrams from conversation history and tool usage JSON files. Auto-updates on each session with clean visualizations and version-control friendly outputs              |

## Sample Usage

### Create Workload Identity Skill

**Scenario:** You need to securely authenticate a pipeline to Azure without managing secrets.

**Command:**

```
Create a workload identity service connection for the az-400 project.
Target subscription: "az-400-demo" and resource group: "rg-devops"
```

**What happens:**

1. Creates a managed identity in Azure with Contributor role assignment
2. Generates a service connection in Azure DevOps with OIDC federation
3. Automatically syncs the Azure DevOps issuer/subject with the federated credential
4. Grants Build Service permissions to use the connection
5. Shares the connection across all project pipelines

**Result:**

```
✓ Managed Identity created: az-400-workload-identity
✓ Service Connection created: az-400-wif
✓ Federated credentials configured for OIDC
✓ Build Service permissions granted
✓ Ready to use in pipeline YAML
```

**Pipeline Usage (After Skill Completes):**

```yaml
trigger:
  - main

stages:
  - stage: Deploy
    jobs:
      - job: DeployInfra
        steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'az-400-wif'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                az group list --output table
```

### Get Pipeline Logs Skill

**Scenario:** A pipeline failed and you need to diagnose the error from logs.

**Command:**

```
Get logs from the latest run of the catalog-ci-cd pipeline.
Show me the failure point and error details.
```

**What happens:**

1. Queries Azure DevOps API for the latest run of catalog-ci-cd
2. Retrieves logs for each stage and step
3. Identifies the failed step(s) with exit codes and error messages
4. Provides structured output highlighting the failure point

**Example Output:**

```
Pipeline: catalog-ci-cd (Latest Run #2847)
Status: Failed ❌

[Build Stage] ✓ Success
  - Restore: Completed in 8s
  - Build: Completed in 42s

[Test Stage] ✓ Success
  - Unit Tests: 145 passed, 0 failed

[Deploy Stage] ❌ Failed
  - Deploy to App Service: Failed at 00:14 UTC
    Error: "Insufficient permissions on resource group 'rg-demo'"
    Exit Code: 1

Recommendation: Grant the service connection Contributor role on rg-demo
```

### Import Pipeline Skill

**Scenario:** You've created a new pipeline and need to test it in Azure DevOps.

**Command:**

```
Import the pipeline from demos/02-ci/01-pipelines/catalog-ci-cd.yml
and run it in the az-400 project.
```

**What happens:**

1. Reads the YAML file from the specified path
2. Validates syntax against Azure DevOps requirements
3. Checks against Microsoft Learn best practices
4. Imports the pipeline to Azure DevOps
5. Executes the pipeline automatically
6. Monitors the run and reports results

**Example Output:**

```
✓ YAML validated (best practices: OK)
✓ Pipeline imported: catalog-ci-cd (Pipeline ID: 42)
✓ Run created: Run #2847
✓ Build stage: Success (2m 34s)
✓ Test stage: Success (1m 12s)
✓ Deploy stage: Success (3m 18s)
✓ Pipeline run completed: Success ✓
```

If errors occur during the run, the skill diagnoses issues and proposes fixes:

```
❌ Deploy Task failed: Task AzureCLI@2 - Step 'Create storage account' failed
  Error: "Storage account name must be between 3 and 24 characters"
  Location: lines 45-48 in catalog-ci-cd.yml

Fix: Change 'st${env}' to 'st${env}001' to ensure valid length
```
