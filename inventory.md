# Gap Inventory

This file records the difference between the customer's target outline in [assets/metro.md](assets/metro.md) and the demo tree on disk under [demos/](demos/) after the renumbering. Every line count below was measured with `wc -l`, every folder was confirmed with `ls`, and every Exercise flag comes from a grep for an `Exercise` heading. It lists facts about the current state only.

## Missing content

Every topic metro.md names has a folder and a `readme.md` on disk. Two of those readmes are bare stubs.

| Module | Topic (metro title) | Folder | State | Notes |
| --- | --- | --- | --- | --- |
| 3 Implementing Agentic Coding | Using Local Agents and Agent Mode | [demos/03-agentic-coding/01-local-agents/](demos/03-agentic-coding/01-local-agents/) | Stub, 3 lines | H1 plus one intro paragraph linking to `03-orchestration` and `02-cloud`. No demo steps, no Exercise, no Links & Resources. |

## On disk but not in metro.md

These topics sit inside modules metro.md does cover, and were appended at the end of their module. Modules 1 and 6 are covered in the next section.

| Module | Topic | Folder | Where it was placed | Notes |
| --- | --- | --- | --- | --- |
| 5 GitHub Copilot CLI & SDK | Extending the CLI with MCP Servers & Skills | [demos/05-cli-sdk/01-cli/04-mcp-skills/](demos/05-cli-sdk/01-cli/04-mcp-skills/) | After `03-agentic-wf`, the last CLI topic metro.md names | 22 lines, has an Exercise section |
| 5 GitHub Copilot CLI & SDK | Codebase Q&A and Onboarding | [demos/05-cli-sdk/01-cli/05-codebase-qa/](demos/05-cli-sdk/01-cli/05-codebase-qa/) | Last topic in the CLI half | 22 lines, has an Exercise section |
| 5 GitHub Copilot CLI & SDK | Deploying an SDK Agent to Azure | [demos/05-cli-sdk/02-sdk/04-deploy-azure/](demos/05-cli-sdk/02-sdk/04-deploy-azure/) | After `03-mcp-apps`, the last SDK topic metro.md names | 22 lines, has an Exercise section |
| 5 GitHub Copilot CLI & SDK | Building a Multi-Agent System | [demos/05-cli-sdk/02-sdk/05-multi-agent/](demos/05-cli-sdk/02-sdk/05-multi-agent/) | Last topic in the SDK half | 22 lines, has an Exercise section |
| 8 Governance, Cost & Observability | Cutting Token Cost with Open-Source Models | [demos/08-governance/05-open-source-models/](demos/08-governance/05-open-source-models/) | After `04-observability`, the last topic metro.md names | 37 lines, carries two subtopics (`01-vscode`, `02-copilot-cli`) |
| 8 Governance, Cost & Observability | EU AI Act, GDPR & Accessibility Compliance | [demos/08-governance/06-compliance/](demos/08-governance/06-compliance/) | Last topic in the module | 89 lines, has an Exercise section |
| 9 Spec-Driven Development & Delivery | Getting Started with GitHub Spec Kit | [demos/09-spec-driven-dev/06-requirements/](demos/09-spec-driven-dev/06-requirements/) | After `05-sample-case`, the last topic metro.md names | 21 lines |

## Modules metro.md does not cover

metro.md names modules 2, 3, 4, 5, 7, 8 and 9. It carries no heading and no topic list for modules 1 and 6, so there is no target title and no target topic order to compare those two against. Both exist in full on disk and keep their current titles and topic order.

| Module | Folder | Current title on disk | Topics on disk |
| --- | --- | --- | --- |
| 1 | [demos/01-fundamentals/](demos/01-fundamentals/) | Fundamentals & Agent Mode Basics | 7: `01-intro`, `02-models`, `03-ai-assisted-coding`, `04-agent-mode-basics`, `05-pr-code-review`, `06-mgmt-settings`, `07-terminal` |
| 6 | [demos/06-copilot-app/](demos/06-copilot-app/) | GitHub Copilot App | 5: `01-overview`, `02-sessions`, `03-validation-loop`, `04-automations`, `05-sync` |

## Thin topics

Topic-level folders whose `readme.md` is under roughly 30 lines, plus topics with no Exercise section where their siblings have one.

