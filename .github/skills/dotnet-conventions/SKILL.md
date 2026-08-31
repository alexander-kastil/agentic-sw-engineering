---
name: dotnet-conventions
description: '.NET 10 / C# 14 conventions, routed to short task-based references. Covers C# style, DI and service lifetimes, async/await, configuration and structured logging, the JSON casing contract with SPA clients, `dotnet watch` hot-reload limits, the dotnet CLI, controllers, EF Core and SQL delta scripts where migrations are banned, xUnit testing, `.http` files, MSAL/Entra JWT and local login with DB RBAC, MCP servers, Agent Framework calls, A2UI SSE endpoints, health checks, NDJSON streaming, Azure Blob, file import/download with SQL blob storage, and WebP conversion. Read the ONE matching reference; never load them all. Use for any .NET 10 work before writing code. Triggers on dotnet convention, c# style, dependency injection, captive dependency, async convention, structured logging, json casing, camelcase undefined, dotnet watch, hot reload, asp.net controller, ef core migration, sql delta script, we do not use migrations, xunit test, msal jwt dotnet, 401 on localhost, local login rbac, mcp server dotnet, agent framework dotnet, a2ui endpoint, sse streaming dotnet, ndjson streaming, azure blob dotnet, encrypt a db field, store a file in the database, file download endpoint, convert an image to webp in c#.'
---

# .NET/C# Conventions

Authoritative conventions for any .NET 10 / C# 14 project. Routes build, test and tooling requests to
the matching reference before any code convention is applied.

> ⚠️ **CRITICAL**: Always validate code practices and API usage against **Microsoft Learn** via the
> `microsoft-learn` MCP before writing code. Do not rely on assumptions about SDK patterns, APIs or
> best practices; check the official documentation.

**This file is a router and holds no conventions of its own.** Find your task below and read that ONE
reference. Loading several defeats the point — each leaf is short so the matching one can be read whole.

## Language, structure and runtime behaviour

| You want to... | Read |
|---|---|
| Name things; structure files, types and members; apply architecture patterns and SOLID/code-quality rules | [`conventions`](references/conventions.md) |
| Inject dependencies, choose `Singleton`/`Scoped`/`Transient`, use primary constructors, dispose resources, fix a captive `DbContext` in a singleton | [`di-and-lifetimes`](references/di-and-lifetimes.md) |
| Write `async`/`await` code: `Task` returns, `ConfigureAwait`, async exception handling | [`async-patterns`](references/async-patterns.md) |
| Bind strongly-typed settings, read `IConfiguration`, log with structure, throw and handle exceptions | [`configuration-and-logging`](references/configuration-and-logging.md) |
| Fix a field arriving `undefined`/empty in a SPA after a 200 response; decide PascalCase vs camelCase on the wire | [`json-casing-contract`](references/json-casing-contract.md) |
| Start or reuse a running app; survive `dotnet watch` rude edits and `TypeLoadException` after a structural edit | [`app-lifecycle-and-watch`](references/app-lifecycle-and-watch.md) |

## Building and testing

| You want to... | Read |
|---|---|
| Build, run, watch, test, publish, format, manage NuGet, solutions or the EF migrations CLI | [`dotnet-cli`](references/dotnet-cli.md) |
| Write unit tests with xUnit, FluentAssertions and NSubstitute; diagnose a failing or permanently-red suite | [`dotnet-testing`](references/dotnet-testing.md) |
| Write or update a `.http` REST client file | [`dotnet-rest-client`](references/dotnet-rest-client.md) |

## API surface and data

