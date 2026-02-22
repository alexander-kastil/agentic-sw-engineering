# Copilot SDK Console Demo

A simple .NET 10 console application demonstrating the GitHub Copilot SDK.

## Overview

This application creates a Copilot session, sends a user prompt, and displays the AI response. Configuration is loaded from appsettings.json.

## Prerequisites

- .NET 10 SDK
- GitHub Copilot CLI installed and authenticated (`copilot --version`)

## Setup

1. Navigate to this directory:
   ```bash
   cd demos/04-copilot-cli/04-sdk/copilot-sdk-console
   ```

2. Restore dependencies:
   ```bash
   dotnet restore
   ```

## Configuration

Edit `appsettings.json` to customize:
- `model`: AI model to use (default: gpt-5-mini)
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

To enable Microsoft Learn MCP or other MCP servers, configure them in VS Code's MCP settings (.vscode/mcp.json) and ensure Copilot CLI is configured to use them.
