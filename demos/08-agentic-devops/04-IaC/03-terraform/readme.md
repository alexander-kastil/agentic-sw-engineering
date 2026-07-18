# Terraform

## Demo

This demo creates infrastructure as code for the food-app using Terraform following the Azure Developer CLI (azd) conventions. We will structure and deploy the necessary Azure resources for the food-app, focusing on hosting the food-shop frontend using Azure Static Web App.

## Switching to Terraform

The Azure Developer CLI supports Terraform as an alternative to Bicep. To switch from Bicep to Terraform, update your `azure.yaml` file with:

```yaml
infra:
  provider: terraform
```

Then add your Terraform files to the `infra/` directory. For remote state management, create a `provider.conf.json` file in the `infra/` folder and configure your storage account details.

## Sample Prompt

```
Create Terraform files for src/food-app following azd conventions:
- main.tf with Azure Static Web App for food-shop frontend
- variables.tf for environment configuration
- outputs.tf for deployment results
- provider.tf with Azure provider setup
```

## Key Topics Covered

[Use Terraform as an infrastructure as code tool for Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/use-terraform-for-azd)

[Azure Static Web App documentation](https://learn.microsoft.com/en-us/azure/static-web-apps/overview)
