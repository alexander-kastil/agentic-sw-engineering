# Fixing Errors

This module demonstrates a C# console application that integrates with Azure AI Foundry using keyless authentication. The sample shows how to configure and use a chat client with DefaultAzureCredential and a Project Endpoint to make chat completions.

The implementation uses the OpenAI SDK with Microsoft Entra ID authentication, eliminating the need for API keys. Key files include [Program.cs](foundry-sdk-cs/Program.cs) which loads configuration from appsettings.json, and [ChatRunner.cs](foundry-sdk-cs/ChatRunner.cs) which demonstrates creating an authenticated chat client and making chat completion requests.

## Task Prompt

```
Examine #terminalLastCommand. I want keyless authentication using the Project Endpoint
and Default Azure Credentials (azure cli logged in). Check packages and use ms learn mcp
to find out if you need to upgrade them. use dotnet cli for all package mgmt and cleaning.
```
