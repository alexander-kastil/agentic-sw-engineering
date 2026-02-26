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

Skills use progressive disclosure to efficiently load content in three levels: Copilot discovers available skills by reading their name and description from YAML frontmatter, then loads detailed instructions only when your request matches a skill's description. Additional resources like scripts and examples load on-demand, ensuring you can install many skills without consuming unnecessary context. This architecture means skills are automatically activated based on your prompt without manual selection. |

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

## Skills in This Repository

| Skill                                                                     | Description                                                                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [ado-create-wif](/.github/skills/ado-create-wif/SKILL.md)                 | Automate creation of Azure DevOps workload identity federation service connections with deployment metadata from deploy.json. Use when users need to create or delete Azure service connections with workload identity federation for secure, passwordless authentication.                                                |
| [ado-get-pipeline-logs](/.github/skills/ado-get-pipeline-logs/SKILL.md)   | Get logs from the latest Azure DevOps pipeline run using patterns that actually work.                                                                                                                                                                                                                                    |
| [ado-import-pipeline](/.github/skills/ado-import-pipeline/SKILL.md)       | Automate the import and execution of Azure DevOps pipelines from YAML files using deployment metadata. Use this when users need to import pipelines to Azure DevOps, run them, and fix any errors that occur during execution.                                                                                           |
| [angular-component](/.github/skills/angular-component/SKILL.md)           | Create modern Angular standalone components following v20+ best practices. Use for building UI components with signal-based inputs/outputs, OnPush change detection, host bindings, content projection, and lifecycle hooks. Triggers on component creation, refactoring class-based inputs to signals, adding host bindings, or implementing accessible interactive components. |
| [angular-di](/.github/skills/angular-di/SKILL.md)                         | Implement dependency injection in Angular v20+ using inject(), injection tokens, and provider configuration. Use for service architecture, providing dependencies at different levels, creating injectable tokens, and managing singleton vs scoped services. Triggers on service creation, configuring providers, using injection tokens, or understanding DI hierarchy.       |
| [angular-forms](/.github/skills/angular-forms/SKILL.md)                   | Build signal-based forms in Angular v21+ using the new Signal Forms API. Use for form creation with automatic two-way binding, schema-based validation, field state management, and dynamic forms. Triggers on form implementation, adding validation, creating multi-step forms, or building forms with conditional fields. Signal Forms are experimental but recommended for new Angular projects. |
| [angular-http](/.github/skills/angular-http/SKILL.md)                     | Implement HTTP data fetching in Angular v20+ using resource(), httpResource(), and HttpClient. Use for API calls, data loading with signals, request/response handling, and interceptors. Triggers on data fetching, API integration, loading states, error handling, or converting Observable-based HTTP to signal-based patterns.                                              |
| [angular-routing](/.github/skills/angular-routing/SKILL.md)               | Implement routing in Angular v20+ applications with lazy loading, functional guards, resolvers, and route parameters. Use for navigation setup, protected routes, route-based data loading, and nested routing. Triggers on route configuration, adding authentication guards, implementing lazy loading, or reading route parameters with signals.                              |
| [angular-signals](/.github/skills/angular-signals/SKILL.md)               | Implement signal-based reactive state management in Angular v20+. Use for creating reactive state with signal(), derived state with computed(), dependent state with linkedSignal(), and side effects with effect(). Triggers on state management questions, converting from BehaviorSubject/Observable patterns to signals, or implementing reactive data flows.                |
| [browser-use](/.github/skills/browser-use/SKILL.md)                       | Automate browser interactions and tasks using CLI or Python. Use when testing web applications, capturing screenshots, extracting data, automating workflows, testing forms, or running autonomous browser agents. Supports local (Chromium, real Chrome) and cloud (remote) browsers.                                   |
| [context7-auto-research](/.github/skills/context7-auto-research/SKILL.md) | Automatically fetch latest library/framework documentation for Claude Code via Context7 API.                                                                                                                                                                                                                             |
| [copilot-sdk](/.github/skills/copilot-sdk/SKILL.md)                       | Build agentic applications with GitHub Copilot SDK. Use when embedding AI agents in apps, creating custom tools, implementing streaming responses, managing sessions, connecting to MCP servers, or creating custom agents.                                                                                              |
| [create-docx](/.github/skills/create-docx/SKILL.md)                       | Create, edit, analyze, and validate Word documents (.docx files) programmatically. Use when generating reports, creating templates, automating document generation, editing existing documents with tracked changes, or converting documents to other formats.                                                           |
| [create-ebook](/.github/skills/create-ebook/SKILL.md)                     | Builds a single PDF (and optional EPUB) from repo Markdown using Pandoc and uploads as a CI artifact. Use when generating documentation PDFs, creating ebook distributions, building PDF from markdown sources, or automating document distribution. Works with GitHub Actions workflow automation and supports custom ordering via .bookorder file. |
| [create-pptx](/.github/skills/create-pptx/SKILL.md)                       | Create, edit, analyze, and validate PowerPoint presentations (PPTX files). Use when asked to build presentations from scratch, modify existing templates, visualize presentation content, convert slides to images, or verify design quality.                                                                            |
| [find-skills](/.github/skills/find-skills/SKILL.md)                       | Help users discover and install specialized skills that extend GitHub Copilot capabilities. Use when users ask how to do something, whether a skill exists for a task, or want to find tools and workflows.                                                                                                              |
| [frontend-design](/.github/skills/frontend-design/SKILL.md)               | Create distinctive, production-grade frontend interfaces with exceptional aesthetic direction and full accessibility compliance. Covers design thinking, typography, color systems, animation, responsive layouts, and WCAG 2.2 accessibility standards.                                                                 |
| [install-openclaw-raspi](/.github/skills/install-openclaw-raspi/SKILL.md) | Deploy OpenClaw AI assistant on Raspberry Pi 4 with Node.js 22+. Use when setting up personal AI assistant, deploying AI chatbot on Pi, configuring voice-enabled AI agent, or automating Raspberry Pi AI setup.                                                                                                         |
| [linkedin-article](/.github/skills/linkedin-article/SKILL.md)             | Write long-form LinkedIn articles that establish deep thought leadership and drive sustained engagement. Use when creating in-depth content pieces, publishing detailed frameworks, sharing research-backed insights, building authority through comprehensive storytelling, documenting industry trends, or creating evergreen content that drives organic traffic. |
| [mermaid-expert](/.github/skills/mermaid-expert/SKILL.md)                 | Create Mermaid diagrams for flowcharts, sequences, ERDs, and architectures. Masters syntax for all diagram types and styling. Use proactively for visual documentation, system diagrams, or process flows.                                                                                                               |
| [net-cli](/.github/skills/net-cli/SKILL.md)                               | Master .NET CLI commands for project management. Use when building, testing, running projects, managing NuGet packages, formatting code, configuring solutions, using hot reload with watch mode, or troubleshooting build issues.                                                                                       |
| [pdf-creator](/.github/skills/pdf-creator/SKILL.md)                       | Create, edit, analyze, and validate PDF files and documents. Use when generating reports, merging PDFs, extracting text and tables, creating documents dynamically, or processing scanned PDFs with OCR.                                                                                                                 |
| [react-skills](/.github/skills/react-skills/SKILL.md)                     | Build clean, accessible React components with TypeScript and Fluent UI. Use when creating new React components, converting designs to code, building reusable UI patterns, optimizing component performance, implementing accessibility guidelines, or structuring React projects.                                       |
| [react-state-mgmt](/.github/skills/react-state-mgmt/SKILL.md)             | Manage React state across projects using modern patterns. Use when setting up global state management, choosing between Redux Toolkit, Zustand, or Jotai, managing server state with React Query, implementing optimistic updates, handling form state, debugging state issues, or migrating from legacy Redux patterns. |
| [sequential-navigation](/.github/skills/sequential-navigation/SKILL.md)   | Transform large markdown documents into organized, guided navigation workflows. Breaks monolithic files into sequential sections with bidirectional navigation (back to hub, next section). Creates seamless user experiences for tutorials, exercises, step-by-step guides, and learning materials across multiple files. |
| [social-content](/.github/skills/social-content/SKILL.md)                 | Expert social media strategist for content creation and audience building. Use when creating social content strategies, developing content calendars, writing engaging posts, repurposing content across platforms, analyzing social metrics, building personal and company brands, or optimizing engagement. Covers LinkedIn, Twitter/X, Instagram, TikTok, and Facebook with platform-specific strategies, hook formulas, and content pillars framework. |
| [visualize-conversation](/.github/skills/visualize-conversation/SKILL.md) | Generate, update or delete Copilot conversation visualization markdown from session JSON data collected by Copilot hooks.                                                                                                                                                                                                |

## Links & Resources

- [VS Code Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Agent Skills Standard](https://agentskills.io/)
- [GitHub Awesome Copilot Community Skills](https://github.com/github/awesome-copilot)
- [Skills.sh - A directory of open-source agent skills across platforms](https://skills.sh/)
- [Awesome Skills](https://github.com/alexander-kastil/skills-collection)
- [npx skills add](https://github.com/vercel-labs/skills)
