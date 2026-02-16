# AI Assisted Coding

AI assisted coding uses GitHub Copilot to accelerate your development workflow through intelligent code suggestions, real-time completions, and on-demand explanations. This module teaches you how to guide Copilot effectively by providing context and clear intent, ensuring the AI produces the exact code and solutions you need for your specific tasks.

## Prompting

Effective prompting is the foundation of getting quality results from AI. By structuring your requests with clear context and specific instructions, you can guide Copilot to generate code that matches your exact requirements and coding patterns.

Prompting Techniques:

- Few-Shot Prompting: Provide example code snippets showing the desired pattern, then ask Copilot to generate similar code for new scenarios
- Chain-of-Thought: Break complex problems into sequential steps and explain your reasoning, helping Copilot generate more logical and accurate solutions
- Context-Based Prompting: Include relevant schema definitions, configuration files, or existing code to give Copilot a complete understanding of your project
- Instruction-Based Prompting: Use clear, structured instructions combined with specifications to ensure Copilot produces consistent and predictable results

## AI Assisted Coding - Techniques  

- Inline Suggestions: Leverage real-time code completions while typing by providing meaningful context through comments and clear patterns
- Chat-Based Prompting: Use natural language in Copilot Chat with slash commands and context variables for targeted assistance
- Prompt Engineering: Combine samples, instructions, and project context to improve response quality and consistency
- Database-Driven Prompts: Reference existing patterns and queries to help Copilot understand your architecture

## Enable Inline Suggestions

Inline suggestions appear as you type, offering code completions tailored to your context. They're essential for rapid development workflows.

Add to your VS Code settings:

```json
{
  "editor.inlineSuggest.enabled": true,
  "github.copilot.enable": {
    "*": true,
    "markdown": false,
    "plaintext": false
  }
}
```

## Key Topics Covered in This Section

- [Inline Suggestions](./01-inline-suggestions/): Real-time code completion with comments and patterns
- [Prompt Samples](./02-prompt-with-samples/): Write prompts that reference code examples for better results
- [Database Patterns](./03-database/): Use query and schema patterns to improve AI understanding
