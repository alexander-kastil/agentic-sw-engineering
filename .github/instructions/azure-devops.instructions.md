---
description: Coding conventions and best practices for Azure DevOps pipelines in this repository
---

# Azure DevOps Pipeline Conventions

This document outlines the coding conventions and best practices for creating and maintaining Azure DevOps (ADO) pipelines in this repository.

## File Naming

### Pipeline Files

Pipelines use clear, descriptive names that indicate their purpose:

Format: `<project>-<stage>.yml`

Examples:

- `frontend-ci-cd.yml`
- `api-build-test.yml`
- `deploy-production.yml`

### Template Files

Reusable templates use the prefix `t-` followed by the function name:

Format: `t-<function>.yml`

Examples:

- `t-build-nodejs.yml`
- `t-build-dotnet.yml`
- `t-deploy-aca.yml`
- `t-deploy-static-webapp.yml`

Note: Use `.yml` extension for consistency (though `.yaml` is also valid).

## Pipeline Structure

### Root-Level Elements

Start pipelines with metadata in this order:

```yaml
name: <pipeline-display-name>

trigger: <trigger-condition>
pr: <PR-condition>

pool:
  vmImage: "<image-name>"

variables:
  # Define all pipeline variables here

stages:
  # Pipeline stages
```

#### Name Element

The `name` field should be human-readable and descriptive:

```yaml
name: Frontend CI/CD Pipeline
```

#### Triggers

Use explicit trigger configuration:

```yaml
trigger: none        # Disable automatic triggers
pr: none             # Disable PR triggers
```

Or enable specific branches:

```yaml
trigger:
  branches:
    include:
      - master
```

#### Pool Configuration

Specify the build agent pool:

```yaml
pool:
  vmImage: "ubuntu-latest"
```

### Variables Section

Group all pipeline-level variables at the top level. Include:

- Build configuration settings
- File paths and directory names
- Tool versions
- Environment-specific values
- Custom parameters for flexibility

```yaml
variables:
  nodeVersion: "22.14.0"
  buildConfiguration: "Release"
  appRoot: src/myapp
  sourceDirectory: "src"
  outputDirectory: "dist"
```

Sensitive values should use pipeline variable groups or secrets, not inline values.

### Stages

Organize work into logical stages using `stages`:

```yaml
stages:
  - stage: Build
    displayName: Build Application
    jobs:
      - job: CompileAndTest
        displayName: Build and Test
        steps:
          # Build steps

  - stage: Deploy
    displayName: Deploy to Environment
    dependsOn: Build
    jobs:
      - template: templates/t-deploy-webapp.yml
        parameters:
          environment: dev
```

Each stage should have a clear, descriptive `displayName`.

### Jobs

Jobs contain the actual work. Use descriptive display names:

```yaml
jobs:
  - job: Build
    displayName: Build Angular
    steps:
      # Task steps

  - deployment: DeployStaticWebApp
    displayName: Deploy to Static Web App
    environment: ${{ parameters.environmentName }}
```

Use `deployment` job type for deployment pipelines with environment tracking.

### Steps and Tasks

Each step must have a `displayName` that clearly describes the action:

```yaml
steps:
  - task: NodeTool@0
    inputs:
      versionSpec: $(nodeVersion)
    displayName: "Install Node.js"

  - task: Npm@1
    displayName: "Install Dependencies"
    inputs:
      command: "install"
      workingDir: $(sourceDirectory)

  - task: DotNetCoreCLI@2
    displayName: "Build Application"
    inputs:
      command: "build"
      projects: "$(sourceDirectory)/*.csproj"
```

Format: `displayName: "<Action> <Target>"` (e.g., "Install Dependencies", "Build Application", "Deploy to Staging")

## Templates

### Template Parameters

Define all parameters at the top of template files with explicit types and defaults:

```yaml
parameters:
  - name: projectPath
    type: string
    default: "src/app"

  - name: configuration
    type: string
    default: "Release"

  - name: publishDir
    type: string
    default: "dist"

  - name: environment
    type: string
    default: "dev"
```

Use consistent, descriptive parameter naming across templates.

### Template Usage

When calling templates, use named parameters for clarity:

```yaml
- template: templates/t-build-nodejs.yml
  parameters:
    nodeVersion: $(nodeVersion)
    projectPath: $(sourceDirectory)
    configuration: "production"
    publishDir: $(outputDirectory)

- template: templates/t-deploy-webapp.yml
  parameters:
    environment: dev
    artifactName: build-artifact
    deploymentSlot: staging
```

## Variables and Parameters

### Variable Naming

Use camelCase for variable names:

```yaml
variables:
  nodeVersion: "22.14.0"
  buildConfiguration: "Release"
  deploymentToken: "<token>"
  appRoot: src/angular/angular-devops
```

### Variable Scoping

Define variables at the appropriate level:

- Pipeline-level: Global project variables (versions, paths)
- Template parameters: Configurable values passed to reusable templates
- Step-level: Task-specific inputs (prefer using task inputs directly)

### Parameter Expression Syntax

Use template expression syntax `${{ }}` for parameters and conditionals:

