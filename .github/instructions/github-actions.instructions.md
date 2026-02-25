---
description: Coding conventions and best practices for GitHub Actions workflows in this repository
---

# GitHub Actions Workflow Conventions

This document outlines the coding conventions and best practices for creating and maintaining GitHub Actions workflows in this repository.

## File Naming

Workflow files use clear, descriptive names that indicate their purpose:

Format: `<project>-<function>.yml`

Examples:

- `catalog-api-cicd.yml`
- `react-static-webapp-deploy.yml`
- `backend-build-test.yml`
- `frontend-lint-deploy.yml`

Place workflow files in `.github/workflows/` directory.

## Workflow Structure

### Root-Level Elements

Start workflows with these elements in order:

```yaml
name: Workflow Display Name

on: <trigger-configuration>

permissions: <required-permissions>

env:
  # Global environment variables

jobs:
  # Workflow jobs
```

### Name Element

Provide a clear, human-readable workflow name:

```yaml
name: Catalog Service CI/CD
```

### Triggers

Define when the workflow runs using the `on` key:

```yaml
on:
  push:
    branches:
      - main
    paths:
      - src/services/**
      - .github/workflows/catalog-api-cicd.yml

  pull_request:
    branches:
      - main

  workflow_dispatch:
    inputs:
      reason:
        description: "Optional note for manual trigger"
        required: false
```

Disable triggers with comments for development:

```yaml
on:
  # push:
  #   branches:
  #     - main
  workflow_dispatch:
```

### Permissions

Declare required permissions explicitly for security. This limits what the workflow token can access:

```yaml
permissions:
  contents: read              # Read repository contents
  id-token: write             # OIDC token for Azure/AWS authentication
  checks: write               # Write test results
  pull-requests: write        # Comment on PRs
```

Common permission levels:

- `read`: Read-only access
- `write`: Read and write access
- Value scoped to specific job or entire workflow

### Environment Variables

Define workflow-level variables at the top:

```yaml
env:
  DOTNET_VERSION: "10.0.x"
  PROJECT_PATH: src/services/catalog-service/api/catalog-service.csproj
  BUILD_OUTPUT: ${{ github.workspace }}/build-output
  APP_LOCATION: src/react/react-devops
  OUTPUT_LOCATION: dist
```

## Jobs

Each job runs in isolation on the specified runner. Define jobs using the `jobs` key:

```yaml
jobs:
  build:
    name: Build Application
    runs-on: ubuntu-latest
    permissions:
      contents: read

    outputs:
      artifact-path: ${{ steps.publish.outputs.artifact-path }}

    steps:
      # Job steps

  deploy:
    name: Deploy
    needs: build
    runs-on: ubuntu-latest
    environment: production
```

### Job Configuration

Key job properties:

- `name`: Human-readable job display name
- `runs-on`: Runner to execute job on (e.g., `ubuntu-latest`, `windows-latest`)
- `permissions`: Job-specific permissions (overrides workflow permissions)
- `outputs`: Output values from this job for use in dependent jobs
- `environment`: Environment context for deployment protection rules
- `needs`: Job dependencies (other jobs that must complete first)
- `if`: Conditional execution based on status or variables

### Job Outputs

Export outputs from steps for downstream jobs:

```yaml
jobs:
  build:
    name: Build
    outputs:
      artifact-path: ${{ steps.publish.outputs.artifact-path }}
    steps:
      - name: Publish Application
        id: publish
        run: dotnet publish . --output ./build

  deploy:
    name: Deploy
    needs: build
    steps:
      - name: Download artifact
        run: echo "Artifact path: ${{ needs.build.outputs.artifact-path }}"
```

### Job Dependencies

Use `needs` to create dependencies between jobs:

```yaml
jobs:
  build:
    name: Build

  test:
    name: Test
    needs: build        # Test runs after build succeeds

  deploy:
    name: Deploy
    needs: [build, test]  # Deploy runs after both build and test succeed
```

## Steps and Actions

Steps execute commands or use pre-built actions.

### Using Actions

Call external actions with `uses`:

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Setup .NET
    uses: actions/setup-dotnet@v4
    with:
      dotnet-version: ${{ env.DOTNET_VERSION }}

  - name: Upload artifact
    uses: actions/upload-artifact@v4
    with:
      name: build-artifact
      path: ./build
      retention-days: 7
```

Action format: `owner/repo@version`

### Running Commands

Run shell commands with `run`:

```yaml
steps:
  - name: Build solution
    run: dotnet build src/myapp.sln --configuration Release

  - name: Create resource group
    run: |
      az group create \
        -n my-resource-group \
        -l westeurope
```

Use `|` for multi-line commands.

### Step Configuration

```yaml
steps:
  - name: Step Display Name
    id: step-identifier              # Used for referencing outputs
    uses: actions/some-action@v4
    with:
      input-param: value
    env:
      STEP_SPECIFIC_VAR: value       # Step-scoped variables
    working-directory: src/app       # Working directory for run steps
    if: success()                    # Conditional execution
    continue-on-error: true          # Don't fail workflow on step failure
```

### Step Names

Use clear, descriptive names that indicate the action:

Format: `<Action> <Target>`

Examples:

- "Checkout code"
- "Setup .NET"
- "Build solution"
- "Deploy to App Service"
- "Run unit tests"

## Variables and Secrets

### Environment Variables

Reference variables in steps:

```yaml
env:
  APP_NAME: my-app

steps:
  - name: Display app name
    run: echo "App: ${{ env.APP_NAME }}"
