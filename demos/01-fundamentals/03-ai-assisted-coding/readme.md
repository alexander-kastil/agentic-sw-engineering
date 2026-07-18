# AI-Assisted Coding Essentials

AI-assisted coding uses GitHub Copilot to accelerate your workflow through intelligent code suggestions, real-time completions, and on-demand explanations. This topic teaches you to guide Copilot with clear context and intent so it produces the exact code you need. It folds three closely related skills into one place: prompting techniques, inline suggestions, the chat slash commands that route your intent, and the context variables that ground a request in your workspace.

## Prompting

Effective prompting is the foundation of quality results. By structuring requests with clear context and specific instructions, you guide Copilot to generate code that matches your requirements and patterns.

Prompting techniques:

- Few-Shot Prompting: provide example snippets showing the desired pattern, then ask Copilot to generate similar code for new scenarios
- Chain-of-Thought: break complex problems into sequential steps and explain your reasoning for more logical solutions
- Context-Based Prompting: include schema definitions, configuration files, or existing code to give Copilot a complete picture
- Instruction-Based Prompting: use clear, structured instructions with specifications for consistent, predictable results

## Inline Suggestions

Inline suggestions appear as you type, offering completions tailored to your context. They are essential for rapid development, and you steer them by providing meaningful context through comments and clear patterns.

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

## Slash Commands

Slash commands are quick shortcuts for common tasks in Copilot Chat, letting you route intent directly to the right capability without typing a full natural-language prompt. They work in VS Code, GitHub.com, and JetBrains IDEs, and combine well with a code selection for context-aware assistance.

Ensure Copilot Chat is enabled in VS Code:

```json
{
  "chat.agent.enabled": true,
  "github.copilot.chat.codesearch.enabled": true
}
```

| Command     | Description                                                       |
| ----------- | ----------------------------------------------------------------- |
| `/help`     | Get usage help for Copilot Chat.                                  |
| `/doc`      | Add documentation comments for the selected code (Visual Studio). |
| `/explain`  | Explain the selected or referenced code.                          |
| `/fix`      | Propose a fix for problems in the selected code.                  |
| `/tests`    | Generate unit tests for selected code.                            |
| `/optimize` | Analyze and propose performance optimizations.                    |
| `/generate` | Generate code based on your request.                              |
| `/clear`    | Start a new session and clear the conversation.                   |

## Context Variables

Context variables let you explicitly reference files, code, documentation, and other workspace elements in a chat request. Using symbols like `#` and `@`, you give Copilot precise context, which reduces ambiguity and improves accuracy. Use them to ground a question in specific code, docs, or terminal output.

Enable context features in VS Code:

```json
{
  "chat.codebase.enabled": true,
  "github.copilot.chat.codesearch.enabled": true,
  "chat.detectParticipant.enabled": true
}
```

| Variable               | Description                                                                |
| ---------------------- | -------------------------------------------------------------------------- |
| `#file`                | Reference a specific file in your workspace for focused analysis.          |
| `#selection`           | Reference the currently selected code in your editor.                      |
| `#codebase`            | Provide codebase-wide context for architecture and patterns.              |
| `#terminalLastCommand` | Reference the last command executed in the terminal.                       |
| `#fetch`               | Fetch and include content from URLs or external sources.                   |
| `@terminal`            | Include output or errors from your active terminal session.                |
| `@vscode`              | Reference VS Code settings, extensions, or configuration context.          |

## Topics

| Topic                                                 | Description                                                                                  |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **[Inline Suggestions](./01-inline-suggestions/)**    | Master real-time code completion by leveraging inline suggestions with meaningful context.   |
| **[Prompts with Samples](./02-prompt-with-samples/)** | Learn how providing code samples helps Copilot understand intent and generate precise code.  |
| **[Using Copilot for Databases](./03-database/)**     | Leverage Copilot to generate database code, schemas, and queries across different platforms. |

## Demos

### Using `#terminalLastCommand` to Fix Errors

Run [tasks-api](./tasks-api) using `dotnet run` and notice the error in the terminal. Then ask Copilot Chat to fix it using `#terminalLastCommand` to reference the error message.

```text
fix #terminalLastCommand
```

### Scaffold a project from an article using `#fetch`

Build a working Microsoft Agent Framework application in Python 3.12 using slash commands and the `#fetch` tool. The `#fetch` tool retrieves official documentation from URLs so you can reference current docs while scaffolding code.

```text
In this topic folder create a folder maf-starter and use it

#fetch https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start?pivots=programming-language-python and create a hello world python 3.12 app with the prompt of "tell me about the microsoft agent framework"

Implement the following steps:

Add required packages to requirements.txt and create and activate a python .venv. No need to upgrade pip.
Add a valid .gitignore for python projects.
Create an .env with PROJECT_ENDPOINT, MODEL_DEPLOYMENT and USE MY VARIABLE NAMES
Implement the sample and run it until all errors are fixed
In the folder create a readme.md with very short instructions for beginners to run the app. Instruct them on where to get the required values for the .env from Microsoft Foundry
```

A solution is available in the [maf-starter-solution](./maf-starter-solution) folder.

## Links & Resources

- [GitHub Copilot Slash Commands](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide#using-slash-commands)
- [GitHub Copilot Context Variables](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide#using-context-variables)
