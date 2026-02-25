# Tasks & Implementation

GitHub Spec Kit's /speckit.tasks command converts high-level architectural decisions from your technical plan into specific, actionable work items in the tasks.md file. Each task represents a discrete unit of work that can be implemented, tested, and verified independently—providing clear guidance that bridges the gap between architecture and actual code. Well-scoped tasks are actionable and specific, testable with clear verification criteria, independent where possible, and time-bounded so developers can complete them in a reasonable timeframe.

Complex features benefit from phase-based organization that groups related tasks into logical milestones like Setup, Foundation, Core Functionality, UI Integration, Security, and Testing. Task granularity matters—tasks should be specific enough to provide clear direction without being so detailed that they remove developer agency. Task sequencing is critical: database schema tasks come first, back-end API tasks follow, front-end components build on the APIs, security hardening comes after core functionality, and testing happens after implementation.

Use the /speckit.tasks command to generate task lists after finalizing your specification and plan, review them critically to verify coverage and sequencing, then work through tasks systematically while tracking progress. The task list becomes your implementation roadmap and provides objective progress metrics for stakeholder communication. If implementation reveals new complexity, update tasks.md to reflect reality, and use task definitions to distribute work across multiple developers without blocking dependencies.

## Key Topics covered in this module

- Task breakdown and granularity for actionable implementation
- Phase-based organization of complex features
- Task dependencies and logical sequencing
- Task generation with /speckit.tasks command
- Progress tracking and team coordination
- Code generation with /speckit.implement using task guidance
- Managing scope changes, blocked tasks, and priority shifts during implementation
