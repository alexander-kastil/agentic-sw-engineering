# Azure Blob Storage Refactoring

Demonstrates code conversion across language stacks using GitHub Copilot by porting a C# Azure Blob Storage console application to Java and Python. Each implementation shows how to interact with Azure Blob Storage using language-specific SDKs to list blobs, manage metadata, and handle file uploads.

## Subfolders

The [blob-console](blob-console/) folder contains the original C# implementation using .NET and the Azure.Storage.Blobs SDK. It demonstrates reading configuration from appsettings.json, managing blob metadata, listing containers, and uploading files with async/await patterns.

The [blob-console-spring](blob-console-spring/) folder shows the Java equivalent using Spring Framework and Gradle for build management. This version translates the C# async operations and configuration handling into idiomatic Java patterns with the same blob storage operations.

The [blob-py](blob-py/) folder provides the Python implementation using the azure-storage-blob library with DefaultAzureCredential for authentication. This minimal example demonstrates how Python simplifies blob enumeration and leverages Azure identity libraries for secure credential handling.

## Converting Code Stacks with GitHub Copilot

GitHub Copilot excels at cross-language refactoring by understanding patterns and translating them to target language idioms. Start by opening the source file (blob-console/Program.cs) and a new empty file in your target language, then use prompts like "Convert this C# blob storage code to Java" or "Translate this C# code to Python". Copilot will analyze the logic, dependency management, and SDK differences to generate functionally equivalent code adapted to the target language's conventions and libraries.

For successful conversions, provide context about which SDK versions or frameworks to use (Spring for Java, azure-storage-blob for Python). Reference the original file in your prompt and let Copilot determine equivalent operations in the target language, such as mapping C# async/await to Java CompletableFuture or Python asyncio patterns. You can then refine specific sections by asking for adjustments to naming conventions, error handling, or configuration management.
