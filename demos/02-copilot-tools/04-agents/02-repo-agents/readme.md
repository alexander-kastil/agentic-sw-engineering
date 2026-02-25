# Custom Agents used in this Class

These agents are configured in this repository and optimized for specific development tasks within the AZ-400 DevOps training environment.

| Agent                                                                                               | Purpose                                                                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Azure DevOps Specialist](/.github/agents/AzDevOps.agent.md)                                        | Azure DevOps pipeline specialist that writes, imports, and runs pipelines using best practices from Microsoft Learn MCP and configuration values from Copilot memory. Diagnoses pipeline issues and manages service connections. |
| [Azure Deployment Specialist](/.github/agents/AzureDeployment.agent.md)                             | Expert Azure deployment agent specializing in Azure CLI operations, infrastructure provisioning, deployment orchestration, and log analysis using official Microsoft documentation.                                              |
| [Codespaces](/.github/agents/Codespaces.agent.md)                                                   | Analyzes any repository to propose and scaffold an optimized GitHub Codespaces and Devcontainer setup. Auto-detects languages/frameworks, recommends VS Code extensions, and tunes devcontainer features for fast startup.       |
| [GH Actions](/.github/agents/GH%20Actions.agent.md)                                                 | GitHub Actions workflow specialist that authors, optimizes, and troubleshoots pipelines using Microsoft Learn MCP guidance and Copilot context.                                                                                  |
| [Microsoft Agent Framework Python](/.github/agents/microsoft-agent-framework-python.agent.md)       | Create, update, refactor, explain or work with code using the Python version of Microsoft Agent Framework.                                                                                                                       |
| [RaspiExpert](/.github/agents/RaspiExpert.agent.md)                                                 | Expert assistant for Raspberry Pi development, configuration, and remote management via SSH.                                                                                                                                     |
| [Team Coder](/.github/agents/team-coder.agent.md)                                                   | Writes code following mandatory coding principles for projects of any complexity or scale.                                                                                                                                       |
| [Team Frontend](/.github/agents/team-frontend.agent.md)                                             | Handles all UI/UX design tasks with expertise in component development and accessibility.                                                                                                                                        |
| [Team Orchestrator](/.github/agents/team-orchestrator.agent.md)                                     | Orchestrates complex workflows and multi-step tasks with model flexibility across Sonnet, Codex, and Gemini.                                                                                                                     |
| [Team Planner](/.github/agents/team-planner.agent.md)                                               | Creates comprehensive implementation plans by researching the codebase, consulting documentation, and identifying edge cases for complex feature work.                                                                           |
| [Azure Terraform IaC Implementation Specialist](/.github/agents/terraform-azure-implement.agent.md) | Act as an Azure Terraform Infrastructure as Code coding specialist that creates and reviews Terraform for Azure resources.                                                                                                       |

## Demo

### Using Terraform Agent

Use the Azure Terraform IaC Implementation Specialist agent to generate infrastructure-as-code for the copilot-api application. This demo shows how to invoke the agent with a structured prompt to create a complete Terraform module.

Sample prompt for the agent:

```
Create a Terraform module for deploying the src/copilot-api application to Azure. The module should:

1. Create an Azure App Service Plan with B2 SKU
2. Create an App Service to host the .NET API
3. Configure application settings
4. Add managed identity for secure authentication
5. Output the API endpoint URL

Place the module in infra/terraform/ following standard Terraform project structure with main.tf, variables.tf, outputs.tf, and terraform.tfvars.
```

### Raspberry Pi Agent

The RaspiExpert agent provides remote management capabilities for Raspberry Pi devices and Linux VMs using SSH MCP tools. It's particularly useful for executing commands, managing services, deploying applications, and configuring devices without needing manual SSH access. Beyond Raspberry Pi, these same techniques apply to any Linux-based environment including Azure Virtual Machines and edge devices.

Connect to your Raspberry Pi and retrieve system information:

```
I have a Raspberry Pi 4 at 192.168.0.143 with username 'alex'. Connect to it and show me the available RAM using the free command with human-readable output.
```

Check Docker service status:

```
Is Docker running on my Raspberry Pi? Check the Docker service status and show me a list of running containers.
```

Test software install capability:

```
Can I install OpenClaw on my Raspberry Pi 4? Check if OpenClaw is available in the default repositories and whether the system has enough disk space and RAM to support it.
```

## Key Topics Covered in This Module

- [GitHub Copilot Agents Documentation](https://docs.github.com/en/copilot/building-copilot-extensions/about-agents)
- [Azure DevOps REST API](https://learn.microsoft.com/en-us/azure/devops/integrate/concepts/rest-api-overview)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Codespaces](https://docs.github.com/en/codespaces)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
