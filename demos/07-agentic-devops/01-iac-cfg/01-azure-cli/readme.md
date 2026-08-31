# Automation using Azure CLI

## Creating Scripts based on Projects

Create deployment scripts based on existing code. The picture-optimizer project is a standard .NET worker service that watches an input folder, resizes every image it finds, and writes the result to an output folder. Its configuration lives in `appsettings.json` under `Folders` and `Processing`, so the storage the workload needs is derivable from the source rather than from a runtime convention.

Use this prompt to generate a provisioning script from your source code:

```prompt
Analyze the .NET worker service in demos\07-agentic-devops\01-iac-cfg\01-azure-cli\picture-optimizer and generate a create-bindings-app.azcli script that:
- Creates a resource group and storage account
- Sets up blob storage containers matching the input and output folders the service is configured with
- Uploads the sample pictures from ./food-pictures into the input container
- Prints the connection string the workload needs

Consider the configuration and dependencies from the source code (Program.cs, Options.cs, ImageOptimizerService.cs, appsettings.json) to ensure the generated script provisions containers whose names match the configured folders.
```

The folder names and the polling interval are configuration, not code. A correct script derives the container names from `appsettings.json` rather than hardcoding them, so renaming a folder in configuration changes what the script provisions.

## Running the Worker

The service reads and writes plain directories, so it runs anywhere without a cloud dependency.

```bash
cd picture-optimizer
dotnet run
```

Drop images into `drop/` and the resized copies appear in `processed/`. The bundled `Dockerfile` mounts `/data` and reads `Folders__InputPath` and `Folders__OutputPath` from the environment, so the same binary runs in a container against any mounted storage.

```bash
docker build -t picture-optimizer ./picture-optimizer
docker run --rm -v "$PWD/food-pictures:/data/drop" -v "$PWD/out:/data/processed" picture-optimizer
```

## Converting Scripts

Execute create-fooddb.azcli to create a Cosmos DB account and database. Ask Copilot to translate the script to PowerShell, and execute the resulting create-fooddb.ps1 script.
