# Labs

Hands-on exercises to reinforce the concepts covered in the Agentic Software Engineering course. Each lab builds on the previous one, providing practical experience with GitHub Copilot and agentic development patterns.

| Lab | Title | Duration |
| --- | ----- | -------- |
| [Lab 01](#lab-01-getting-started) | Getting Started | 30 min |
| [Lab 02](#lab-02-github-codespaces) | GitHub Codespaces | 30 min |
| [Lab 03](#lab-03-ai-assisted-coding) | AI-Assisted Coding | 45 min |
| [Lab 04](#lab-04-testing-with-copilot) | Testing with Copilot | 60 min |
| [Lab 05](#lab-05-spec-driven-development) | Spec-Driven Development | 120 min |
| [Lab 06](#lab-06-agentic-software-engineering) | Agentic Software Engineering | 60 min |

---

## Lab 01: Getting Started

[Lab Materials](./01-get-started/)

Set up your development environment and explore the foundational features of GitHub Copilot in GitHub Codespaces.

### Learning Objectives

- Launch a GitHub Codespaces environment from the repository
- Navigate the cloud-based IDE and understand how Codespaces works
- Verify that GitHub Copilot is enabled and functional in the environment

### Prerequisites

- A GitHub account with access to GitHub Codespaces
- Basic familiarity with a code editor

---

## Lab 02: GitHub Codespaces

[Lab Materials](./02-codespaces/)

Develop code with AI-powered suggestions using GitHub Copilot inside GitHub Codespaces.

### Learning Objectives

- Use GitHub Copilot inline suggestions to write code faster
- Apply Copilot completions in a real coding scenario within VS Code
- Understand how Copilot interprets context to generate relevant suggestions

### Prerequisites

- Completed Lab 01
- Basic programming knowledge in any language

### Resources

- [Microsoft Learn: Introduction to GitHub Copilot – Exercise](https://learn.microsoft.com/en-us/training/modules/introduction-to-github-copilot/5-exercise)

---

## Lab 03: AI-Assisted Coding

[Lab Materials](./03-assisted-coding/)

Extend an existing Python web API using GitHub Copilot to add new routes, tests, and documentation.

### Learning Objectives

- Use Copilot to add new endpoints to a FastAPI web application
- Generate unit tests for new functionality using Copilot's `/tests` command
- Write project documentation with the help of `@workspace`

### Prerequisites

- Completed Lab 02
- Basic knowledge of Python and REST APIs
- Familiarity with FastAPI (helpful but not required)

### Resources

- [Microsoft Learn: Update a Web API with GitHub Copilot – Exercise](https://learn.microsoft.com/en-us/training/modules/advanced-github-copilot/5-exercise-update-a-web-api)

---

## Lab 04: Testing with Copilot

[Lab Materials](./04-testing/)

Use GitHub Copilot to accelerate test authoring for a .NET library application.

### Learning Objectives

- Generate unit tests for existing .NET service classes using Copilot
- Understand how Copilot maps domain logic to test scenarios
- Work with test factories and mocks to write isolated, maintainable tests

### Prerequisites

- Completed Lab 02
- Basic knowledge of C# and .NET
- Familiarity with unit testing concepts (xUnit, NUnit, or MSTest)

---

## Lab 05: Spec-Driven Development

[Lab Materials](./05-spec-driven/)

Implement a product feature end-to-end using the GitHub Spec Kit workflow and specification-driven agents.

### Learning Objectives

- Apply specification-driven development to decompose a feature into actionable tasks
- Use the GitHub Spec Kit agents (analyze, clarify, plan, implement, specify) to guide the workflow
- Maintain persistent specification context and decision history across development sessions

### Prerequisites

- Completed Labs 01–04
- Solid experience with software development
- Familiarity with GitHub Copilot agents and prompt files (Module 2)

> **Note:** This is an advanced lab designed for senior software engineers and architects. Expect to spend approximately 120 minutes to complete it.

### Resources

- [Spec-Driven Development Lab Repository](https://github.com/alexander-kastil/spec-drive-development-lab)

---

## Lab 06: Agentic Software Engineering

[Lab Materials](../demos/03-agentic-coding/)

Experience agentic software engineering hands-on by orchestrating multiple AI agents to plan, implement, and validate a real-world coding task using GitHub Copilot agent mode and cloud agents.

### Description

This lab introduces the core concepts and workflows of agentic software engineering. You will move beyond simple code completion into multi-step, autonomous agent workflows: delegating tasks to local and cloud agents, coordinating multiple agents to solve complex problems, and using Anthropic Claude Code Agents for advanced code generation and analysis. The lab gives you practical experience with the patterns that underpin modern agentic development.

### Learning Objectives

- Use GitHub Copilot in agent mode to autonomously complete multi-step coding tasks
- Delegate complex tasks to cloud-based agents and interpret their outputs
- Orchestrate multiple agents to coordinate solutions across a codebase
- Apply Claude Code Agents for advanced code generation, refactoring, and analysis
- Evaluate and validate agent-produced code with confidence

### Prerequisites

- Completed Labs 01–03
- GitHub Copilot access with agent mode enabled
- Familiarity with GitHub Copilot chat and inline suggestions
- Basic understanding of software architecture and design patterns

### Resources

- [Module 3: Implementing Agentic Coding](../demos/03-agentic-coding/)
- [GitHub Copilot Agent Mode Documentation](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent)
- [Anthropic Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
