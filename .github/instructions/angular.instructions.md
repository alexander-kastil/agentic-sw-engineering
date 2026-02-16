---
description: This file describes the conventions for Angular projects in this repository
---

## Standards

- **Angular Version**: 21.x or later
- **Architecture**: Standalone components preferred

## Code Generation

Use Angular CLI for scaffolding components, services, and other constructs

```bash
ng generate component my-component
ng generate service my-service
ng generate directive my-directive
ng generate pipe my-pipe
```

## Development

- Run `ng serve` for local development server
- Run `ng build` for production builds
- Run `ng build --watch` for watch mode
- Follow feature-based folder organization for large projects
- Use routing modules or `app.routes.ts` as appropriate for the project structure

## Deployment

Angular projects are typically deployed to Azure Static Web Apps or Container Apps. Refer to project-specific deployment scripts and documentation.
