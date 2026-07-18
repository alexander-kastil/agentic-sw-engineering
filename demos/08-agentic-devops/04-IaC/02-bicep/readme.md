# Bicep

## Demo

This demo creates infrastructure as code for the food-app using Bicep templates following the Azure Developer CLI (azd) conventions. We will structure and deploy the necessary Azure resources for the food-app, which includes services like container apps, databases, and API management components.

The implementation follows azd module conventions, organizing bicep files with proper parameterization for environment-specific configurations. We focus exclusively on the src/food-app infrastructure and do not cover other src folder projects.

## Sample Prompt

```
Create Azure Infrastructure as Code bicep files for src/food-app following azd conventions.

Include:
- Main bicep file (main.bicep) with module references
- Separate modules for azure container apps and networking
- Parameters file with environment-specific values
- Outputs for deployment results

Structure the files in a way that matches azd expected directory layout:
- infra/ directory with main.bicep
- infra/modules/ directory with individual resource modules
- infra/parameters.json for configuration

The food-app consists of:
- catalog-service: Backend API service
- food-shop: Frontend application
```

## Key Topics Covered

[Create Bicep files with Visual Studio Code and Bicep MCP server](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/quickstart-create-bicep-use-visual-studio-code-model-context-protocol?tabs=azure-cli)
