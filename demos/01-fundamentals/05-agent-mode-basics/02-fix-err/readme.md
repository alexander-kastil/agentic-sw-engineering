# Fixing Errors

A C# console application calls Microsoft Foundry with keyless authentication: a chat client using DefaultAzureCredential and a Project Endpoint, with no API keys. Key files are [Program.cs](foundry-sdk-cs/Program.cs) which loads configuration from appsettings.json, and [ChatRunner.cs](foundry-sdk-cs/ChatRunner.cs) which demonstrates creating an authenticated chat client and making chat completion requests.

## Task Prompt

```text
Examine #terminalLastCommand. I want keyless authentication using the Project Endpoint
and Default Azure Credentials (azure cli logged in). Check packages and use ms learn mcp
to find out if you need to upgrade them. use dotnet cli for all package mgmt and cleaning.
```
