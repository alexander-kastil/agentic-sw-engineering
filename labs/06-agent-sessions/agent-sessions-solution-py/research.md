# How this repository organizes its runnable sample projects under `src/`

Scoping report for Lab 06, Step 2. Every path below is repo-root relative and was checked on disk before being written down.

## The convention

One folder per sample project sits directly under `src/`. There are six of them: `src/copilot-api`, `src/devops-app`, `src/doubler-api`, `src/food-app`, `src/hr-mcp-server`, `src/qr-server`.

Those folders come in two shapes.

**Leaf projects** put their manifest at the folder root, so the folder itself is the runnable unit:

- `src/qr-server/qr-server-py/requirements.txt` next to `src/qr-server/qr-server-py/server.py`
- `src/doubler-api/pyproject.toml` next to `src/doubler-api/main.py`
- `src/hr-mcp-server/hr-mcp-server-cs/hr-mcp-server.csproj` next to `src/hr-mcp-server/hr-mcp-server-cs/Program.cs`
- `src/copilot-api/copilot-api-cs/copilot-api.csproj`
- `src/qr-server/qr-server-cs/qr-server-cs.csproj`

**Container folders** hold the runnable app one level down, and the outer folder carries only a readme:

- `src/devops-app/devops-ng/` with `src/devops-app/devops-ng/angular.json` and `src/devops-app/readme.md` above it
- `src/devops-app/devops-react/` with `src/devops-app/devops-react/package.json` and `src/devops-app/readme.md` above it
- `src/food-app/` holds the shop UI and the catalog API in several stacks: the Angular `src/food-app/shop-ui/food-shop-ng/angular.json` and the .NET `src/food-app/catalog-api/catalog-service-cs/catalog-service.csproj` are the defaults, with React and Vue shops in `src/food-app/shop-ui/` and Java, Python, TypeScript and Go APIs in `src/food-app/catalog-api/`

## The manifest each project type carries

| Project type | Manifest | Example on disk |
|--------------|----------|-----------------|
| Python, pinned requirements | `requirements.txt` | `src/qr-server/qr-server-py/requirements.txt` |
| Python, PEP 621 project | `pyproject.toml` | `src/doubler-api/pyproject.toml` |
| .NET | one `.csproj` named after its folder | `src/hr-mcp-server/hr-mcp-server-cs/hr-mcp-server.csproj`, `src/copilot-api/copilot-api-cs/copilot-api.csproj`, `src/qr-server/qr-server-cs/qr-server-cs.csproj`, `src/food-app/catalog-api/catalog-service-cs/catalog-service.csproj` |
| Angular | `package.json` plus `angular.json` | `src/devops-app/devops-ng/angular.json`, `src/food-app/shop-ui/food-shop-ng/angular.json` |
| React | `package.json` | `src/devops-app/devops-react/package.json` |

There is no solution file and no workspace file above these projects. Each manifest stands alone, which is what lets a module reference a single folder without pulling the rest of `src/` in.

Containerized projects add a Dockerfile beside the manifest rather than centralizing them: `src/hr-mcp-server/hr-mcp-server-cs/Dockerfile`, `src/qr-server/qr-server-cs/Dockerfile`, `src/devops-app/devops-ng/dockerfile`, `src/devops-app/devops-react/dockerfile`, `src/food-app/shop-ui/food-shop-ng/dockerfile`, `src/food-app/catalog-api/catalog-service-cs/dockerfile`. The casing is inconsistent across those six.

## Two facts the convention does not hold up

- `src/readme.md` exists but is zero bytes, so the index the layout implies is not actually written.

Per-project readmes are present for `src/qr-server/qr-server-py`, `src/hr-mcp-server/hr-mcp-server-cs`, `src/devops-app`, `src/food-app/catalog-api/catalog-service-cs`, and the two scaffolded ones at `src/devops-app/devops-ng/README.md` and `src/devops-app/devops-react/README.md`. They are absent for `src/copilot-api`, `src/doubler-api` and `src/qr-server/qr-server-cs`.
