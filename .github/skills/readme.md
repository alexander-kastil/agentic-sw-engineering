# Copilot Skills

Skills packaged for this repository. Each folder holds a `SKILL.md` that Copilot loads on demand, so the roster below is what the agent can reach for without being told how.

## Development Conventions

| Skill                                            | Purpose                                                                                                          |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| **[angular-conventions](angular-conventions/)**  | Entry point for Angular 22+ work: signals, DI, forms, routing, NgRx Signal Store, testing, and bundle size.       |
| **[angular-component](angular-component/)**      | Create standalone Angular components with signal inputs and outputs, OnPush change detection, and host bindings.  |
| **[dotnet-conventions](dotnet-conventions/)**    | .NET 10 and C# 14 conventions routed to short task references: DI, EF Core, controllers, auth, streaming, tests.  |
| **[react-skills](react-skills/)**                | Build accessible React components with TypeScript and Fluent UI, including scaffolding and hook patterns.         |
| **[react-state-mgmt](react-state-mgmt/)**        | Choose and wire React state: Redux Toolkit, Zustand, Jotai, React Query server state, and optimistic updates.     |
| **[frontend-design](frontend-design/)**          | Production-grade interfaces with deliberate typography, color, and animation under WCAG 2.2 accessibility rules.  |

## Agents & SDKs

| Skill                                                | Purpose                                                                                                       |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **[copilot-sdk](copilot-sdk/)**                      | Build agentic applications on the GitHub Copilot SDK: custom tools, streaming, sessions, and MCP servers.     |
| **[maf-skill](maf-skill/)**                          | Microsoft Agent Framework Python reference covering the Foundry chat client, packages, credentials, and env.  |
| **[find-skills](find-skills/)**                      | Discover and install skills that extend Copilot when the right capability is not yet in the repository.       |
| **[context7-auto-research](context7-auto-research/)** | Fetch current library and framework documentation through the Context7 API before writing code.               |

## Documents & Diagrams

| Skill                                        | Purpose                                                                                                   |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **[create-docx](create-docx/)**              | Generate, edit, and validate Word documents, including tracked changes and template-driven output.        |
| **[create-pptx](create-pptx/)**              | Build and review PowerPoint decks with slide thumbnails, text extraction, and design validation.          |
| **[pdf-creator](pdf-creator/)**              | Create, merge, split, and mine PDFs, including OCR for scanned documents and generated reports.           |
| **[create-ebook](create-ebook/)**            | Build a single PDF or EPUB from repository Markdown with Pandoc and publish it as a CI artifact.          |
| **[mermaid-expert](mermaid-expert/)**        | Author flowcharts, sequence diagrams, ERDs, and architecture diagrams with correct Mermaid syntax.        |
| **[qr-batch](qr-batch/)**                    | Render a batch of QR code images from a list of URLs with a shared size and error-correction setting.     |

## Automation & Operations

| Skill                                                    | Purpose                                                                                                |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **[browser-use](browser-use/)**                          | Drive a browser from CLI or Python for screenshots, form flows, data extraction, and autonomous agents. |
| **[ssh-ops](ssh-ops/)**                                  | Operate a remote Linux host over SSH, diagnose failed connections, and deploy container stacks.         |
| **[install-openclaw-raspi](install-openclaw-raspi/)**    | Deploy the OpenClaw assistant to a Raspberry Pi 4 end to end, from OS image to running service.         |
| **[sequential-navigation](sequential-navigation/)**      | Split a monolithic Markdown document into guided sections with hub and next-section navigation.         |

## Content

| Skill                                        | Purpose                                                                                             |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **[linkedin-article](linkedin-article/)**    | Write long-form LinkedIn articles with a defensible argument, readable structure, and SEO framing.  |
| **[social-content](social-content/)**        | Plan and write platform-specific social posts, content calendars, and repurposing across channels.  |

## Using a Skill

Copilot picks a skill from its description, so a task-shaped prompt is usually enough:

```
Make scannable images for these six session links for the printed handout
```

To force one, reference its `SKILL.md` directly:

```
Follow instructions in .github/skills/qr-batch/SKILL.md for the links in docs/sessions.md
```
