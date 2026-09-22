# Deploy a static UI to Azure Static Web Apps

SWA hosts a static frontend plus an optional serverless (Functions) API. Path: provision -> configure -> emulate locally -> deploy. CI/CD uses passwordless OIDC; no deployment token stored as a GitHub secret.

Real values (subscription/tenant/client IDs, deployment tokens): the repo's `credentials.json` / `config.json` (git-ignored).

## Key insight

`azure/static-web-apps-deploy@v1` **cannot use the OIDC session directly**. After `azure/login@v2` succeeds, fetch the SWA deployment token via Azure CLI and pass it explicitly. The "Get SWA Deployment Token" step is always required.

## Config files

| File | Owner | Purpose |
|---|---|---|
| `swa-cli.config.json` | created by `swa init`, never hand-created | CLI settings (app/api/output locations, build + dev commands) |
| `staticwebapp.config.json` | hand-written, in `app_location` or `output_location` | runtime routes, auth, headers, `platform.apiRuntime` |

## Read configuration

```bash
cfg=.claude/skills/azure-deploy/deploy.json
RG=$(jq -r '.ResourceGroup' $cfg)
SWA_NAME=$(jq -r '.SWA.Name' $cfg)
APP_LOC=$(jq -r '.SWA.AppLocation' $cfg)
OUT_LOC=$(jq -r '.SWA.OutputLocation' $cfg)
```

## Create Static Web App (one-time)

```bash
az staticwebapp create \
    --name $SWA_NAME \
    --resource-group $RG \
    --location $LOC \
    --sku Free
```

## Assign role to WIF identity (one-time)

```bash
WIF=$(jq -r '.WIF' $cfg)
SWA_ID=$(az staticwebapp show --name $SWA_NAME --resource-group $RG --query id -o tsv)
PRINCIPAL=$(az identity show --name $WIF --resource-group $RG --query principalId -o tsv)

az role assignment create \
    --assignee $PRINCIPAL \
    --role Contributor \
    --scope $SWA_ID
```

## SWA CLI

Install and verify:

```bash
npm install -D @azure/static-web-apps-cli
npx swa --version
```

Order: `swa init` -> `swa start` -> `swa login` -> `swa deploy`. **Always `swa init` before `start` or `deploy`.**

```bash
npx swa init              # interactive, auto-detects framework
npx swa init --yes        # accept auto-detected defaults
npm run build
npx swa start             # emulator at http://localhost:4280
npx swa login
npx swa deploy --env production
```

Generated `swa-cli.config.json` (reference only, edit after init to customize):

```json
{
  "$schema": "https://aka.ms/azure/static-web-apps-cli/schema",
  "configurations": {
    "app": {
      "appLocation": ".",
      "apiLocation": "api",
      "outputLocation": "dist",
      "appBuildCommand": "npm run build",
      "run": "npm run dev",
      "appDevserverUrl": "http://localhost:3000"
    }
  }
}
```

### swa login

```bash
swa login                              # interactive
swa login --subscription-id <id>       # specific subscription
swa login --clear-credentials          # clear cached credentials
```

Flags: `--subscription-id, -S` | `--resource-group, -R` | `--tenant-id, -T` | `--client-id, -C` | `--client-secret, -CS` | `--app-name, -n`

### swa build

```bash
swa build                   # build using config
swa build --auto            # auto-detect and build
swa build myApp             # build a specific configuration
```

Flags: `--app-location, -a` | `--api-location, -i` | `--output-location, -O` | `--app-build-command, -A` | `--api-build-command, -I`

### swa start (local emulator)

```bash
swa start                                    # serve from outputLocation
swa start ./dist                             # serve specific folder
swa start http://localhost:3000              # proxy to dev server
swa start ./dist --api-location ./api        # with API folder
swa start http://localhost:3000 --run "npm start"  # auto-start dev server
```

Flags: `--port, -p` (default 4280) | `--api-location, -i` | `--api-port, -j` (default 7071) | `--run, -r` | `--open, -o` | `--ssl, -s`

Dev-server ports: React/Vue/Next.js 3000, Angular 4200, Vite 5173.

### swa deploy

```bash
swa deploy                              # deploy using config
swa deploy ./dist                       # deploy specific folder
swa deploy --env production             # deploy to production
swa deploy --deployment-token <TOKEN>   # use deployment token
swa deploy --dry-run                    # preview without deploying
```

Flags: `--env` (`preview` or `production`) | `--deployment-token, -d` | `--app-name, -n`

Deployment token sources: Azure Portal (Static Web App -> Overview -> Manage deployment token), `swa deploy --print-token`, or env var `SWA_CLI_DEPLOYMENT_TOKEN`.

### swa db

```bash
swa db init --database-type mssql
swa db init --database-type postgresql
swa db init --database-type cosmosdb_nosql
```

