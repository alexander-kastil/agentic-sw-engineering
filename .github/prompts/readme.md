# Reusable Prompts

Pre-built prompt templates that guide GitHub Copilot for common tasks. Select the appropriate prompt and provide required context to accelerate repetitive work with consistent guidance.

## Prompts Overview

| Prompt                                         | Purpose                                                                                                                                                                            |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Create Docs](create-docs.prompt.md)**       | Structured approach for generating comprehensive documentation across different levels: top-level overview, service documentation, configuration guides, and deployment procedures |
| **[Describe Demos](describe-demos.prompt.md)** | Enhance demo documentation by extracting key features from source code, scripts, and pipelines. Includes style consistency, image links, and code snippet integration              |
| **[Import to ADO](import-to-ado.prompt.md)**   | Guide for importing and executing Azure DevOps pipelines from YAML files, including validation, pipeline execution, and error diagnosis                                            |

## Sample Usage

### Create Docs Prompt

**Scenario:** You need to document a new microservice with consistent structure.

**Command:**

```
Follow the Create Docs prompt to document the payment-service.
Include service overview, API endpoints, configuration options, and local setup steps.
```

**What happens:**

- Copilot reads your service code and configuration files
- Generates structured documentation following the template hierarchy
- Creates README.md with service purpose, dependencies, and configuration table
- Produces API documentation from code comments and endpoints

**Example Output:**

```markdown
# Payment Service

## Overview
Processes payment transactions with PCI-DSS compliance.

## Configuration
| Key | Purpose | Required | Default |
|-----|---------|----------|---------|
| PaymentProvider | API provider | Yes | stripe |
| ApiKey | Authentication token | Yes | - |
| Timeout | Request timeout (ms) | No | 30000 |

## Setup
1. Install dependencies: `dotnet restore`
2. Configure secrets in `appsettings.json`
3. Run tests: `dotnet test`
```

### Describe Demos Prompt

**Scenario:** Your demo folder has scripts and pipelines but the readme lacks clear descriptions.

**Command:**

```
Follow the Describe Demos prompt to update demos/02-ci/01-pipelines/readme.md.
Describe what each pipeline demonstrates with technical details and notable features.
```

**What happens:**

- Copilot analyzes pipeline YAML files in the folder
- Extracts trigger types, stages, tasks, and variables
- Identifies key technical patterns (e.g., parallel jobs, approval gates)
- Rewrites descriptions with consistent formatting

**Example Output:**

```markdown
| Demo | Description |
|------|-------------|
| **Pipeline Basics** | Multi-stage YAML pipeline with artifact management and deployment stages |
| **CI/CD: .NET API** | Automated build, test, and deployment to App Service with unit test reporting |
```

### Import to ADO Prompt

**Scenario:** You've created a new pipeline and need to import it to Azure DevOps.

**Command:**

```
Follow the Import to ADO prompt to import demos/02-ci/01-pipelines/catalog-ci-cd.yml
```

**What happens:**

- Copilot validates YAML syntax against Azure DevOps requirements
- Checks Microsoft Learn for best practices
- Imports the pipeline to your Azure DevOps project
- Runs the pipeline and reports any errors with fixes

**Example Output:**

```
✓ YAML validated successfully
✓ Pipeline imported: catalog-ci-cd (ID: 42)
✓ Pipeline executed (Run ID: 2847)
✓ Build completed successfully
```

If errors occur, Copilot diagnoses and fixes them automatically before reporting back.
