# Deploying an SDK Agent to Azure

A local SDK agent becomes a product when it runs as a hosted service. This topic takes an agent built with the Copilot SDK from your machine to Azure, so it can serve requests, scale, and sit behind your own API. The hosting library handles the protocol, the HTTP server, health checks, and request and response schemas, leaving your agent logic unchanged.

## The hosting pattern

Package the agent with a hosting library and deploy it to Azure Container Apps or App Service. The agent keeps its `CopilotClient`, sessions, and custom tools; only the entry point changes, from a terminal run to an HTTP handler. Configuration and secrets move to environment variables and Azure Key Vault rather than local files.

## Bring your own model

For data-control or cost reasons you can back the hosted agent with Azure OpenAI instead of the default model, the same bring-your-own-model idea covered in the Governance module. Point the client at your Azure OpenAI deployment and endpoint, and keep the key in Key Vault.

## Exercise

1. Wrap an existing SDK agent with the hosting library so it exposes an HTTP handler.
2. Deploy it to Azure Container Apps and confirm the health check responds.
3. Switch the model to an Azure OpenAI deployment and verify the agent still answers.

## Links & Resources

- [GitHub Copilot SDK Repository](https://github.com/github/copilot-sdk) - the SDK, hosting samples, and cookbook
- [Azure hosted Copilot SDK skill](https://learn.microsoft.com/azure/developer/azure-skills/skills/azure-hosted-copilot-sdk) - deploy an SDK app to Container Apps or App Service with BYOM
