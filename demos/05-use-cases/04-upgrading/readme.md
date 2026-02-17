# Upgrading & Modernization

This module demonstrates both the Semantic Kernel version (sk-students-ai) and the modernized Microsoft Agent Framework version (maf-students-ai), showing side-by-side how the same RAG-based student roster application evolves with the new framework.

sk-students-ai is an ai solution demonstrating RAG (Retrieval Augmented Generation) using Semantic Kernel. In September 2025 Semantic Kernel has been replaced by Microsoft Agent Framework.

Microsoft Agent Framework is a unified platform for building agentic AI applications with native support for multi-turn conversations, function calling, and tool orchestration. The framework replaces the earlier Semantic Kernel approach with a streamlined agent-centric model that makes it easier to build AI-powered applications.

The upgrade from Semantic Kernel to Microsoft Agent Framework involves these key migration tasks:

- Replace Microsoft.SemanticKernel with Microsoft.Agents.AI and Microsoft.Agents.AI.OpenAI packages
- Switch from kernel builder pattern to direct agent creation using chatClient.AsAIAgent()
- Rename Plugins folder to Tools and use AIFunctionFactory.Create() for tool registration
- Update authentication from API key configuration to DefaultAzureCredential
- Register agent as singleton service instead of kernel service
