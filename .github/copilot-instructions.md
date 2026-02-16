# AZ-400 Training Repository - AI Coding Agent Instructions

This repository contains training materials, demos, and infrastructure for Microsoft AZ-400 (DevOps Solutions) certification. It's a **teaching repository** - not a production application - designed to demonstrate DevOps concepts through hands-on examples.

## Repository Purpose & Structure

**Primary Goal**: Provide instructor-led demos and labs for Azure DevOps, GitHub Actions, IaC, and cloud-native development patterns.

### Key Directories

- **`.azdo/`** - Azure DevOps (ADO) pipeline definitions (50+ pipelines covering CI/CD patterns)
- **`demos/`** - Module-organized demonstrations (8 modules covering entire AZ-400 curriculum)
- **`src/`** - Sample applications (Angular, React, .NET, Python, Java, SPFx)
- **`infra/`** - Infrastructure as Code (Bicep, Terraform, Azure CLI)

Always start applications from their respective project folders and not the repository root.

## General RULES

- Write clean code. No comments. Do not over engineer!!!
- Do not write docs if you are not asked to. If you are asked to write docs, be concise, short and to the point. Avoid more than 2 nesting levels.
- When asked to implement, update or fix code always consult the Microsoft Learn MCP

## Deployment Metadata

`.github/deploy.json` contains essential metadata for pipeline imports and configurations for deployment environments.

**Never hardcode these values** - always read from `deploy.json` when creating/importing pipelines.

## Pipeline Architecture & Patterns

Pipelines might use reusable templates from `.azdo/templates/`:

### Pipeline Naming Convention

Format: `<module>-<demo>-<description>` (from YAML `name:` attribute)

- Examples: `03-02-angular-cd-aca`, `02-01-03-pipeline-basics`
- Module numbers align with demos folder structure

## Authentication & Security

### Workload Identity Federation (Preferred)

**All new pipelines must use WIF** instead of service principals with secrets.

**Creation Script**: `demos/03-release-strategy/01-release-pipelines/01-service-connections/create-workload-identity.ps1`

**What it does:**

1. Creates managed identity + resource group
2. Assigns Contributor role with retry logic (eventual consistency)
3. Creates Azure DevOps service connection via REST API
4. Queries auto-generated OIDC issuer/subject from Azure DevOps
5. Syncs federated credentials to match Azure DevOps values
6. Shares connection with all pipelines

**Critical:** You cannot set custom issuer/subject - Azure DevOps generates these. Scripts use a two-phase approach:

1. Create connection (ADO auto-generates values)
2. Query connection to get actual issuer/subject
3. Update federated credential to match

## Application Stack & Technologies

### Multi-Language Support

- **.NET** (Azure Functions, APIs) - See `src/az-functions/`, `src/services/`
- **Angular** - `src/angular/food-shop/` (18.x with standalone components)
- **React** - `src/react/` (Static Web Apps demos)
- **Python** - Azure Functions (`src/az-functions/payment-py/`)
- **Java** - Jobs and services (`src/jobs/blob-java/`)
- **SPFx** - SharePoint Framework (`src/spfx/food-list/`)

For dockerfiles we use the convention `dockerfile` (all lowercase) to avoid issues on case-sensitive systems.

### Infrastructure Technologies

- **Bicep** - Modular templates in `infra/bicep/` (preferred for new IaC)
- **Terraform** - `infra/terraform/` (cross-cloud examples)
- **Azure CLI** - `infra/cli/` (scripting demos)
