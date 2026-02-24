# Automation using Azure CLI

## Creating Scripts based on Projects

Create deployment scripts based on existing code. The picture-optimizer function app demonstrates generating a create-bindings-app.azcli script from Azure Function source code. This function processes images by automatically resizing them when uploaded to blob storage, using blade triggers to monitor an input container and output resized images to a processed container.

Use this prompt to generate deployment scripts from your source code:

```prompt
Analyze the Azure Function source code in demos\06-agentic-devops\01-azure-cli\picture-optimizer and generate a create-bindings-app.azcli script that:
- Creates a resource group and storage account
- Sets up blob storage containers for input (drop) and output (processed)
- Creates an Azure Function App configured to use the storage containers
- Configures the necessary environment variables and connection strings
- Uploads sample data if needed
- Deploys the function app

Consider the dependencies, bindings, and configuration from the source code (Program.cs, function triggers, appsettings) to ensure the generated script properly provisions all required resources.
```

## Converting Scripts

Execute create-fooddb.azcli to create a Cosmos DB account and database. Ask Copilot to translate the script to PowerShell, and execute the resulting create-fooddb.ps1 script.