| You want to... | Read |
|---|---|
| Add or change an `[ApiController]` controller and its CRUD endpoint patterns | [`dotnet-controllers`](references/dotnet-controllers.md) |
| Configure an EF Core model (`IEntityTypeConfiguration`), write queries, add a migration where the project uses them, or hand-create a table a migration owns | [`dotnet-efcore`](references/dotnet-efcore.md) |
| Ship a schema or data change as a hand-written SQL delta script applied to every slot, in a project that does not use EF migrations — including marking the replaced migration applied in `__EFMigrationsHistory` so `Database.Migrate()` does not recreate the tables | [`sql-delta-scripts`](references/sql-delta-scripts.md) |
| Encrypt individual columns so the plaintext is recoverable from the database alone (attach it anywhere, paste one statement), encrypt only new values without migrating existing rows, or debug a decrypt that silently returns NULL | [`dotnet-column-encryption`](references/dotnet-column-encryption.md) |
| Accept an uploaded file and turn it into reviewable domain rows (`IFormFile` upload → OCR/Excel extraction → AI draft → review → EF commit) | [`file-import-ingest`](references/file-import-ingest.md) |
| Store files in Azure Blob Storage with passwordless `DefaultAzureCredential` and `BlobServiceClient`, stage→confirm promotion, document retention (`ImportDocument`) | [`azure-blob-storage`](references/azure-blob-storage.md) |
| Keep an uploaded file's bytes IN SQL Server (`varbinary(max)` in a side table on a shared primary key) and serve them back as a download, without the blob leaking into list queries | [`sql-stored-files`](references/sql-stored-files.md) |
| Convert an uploaded JPEG/PNG to WebP in-process with ImageSharp: encode both ways and keep the smaller, pass everything else through untouched | [`imagesharp-webp`](references/imagesharp-webp.md) |

## Authentication

| You want to... | Read |
|---|---|
| Wire MSAL / Microsoft.Identity.Web JWT auth, or triage a 401 / IDX error | [`dotnet-msal-auth`](references/dotnet-msal-auth.md) |
| Add local username/password login (BCrypt + local JWT) and DB RBAC alongside MSAL | [`dotnet-local-auth-rbac`](references/dotnet-local-auth-rbac.md) |
| Sign in with GitHub via **device flow** (onboard/clone private repos, list repos) — no secret, no callback, Client ID in `appsettings.json`, mandatory `slow_down` back-off | [`dotnet-github-oauth`](references/dotnet-github-oauth.md) |

## AI, agents and streaming

| You want to... | Read |
|---|---|
| Expose an MCP server (`ModelContextProtocol` / `ModelContextProtocol.AspNetCore`): packages, transports, ports, client config | [`dotnet-mcp`](references/dotnet-mcp.md) |
| Design the tool surface a model calls: parameter shape, natural keys over ids, descriptions, return payloads, propose/confirm pairs | [`dotnet-mcp-tool-design`](references/dotnet-mcp-tool-design.md) |
| Secure an MCP server: `[Authorize]` per tool, dual auth on `/mcp`, reverse-proxy `X-Forwarded-Proto` | [`dotnet-mcp-auth`](references/dotnet-mcp-auth.md) |
| Verify a running MCP server over HTTP and log every tool call | [`dotnet-mcp-verify`](references/dotnet-mcp-verify.md) |
| Call an Azure AI Foundry hosted or prompt-based agent (Microsoft Agent Framework) | [`dotnet-maf`](references/dotnet-maf.md) |
| Call the app's own DB-configured AI model (`AiModel.IsDefault`) to draft customer-facing copy; normalise a provider `BaseUrl`; turn any provider failure into one safe 503 | [`dotnet-db-configured-ai-model`](references/dotnet-db-configured-ai-model.md) |
| Set up an A2UI generative-UI endpoint (no .NET SDK; protocol-level JSON): what it is, protocol version, packages, config, registration | [`dotnet-a2ui`](references/dotnet-a2ui.md) |
| Define or validate the C# message types that cross the A2UI wire | [`dotnet-a2ui-messages`](references/dotnet-a2ui-messages.md) |
| Serve the A2UI component catalog or implement the agent endpoint | [`dotnet-a2ui-endpoint`](references/dotnet-a2ui-endpoint.md) |
| Stream A2UI over SSE — wire format, full example, anti-patterns | [`dotnet-a2ui-streaming`](references/dotnet-a2ui-streaming.md) |
| Stream pipeline progress as NDJSON with a correlated trace a controller can tap | [`ndjson-streaming`](references/ndjson-streaming.md) |

## Operations

| You want to... | Read |
|---|---|
| Add `/health` readiness and liveness probes, dependency checks, Docker `HEALTHCHECK` wiring | [`dotnet-health-checks`](references/dotnet-health-checks.md) |

## The one rule that belongs here

Always use the dotnet CLI for package and project operations — **never hand-edit `.csproj`** to add or
remove packages.
