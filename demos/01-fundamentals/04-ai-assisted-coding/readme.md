# AI-Assisted Coding Essentials

AI-assisted coding uses GitHub Copilot to accelerate your workflow through code suggestions, real-time completions, and on-demand explanations. This topic teaches you to guide Copilot with clear context and intent: prompting techniques, inline suggestions, the chat slash commands that route your intent, and the context variables that ground a request in your workspace.

## Prompting

Structuring a request with clear context and specific instructions guides Copilot to code that matches your requirements and patterns.

- Few-Shot Prompting: provide example snippets showing the desired pattern, then ask for similar code for new scenarios
- Chain-of-Thought: break complex problems into sequential steps and explain your reasoning
- Context-Based Prompting: include schema definitions, configuration files, or existing code
- Instruction-Based Prompting: use clear, structured instructions for consistent, predictable results

## Inline Suggestions

Inline suggestions appear as you type, offering completions tailored to your context. You steer them with meaningful comments and clear patterns. The settings that enable them are in [Getting Started](../01-intro/readme.md#copilot-settings).

## Slash Commands

Slash commands route intent directly to the right capability without a full natural-language prompt. They combine well with a code selection for context-aware assistance.

| Command     | Description                                                   |
| ----------- | ------------------------------------------------------------- |
| `/help`     | Get usage help for Copilot Chat.                              |
| `/explain`  | Explain the selected or referenced code.                      |
| `/fix`      | Propose a fix for problems in the selected code.              |
| `/tests`    | Generate unit tests for selected code.                        |
| `/doc`      | Add documentation comments for the selected code.             |
| `/optimize` | Analyze and propose performance optimizations (Visual Studio). |
| `/clear`    | Start a new session and clear the conversation.               |

## Context Variables

Context variables reference files, code, documentation, and other workspace elements explicitly, which reduces ambiguity and improves accuracy.

| Variable               | Description                                                       |
| ---------------------- | ----------------------------------------------------------------- |
| `#file`                | Reference a specific file in your workspace for focused analysis. |
| `#selection`           | Reference the currently selected code in your editor.             |
| `#codebase`            | Provide codebase-wide context for architecture and patterns.      |
| `#terminalLastCommand` | Reference the last command executed in the terminal.              |
| `#fetch`               | Fetch and include content from URLs or external sources.          |
| `@terminal`            | Include output or errors from your active terminal session.       |
| `@vscode`              | Reference VS Code settings, extensions, or configuration context. |

## Demos

### Inline suggestions in three languages

Open [password-validator.js](./01-inline-suggestions/password-validator.js) and run:

```text
Generate a password validator that will check the following rules: min 6 characters, one uppercase letter or special character.
```

```text
#codebase how can i run #file:password-validator.js
```

Open [food.model.ts](./01-inline-suggestions/food.model.ts), then repeat the same three prompts in [math.java](./01-inline-suggestions/math.java) with Math and Spring in place of food and Angular:

```text
Create a food model with the following properties: name, description, price, and in-stock. Use the constructor to initialize the properties of the class
```

```text
Explain the different uses cases for classes and literal types for typescript projects like angular
```

```text
Convert the food model to a literal type
```

A reference result is in [food.model-result.ts](./01-inline-suggestions/food.model-result.ts).

### Few-shot prompts with samples

In [prompts.js](./02-prompt-with-samples/01-java-script/prompts.js), give Copilot the data shape by example, then build on it:

```text
create an array of users:
name: 'John Doe', age: 30, city: 'New York'
name: 'Jane Fonda', age: 25, city: 'Los Angeles'
name: 'Jim the cat', age: 40, city: 'Chicago'
```

```text
Create a function to filter one of the users by name, call it with 'Jane Fonda' and log it to the console
```

In [greetings.py](./02-prompt-with-samples/02-python/greetings.py), paste input/output examples as comments and let Copilot infer the rule:

```python
# generate a python code that takes the current time as input using the datetime module
# and returns the appropriate greeting message based on the current time.
# Input: 9 AM  Output: "Good Morning!"
# Input: 2 PM  Output: "Good Afternoon!"
# Input: 9 PM  Output: "Good Evening!"
```

Reference results: [prompts-result.js](./02-prompt-with-samples/01-java-script/prompts-result.js), [greetings-result.py](./02-prompt-with-samples/02-python/greetings-result.py).

### SQL from a type definition

With the [MSSQL extension](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql) installed, run these prompts in order:

```text
create a table for microsoft sql server azure to store the data of the following type:

export type Food = {
    name: string;
    price: number;
    description: string;
    category: string;
};
```

```text
create a view to get the food items with price less than 10, a stored procedure to get all food items in a certain category, and a stored procedure to insert a new food item
```

```text
generate some sample data to insert into the table using the stored procedure
```

The [MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode) extension adds an `@MongoDB` participant with `/docs`, `/query`, and `/schema` for the same flow against a MongoDB cluster.

### Fix an error with `#terminalLastCommand`

Run [tasks-api](./tasks-api) using `dotnet run` and notice the error in the terminal. Then ask Copilot Chat:

```text
fix #terminalLastCommand
```

### Scaffold a project from an article with `#fetch`

Build a Microsoft Agent Framework application in Python 3.12. The `#fetch` tool retrieves the official documentation so you scaffold against current docs:

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
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

[← Previous: Shaping the Context Window](../03-context-window/readme.md) | [Back to Fundamentals](../readme.md) | [Next: Agent Mode Basics →](../05-agent-mode-basics/readme.md)
