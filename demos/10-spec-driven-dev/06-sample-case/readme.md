# Exercise: Implement a product feature using GitHub Spec Kit

[Exercise: Implement a product feature using GitHub Spec Kit](https://github.com/alexander-kastil/spec-drive-development-lab)

> Note: This is an advanced lab designed for senior software engineers and architects. This exercise is designed to be completed after going through the Spec-Driven Development training modules. It provides a practical application of the concepts and tools covered in the training, allowing you to implement a product feature using the GitHub Spec Kit workflow. Expect to spend approximately 120 minutes to complete this lab.

This exercise requires a dedicated repository because the GitHub Spec Kit workflow relies on artifacts and configuration files that must reside in specific root folder locations. While we could integrate these files into the required root folders of this training repository, we maintain a separate dedicated repository to preserve a clear separation of concerns. This approach keeps the training materials focused while allowing the spec-driven development lab to operate independently with its own project structure and configuration.

The repository includes essential artifacts that power the spec-driven development workflow:

| Artifact              | Description                                                                                                                         |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `.github/agents/`     | Specialized agents that execute different phases of the spec-driven workflow (analyze, clarify, plan, implement, specify, and more) |
| `.github/prompts/`    | System prompts that guide agent behavior for each workflow phase and capability                                                     |
| `.specify/memory/`    | Persistent storage for specification context and decision history maintained throughout the workflow                                |
| `.specify/scripts/`   | Automation scripts (bash and PowerShell) for executing workflow tasks and setup operations                                          |
| `.specify/templates/` | Pre-defined templates for creating constitutions, specifications, plans, checklists, and other workflow artifacts                   |
| `settings.json`       | VS Code configuration enabling Spec Kit tools in the editor (constitution, specify, plan, tasks, implement)                         |
