# Copilot SDK Console Demo

A simple .NET 10 console application demonstrating the GitHub Copilot SDK.

## Overview

This application creates a Copilot session, sends a user prompt, and displays the AI response. Configuration is loaded from appsettings.json.

## Prerequisites

- .NET 10 SDK
- A signed-in GitHub Copilot account. The `GitHub.Copilot.SDK` package bundles the CLI runtime, so a separate install is optional; run `copilot` once and `/login`, or set `GITHUB_TOKEN` for an unattended run.

## Setup

1. Navigate to this directory:
   ```bash
   cd demos/05-cli-sdk/02-sdk/01-intro/copilot-sdk-console-cs
   ```

2. Restore dependencies:
   ```bash
   dotnet restore
   ```

## Configuration

Edit `appsettings.json` to customize:

- `model`: AI model to use (default: gpt-5-mini). Which models you can pick depends on your Copilot plan and organization policy; call `client.ListModelsAsync()` or run `/model` in the CLI to see the list for your account.
- `prompt`: User prompt to send (default: "What are the use cases for Copilot SDK?")

## Running the Application

```bash
dotnet run
```

Output shows the model name, prompt, and AI response.

## Features

- Loads configuration from appsettings.json
- Uses GitHub Copilot SDK to create sessions and send messages
- Includes error handling for missing responses
- Clean separation of configuration and logic

## MCP Integration

To reach Microsoft Learn or any other MCP server, register it with `copilot mcp add` so the bundled runtime picks it up, or pass the server on `SessionConfig` when you create the session.

## Links & Resources

- [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md) - the client, session, and message flow this sample implements
- [.NET SDK reference](https://github.com/github/copilot-sdk/blob/main/dotnet/README.md) - `CopilotClient`, `SessionConfig`, and `MessageOptions` in full
- [GitHub.Copilot.SDK on NuGet](https://www.nuget.org/packages/GitHub.Copilot.SDK) - released versions and target frameworks
