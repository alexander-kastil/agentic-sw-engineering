# Agent Skills

## What are Agent Skills?

Agent Skills are portable folders containing instructions, scripts, and resources that Copilot can load to perform specialized tasks. Skills follow an open standard that works across multiple AI agents—GitHub Copilot in VS Code, GitHub Copilot CLI, and GitHub Copilot coding agent—making them reusable and composable for complex workflows.

## Enable Agent Skills

Enable skills discovery and auto-loading in VS Code:

```json
{
  "chat.useAgentSkills": true,
  "chat.agent.enabled": true,
  "chat.detectParticipant.enabled": true
}
```

## How Skills are Loaded

Skills use progressive disclosure to efficiently load content in three levels: Copilot discovers available skills by reading their name and description from YAML frontmatter, then loads detailed instructions only when your request matches a skill's description. Additional resources like scripts and examples load on-demand, ensuring you can install many skills without consuming unnecessary context. This architecture means skills are automatically activated based on your prompt without manual selection.

## Skills in This Repository

| Skill                                                                     | Description                                                                                                                                                                   |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [copilot-sdk](/.github/skills/copilot-sdk/SKILL.md)                       | Build agentic applications with GitHub Copilot SDK in Python, TypeScript, Go, or .NET. Embed AI agents in apps, create custom tools, and connect to MCP servers.              |
| [create-pptx](/.github/skills/create-pptx/SKILL.md)                       | Create, edit, analyze, and validate PowerPoint presentations from scratch or templates. Build presentations with design validation, slide thumbnails, and content extraction. |
| [get-pipeline-logs](/.github/skills/get-pipeline-logs/SKILL.md)           | Retrieve logs from Azure DevOps pipeline runs using patterns that work reliably even with deleted builds.                                                                     |
| [import-pipeline](/.github/skills/import-pipeline/SKILL.md)               | Automate Azure DevOps pipeline import and execution from YAML files using deployment metadata. Diagnoses errors and applies fixes automatically.                              |
| [install-openclaw-raspi](/.github/skills/install-openclaw-raspi/SKILL.md) | Deploy OpenClaw AI assistant on Raspberry Pi 4 with Node.js 22+. Handles hardware requirements, OS installation, SSH setup, and full deployment.                              |
| [net-cli](/.github/skills/net-cli/SKILL.md)                               | Master .NET CLI commands for project management, builds, tests, and package management. Supports hot reload, code formatting, and solution configuration.                     |
| [react-skills](/.github/skills/react-skills/SKILL.md)                     | Build clean, accessible React components with TypeScript and Fluent UI. Create reusable UI patterns with WCAG 2.2 compliance and performance optimization.                    |
| [react-state-mgmt](/.github/skills/react-state-mgmt/SKILL.md)             | Manage React state using Redux Toolkit, Zustand, Jotai, or React Query. Handle global state, server state synchronization, and optimistic updates.                            |
| [visualize-conversation](/.github/skills/visualize-conversation/SKILL.md) | Generate Mermaid sequence diagrams from Copilot conversation session data collected by hooks. Visualize or delete conversations interactively.                                |

## Sample Skill YAML

Skills are defined with a `SKILL.md` file containing YAML frontmatter and Markdown body:

```yaml
---
name: skill-name
description: Description of what the skill does and when to use it
---

# Skill Instructions

Your detailed instructions, guidelines, and examples go here...
```

## Demos

### Build Agentic Applications with Copilot SDK

Sample prompts to trigger this skill:

- "Help me create an agentic application using Copilot SDK"
- "Build a custom tool that uses the GitHub Copilot SDK"
- "Set up a Python agent with Copilot SDK and MCP server integration"
- "Create a TypeScript agent application with streaming responses"

### Create PowerPoint Presentations

Sample prompts to trigger this skill:

- "Create a PowerPoint presentation about Azure DevOps best practices"
- "Generate slides from markdown content for my project"
- "Build a presentation with 5 slides on CI/CD pipelines"
- "Create a professional PowerPoint and validate the design"

### Import Pipeline to Azure DevOps and Troubleshoot Failures

Sample prompts to trigger this skill:

- "Import the angular-cd pipeline to Azure DevOps and run it"
- "Load the ci-build pipeline from YAML and execute it"
- "Import my DevOps pipeline and fix any failures"
- "Deploy the pipeline from .azdo/pipelines/ and troubleshoot errors"

### Install OpenClaw on Raspberry Pi

Sample prompts to trigger this skill:

- "Deploy OpenClaw AI assistant on my Raspberry Pi 4"
- "Set up a voice-enabled AI chatbot on Raspberry Pi with Node.js"
- "Configure Raspberry Pi for 24/7 OpenClaw operation"
- "Help me install OpenClaw and set up SSH access"

### Master .NET CLI

Sample prompts to trigger this skill:

- "Help me build and test my .NET project with hot reload"
- "Format my C# code and manage NuGet packages"
- "Set up a multi-project .NET solution with proper SDK configuration"
- "Run my .NET tests and troubleshoot build issues"

### Build React Components

Sample prompts to trigger this skill:

- "Create an accessible React component with TypeScript"
- "Convert this design mockup to a React component"
- "Build a reusable UI pattern with WCAG compliance"
- "Optimize my React component for performance and accessibility"

### Manage React State

Sample prompts to trigger this skill:

- "Set up global state management with Redux Toolkit"
- "Help me choose between Zustand and Jotai for state management"
- "Implement React Query for server state management"
- "Migrate from old Redux patterns to a modern approach"

## Key Topics Covered in This Section

- [VS Code Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Agent Skills Standard](https://agentskills.io/)
- [GitHub Awesome Copilot Community Skills](https://github.com/github/awesome-copilot)
- [Skills.sh - A directory of open-source agent skills across platforms](https://skills.sh/)
- [Awesome Skills](https://github.com/alexander-kastil/skills-collection)
