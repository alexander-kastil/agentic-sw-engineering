# Agentic Software Engineering Repository - Developer & Agent Guide

This repository contains training materials, demos, and infrastructure for Microsoft AZ-400 (DevOps Solutions) certification and agentic software engineering patterns. It's a **teaching repository** - not a production application - designed to demonstrate DevOps concepts and AI-driven development through hands-on examples.

## Repository Purpose & Structure

**Primary Goal**: Provide instructor-led demos and labs for Azure DevOps, GitHub Actions, IaC, and cloud-native development patterns.

### Key Directories

**`.azdo/`** - Azure DevOps (ADO) pipeline definitions containing 50+ pipelines demonstrating CI/CD patterns, both classic and YAML formats. Includes reusable templates for build, release, and deployment strategies aligned with AZ-400 curriculum. Also stores service connection setup scripts using Workload Identity Federation.

**`demos/`** - Instructor-led demonstrations organized into 7 progressive modules covering the entire AZ-400 curriculum. Each module combines theory with hands-on examples, from fundamental DevOps concepts through advanced agentic development, IaC patterns, and specification-driven workflows.

**`src/`** - Sample applications spanning multiple technology stacks including Angular (standalone components), React, .NET (APIs and Azure Functions), Python, Java, and SharePoint Framework. These apps serve as deployment targets for CI/CD pipelines and showcase real-world patterns for different platform capabilities.

**`infra/`** - Infrastructure as Code templates using Bicep (preferred for new projects), Terraform, and Azure CLI scripts. Demonstrates declarative infrastructure management, modularization patterns, and cross-cloud deployment strategies.

**`labs/`** - Hands-on lab exercises with guided walkthroughs. Provides structured practice environments for learners to apply concepts from demo modules in isolation.

Always start applications from their respective project folders and not the repository root.

## General RULES

- Write clean code. No comments. Do not over engineer!!!
- Do not write docs if you are not asked to. If you are asked to write docs, be concise, short and to the point. Avoid more than 2 nesting levels.
- When asked to implement, update or fix code always consult the Microsoft Learn MCP

## Deployment Metadata

`.github/deploy.json` contains essential metadata for pipeline imports and configurations for deployment environments.

**Never hardcode these values** - always read from `deploy.json` when creating/importing pipelines.

## Demo Modules Overview

The `demos/` folder is structured by learning progression:

**Module 01: Fundamentals** (Copilot Essentials) - Introduces core Copilot features including inline suggestions, slash commands, context variables, and prompt engineering. Includes basic AI-assisted coding patterns and code review workflows.

**Module 02: Copilot Tools** (Advanced Features) - Covers instructions, prompts, MCP servers, agents, skills, plugins, memory, and context window optimization. Foundation for understanding how to extend and customize Copilot capabilities.

**Module 03: Agentic Coding** (Agent Patterns) - Explores local agents, cloud agents, background tasks, orchestration patterns, and Claude Code integration. Demonstrates autonomous agent workflows and multi-step task automation.

**Module 04: Advanced Topics** (Expert Patterns) - Deep dives into CLI patterns, agentic workflows, SDK integration, MCP app development, and business case analysis. For experienced developers building sophisticated AI solutions.

**Module 05: Agentic DevOps** (Infrastructure & CI/CD) - Applies agentic patterns to DevOps scenarios including Azure CLI automation, Infrastructure as Code, and pipeline intelligence. Bridges DevOps practices with agent-driven workflows.

**Module 06: Spec-Driven Development** (Quality & Process) - Covers specification-driven workflows, requirement analysis, constitution mapping, and systematic task decomposition. Teaches structured approaches to complex feature development.

**Module 07: Capstone Project** (Synthesis & Application) - Integrates all concepts through planning, implementation, upgrading, testing, and documentation of a complete project. Demonstrates end-to-end patterns from design through deployment.

## Pipeline Architecture & Patterns

Pipelines use reusable templates from `.azdo/templates/` with naming convention: `<module>-<demo>-<description>` aligned with the demos folder structure. All new pipelines use Workload Identity Federation for secure authentication with Azure resources.
