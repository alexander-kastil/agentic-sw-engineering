---
name: get-pipeline-logs
description: Get logs from the latest Azure DevOps pipeline run using patterns that actually work.
license: MIT
---

# Azure DevOps Pipeline Log Retrieval

Get logs from Azure DevOps pipeline runs. Always work with the **latest run** to ensure logs are available (deleted builds have no logs).

## Prerequisites

- Azure DevOps organization and project (from deploy.json)
- Pipeline ID (get via `az pipelines list`)
- Azure CLI for authentication

## Complete Workflow: Latest Run Logs

### 1) Get latest run ID

```powershell
# Load configuration from deploy.json
$config = Get-Content .github/skills/deploy.json | ConvertFrom-Json
$org = ($config.ADOOrg -replace 'https://dev.azure.com/', '')
$project = $config.ADOProject
$pipelineId = 45  # Replace with your pipeline ID# Get latest run (top 1, newest first)$latestRun = az pipelines runs list `  --org "https://dev.azure.com/$org" `  --project $project `  --pipeline-ids $pipelineId `  --top 1 `  --query-order QueueTimeDesc `  --query "[0]" | ConvertFrom-Json$buildId = $latestRun.idWrite-Host "Latest run: $buildId (Status: $($latestRun.status), Result: $($latestRun.result))"
```

### 2) List all logs for the build

```powershell$token = az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv$headers = @{ Authorization = "Bearer $token" }$uri = "https://dev.azure.com/$org/$project/_apis/build/builds/$buildId/logs?api-version=7.1-preview.2"$logs = Invoke-RestMethod -Uri $uri -Headers $headers$logs.value | Select-Object id, lineCount | Sort-Object lineCount -Descending

```

### 3) Download specific log

```powershell$logId = 13  # or get from logs list above$token = az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv$headers = @{ Authorization = "Bearer $token" }$uri = "https://dev.azure.com/$org/$project/_apis/build/builds/$buildId/logs/$logId`?api-version=7.1-preview.2"# Download to fileInvoke-RestMethod -Uri $uri -Headers $headers | Out-File "$env:TEMP\build-$buildId-log-$logId.txt"# Search for errorsGet-Content "$env:TEMP\build-$buildId-log-$logId.txt" | Select-String -Pattern "error|Error|##\[error\]|failed|Failed" -Context 3

````

### 4) Download all logs as ZIP

```powershell$token = az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv$headers = @{ Authorization = "Bearer $token" }$uri = "https://dev.azure.com/$org/$project/_apis/build/builds/$buildId/logs?api-version=7.1-preview.2&`$format=zip"Invoke-WebRequest -Uri $uri -Headers $headers -OutFile "$env:TEMP\build-$buildId-logs.zip"Expand-Archive -Path "$env:TEMP\build-$buildId-logs.zip" -DestinationPath "$env:TEMP\build-$buildId-logs" -Force# List largest logsGet-ChildItem "$env:TEMP\build-$buildId-logs" | Sort-Object Length -Descending | Select-Object -First 10
````

## One-Liner: Get Latest Run Logs

```powershell
$config = Get-Content .github/deploy.json | ConvertFrom-Json
$org = ($config.ADOOrg -replace 'https://dev.azure.com/', '')
$project = $config.ADOProject
$pipelineId = 45$buildId = (az pipelines runs list --org "https://dev.azure.com/$org" --project $project --pipeline-ids $pipelineId --top 1 --query-order QueueTimeDesc --query "[0].id" -o tsv)$token = az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv$logs = Invoke-RestMethod -Uri "https://dev.azure.com/$org/$project/_apis/build/builds/$buildId/logs?api-version=7.1-preview.2" -Headers @{Authorization="Bearer $token"}$largestLog = $logs.value | Sort-Object lineCount -Descending | Select-Object -First 1Invoke-RestMethod -Uri "https://dev.azure.com/$org/$project/_apis/build/builds/$buildId/logs/$($largestLog.id)?api-version=7.1-preview.2" -Headers @{Authorization="Bearer $token"} | Out-File "$env:TEMP\latest-error.txt"Get-Content "$env:TEMP\latest-error.txt" | Select-String "error|Error|##\[error\]" -Context 3
```

## Critical Notes

- **Always use latest run**:
- **Token resource ID**: `499b84ac-1321-427f-aa17-267ca6975798` is Azure DevOps Entra ID resource
- **Build vs Run**: Terms are interchangeable in Azure DevOps (buildId = runId)
- **Configuration**: Load org/project from `.github/deploy.json`

## Troubleshooting

## References- Review logs to diagnose pipeline issues: https://learn.microsoft.com/en-us/azure/devops/pipelines/troubleshooting/review-logs- Builds API: https://learn.microsoft.com/en-us/rest/api/azure/devops/build/builds## LicenseMIT
