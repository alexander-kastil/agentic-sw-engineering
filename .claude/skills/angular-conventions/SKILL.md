---
name: angular-conventions
description: Consolidated Angular conventions for components, dependency injection, forms, HTTP, routing, and signals. Use when working on Angular applications and you need modern Angular guidance or routing into a specific Angular concern. Triggers on component creation, inject(), signal forms, httpResource(), guards, route configuration, computed(), linkedSignal(), and Angular architecture.
---

# Angular Conventions

Group reusable Angular guidance under one entry skill.

## When to Use This Skill

- The task is Angular-specific but not yet narrowed to one Angular topic.
- You need a single entry point for Angular components, DI, forms, HTTP, routing, or signals.
- The repository has its own Angular rules in `docs/` and you want to pair those with general Angular conventions.

## Repository Defaults

| Topic             | Current rule                                                                               |
| ----------------- | ------------------------------------------------------------------------------------------ |
| Angular version   | Angular `21.x` or later                                                                    |
| Architecture      | Prefer standalone components                                                               |
| Scaffolding       | Use Angular CLI for components, services, directives, and pipes                            |
| Project structure | Use feature-based folder organization for larger Angular apps                              |
| Routing           | Use route configuration that fits the project, including `app.routes.ts` where appropriate |

## Project-Specific Rule

- Use this skill for reusable Angular guidance.
- Check the repository's `docs/` for project-specific architecture, folder layout, naming, and build rules before applying these conventions.

## Code Generation

Use Angular CLI rather than hand-writing the initial file structure.

```bash
ng generate component my-component
ng generate service my-service
ng generate directive my-directive
ng generate pipe my-pipe
```

## Development Commands

| Command            | Use                                        |
| ------------------ | ------------------------------------------ |
| `ng serve`         | Start the local Angular development server |
| `ng build`         | Create a production build                  |
| `ng build --watch` | Rebuild continuously during development    |

## Deployment Note

Angular projects in this repository are typically deployed to Azure Static Web Apps or Azure Container Apps. Use the project-specific deployment scripts and documentation instead of inventing a new deployment path.

## Delegate Map

| Request type                                | Reference to use                                       |
| ------------------------------------------- | ------------------------------------------------------ |
| Build or refactor standalone components     | [`angular-component`](references/angular-component.md) |
| Configure dependency injection or providers | [`angular-di`](references/angular-di.md)               |
| Build forms and validation flows            | [`angular-forms`](references/angular-forms.md)         |
| Implement API calls and data loading        | [`angular-http`](references/angular-http.md)           |
| Configure navigation and route behavior     | [`angular-routing`](references/angular-routing.md)     |
| Model reactive state with signals           | [`angular-signals`](references/angular-signals.md)     |

## Example Prompts

- "Use angular-conventions to choose the right pattern for a new Angular form."
- "Route this Angular data-loading task to the right conventions reference."
- "Use angular-conventions for a component and signals refactor."

- "Use angular-conventions to scaffold a standalone Angular component and confirm the right CLI command."
- "Use angular-conventions to check the expected Angular build and deployment defaults in this repo."