| Module | Topic | Folder | readme lines | What is missing |
| --- | --- | --- | --- | --- |
| 1 | Pull Requests & Code Reviews | [demos/01-fundamentals/05-pr-code-review/](demos/01-fundamentals/05-pr-code-review/) | 11 | Prose only, two short sections. No demo steps, no Exercise, no Links & Resources |
| 1 | Agent Mode Basics | [demos/01-fundamentals/04-agent-mode-basics/](demos/01-fundamentals/04-agent-mode-basics/) | 24 | Index readme with a table linking its three subtopics, no Exercise |
| 4 | Agent Host Protocol (AHP vs ACP) | [demos/04-agent-sessions/02-host-protocol/](demos/04-agent-sessions/02-host-protocol/) | 34 | No Exercise section. The other six topics in module 4 all have one |
| 3 | Using Local Agents and Agent Mode | [demos/03-agentic-coding/01-local-agents/](demos/03-agentic-coding/01-local-agents/) | 3 | Everything past the intro paragraph |
| 3 | Delegating Tasks to Cloud Agents | [demos/03-agentic-coding/02-cloud/](demos/03-agentic-coding/02-cloud/) | 12 | One paragraph and one comparison table. No demo steps, no Exercise, no Links & Resources |
| 5 | Extending the CLI with MCP Servers & Skills | [demos/05-cli-sdk/01-cli/04-mcp-skills/](demos/05-cli-sdk/01-cli/04-mcp-skills/) | 22 | Under the 30-line mark. Intro, two sections, Exercise and Links & Resources are all present |
| 5 | Codebase Q&A and Onboarding | [demos/05-cli-sdk/01-cli/05-codebase-qa/](demos/05-cli-sdk/01-cli/05-codebase-qa/) | 22 | Under the 30-line mark. Intro, two sections, Exercise and Links & Resources are all present |
| 5 | Deploying an SDK Agent to Azure | [demos/05-cli-sdk/02-sdk/04-deploy-azure/](demos/05-cli-sdk/02-sdk/04-deploy-azure/) | 22 | Under the 30-line mark. Intro, two sections, Exercise and Links & Resources are all present |
| 5 | Building a Multi-Agent System | [demos/05-cli-sdk/02-sdk/05-multi-agent/](demos/05-cli-sdk/02-sdk/05-multi-agent/) | 22 | Under the 30-line mark. Intro, two sections, Exercise and Links & Resources are all present |
| 6 | Meet the Desktop Agents App | [demos/06-copilot-app/01-overview/](demos/06-copilot-app/01-overview/) | 36 | No Exercise section. `02-sessions`, `03-validation-loop` and `04-automations` each have one |
| 6 | Syncing Skills & MCP Servers | [demos/06-copilot-app/05-sync/](demos/06-copilot-app/05-sync/) | 35 | No Exercise section. `02-sessions`, `03-validation-loop` and `04-automations` each have one |
| 7 | Automation using Azure CLI | [demos/07-agentic-devops/01-azure-cli/](demos/07-agentic-devops/01-azure-cli/) | 23 | No Exercise, no Links & Resources |
| 7 | Infrastructure as Code (IaC) | [demos/07-agentic-devops/02-IaC/](demos/07-agentic-devops/02-IaC/) | 23 | Index readme with a demos table for its three subtopics, no Exercise |
| 7 | Azure DevOps Pipelines & GitHub Actions | [demos/07-agentic-devops/03-pipelines/](demos/07-agentic-devops/03-pipelines/) | 19 | Two prose sections and one skills table. No demo steps, no Exercise, no Links & Resources |
| 7 | Testing using Copilot | [demos/07-agentic-devops/04-testing/](demos/07-agentic-devops/04-testing/) | 9 | One-line intro and a topics table listing only `food-app`. The `01-unit-tests` and `02-e2e` subtopics are not linked. No Exercise |
| 7 | Agentic E2E Testing using Playwright (subtopic of `04-testing`) | [demos/07-agentic-devops/04-testing/02-e2e/](demos/07-agentic-devops/04-testing/02-e2e/) | 1 | H1 only, no body at all |
| 8 | Cutting Token Cost with Open-Source Models | [demos/08-governance/05-open-source-models/](demos/08-governance/05-open-source-models/) | 37 | No Exercise at topic level. The other five topics in module 8 have one. Its `01-vscode` subtopic has one, `02-copilot-cli` does not |
| 9 | From Tasks to Working Code | [demos/09-spec-driven-dev/04-tasks/](demos/09-spec-driven-dev/04-tasks/) | 17 | Prose and a key-topics list. No demo steps, no Exercise, no Links & Resources |
| 9 | Exercise: Implement a product feature using GitHub Spec Kit | [demos/09-spec-driven-dev/05-sample-case/](demos/09-spec-driven-dev/05-sample-case/) | 18 | Points at an external lab repository and lists its artifacts. No in-repo demo steps |
| 9 | Getting Started with GitHub Spec Kit | [demos/09-spec-driven-dev/06-requirements/](demos/09-spec-driven-dev/06-requirements/) | 21 | Install snippet and a command list. The fenced block declares no language. No Exercise |
