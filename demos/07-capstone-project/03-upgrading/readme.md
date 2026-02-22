# Upgrading & Modernization

This module demonstrates both the Semantic Kernel version (sk-students-ai) and the modernized Microsoft Agent Framework version (maf-students-ai), showing side-by-side how the same RAG-based student roster application evolves with the new framework.

## Migration Implementations

| Implementation                                                      | Description                                                                                    |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **[Semantic Kernel Version (sk-students-ai)](./sk-students-ai/)**   | RAG-based student roster application using Microsoft Semantic Kernel (legacy approach).        |
| **[Agent Framework Version (maf-students-ai)](./maf-students-ai/)** | Modernized same application using Microsoft Agent Framework with new tools-based architecture. |

Microsoft Agent Framework is a unified platform for building agentic AI applications with native support for multi-turn conversations, function calling, and tool orchestration. The framework replaces the earlier Semantic Kernel approach with a streamlined agent-centric model that makes it easier to build AI-powered applications.

The upgrade from Semantic Kernel to Microsoft Agent Framework involves these key migration tasks:

- Replace Microsoft.SemanticKernel with Microsoft.Agents.AI and Microsoft.Agents.AI.OpenAI packages
- Switch from kernel builder pattern to direct agent creation using chatClient.AsAIAgent()
- Rename Plugins folder to Tools and use AIFunctionFactory.Create() for tool registration
- Update authentication from API key configuration to DefaultAzureCredential
- Register agent as singleton service instead of kernel service

## Proposed Prompts

Update project dependencies to Agent Framework. Replace Microsoft.SemanticKernel with Microsoft.Agents.AI, Microsoft.Agents.AI.OpenAI, and Microsoft.Extensions.AI packages. Use Microsoft Learn MCP to find the latest stable versions and ensure compatibility.

```
Use Microsoft Learn MCP to find the latest version information for Microsoft.Agents.AI packages. Identify what versions are required for a Semantic Kernel to Agent Framework migration. What are the key breaking changes I should be aware of?
```

Refactor Program.cs to use Agent Framework. Remove the Kernel.CreateBuilder() pattern and replace it with direct agent creation. Use Microsoft Learn MCP to understand the ChatClientAgent API and how to configure it with instructions and tools.

```
Use Microsoft Learn MCP to find documentation on creating agents with ChatClientAgent. Show me how to migrate from a kernel-based architecture to a direct agent creation pattern. What are the key API differences?
```

Rename the Plugins folder to Tools and update tool registrations. Use Microsoft Learn MCP to understand AIFunctionFactory and how tools are registered in Agent Framework compared to Semantic Kernel plugins.

```
Use Microsoft Learn MCP to research how tools work in Microsoft Agent Framework. What is the difference between Semantic Kernel plugins and Agent Framework tools? How do I use AIFunctionFactory.Create() to register tools?
```

Update authentication to use DefaultAzureCredential. Remove hardcoded API key configuration. Use Microsoft Learn MCP to understand why DefaultAzureCredential is the recommended approach for cloud-native applications.

```
Use Microsoft Learn MCP to find best practices for Azure authentication in Agent Framework applications. Why is DefaultAzureCredential preferred over API key configuration? What security benefits does it provide?
```

Register the agent as a singleton service. Update dependency injection configuration to use builder.Services.AddSingleton<AIAgent>(). Use Microsoft Learn MCP to understand service lifetime management in Agent Framework applications.

```
Use Microsoft Learn MCP to find documentation on dependency injection patterns for Microsoft Agent Framework. How should agents be registered in the dependency injection container? What are the implications of different service lifetimes?
```

- [Microsoft Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/overview/)

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/overview/?pivots=programming-language-csharp)
