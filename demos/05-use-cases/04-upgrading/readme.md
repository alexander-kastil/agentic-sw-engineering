# Upgrading & Modernization

sk-students-ai is an ai solution demonstrating RAG (Retrieval Augmented Generation) using Semantic Kernel. In September 2025 Semantic Kernel has been replaced by Microsoft Agent Framework.

Microsoft Agent Framework is a unified platform for building agentic AI applications with native support for multi-turn conversations, function calling, and tool orchestration. It provides a simpler, more direct API for creating agents that can interact with language models while leveraging external tools and plugins to accomplish complex tasks. The framework replaces the earlier Semantic Kernel approach with a streamlined agent-centric model that makes it easier to build AI-powered applications.

The upgrade from Semantic Kernel to Microsoft Agent Framework involves replacing the kernel builder pattern with direct agent creation using AIFunctionFactory for tool registration. Key steps include switching dependencies from Microsoft.SemanticKernel to Microsoft.Agents.AI, converting plugin registration from kernel plugins to agent tools, and updating the agent initialization to use the new CreateAIAgent method. Authentication also transitions from API key-based approaches to Azure credential chains like DefaultAzureCredential for better security in cloud deployments.

This module demonstrates both the Semantic Kernel version (sk-students-ai) and the modernized Microsoft Agent Framework version (maf-students-ai), showing side-by-side how the same RAG-based student roster application evolves with the new framework.
