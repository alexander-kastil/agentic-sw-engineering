# IaC & Configuration

Infrastructure as Code enables repeatable, version-controlled deployments through scripts and declarative templates. This topic walks the full spectrum, starting with imperative Azure CLI automation, moving through remote host configuration over SSH, and ending with the declarative templates used by Bicep and Terraform.

Copilot is useful at every point on that spectrum. It reads application source code to derive the resources an app actually needs, translates scripts between shells and template languages, scaffolds module layouts that follow azd conventions, and drives a shell on a remote host through an MCP server.

Pipelines that run these deployments authenticate to Azure with OpenID Connect rather than stored credentials. The federated credential setup lives with the pipeline topic in [CI/CD with GitHub Actions](../02-cicd/), so run that script before deploying any of the demos below from a workflow.

Not every deployment target is a managed Azure service. The SSH topic covers the case where the infrastructure is a plain Linux box with no cloud control plane, where configuration is something an agent applies over a shell session rather than something a template declares.

> Note: The azd topic is optional. It is a workflow layer over Bicep and Terraform, so teams that provision with those directly can skip it and go straight to `03-ssh`.

## Demos

| Demo                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Automation using Azure CLI](01-azure-cli)**           | Imperative provisioning with `az` scripts. Generate a deployment script from Azure Function source code by reading its bindings and configuration, then translate an existing script to PowerShell.                                                                                                                                                                                                                        |
| **[Azure Developer CLI (azd)](02-azd)** *(optional)*     | Infrastructure orchestration framework demonstrating how Azure Developer CLI streamlines development workflow by integrating infrastructure provisioning with application code while maintaining separation of concerns through structured project conventions. The azd tool provides hooks for custom deployment logic and integrates with either Bicep or Terraform.                                                     |
| **[Remote Configuration over SSH](03-ssh)**              | Operate a Linux host that has no cloud control plane. Wire the SSH MCP server so Copilot runs commands on the box, install the `ssh-ops` skill so it knows the key handling, diagnostic order, and deployment sequence, then let the agent bring a container stack up and prove it healthy.                                                                                                                                 |
| **[Bicep Infrastructure Templates](04-bicep)**           | Infrastructure as Code for the food-app using Microsoft's Bicep domain-specific language following Azure Developer CLI conventions. Bicep provides declarative, modular Azure resource definitions with strong type safety and built-in support for Azure best practices. Focuses on structuring Bicep files with proper parameterization, module organization, and environment-specific configurations.                   |
| **[Terraform Multi-Cloud Infrastructure](05-terraform)** | Demonstrates using Terraform with Azure Developer CLI to manage infrastructure across multiple cloud providers. Terraform's HCL language and provider ecosystem enable consistent infrastructure management whether deploying to Azure, AWS, or other cloud platforms. Shows how to structure Terraform files following azd conventions while maintaining compatibility with the broader infrastructure-as-code ecosystem. |

## Links & Resources

[Infrastructure as Code on Azure](https://learn.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code)

[Azure Workload Identity Federation Overview](https://learn.microsoft.com/en-us/azure/active-directory/workload-identities/workload-identity-federation)
