# Azure Developer CLI (azd)

Azure Developer CLI is a command-line tool that streamlines the development, deployment, and lifecycle management of cloud applications on Azure. It provides commands to create, provision, and manage Azure resources using infrastructure as code templates while maintaining a developer-focused experience that reduces boilerplate configuration.

The azd tool integrates with infrastructure as code frameworks to enable repeatable, version-controlled deployments. You can use azd with Bicep for declarative Azure resource definitions or Terraform for multi-cloud infrastructure management, leveraging language-specific conventions and patterns for each approach.

## Azure Developer CLI Project Structure

A typical azd project is organized with infrastructure as code separate from application code:

```
azd-project/
├── azure.yaml                   # AZD Configuration
├── infra/                       # IaC (Bicep/Terraform)
│   ├── main.bicep               # Primary infrastructure
│   ├── main.parameters.json     # Parameter values
│   └── abbreviations.json       # Resource naming rules
├── src/                         # Application source code
│   ├── api/                     # Backend services
│   ├── web/                     # Frontend application
│   └── ...                      # Additional services
├── .env                         # Local environment variables
```

The azure.yaml file serves as the control plane, defining services, infrastructure requirements, and deployment hooks. The infra/ folder contains Bicep or Terraform templates that provision Azure resources, while src/ holds your application code organized by component.

## Key Topics covered in this module

[Azure Developer CLI (azd)](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/)

[Azure Developer CLI with GitHub Copilot coding agent extension](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/extensions/copilot-coding-agent-extension)

[Azure Developer CLI with Azure AI Foundry extension](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/extensions/azure-ai-foundry-extension)