## staticwebapp.config.json

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/images/*", "/css/*"]
  },
  "routes": [
    { "route": "/api/*", "allowedRoles": ["authenticated"] }
  ],
  "platform": {
    "apiRuntime": "node:20"
  }
}
```

## Azure Functions API backend

```bash
mkdir api && cd api
func init --worker-runtime node --model V4
func new --name message --template "HTTP trigger"
```

`api/src/functions/message.js`:

```javascript
const { app } = require('@azure/functions');

app.http('message', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: async (request) => {
        const name = request.query.get('name') || 'World';
        return { jsonBody: { message: `Hello, ${name}!` } };
    }
});
```

Set `platform.apiRuntime` in `staticwebapp.config.json`, set `apiLocation` in `swa-cli.config.json`:

```json
{
  "configurations": {
    "app": { "apiLocation": "api" }
  }
}
```

Test: `npx swa start ./dist --api-location ./api`, API at `http://localhost:4280/api/message`.

Supported API runtimes: `node:18`, `node:20`, `node:22`, `dotnet:8.0`, `dotnet-isolated:8.0`, `python:3.10`, `python:3.11`.

## GitHub Actions, OIDC (preferred)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: actions/checkout@v4

  - name: Azure Login (OIDC)
    uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

  - name: Get SWA Deployment Token
    run: |
      SWA_TOKEN=$(az staticwebapp secrets list \
        --name <swa-name> \
        --resource-group <resource-group> \
        --query "properties.apiKey" -o tsv)
      echo "::add-mask::$SWA_TOKEN"
      echo "SWA_DEPLOYMENT_TOKEN=$SWA_TOKEN" >> $GITHUB_ENV

  - name: Build UI
    run: npm ci && npm run build
    working-directory: <app-location>

  - name: Deploy to Static Web Apps
    uses: azure/static-web-apps-deploy@v1
    with:
      azure_static_web_apps_api_token: ${{ env.SWA_DEPLOYMENT_TOKEN }}
      repo_token: ${{ secrets.GITHUB_TOKEN }}
      action: upload
      app_location: <app-location>
      output_location: <output-location>
```

Substitute `<swa-name>`, `<resource-group>`, `<app-location>`, `<output-location>` from `deploy.json`.

### Full workflow, Angular example

`food-shop-ng` (Angular 21, output at `dist/food-shop-ui/browser`):

```yaml
name: Deploy UI

on:
  push:
    branches: [main]
    paths: ['src/food-app/shop-ui/food-shop-ng/**']
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Get SWA Deployment Token
        run: |
          cfg=.claude/skills/azure-deploy/deploy.json
          SWA_NAME=$(jq -r '.SWA.Name' $cfg)
          RG=$(jq -r '.ResourceGroup' $cfg)
          SWA_TOKEN=$(az staticwebapp secrets list \
            --name $SWA_NAME --resource-group $RG \
            --query "properties.apiKey" -o tsv)
          echo "::add-mask::$SWA_TOKEN"
          echo "SWA_DEPLOYMENT_TOKEN=$SWA_TOKEN" >> $GITHUB_ENV

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Build
        run: npm ci && npm run build
        working-directory: ${{ fromJson(steps.cfg.outputs.cfg).SWA.AppLocation }}

      - name: Deploy
        uses: azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ env.SWA_DEPLOYMENT_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: upload
          app_location: ${{ fromJson(steps.cfg.outputs.cfg).SWA.AppLocation }}
          output_location: ${{ fromJson(steps.cfg.outputs.cfg).SWA.OutputLocation }}
```

## GitHub Actions, stored-token variant (portal-linked repo)

Applies when the SWA resource is linked to the repo in the portal (workflow auto-generated) and the token lives in repo secret `AZURE_STATIC_WEB_APPS_API_TOKEN`. Adds PR preview environments and PR-close cleanup, which the OIDC variant above does not cover.

`.github/workflows/azure-static-web-apps.yml`:

```yaml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]

jobs:
  build_and_deploy:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: upload
          app_location: /
          api_location: api
          output_location: dist

  close_pr:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: close
```

Workflow inputs: `app_location` (frontend source), `api_location` (API source), `output_location` (built output), `skip_app_build: true` (pre-built), `app_build_command` (custom build).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `deployment_token was not provided` | Deploy action needs an explicit token even with OIDC | Add the "Get SWA Deployment Token" step; always required |
| `client-id not supplied` | GitHub secrets not set | `gh secret set` for all three `AZURE_*` secrets, see [devops-wif.md](devops-wif.md) |
| Output folder not found / build output not found | Wrong `OutputLocation` in `deploy.json` or `output_location` | Angular outputs to `dist/<project-name>/browser`; verify `outputPath` in `angular.json` |
| OIDC login fails after secrets set | Federated credential subject mismatch | `--subject repo:<org>/<repo>:ref:refs/heads/main` must match exactly, see [oidc-github-actions.md](oidc-github-actions.md) |
| 404 on client routes | No SPA fallback | `navigationFallback` with `rewrite: "/index.html"` in `staticwebapp.config.json` |
| API returns 404 | api folder structure, runtime, or exports | Verify `api` folder layout, set `platform.apiRuntime`, check function exports |
| Auth not working locally | Emulator auth path | Use `/.auth/login/<provider>` for the auth emulator UI |
| CORS errors | External API called from the SPA | `/api/*` is same-origin; external APIs need CORS headers |
| Deployment token expired | Rotated/expired token | Regenerate: Azure Portal -> Static Web App -> Manage deployment token |
| Config not applied | File in the wrong folder | `staticwebapp.config.json` must sit in `app_location` or `output_location` |
| Local API timeout | Default limit 45 seconds | Optimize the function or remove blocking calls |

Debug:

```bash
swa start --verbose log        # verbose output
swa deploy --dry-run           # preview deployment
swa --print-config             # show resolved configuration
```

## See also

[oidc-github-actions.md](oidc-github-actions.md), [devops-wif.md](devops-wif.md), [deploy-appservice.md](deploy-appservice.md), [cli-conventions.md](cli-conventions.md)
