# Automation using Azure CLI

## Creating Scripts based on Projects

Create deployment scripts based on existing code. The picture-optimizer project is a standard .NET worker service that watches an input folder, resizes every image it finds, and writes the result to an output folder. Its configuration lives in `appsettings.json` under `Folders` and `Processing`, so the storage the workload needs is derivable from the source rather than from a runtime convention.

Use this prompt to generate a provisioning script from your source code:

```prompt
Analyze the .NET worker service in demos\07-agentic-devops\01-iac\01-azure-cli\picture-optimizer and generate a create-bindings-app.azcli script that:
- Creates a resource group and storage account
- Sets up blob storage containers matching the input and output folders the service is configured with
- Uploads the sample pictures from ./food-pictures into the input container
- Prints the connection string the workload needs

Consider the configuration and dependencies from the source code (Program.cs, Options.cs, ImageOptimizerService.cs, appsettings.json) to ensure the generated script provisions containers whose names match the configured folders.
```

The folder names and the polling interval are configuration, not code. A correct script derives the container names from `appsettings.json` rather than hardcoding them, so renaming a folder in configuration changes what the script provisions.

## Running the Worker

The service reads and writes plain directories, so it runs anywhere without a cloud dependency. It targets `net10.0`, so you need the .NET 10 SDK on the machine.

```bash
cd picture-optimizer
dotnet run
```

Drop images into `picture-optimizer/drop/` and the resized copies appear in `picture-optimizer/processed/`. Those two names come from `Folders:InputPath` and `Folders:OutputPath` in `appsettings.json`, and the same two keys are what the container reads as `Folders__InputPath` and `Folders__OutputPath`, so the same binary runs against any mounted storage.

Run the container commands from this topic folder, not from inside `picture-optimizer`, because the build context is the project folder and the volume paths point at `food-pictures` beside it.

```bash
docker build -t picture-optimizer ./picture-optimizer
docker run --rm -v "$PWD/food-pictures:/data/drop" -v "$PWD/out:/data/processed" picture-optimizer
```

## Converting Scripts

Execute `create-fooddb.azcli` to create a Cosmos DB account, a database, and the `food` and `orders` containers. Ask Copilot to translate the script to PowerShell, and execute the resulting `create-fooddb.ps1` script.

> Note: `az cosmosdb create --enable-free-tier true` is still a preview argument, and a subscription may hold only one free-tier Cosmos DB account. Drop the flag if the account creation fails with a free-tier conflict.

## Links & Resources

- [az storage blob upload-batch](https://learn.microsoft.com/en-us/cli/azure/storage/blob#az-storage-blob-upload-batch) - every flag the upload step in `create-bindings-app.azcli` uses
- [az cosmosdb reference](https://learn.microsoft.com/en-us/cli/azure/cosmosdb) - account, database, and container commands used by `create-fooddb.azcli`
- [Use the Azure CLI successfully in PowerShell](https://learn.microsoft.com/en-us/cli/azure/use-azure-cli-successfully-powershell) - quoting and variable rules that differ when Copilot translates the script

[← Back to IaC & Configuration](../readme.md) | [Next: Remote Configuration over SSH →](../02-ssh/readme.md)
