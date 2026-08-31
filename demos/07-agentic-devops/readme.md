# Agentic DevOps

## Infrastructure, CI/CD, Testing & Documentation

Integrate AI-assisted development with enterprise DevOps practices. This module opens with infrastructure as code, from imperative Azure CLI scripts to declarative azd, Bicep, and Terraform templates, then adds remote host configuration over SSH before moving to GitHub Actions pipelines, agent-generated tests, and documentation so shipped work stays measurable and verifiable.

| Topic                                                    | Description                                                                                                    |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **[IaC & Configuration](./01-iac-cfg/)**       | Provision Azure with CLI automation, azd, Bicep, and Terraform, and configure remote Linux hosts over SSH, all driven by Copilot. |
| **[CI/CD with GitHub Actions](./02-cicd/)**              | Build workflows that test, build, and deploy to Azure using OpenID Connect instead of stored secrets.          |
| **[Testing using Copilot](./03-testing/)**               | Generate unit tests and end-to-end Playwright suites for agentic implementations.                              |
| **[Documentation using Copilot](./04-documentation/)**   | Produce docs with Mermaid diagrams rendered in Markdown preview, notebooks, and chat.                          |
