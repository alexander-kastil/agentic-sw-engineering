# Infrastructure as Code (IaC)

Infrastructure as Code enables repeatable, version-controlled deployments of Azure resources through declarative templates and automation scripts. This module demonstrates creating and managing Azure resources using Azure CLI automation, the Azure Developer CLI framework, and popular IaC tools like Bicep and Terraform.

All demonstrations in this module require secure authentication from Azure DevOps pipelines to Azure resources. The [create-workload-identity.azcli](create-workload-identity.azcli) script establishes this foundation by setting up workload identity federation between Azure DevOps and managed identities. This secure, passwordless authentication method eliminates the need to manage secrets while enabling safe deployment automation.

## Workload Identity Federation Setup

The [create-workload-identity.azcli](create-workload-identity.azcli) script demonstrates setting up workload identity federation for Azure DevOps pipelines. This script creates an Azure resource group, managed identity, and Azure DevOps service connection using OIDC-based authentication with federated credentials. The script automates the two-phase process of creating the service connection in Azure DevOps, then querying the auto-generated issuer and subject values to configure the corresponding federated credential in Azure.

Execute this script before deploying resources with the demonstrations below to ensure secure authentication is properly configured. The create-wif skill provides automation capabilities for creating and managing these workload identity service connections across your deployment automation.

## Demos

| Demo                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Azure Developer CLI (azd)](01-azd)**                  | Infrastructure orchestration framework demonstrating how Azure Developer CLI streamlines development workflow by integrating infrastructure provisioning with application code while maintaining separation of concerns through structured project conventions. The azd tool provides hooks for custom deployment logic and integrates with either Bicep or Terraform.                                                     |
| **[Bicep Infrastructure Templates](02-bicep)**           | Infrastructure as Code for the food-app using Microsoft's Bicep domain-specific language following Azure Developer CLI conventions. Bicep provides declarative, modular Azure resource definitions with strong type safety and built-in support for Azure best practices. Focuses on structuring Bicep files with proper parameterization, module organization, and environment-specific configurations.                   |
| **[Terraform Multi-Cloud Infrastructure](03-terraform)** | Demonstrates using Terraform with Azure Developer CLI to manage infrastructure across multiple cloud providers. Terraform's HCL language and provider ecosystem enable consistent infrastructure management whether deploying to Azure, AWS, or other cloud platforms. Shows how to structure Terraform files following azd conventions while maintaining compatibility with the broader infrastructure-as-code ecosystem. |

## Links & Resources

[Azure Workload Identity Federation Overview](https://learn.microsoft.com/en-us/azure/active-directory/workload-identities/workload-identity-federation)
