# Spec Driven Development

## Introduction to Spec Driven Development

Spec-driven development reverses the traditional code-first approach by starting with a specification that acts as an executable contract between your intent and the implementation. Instead of writing vague prompts and hoping for the right output, you provide a clear specification that becomes the source of truth for what gets built, tested, and validated. This approach eliminates guesswork and ensures that coding agents like GitHub Copilot understand exactly what you want before they start writing code.

GitHub Spec Kit provides a structured four-phase process that turns specifications into working code. You begin by specifying your requirements from the user perspective, then create a technical plan with your desired stack and constraints, break it down into concrete tasks, and finally implement them with focused code reviews. Each phase has explicit checkpoints where you verify the artifacts before moving forward, keeping the coding agent aligned with your actual needs throughout the project.

The four-phase SDD workflow:

- Specify: Define what the software should do and why—user stories, acceptance criteria, requirements, and edge cases.
- Plan: Decide how to build it—architecture, technology stack, and implementation approach.
- Tasks: Break down the plan into discrete, actionable development tasks organized by phase.
- Implement: Write code guided by the spec, plan, and task list, verifying each task against the specification.

## Getting Started with GitHub Spec Kit

To try spec-driven development, install the Spec Kit CLI tool:

```
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

Once initialized, use these commands to guide your coding agent:

- `/specify` - Describe what you're building and why (user experience focused)
- `/plan` - Provide technical direction and constraints
- `/tasks` - Break down the specification into actionable work items
- `/implement` - Let the coding agent tackle tasks with clear, reviewable changes

A minimal 10-minute implementation flow: create a simple project spec for a specific feature, generate a plan for a small service, create focused tasks, and let Copilot implement one or two tasks to see how the process works in practice.

## Key Topics Covered in This Module

- [GitHub Spec Kit Repository](https://github.com/github/spec-kit)
- [Spec-Driven Development with AI Guide](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
