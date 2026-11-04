# Labs

Eleven hands-on exercises for [Agentic Software Engineering with GitHub Copilot](../demos/readme.md). Lab numbers follow the schedule, not the module numbers: Lab 03 belongs to Module 2, Lab 05 to Module 3, and so on.

Each lab folder holds a `readme.md` with the exercise. Labs 02 through 10 also carry a `*-solution/` folder: a reference copy of the finished artifacts plus a `test-results.md` recording the commands that were run against them. Compare against it, do not copy from it.

| Lab | Exercise | Module | Day | Dur. | Solution |
| --- | -------- | ------ | :-: | ---: | -------- |
| [01](01-get-started/) | Getting started | [M1 Fundamentals](../demos/01-fundamentals/) | 1 | 1.0h | |
| [02](02-assisted-coding/) | Update a web API with GitHub Copilot | [M1 Fundamentals](../demos/01-fundamentals/) | 1 | shared with Lab 01 | [assisted-coding-solution/](02-assisted-coding/assisted-coding-solution/readme.md) |
| [03](03-harness/) | Configure Copilot instructions and create custom agents | [M2 Harness](../demos/02-agentic-harness/) | 2 | 1.5h | [harness-solution/](03-harness/harness-solution/readme.md) |
| [04](04-plugin-marketplace/) | Publish a team plugin marketplace | [M2 Harness](../demos/02-agentic-harness/) | 2 | shared with Lab 03 | [team-plugins-solution/](04-plugin-marketplace/team-plugins-solution/readme.md) |
| [05](05-orchestration/) | Orchestrate a multi-agent build with one prompt | [M3 Agentic Coding](../demos/03-agentic-coding/) | 2 | 1.0h | [orchestration-solution/](05-orchestration/orchestration-solution/readme.md) |
| [06](06-agent-sessions/) | Run two isolated agent sessions and reconstruct what they did | [M4 Agent Sessions](../demos/04-agent-sessions/) | 3 | 1.0h | [agent-sessions-solution/](06-agent-sessions/agent-sessions-solution/readme.md) |
| [07](07-copilot-sdk/) | Integrate an AI agent into an existing app with the Copilot SDK | [M5 CLI & SDK](../demos/05-cli-sdk/) | 3 | 1.0h | [copilot-sdk-solution/](07-copilot-sdk/copilot-sdk-solution/readme.md) |
| [08](08-copilot-app/) | Ship a verified pull request from the Copilot desktop app | [M6 Copilot App](../demos/06-copilot-app/) | 3 | 1.0h | [copilot-app-solution/](08-copilot-app/copilot-app-solution/readme.md) |
| [09](09-devops/) | Resolve GitHub issues using GitHub Copilot | [M7 Agentic DevOps](../demos/07-agentic-devops/) | 4 | 1.0h | [devops-solution/](09-devops/devops-solution/readme.md) |
| [10.1](10-plan-spec-deliver/01-analyze/) | Harvest the current state of vacancy tracking | [M9 Plan, Specify, Deliver](../demos/09-plan-spec-deliver/) | 4 | shared with Lab 10.2 | [hr-current-state-solution/](10-plan-spec-deliver/01-analyze/hr-current-state-solution/) |
| [10.2](10-plan-spec-deliver/02-plan-spec-deliver/) | Ship a feature with GitHub Spec Kit | [M9 Plan, Specify, Deliver](../demos/09-plan-spec-deliver/) | 4 | 1.0h | [meeting-cost-solution/](10-plan-spec-deliver/02-plan-spec-deliver/meeting-cost-solution/readme.md) |

## Before you start

- A GitHub account with GitHub Copilot enabled, or a configured bring-your-own-key endpoint. Labs 03, 07 and 09 import a starter repository into your own account.
- Autopilot is the assumed default permission level. Labs that write to a repository say so and name the level they need.
- The lowest-risk lab to start with is the read-only `/research` session in [Lab 06](06-agent-sessions/).

Runtimes are per lab and each `readme.md` lists its own: the .NET SDK for Labs 03, 07 and 09, Python for Lab 02, Node.js for Labs 06 and 08.

## Where the labs run

Labs 03, 07 and 09 are Microsoft Learn exercises that start by importing a starter repository, so their work happens in your own clone rather than in this repository. Labs 05, 06 and 08 run against this repository and clean up after themselves. Lab 02 runs against [webapi-py](02-assisted-coding/webapi-py/), the starter app checked in beside it. Lab 04 copies its starter out of this repository and publishes it as a new repository in your own account.

The exact placement of each lab in the four-day schedule is in the [course schedule](../demos/readme.md#schedule).