```

### Secrets

Reference secrets for sensitive values:

```yaml
steps:
  - name: Authenticate
    run: tool login --key ${{ secrets.API_KEY }}
```

Mask secrets automatically with `::add-mask::`:

```yaml
- name: Get deployment token
  id: token
  run: |
    token=$(az staticwebapp secrets list --query 'properties.apiKey' -o tsv)
    echo "::add-mask::$token"
    echo "token=$token" >> $GITHUB_OUTPUT
```

### Step Outputs

Export values from a step for use in later steps:

```yaml
- name: Publish application
  id: publish
  run: |
    dotnet publish . --output build
    echo "output-path=build" >> $GITHUB_OUTPUT

- name: Use published path
  run: echo "Path: ${{ steps.publish.outputs.output-path }}"
```

Output format: `echo "key=value" >> $GITHUB_OUTPUT`

Reference format: `${{ steps.<step-id>.outputs.<output-name> }}`

## Context Variables

GitHub provides context variables:

```yaml
steps:
  - name: Display context
    run: |
      echo "Repository: ${{ github.repository }}"
      echo "Branch: ${{ github.ref }}"
      echo "Workspace: ${{ github.workspace }}"
      echo "Event: ${{ github.event_name }}"
      echo "Actor: ${{ github.actor }}"
```

Common contexts:

- `github.repository` - Owner/repo name
- `github.ref` - Branch or tag reference
- `github.workspace` - Workflow working directory
- `github.event_name` - Event that triggered the workflow
- `github.actor` - User who triggered the workflow

## Deployment Environments

Use GitHub environments for deployment gates and secrets:

```yaml
jobs:
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    environment: production    # Requires approval; uses production secrets
    steps:
      - name: Deploy
        env:
          DEPLOY_KEY: ${{ secrets.PRODUCTION_DEPLOY_KEY }}
        run: ./deploy.sh
```

Environment configuration:

- Define environment-specific secrets in repository settings
- Set approval requirements for production deployments
- Environment variables are scoped to that environment

## Conditional Execution

Execute steps or jobs conditionally:

```yaml
steps:
  - name: Build
    run: npm run build

  - name: Upload artifact
    if: success()              # Run only if previous steps succeeded
    uses: actions/upload-artifact@v4

  - name: Publish test results
    if: always()               # Run even if previous steps failed
    uses: dorny/test-reporter@v1

  - name: Deploy production
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    run: ./deploy-prod.sh

jobs:
  deploy:
    if: success()              # Job runs only if all dependencies succeeded
    needs: [build, test]
```

Common conditions:

- `success()` - Previous step or job succeeded
- `failure()` - Previous step or job failed
- `always()` - Always run regardless of status
- `github.ref == 'refs/heads/main'` - On main branch
- `github.event_name == 'push'` - On push event

## Best Practices

### Artifact Management

Publish artifacts for downstream jobs and debugging:

```yaml
- name: Upload build artifact
  uses: actions/upload-artifact@v4
  with:
    name: app-build
    path: ./dist
    retention-days: 7
    if-no-files-found: error    # Fail if artifact not found

- name: Download artifact
  uses: actions/download-artifact@v4
  with:
    name: app-build
    path: ./artifact
```

Use descriptive artifact names. Set short retention periods to save storage.

### Verification Steps

Include verification steps after operations:

```yaml
- name: Build output
  run: dotnet publish . --output build

- name: Verify build
  run: |
    if [ ! -d "./build" ]; then
      echo "Build output not found"
      exit 1
    fi
    echo "Build verified successfully"
    ls -la ./build/
```

### Matrix Builds

Run jobs across multiple configurations:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        dotnet-version: ["8.0.x", "9.0.x", "10.0.x"]
        os: [ubuntu-latest, windows-latest]

    steps:
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ matrix.dotnet-version }}

      - name: Build for ${{ matrix.dotnet-version }} on ${{ matrix.os }}
        run: dotnet build
```

## Common Patterns

### Build and Publish

```yaml
jobs:
  build:
    name: Build Application
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ env.DOTNET_VERSION }}

      - name: Build and Publish
        run: dotnet publish ${{ env.PROJECT_PATH }} --configuration Release --output ${{ env.BUILD_OUTPUT }}

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-artifact
          path: ${{ env.BUILD_OUTPUT }}
          retention-days: 7
```

### Build, Test, and Deploy

```yaml
jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: app-build
          path: dist

  test:
    name: Test
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run test

  deploy:
    name: Deploy
    needs: [build, test]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app-build
          path: dist
      - name: Deploy
        run: ./scripts/deploy.sh
```

### Azure Authentication with OIDC

Use workload identity federation for secure Azure authentication:

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Azure login with federated identity
    uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

  - name: Run Azure CLI commands
    run: az group list

  - name: Logout from Azure
    run: az logout
```

## Security Best Practices

1. Use OIDC authentication instead of secrets when possible
2. Limit permissions to only what's needed
3. Use environment-specific secrets for sensitive values
4. Mask sensitive outputs with `::add-mask::`
5. Pin action versions (use `@v4` not `@latest`)
6. Review workflow permissions in repository settings
7. Use `if-no-files-found: error` on artifact uploads to catch issues
8. Don't log secrets in workflow output

## Documentation

### Comments

Add comments for complex logic:

```yaml
# Install Playwright browsers required for E2E tests
- name: Install Playwright browsers
  run: npx playwright install chromium msedge --with-deps
```

### Workflow Headers

Include descriptive comments at the top:

```yaml
# CI/CD pipeline for the Catalog Service API
# - Builds and tests .NET application
# - Publishes artifact for deployment
# - Deploys to App Service on manual trigger
```
