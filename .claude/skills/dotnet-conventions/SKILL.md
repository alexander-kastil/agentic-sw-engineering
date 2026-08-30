---
name: dotnet-conventions
description: '.NET/C# conventions for .NET 10 / C# 14, routed to short task-based references. Covers C# style and architecture, dependency injection and service lifetimes, async/await, configuration and structured logging, the JSON casing contract with SPA clients, app lifecycle and `dotnet watch` hot-reload limits, the dotnet CLI, `[ApiController]` controllers, EF Core models/migrations/queries, SQL delta scripts for projects that do not use migrations, xUnit + FluentAssertions + NSubstitute testing, `.http` REST client files, MSAL/Entra ID JWT auth, local username/password login with DB RBAC, GitHub OAuth device flow, MCP servers, Microsoft Agent Framework agent calls, the app''s own DB-configured AI model (`AiModel.IsDefault`), A2UI generative-UI endpoints and their SSE streaming, health checks and Docker HEALTHCHECK wiring, NDJSON pipeline streaming, Azure Blob storage with passwordless auth, file-import/ingest endpoints, storing an uploaded file''s bytes in SQL Server itself and serving them back, and server-side WebP conversion with ImageSharp. Read the ONE matching reference; never load them all. Use for any .NET 10 work before writing code. Triggers on "dotnet convention", "c# style", "naming convention", "dependency injection", "service lifetime", "captive dependency", "a second operation was started on this context instance", "addsingleton dbcontext", "endpoint 500s only sometimes", "async convention", "configureawait", "logging convention", "structured logging", "strongly typed configuration", "json casing", "propertynamingpolicy", "jsonpropertyname", "camelcase undefined", "dotnet watch", "hot reload", "typeloadexception", "dotnet cli", "asp.net controller", "ef core migration", "efmigrationshistory", "sql delta script", "schema change", "we do not use migrations", "apply to blue and green", "schema change without migration", "xunit test", "nsubstitute", "fluentassertions", "http rest client file", "msal jwt dotnet", "401 on localhost", "authenabled false", "authorize breaks local dev", "no token works locally", "webapplicationfactory auth passes trivially", "local login rbac", "github oauth device flow", "mcp server dotnet", "mcp tool parameter", "pass the name not the id", "tool takes an id the model cannot know", "mcp tool description", "secure the mcp endpoint", "verify an mcp server", "agent framework dotnet", "db configured ai model", "aimodel isdefault", "provider baseurl", "a2ui endpoint", "sse streaming dotnet", "health check endpoint", "ndjson streaming", "azure blob dotnet", "file import endpoint", "column encryption", "encrypt a db field", "DbEncrypted", "encryptbypassphrase", "decryptbypassphrase", "decrypt with only the database", "encrypt new values only", "decrypt returns null", "store a file in the database", "varbinary(max)", "blob column ef core", "save an uploaded file to sql server", "file download endpoint", "content-disposition filename", "one-to-one shared primary key", "hasforeignkey withone", "list query is slow after adding a file column", "iformfile plus form fields", "requestsizelimit", "convert an image to webp in c#", "imagesharp", "webpencoder", "WebpFileFormat does not exist", "lossy or lossless webp", "webp is bigger than the png", "shrink an uploaded image", "imageformatexception".'
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
