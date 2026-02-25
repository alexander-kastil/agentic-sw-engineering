# Azure DevOps Pipelines & GitHub Actions

## Azure DevOps Pipelines

GitHub Copilot with the Azure DevOps agent can write production-ready pipeline YAML following Microsoft Learn best practices. The agent understands your project structure, generates pipelines for CI/CD workflows, and handles the full lifecycle from creation through execution and troubleshooting.

Three core skills complement the Azure DevOps agent to handle operational tasks you'll encounter when managing pipelines. These skills automate common workflows like importing pipelines, retrieving execution logs, and setting up secure authentication with workload identity federation. Together, the agent and skills provide a complete pipeline development and operations toolkit.

| Skill                                                                   | Purpose                                                                             | Works with Azure DevOps Agent                                              |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [ado-import-pipeline](/.github/skills/ado-import-pipeline/SKILL.md)     | Automate importing pipeline YAML to Azure DevOps and execute runs                   | Imports and executes pipelines created by the agent                        |
| [ado-get-pipeline-logs](/.github/skills/ado-get-pipeline-logs/SKILL.md) | Retrieve execution logs from pipeline runs for diagnostics and troubleshooting      | Collects logs when agent diagnostics need detailed failure analysis        |
| [ado-create-wif](/.github/skills/ado-create-wif/SKILL.md)               | Automate workload identity federation service connections for secure authentication | Provides authentication infrastructure needed by agent-generated pipelines |

## GitHub Actions

The GitHub Actions agent writes and manages workflows using Microsoft Learn best practices, handling authoring, optimization, troubleshooting, and security posture. It creates production-ready YAML for single and multi-job workflows, manages environments and secrets, and integrates third-party marketplace actions securely.

This agent assists with designing workflows that match your repository structure, evaluating and locking down action dependencies, and diagnosing workflow failures with detailed root cause analysis. It enforces least-privilege access controls and helps you adopt reusable workflows and OpenID Connect federation for cloud deployments.
