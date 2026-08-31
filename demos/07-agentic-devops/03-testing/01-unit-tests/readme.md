# Unit Testing

## Angular MCP

Add the Angular CLI MCP to `.vscode/mcp.json` to enable code generation, testing, and analysis capabilities within your agent. This allows automated component creation, test generation, and schema validation.

```json
"angular-cli": {
  "command": "npx",
  "args": [
    "-y",
    "@angular/cli",
    "mcp"
  ]
}
```

## Create an Angular Agent

Learn how to build custom agents for Angular development and testing (see https://angular.love/agent-skills-in-claude-a-practical-guide-for-angular-developers). Create a `.agent.md` file with Angular specialization, enable development tools, and configure MCPs for Angular CLI and testing capabilities.

Steps:

1. Create `.github/agents/angular-specialist.agent.md`
2. Add settings header (name, description, tools, MCPs)
3. Enable Angular CLI MCP (see https://angular.dev/ai/mcp) for code generation and testing
4. Configure additional MCPs (GitHub, Azure) as needed
5. Write agent instructions for your specialization (components, services, tests, forms, routing)
6. Test in VS Code or GitHub.com

## Implementing Angular 21 State of the Art Tests

Prompts for agentic test crafting:

```text
Create comprehensive unit tests by organizing test cases into logical describe blocks grouped by concern—initialization, state management, rendering, interactions, accessibility, and edge cases. Use TestBed for setup, async/await patterns with fixture.whenStable() for zoneless change detection, and test both component logic and DOM updates. This structure ensures clear test intent, easy maintenance, and complete coverage across all aspects of component functionality.
```
