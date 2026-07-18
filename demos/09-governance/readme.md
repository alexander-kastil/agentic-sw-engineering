# Governance, Cost & Observability

## Running Agents Safely, Affordably, and Observably

This module serves the architects, team leads, and managers the course is built for. As agents gain autonomy and billing moves to usage-based AI credits, the questions that matter are governance, cost, and observability: what an agent is allowed to do, what each action costs, and how you see what happened. You will work through the permission model and sandboxing, the credit-based cost model, cutting that cost with open-source models, enterprise managed settings, OpenTelemetry tracing into an Azure Managed Grafana dashboard, and the regulatory compliance obligations that attach to the software your agents ship.

| Topic | Description |
|-------|-------------|
| [Trust, Safety & the Permission Model](./01-permissions/) | Permission levels, Autopilot defaults, terminal sandboxing, and risk badges. |
| [Cost Model & AI Credits](./02-cost/) | Usage-based billing, cost in the model picker, and per-session and per-subagent cost. |
| [Cutting Token Cost with Open-Source Models](./03-open-source-models/) | Route Copilot Chat and the CLI to DeepSeek and DeepInfra via OpenAI-compatible endpoints to cut per-token spend. |
| [Enterprise Policy & Managed Settings](./04-enterprise-policy/) | MDM delivery, managed-settings.json, and plugin and network policies. |
| [Observability with OpenTelemetry](./05-observability/) | GenAI-semantic-convention traces and the Azure Managed Grafana dashboard. |
| [EU AI Act, GDPR & Accessibility Compliance](./06-compliance/) | AI Act risk tiers and Article 50, DSGVO/GDPR personal-data checks, third-country transfers, and WCAG accessibility. |
