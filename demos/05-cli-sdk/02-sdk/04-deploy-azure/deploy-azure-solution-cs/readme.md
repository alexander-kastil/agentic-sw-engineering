# Deploying an SDK Agent to Azure: Worked Solution (C#)

An SDK agent behind an HTTP API, containerized, with the Azure Container Apps commands to publish it. Verified against `GitHub.Copilot.SDK` 1.0.14 on .NET 10, which bundles Copilot CLI 1.0.85.

## What is here

| File | What it does |
|------|--------------|
| `Program.cs` | The whole service: an ASP.NET Core minimal API with `GET /health` and `POST /ask`, one custom tool, and a client that connects to either the bundled runtime or an external one |
| `deploy-azure-solution-cs.csproj` | .NET 10 web SDK project with the `GitHub.Copilot.SDK` package reference |
| `Dockerfile` | Multi-stage build: the SDK image restores, publishes for `linux-x64`, and downloads the matching Copilot CLI; the runtime image adds `curl` for the `HEALTHCHECK` |
| `deploy.azcli` | The Container Apps commands, one step at a time, including the Key Vault secret reference for the token |
| `.dockerignore` | Keeps `bin/` and `obj/` out of the build context |

## Run it locally

```bash
dotnet build
dotnet run
```

```bash
curl http://127.0.0.1:8080/health
curl -X POST -H "content-type: application/json" \
  -d '{"prompt":"What is the deployment status of the checkout service?"}' \
  http://127.0.0.1:8080/ask
```

Healthy responses:

```json
{"status":"ok","model":"gpt-5-mini","runtime":"bundled"}
{"answer":"The checkout service is currently running (revision: local, region: local)."}
```

## Run it in a container

```bash
docker build -t copilot-agent-api-cs:local .
docker run -d --name cagent-cs -p 8080:8080 -e COPILOT_GITHUB_TOKEN=$GITHUB_TOKEN copilot-agent-api-cs:local
curl http://127.0.0.1:8080/health
docker inspect --format='{{.State.Health.Status}}' cagent-cs
```

The image builds and `/health` answers 200 with no credentials at all, because the health probe deliberately does not touch the model. `POST /ask` needs a token: the container has no interactive login, so `COPILOT_GITHUB_TOKEN` is how the runtime gets an identity.

## Configuration

| Variable | Default | What it does |
|----------|---------|---------------|
| `PORT` | `8080` | The port the HTTP server binds |
| `COPILOT_MODEL` | `gpt-5-mini` | The model each session requests |
| `COPILOT_GITHUB_TOKEN` | none | The GitHub identity for unattended runs. Required in a container |
| `COPILOT_RUNTIME_URL` | unset | Connect to an already-running `copilot --headless` instead of spawning the bundled runtime |
| `CONTAINER_APP_REVISION`, `AZURE_REGION` | `local` | Surfaced by the sample tool so you can see which revision answered |

`COPILOT_MODEL` is read from the ambient environment. If it is already exported on your machine the default never applies, which is worth knowing before you conclude the code ignored you.

## Two ways to reach the runtime

`Program.cs` picks between them on one environment variable.

Bundled, the default: the SDK spawns the CLI as a child process of your service. One container, nothing else to run, and the agent's lifetime is the service's lifetime.

External, when `COPILOT_RUNTIME_URL` is set: you run `copilot --headless --port 4321` yourself and the client attaches with `RuntimeConnection.ForUri`. This is the shape you want when several service replicas share one runtime, or when you want to restart the API without restarting the agent runtime.

## A C#-specific pitfall: the CLI downloads at build time, not at run time

The Node SDK bundles Copilot CLI as an npm dependency, so `npm ci` fetches it. `GitHub.Copilot.SDK` instead downloads a platform-specific Copilot CLI archive from `github.com/github/copilot-cli` releases as an MSBuild target that runs on every `dotnet build` or `dotnet publish`, and copies it into `runtimes/<rid>/native/` next to your app. Two consequences:

- The build machine (and the Docker build stage) needs outbound internet access, separate from NuGet restore.
- Without an explicit `-r linux-x64` on `dotnet restore`/`dotnet publish`, the SDK downloads the CLI for the build host's own RID (`win-x64` on a Windows dev box), which is useless inside a Linux container. The Dockerfile pins `-r linux-x64` on both steps so the container gets the right binary.

## What was verified, and what was not

| Claim | Status |
|-------|--------|
| `dotnet build` clean, no warnings | Verified |
| `GET /health` returns 200 with the model and runtime | Verified locally and in the container |
| `POST /ask` drives the agent and its custom tool | Verified locally, with a real model call |
| Unknown path returns 404, missing prompt returns 400 | Verified |
| `docker build` succeeds and the container serves `/health` | Verified |
| The `HEALTHCHECK` reaches `healthy` | Verified |
| `POST /ask` inside the container | Not executed: needs a `COPILOT_GITHUB_TOKEN` in the container |
| `deploy.azcli` against a live subscription | Not executed: creates billable Azure resources, so it is yours to run |

## Timeouts

`SendAndWaitAsync` defaults to a 60 second timeout, passed as a nullable `TimeSpan` second argument. An agent turn that calls tools and then writes will exceed that, and the failure arrives as a thrown `TimeoutException` rather than a slow answer. Pass a longer `TimeSpan` when a route can legitimately take longer, and set the platform's own timeouts to match: Container Apps ingress has its own request limit, and a proxy in front of it will have another.
