# How this repository organizes its runnable sample projects under `src/`

Scoping report for Lab 05, Step 2. Every path below is repo-root relative and was checked on disk before being written down.

## The convention

One folder per sample project sits directly under `src/`. There are nine of them: `src/angular`, `src/copilot-api`, `src/copilot-api-ui`, `src/doubler-api`, `src/food-app`, `src/hr-mcp-server`, `src/qr-server-cs`, `src/qr-server-py`, `src/react`.

Those folders come in two shapes.

**Leaf projects** put their manifest at the folder root, so the folder itself is the runnable unit:

- `src/qr-server-py/requirements.txt` next to `src/qr-server-py/server.py`
- `src/doubler-api/pyproject.toml` next to `src/doubler-api/main.py`
- `src/hr-mcp-server/hr-mcp-server.csproj` next to `src/hr-mcp-server/Program.cs`
- `src/copilot-api/copilot-api.csproj`
- `src/qr-server-cs/qr-server-cs.csproj`

**Container folders** hold the runnable app one level down, and the outer folder carries only a readme:

- `src/angular/angular-devops/` with `src/angular/angular-devops/angular.json` and `src/angular/readme.md` above it
- `src/react/react-devops/` with `src/react/react-devops/package.json` and `src/react/readme.md` above it
- `src/food-app/` holds two apps: `src/food-app/food-shop/angular.json` and `src/food-app/catalog-service/api/catalog-service.csproj`

## The manifest each project type carries

| Project type | Manifest | Example on disk |
|--------------|----------|-----------------|
| Python, pinned requirements | `requirements.txt` | `src/qr-server-py/requirements.txt` |
| Python, PEP 621 project | `pyproject.toml` | `src/doubler-api/pyproject.toml` |
| .NET | one `.csproj` named after its folder | `src/hr-mcp-server/hr-mcp-server.csproj`, `src/copilot-api/copilot-api.csproj`, `src/qr-server-cs/qr-server-cs.csproj`, `src/food-app/catalog-service/api/catalog-service.csproj` |
| Angular | `package.json` plus `angular.json` | `src/angular/angular-devops/angular.json`, `src/food-app/food-shop/angular.json` |
| React | `package.json` | `src/react/react-devops/package.json` |

There is no solution file and no workspace file above these projects. Each manifest stands alone, which is what lets a module reference a single folder without pulling the rest of `src/` in.

Containerized projects add a Dockerfile beside the manifest rather than centralizing them: `src/hr-mcp-server/Dockerfile`, `src/qr-server-cs/Dockerfile`, `src/angular/angular-devops/dockerfile`, `src/react/react-devops/dockerfile`, `src/food-app/food-shop/dockerfile`, `src/food-app/catalog-service/api/dockerfile`. The casing is inconsistent across those six.

## Two facts the convention does not hold up

- `src/readme.md` exists but is zero bytes, so the index the layout implies is not actually written.
- `src/copilot-api-ui` carries no manifest and no files at all. It contains three empty folders: `src/copilot-api-ui/src/api`, `src/copilot-api-ui/src/components`, `src/copilot-api-ui/src/types`. It is a placeholder, not a runnable project, so a count of "runnable projects under `src/`" is eight, not nine.

Per-project readmes are present for `src/qr-server-py`, `src/hr-mcp-server`, `src/angular`, `src/react`, `src/food-app/catalog-service`, and the two scaffolded ones at `src/angular/angular-devops/README.md` and `src/react/react-devops/README.md`. They are absent for `src/copilot-api`, `src/copilot-api-ui`, `src/doubler-api` and `src/qr-server-cs`.
