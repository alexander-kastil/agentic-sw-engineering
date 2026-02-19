# Spec-driven workflow

GitHub Spec Kit is an open-source toolkit that enables spec-driven development (SDD) by integrating specifications with AI coding assistants. It transforms how you work with GitHub Copilot, Claude Code, and other AI partners by providing a systematic approach to turning specifications into working implementations. The toolkit uses plain markdown files to document specifications, plans, and tasks alongside your code, creating persistent artifacts that drive development forward.

The toolkit includes a specify CLI for project initialization, markdown artifact files (constitution.md, spec.md, plan.md, tasks.md) that drive development, and slash commands (/speckit.specify, /speckit.plan, /speckit.tasks, /speckit.implement) that invoke GitHub Spec Kit workflows. GitHub Spec Kit also uses environment variables to track which feature you're currently developing. The SPECIFY_FEATURE variable indicates the active feature directory, and in Git-based workflows, GitHub Spec Kit infers the feature from your branch name—if you're on branch feature/document-upload, GitHub Spec Kit automatically works with the features/document-upload/ directory.

## Version control integration

All GitHub Spec Kit artifacts are plain markdown files stored in your Git repository, providing change tracking for every modification to specifications, plans, or tasks. This approach enables branch-based development where feature branches contain both specification artifacts and implementation code, keeping requirements and implementation synchronized. When you submit a pull request for a feature, include spec.md, plan.md, and tasks.md alongside code changes so reviewers see both what you're building and how you built it. This complete picture enables thorough review where questions about implementation details can be traced back to specification decisions.

## Project structure

GitHub Spec Kit organizes artifacts using a consistent directory structure that separates specification artifacts from implementation code:

```
my-project/
├── .github/
│   ├── agents/
│   └── prompts/
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   ├── scripts/
│   └── templates/
├── SourceCode/
│   └── ...
└── specs/
    ├── 001-document-upload-feature/
    │   ├── plan.md
    │   ├── spec.md
    │   └── tasks.md
    └── 002-authentication-feature/
        ├── plan.md
        ├── spec.md
        └── tasks.md
```

Features are numbered sequentially to track development order. For teams working on multiple features concurrently, each feature has its own directory containing its complete specification, plan, and tasks, which prevents confusion and enables parallel work without conflicts.

## Core commands and workflows

| Command | Purpose | Use case |
|---------|---------|----------|
| /speckit.constitution | Establish project principles and constraints | Initialize project governance and architectural standards |
| /speckit.specify | Generate detailed specifications | Transform feature descriptions into complete spec.md with user stories and acceptance criteria |
| /speckit.clarify | Perform gap analysis | Identify ambiguities and missing details in specifications |
| /speckit.analyze | Verify cross-artifact consistency | Ensure plan implements all spec requirements and tasks cover all plan elements |
| /speckit.checklist | Generate quality validation checklists | Verify requirement completeness, clarity, and consistency before sharing with stakeholders |
| /speckit.plan | Create implementation plans | Transform specifications into architectural and design approaches |
| /speckit.tasks | Generate implementation tasks | Break down plan elements into actionable development steps |
| /speckit.implement | Implement incrementally | Generate code following specification and task requirements |

The typical workflow progresses through specification, gap clarification, plan creation, consistency verification, task breakdown, and incremental implementation. However, at any point if requirements change, you can return to earlier phases—update the specification, regenerate downstream artifacts, and the system ensures changes propagate systematically rather than being patched into code without documentation.

## Key Topics covered in this module

- GitHub Spec Kit foundations and core concepts
- Specification-first development approach
- Integration with GitHub Copilot and AI coding assistants
- Version control and Git workflow integration
- Project structure conventions for multi-feature development
- Advanced workflows including gap analysis, consistency verification, and quality validation
