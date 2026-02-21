# Business Case: Code Audit and Documentation Coverage Review

This scenario demonstrates how Copilot CLI streamlines repository maintenance for a training codebase with multiple languages and frameworks. A training coordinator needs to audit the repository to find all Python scripts, locate any TODO or FIXME comments indicating incomplete work, and ensure all demo folders have documentation.

**Scenario Setup**

You are in the root of the github-copilot training repository. The task is to assess code quality and documentation coverage across modules without manually exploring directories or writing complex search commands.

### Find All Python Files in the Demos

In Copilot CLI, ask it to locate all Python files in the demos directory:

```bash
find all Python files in the demos directory and show their paths
```

Copilot will generate a find or grep command that lists every .py file, allowing you to understand the Python sample coverage across modules.

### Search for Incomplete Work

Ask Copilot to find all TODO and FIXME comments in the codebase:

```bash
search for all TODO and FIXME comments in the src and demos directories
```

Copilot will generate a grep command that identifies work items and incomplete implementations, helping you prioritize fixes.

### Count Documentation Files

Ask Copilot to count how many readme.md files exist in the demos structure:

```bash
count the total number of readme.md files in the demos directory
```

Copilot will generate a find command that produces a count, giving you a quick metric on documentation coverage.

### Generate a Coverage Report

Ask Copilot to create a summary report showing the count of files by language in the src directory:

```bash
count files by extension in the src directory and create a summary
```

Copilot will generate commands using find and sort to produce a breakdown of code distribution across languages.

**Expected Outcome**

Within minutes, you have audited code quality indicators, identified incomplete work, confirmed documentation coverage, and generated a coverage report. This workflow would normally require opening multiple terminals, writing complex commands, and manually navigating the repository structure. Copilot CLI accomplishes it in natural language from a single prompt.

### Key Takeaways

Copilot CLI eliminates context switching by bringing AI assistance directly to your terminal. It handles command discovery, generation, and explanation in one tool. Autopilot mode is particularly useful for complex multi-step tasks where manual command entry would be time-consuming. The ability to switch models allows you to choose the best AI behavior for your specific task.
