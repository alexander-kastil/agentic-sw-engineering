# Copilot Instructions

Copilot uses two layers of instructions to shape AI behavior: **general repository rules** that apply everywhere, and **stack-specific guidelines** that activate based on the technologies you're working with. Understanding how these are loaded and managed is essential for optimizing your LLM context window and ensuring consistent code quality across different domains.

## Enable Instructions in VS Code

Configure VS Code to automatically load instructions from your repository:

```json
{
  "chat.instructionsFilesLocations": {
    ".github/instructions": true,
    ".github/copilot-instructions.md": true,
    ".copilot-instructions.md": true
  }
}
```

## General Repository Instructions

**File**: [.github/copilot-instructions.md](/.github/copilot-instructions.md)

General instructions establish repository-wide policies and conventions that apply to all development work, regardless of technology stack. They cover philosophy, architecture decisions, naming conventions, security practices, and project structure.

**Key Rules**:

- Write clean code with no unnecessary comments or over-engineering
- Consult Microsoft Learn MCP when implementing, updating, or fixing code
- Never hardcode deployment values—always read from [.github/deploy.json](/.github/deploy.json)
- Use Workload Identity Federation (WIF) for all Azure DevOps authentication
- Follow strict naming conventions for pipelines, resources, and Docker artifacts

**Example**: When creating any Azure DevOps pipeline, the general instructions require consulting `deploy.json` for environment metadata and using WIF for service connections instead of storing secrets. This ensures security practices are consistent across all pipelines.

**Context Window Impact**: General instructions are broad but focused—typically 1-2 KB of guidance. They establish framework rules that narrow the scope of subsequent stack-specific instructions, reducing overall context consumption by preventing redundant or conflicting guidance.

## Stack-Specific Instructions

**Directory**: [.github/instructions/](/.github/instructions/)

Stack-specific instructions provide detailed, technology-focused conventions for the languages and frameworks used in the repository. They're self-contained guides for formatting, tooling, and best practices within their domain.

**Stack Specific Instructions**:

| Instruction                                                          | Focus                                                                                                                                                                   |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Accessibility](/.github/instructions/a11y.instructions.md)          | WCAG 2.2 Level AA conformance, keyboard navigation, focus management, contrast requirements, reflow at 320px, color accessibility, and forced colors mode support.      |
| [Agent Skills](/.github/instructions/agent-skills.instructions.md)   | Guidelines for creating portable Agent Skills with multiple entrypoints, bundled resources, semantic versioning, and integration patterns for GitHub Copilot.           |
| [Agents](/.github/instructions/agents.instructions.md)               | Custom agent file creation for specialized development tasks, expertise definitions, runtime configuration, and Copilot integration best practices.                     |
| [Angular](/.github/instructions/angular.instructions.md)             | Framework conventions for Angular 18+ with standalone components, reactive patterns, Angular CLI scaffolding, and deployment targets (Static Web Apps, Container Apps). |
| [Azure CLI](/.github/instructions/azure-cli.instructions.md)         | Bash/PowerShell scripting for resource provisioning, variable naming (camelCase), resource composition, command substitution, and automation workflows.                 |
| [Documentation](/.github/instructions/documentation.instructions.md) | Markdown structure, readability standards, code block formatting, heading hierarchy, and technical guide organization.                                                  |
| [.NET](/.github/instructions/dotnet.instructions.md)                 | C# naming conventions (PascalCase/camelCase), primary constructors, async/await patterns, dotnet CLI usage, and instance lifecycle management.                          |

**Example**: When you're working in an Angular project, the Angular instructions are automatically loaded into context. They specify that components should use standalone APIs, Angular CLI for scaffolding, feature-based folder organization, and Static Web Apps or Container Apps for deployment. If you then write a `.NET` service to support the Angular app, the .NET instructions activate, adding guidance on PascalCase conventions and primary constructors.

**Context Window Impact**: Stack-specific instructions are compact but targeted—typically 500 bytes to 2 KB each. They **only load when relevant** (e.g., opening an Angular file or a .NET project), avoiding unnecessary context bloat. This selective activation means your context window stays efficient because guidance for irrelevant stacks isn't included.

## Context Loading & LLM Window Management

Copilot's instruction loading follows a **layered, on-demand approach**:

### Loading Sequence

1. **General Instructions Load First** (~1-2 KB)
   - Repository philosophy, security policies, naming conventions
   - Applies to all work regardless of technology
   - Establishes guardrails and best practices framework

2. **Stack-Specific Instructions Load Conditionally** (~500 bytes - 2 KB per technology)
   - Detected from file types, project structure, or explicit user context
   - Only included if the current workspace or file matches the stack
   - Allows precise guidance without cross-technology pollution

3. **Inline Prompt Context** (variable)
   - Additional context from the user's current file or selection
   - Merged with the general + stack-specific layers
   - Ensures task-specific guidance takes precedence

### Example Context Window Flow

When you're working on an Angular component in `src/angular/food-shop/app.component.ts`:

```
┌─ General Instructions (~1 KB)
│  ├ Repository rules, security, naming patterns
│  └ "Write clean code, consult Microsoft Learn MCP"
│
├─ Stack-Specific Instructions (~1.5 KB)
│  ├ Angular 18+ standards, CLI usage, routing
│  └ "Use standalone components, feature-based folders"
│
└─ Current File Context (~2-5 KB typical)
   ├ app.component.ts content
   ├ Related imports and dependencies
   └ User's specific edit or question context
```

**Total Context Used**: ~4.5-7.5 KB for this scenario—a small fraction of Claude's 200K context window.

If you then open a `.NET` service file, the loading automatically adjusts:

```
┌─ General Instructions (~1 KB)
│  └ Same as above
│
├─ Stack-Specific Instructions (~1 KB)
│  ├ .NET conventions, PascalCase, primary constructors
│  └ Replaces Angular-specific guidance
│
└─ Current File Context (~3-6 KB)
   ├ Service.cs content
   └ Related code
```

**Context Efficiency**: By swapping Angular guidance for .NET guidance rather than accumulating both, Copilot stays focused and responsive.

## Best Practices for Using Instructions

- **Read Them First**: Familiarize yourself with general rules and the stack you're working in—they answer most "how do I...?" questions
- **Respect the Separation**: General instructions enforce repository-wide consistency; stack-specific ones ensure quality within their domain
- **Consult for Changes**: When modifying or extending instructions, ensure alignment between general and stack-specific layers
- **Use as Reference**: Stack-specific instructions often include examples (Angular CLI commands, .NET naming patterns, Azure CLI resource composition)—reference these before asking Copilot

## Links & Resources

- [Use custom instructions in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
