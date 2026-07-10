# Implementing Agentic Coding

## Coding Agent Fundamentals

Coding agents extend GitHub Copilot with specialized execution capabilities, enabling autonomous multi-step workflows for development tasks. Unlike chat-based interactions, coding agents can spawn terminals, modify files, run tests, and coordinate multiple tools to accomplish complex objectives. Understanding the different agent types and their execution models is essential for choosing the right approach for your development workflow.

The primary distinction between agent types centers on where and how they execute: locally within your current VS Code environment, on remote or cloud infrastructure for resource-intensive tasks, or delegated across multiple specialized agents. Each model offers different tradeoffs between resource requirements, isolation, throughput, and integration with your development tools.

## Topics

| Topic | Focus | Best For |
|-------|-------|----------|
| [Using Local Agents in Agent Mode](./01-local/) | Current VS Code session | Single focused tasks with immediate feedback |
| [Delegating Tasks to Cloud Agents](./02-cloud/) | Remote Azure environment | Large-scale tasks exceeding local resources |
| [Multi-Agent Orchestration](./03-orchestration/) | Delegated specialized agents | Multi-step workflows with parallel execution |
| [Using Anthropic Claude Code Agents](./04-claude-code/) | Desktop app with VS Code integration | Large-scale refactoring, review, and security audits |
| [Agentic Browser Automation](./05-browser-tools/) | Built-in browser tools | Agents verifying their own web changes |
| [Upgrading & Modernization](./06-upgrading/) | Framework migration | Modernizing existing code, such as Semantic Kernel to the Agent Framework |
