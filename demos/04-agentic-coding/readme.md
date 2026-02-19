# Agent Types

## Coding Agent Fundamentals

Coding agents extend GitHub Copilot with specialized execution capabilities, enabling autonomous multi-step workflows for development tasks. Unlike chat-based interactions, coding agents can spawn terminals, modify files, run tests, and coordinate multiple tools to accomplish complex objectives. Understanding the different agent types and their execution models is essential for choosing the right approach for your development workflow.

The primary distinction between agent types centers on where and how they execute: locally within your current VS Code environment, in the background as isolated parallel processes, or in cloud environments for resource-intensive tasks. Each model offers different tradeoffs between resource requirements, isolation, throughput, and integration with your development tools.

## Agent Type Comparison

| Agent Type                                  | Execution Context                    | Best For                                                   | Parallelism                    | Resource Isolation           |
| ------------------------------------------- | ------------------------------------ | ---------------------------------------------------------- | ------------------------------ | ---------------------------- |
| **[Local Agent](./01-local/)**              | Current VS Code session              | Single focused tasks with immediate feedback               | Single sequential task         | Minimal (shared workspace)   |
| **[Cloud Agent](./02-cloud/)**              | Remote Azure environment             | Large-scale tasks exceeding local resources                | High (scalable infrastructure) | Excellent (remote isolation) |
| **[Background Agent](./03-background/)**    | Isolated process on your machine     | Parallel tasks without blocking your editor                | Multiple concurrent tasks      | Good (separate process)      |
| **[Sub-agents](./04-sub-agents/)**          | Delegated to specialized agents      | Orchestrating multi-step workflows with parallel execution | Parallel across sub-agents     | Depends on delegation target |
| **[Claude Code Agents](./05-claude-code/)** | Desktop app with VS Code integration | Large-scale refactoring, code review, security audits      | Task-dependent                 | Configurable permissions     |
