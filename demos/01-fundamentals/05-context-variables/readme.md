# Context Variables

Context variables enable you to explicitly reference files, code, documentation, and other workspace elements in your GitHub Copilot Chat conversations. By using special symbols like `#` and `@`, you provide Copilot with precise context about what you want assistance with, reducing ambiguity and improving response accuracy. Context variables integrate seamlessly with your codebase, allowing Copilot to understand relationships between files, track dependencies, and generate more contextually relevant solutions. Use context variables to ground your questions in specific code, documentation, or terminal output for targeted, intelligent assistance.

## Enable Context Features in Chat

Enable context-aware capabilities in VS Code:

```json
{
  "chat.codebase.enabled": true,
  "github.copilot.chat.codesearch.enabled": true,
  "chat.detectParticipant.enabled": true
}
```

## Available Context Variables

| Variable               | Description                                                                |
| ---------------------- | -------------------------------------------------------------------------- |
| `#file`                | Reference a specific file in your workspace for focused analysis.          |
| `#selection`           | Reference the currently selected code in your editor.                      |
| `#codebase`            | Provide codebase-wide context for understanding architecture and patterns. |
| `#agent`               | Access Copilot Agents and specialized AI capabilities for advanced tasks.  |
| `#terminalLastCommand` | Reference the last command executed in the terminal.                       |
| `#fetch`               | Fetch and include content from URLs or external sources.                   |
| `#repository`          | Include repository metadata, commits, or branch information.               |
| `#docs`                | Reference documentation files in your workspace.                           |
| `@terminal`            | Include terminal output or errors from your active terminal session.       |
| `@vscode`              | Reference VS Code settings, extensions, or configuration context.          |
| `@recent`              | Access recent files or conversations for continuity.                       |

## Demos

### Using `#terminalLastCommand` to Fix Errors

Run [tasks-api](tasks-api) using `dotnet run` and notice the error in the terminal. Then ask Copilot Chat to help you fix the error using the `#terminalLastCommand` variable to reference the error message.

```
fix #terminalLastCommand
```

### Scaffold a project based on an article using `#fetch`

Build a working Microsoft Agent Framework application in Python 3.12 using slash commands and the #fetch tool. The #fetch tool retrieves official documentation from URLs so you can reference current docs while scaffolding code.

```
In [demos/01-fundamentals/04-slash-commands](demos/01-fundamentals/04-slash-commands) create a folder maf-starter and use it

#fetch https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start?pivots=programming-language-python and create a hello world python 3.12 app with the prompt of "tell me about the microsoft agent framework"

Implement the following steps:

Add required packages to requirements.txt and create and activate a python .venv. No need to upgrade pip.
Add a valid .gitignore for python projects.
Create an .env with PROJECT_ENDPOINT, MODEL_DEPLOYMENT and USE MY VARIABLE NAMES
Implement the sample and run it until all errors are fixed
In the folder create a readme.md with very short instructions for beginners to run the app. Instruct them on where to get the required values for the .env from Microsoft Foundry
```

A solution is available in the [maf-starter-solution](maf-starter-solution) folder.

## Key Topics Covered in This Section

- [GitHub Copilot Context Variables](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide#using-context-variables)
