# Copilot CLI Demos

## Getting Started with Copilot CLI

This 5-minute demo introduces the core capabilities of GitHub Copilot CLI by walking through a practical workflow. You will learn how to authenticate, discover commands, and leverage AI-powered assistance directly in your terminal. By the end, you will understand how Copilot CLI accelerates development tasks and reduces context switching between your editor and terminal. The demo uses a simple Node.js project scenario to showcase real-world usage patterns.

### Prerequisites

Ensure you have Copilot CLI installed. If not, install it using:

```bash
npm install -g @github/copilot
```

### Demo Steps

**Step 1: Authenticate with Copilot CLI**

Start by opening your terminal and running the copilot command to launch the interactive shell.

```bash
copilot
```

When prompted, use the `/login` command to authenticate with your GitHub account.

```
/login
```

Follow the browser prompt to authorize the application. Once authenticated, you will return to the Copilot CLI prompt.

**Step 2: Get Help Explaining a Command**

Ask Copilot to explain a common terminal command you might be unfamiliar with. For example, list all files in the current directory including hidden files.

```bash
ls -la
```

Copilot will explain what the command does, each flag, and when you might use it.

**Step 3: Generate a Command**

Now ask Copilot to suggest a command for a task. For example, find all JavaScript files in your project directory that were modified in the last 7 days.

```bash
find . -name "*.js" -type f -mtime -7
```

Copilot will generate the appropriate command and explain what it does before execution.

**Step 4: Enable Autopilot Mode**

Press `Shift+Tab` to switch to Autopilot mode. This mode encourages Copilot to handle multi-step tasks autonomously. Ask Copilot to initialize a new Node.js project with Express and list the created files.

Autopilot will execute the setup steps automatically and show progress as it works.

**Step 5: Switch Models (Optional)**

Use the `/model` command to view available models and switch between Claude Sonnet 4.5, Claude Sonnet 4, or GPT-5 based on your preference.

```
/model
```

Select a different model to experience how various AI models handle the same requests.

**Step 6: Exit Copilot CLI**

Type `exit` to leave the Copilot CLI interactive shell and return to your standard terminal.

```bash
exit
```

## Business Case: Code Audit and Documentation Coverage Review

This scenario demonstrates how Copilot CLI streamlines repository maintenance for a training codebase with multiple languages and frameworks. A training coordinator needs to audit the repository to find all Python scripts, locate any TODO or FIXME comments indicating incomplete work, and ensure all demo folders have documentation.

**Scenario Setup**

You are in the root of the github-copilot training repository. The task is to assess code quality and documentation coverage across modules without manually exploring directories or writing complex search commands.

**Step 1: Find All Python Files in the Demos**

In Copilot CLI, ask it to locate all Python files in the demos directory:

```bash
find all Python files in the demos directory and show their paths
```

Copilot will generate a find or grep command that lists every .py file, allowing you to understand the Python sample coverage across modules.

**Step 2: Search for Incomplete Work**

Ask Copilot to find all TODO and FIXME comments in the codebase:

```bash
search for all TODO and FIXME comments in the src and demos directories
```

Copilot will generate a grep command that identifies work items and incomplete implementations, helping you prioritize fixes.

**Step 3: Count Documentation Files**

Ask Copilot to count how many readme.md files exist in the demos structure:

```bash
count the total number of readme.md files in the demos directory
```

Copilot will generate a find command that produces a count, giving you a quick metric on documentation coverage.

**Step 4: Generate a Coverage Report**

Ask Copilot to create a summary report showing the count of files by language in the src directory:

```bash
count files by extension in the src directory and create a summary
```

Copilot will generate commands using find and sort to produce a breakdown of code distribution across languages.

**Expected Outcome**

Within minutes, you have audited code quality indicators, identified incomplete work, confirmed documentation coverage, and generated a coverage report. This workflow would normally require opening multiple terminals, writing complex commands, and manually navigating the repository structure. Copilot CLI accomplishes it in natural language from a single prompt.

### Key Takeaways

Copilot CLI eliminates context switching by bringing AI assistance directly to your terminal. It handles command discovery, generation, and explanation in one tool. Autopilot mode is particularly useful for complex multi-step tasks where manual command entry would be time-consuming. The ability to switch models allows you to choose the best AI behavior for your specific task.

### Key Takeaways

Copilot CLI eliminates context switching by bringing AI assistance directly to your terminal. It handles command discovery, generation, and explanation in one tool. Autopilot mode is particularly useful for complex multi-step tasks where manual command entry would be time-consuming. The ability to switch models allows you to choose the best AI behavior for your specific task.

## Links & Resources

- [GitHub Copilot CLI Repository](https://github.com/github/copilot-cli)
- [Official Copilot CLI Documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [GitHub Copilot Overview](https://github.com/features/copilot)