```yaml
versionSpec: ${{ parameters.nodeVersion }}
workingDir: ${{ parameters.appLocation }}
```

Use variable expression syntax `$()` for pipeline variables:

```yaml
sources: "$(appRoot)/src/environments/environment.ts"
displayName: "Build $(buildConfiguration)"
```

## Tasks and Best Practices

### Task Ordering

Order tasks logically to ensure dependencies are met:

1. Install/setup tools (e.g., NodeTool, UseDotNet)
2. Dependency installation/restore
3. Build/compile
4. Publish artifacts
5. Deployment steps

### Artifact Publishing

Always publish build artifacts for downstream stages:

```yaml
- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: "$(outputDirectory)"
    ArtifactName: "app-build"
    publishLocation: "Container"
  displayName: "Publish Build Artifacts"

- task: PublishPipelineArtifact@1
  inputs:
    targetPath: "$(Build.ArtifactStagingDirectory)"
    artifact: "docker-image"
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/master'))
  displayName: "Publish Docker Image"
```

Use descriptive artifact names that indicate content type (e.g., `app-build`, `docker-image`, `test-results`).

### Conditional Execution

Use conditions for environment-specific or status-specific tasks:

```yaml
condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/master'))
```

## Environment Configuration

### Environment Names

Use descriptive environment names that indicate deployment target:

```yaml
environmentName: "dev"
```

Or reference a pipeline variable:

```yaml
environmentName: "$(deploymentEnvironment)"
```

Define the variable at pipeline level:

```yaml
variables:
  deploymentEnvironment: "production"
```

### Deployment Job Strategy

Use `runOnce` strategy with `deploy` steps for consistent deployments:

```yaml
- deployment: Deploy
  displayName: Deploy Application
  environment: $(deploymentEnvironment)
  strategy:
    runOnce:
      deploy:
        steps:
          - checkout: none
          - task: DownloadPipelineArtifact@2
            inputs:
              buildType: "current"
              artifactName: $(artifactName)
              targetPath: $(Pipeline.Workspace)
            displayName: "Download Build Artifacts"

          - task: AzureAppServiceDeploy@0
            inputs:
              azureSubscription: "$(serviceConnection)"
              appType: "webApp"
              appName: "$(appName)"
              package: "$(Pipeline.Workspace)/**/*.zip"
            displayName: "Deploy to App Service"
```

## Documentation

### Comments

Add comments for complex logic or non-obvious configuration:

```yaml
# Cache node_modules to improve build performance
- task: Cache@2
  inputs:
    key: 'npm | "$(Agent.OS)" | package-lock.json'
    path: "node_modules"
```

### File Headers

Include clear header comments explaining pipeline purpose:

```yaml
# Build and test pipeline for the API service
# Runs on commits to master branch
# Produces Docker image artifact for deployment
```

## Common Patterns

### Multi-Stage CI/CD Pipeline

```yaml
stages:
  - stage: Build
    displayName: Build Artifacts
    jobs:
      - job: Build
        displayName: Compile and Test
        steps:
          - template: templates/t-build-dotnet.yml
            parameters:
              configuration: Release

  - stage: Deploy
    displayName: Deploy to Staging
    dependsOn: Build
    jobs:
      - deployment: DeployStaging
        displayName: Deploy to Staging Environment
        environment: staging
        strategy:
          runOnce:
            deploy:
              steps:
                - template: templates/t-deploy-aca.yml
                  parameters:
                    environment: staging
```

### Parameterized Build Template

```yaml
# t-build-dotnet.yml
parameters:
  - name: projectPath
    type: string
  - name: configuration
    type: string
    default: "Release"

steps:
  - task: UseDotNet@2
    displayName: "Install .NET SDK"
    inputs:
      packageType: "sdk"
      version: "10.0.x"

  - task: DotNetCoreCLI@2
    displayName: "Restore dependencies"
    inputs:
      command: "restore"
      projects: "${{ parameters.projectPath }}"

  - task: DotNetCoreCLI@2
    displayName: "Build - ${{ parameters.configuration }}"
    inputs:
      command: "build"
      projects: "${{ parameters.projectPath }}"
      arguments: "--configuration ${{ parameters.configuration }}"

  - task: PublishBuildArtifacts@1
    inputs:
      PathtoPublish: "$(Build.ArtifactStagingDirectory)"
      ArtifactName: "drop"
    displayName: "Publish Artifacts"
```

## Configuration Management

When creating pipelines that depend on environment-specific settings:

- Store configuration values in pipeline variable groups (shared across pipelines)
- Use pipeline parameters for values that change per execution
- Avoid hardcoding service names, resource names, or environments
- Document which variables are required for pipeline execution
- Use environment-specific variable groups for dev/staging/production

Example setup:

```yaml
variables:
  - group: shared-build-config      # Shared across all pipelines
  - group: ${{ variables.environment }}-deployment  # Environment-specific

trigger:
  branches:
    include:
      - master
```

## Validation

Before committing pipelines:

1. Verify all variables are defined
2. Check task display names are descriptive
3. Confirm artifact names are consistent
4. Validate parameter types and defaults
5. Test trigger conditions for intended branches
6. Verify stage/job dependencies if using multi-stage pipelines
