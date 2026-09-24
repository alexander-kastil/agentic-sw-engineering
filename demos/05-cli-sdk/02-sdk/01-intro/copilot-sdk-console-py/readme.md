# Copilot SDK Console Demo (Python)

A simple Python console application demonstrating the GitHub Copilot SDK. It is the Python port of [copilot-sdk-console-cs](../copilot-sdk-console-cs/).

## Overview

This application creates a Copilot session, sends a user prompt, and displays the AI response. Configuration is loaded from appsettings.json.

## Prerequisites

- Python 3.11 or later
- A signed-in GitHub Copilot account. The `github-copilot-sdk` package bundles the CLI runtime, so a separate install is optional; run `copilot` once and `/login`, or set `GITHUB_TOKEN` for an unattended run.

## Setup

1. Navigate to this directory:
   ```bash
   cd demos/05-cli-sdk/02-sdk/01-intro/copilot-sdk-console-py
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv/Scripts/python -m pip install -r requirements.txt
   ```

   On macOS or Linux the interpreter is `.venv/bin/python`.

## Configuration

Edit `appsettings.json` to customize:

- `model`: AI model to use (default: gpt-5-mini). Which models you can pick depends on your Copilot plan and organization policy; call `await client.list_models()` or run `/model` in the CLI to see the list for your account.
- `prompt`: User prompt to send (default: "What are the use cases for Copilot SDK?")

## Running the Application

```bash
.venv/Scripts/python main.py
```

Output shows the model name, prompt, and AI response.

## Links & Resources

- [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md) - the client, session, and message flow this sample implements
- [Python SDK reference](https://github.com/github/copilot-sdk/blob/main/python/README.md) - `CopilotClient`, `create_session`, and `send_and_wait` in full
- [github-copilot-sdk on PyPI](https://pypi.org/project/github-copilot-sdk/) - released versions
