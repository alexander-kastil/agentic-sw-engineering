# IaC & Configuration


Infrastructure as Code enables repeatable, version-controlled deployments through scripts and declarative templates. This topic walks the full spectrum, starting with imperative Azure CLI automation, moving through remote host configuration over SSH, and ending with the declarative templates used by Bicep and Terraform.

Copilot is useful at every point on that spectrum. It reads application source code to derive the resources an app actually needs, translates scripts between shells and template languages, scaffolds module layouts that follow azd conventions, and drives a shell on a remote host through an MCP server.

Pipelines that run these deployments need an Azure credential before they can provision anything. The credential setup lives with the pipeline topic in [CI/CD with GitHub Actions](../02-cicd/), so run `set-repo-secrets.sh` there before deploying any of the demos below from a workflow.

Not every deployment target is a managed Azure service. The SSH topic covers the case where the infrastructure is a plain Linux box with no cloud control plane, where configuration is something an agent applies over a shell session rather than something a template declares.

## Demos

| Demo                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Automation using Azure CLI](01-azure-cli)**           | Imperative provisioning with `az` scripts. Generate a deployment script from Azure Function source code by reading its bindings and configuration, then translate an existing script to PowerShell.                                                                                                                                                                                                                        |
| **[Remote Configuration over SSH](02-ssh)**              | Drive a Raspberry Pi or any Linux host from chat. Register the ssh-mcp server, use the Raspi SSH agent and the `ssh-ops` skill, and let the agent probe the box, install what it needs, and prove the result with real command output. |
| **[Declarative Templates with Bicep and Terraform](03-declarative)** | Write the desired end state instead of the steps to reach it. Generate azd-compatible Bicep modules and Terraform HCL for the same food-app, switch azd between the two providers, and validate both without touching a subscription. |

## Links & Resources

- [Infrastructure as Code on Azure](https://learn.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code) - what IaC is and how imperative scripts and declarative templates differ
- [Workload identity federation](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation) - how a pipeline trades a GitHub token for an Azure token instead of holding a secret

[← Back to Agentic DevOps](../readme.md) | [Next: CI/CD with GitHub Actions →](../02-cicd/readme.md)
