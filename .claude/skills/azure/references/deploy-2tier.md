# End to end: Angular SWA + .NET App Service on the free tiers

The SEQUENCE for a 2-tier app: Angular UI on Azure Static Web Apps Free, .NET API on App Service Free (F1), provisioned with `azcli` scripts, shipped by two GitHub Actions workflows. API deploys through OIDC workload identity; the UI deploys with a SWA deployment token. Modeled on vouchers-ai and carpet-visualizer.

Per-surface detail lives elsewhere: identity + federated credential + `azure/login` in [oidc-github-actions.md](oidc-github-actions.md), SWA specifics in [deploy-swa.md](deploy-swa.md), App Service specifics in [deploy-appservice.md](deploy-appservice.md), Entra-auth database access in [sql-auth.md](sql-auth.md).

## Topology

```
subscription
└── resource group
    ├── App Service plan (Free / F1)
    │   └── Web App (dotnet:10, system-assigned identity)   ← API
    ├── Static Web App (Free)                               ← Angular UI
    └── User-assigned managed identity
        └── Federated credential → GitHub Actions OIDC
```

## Stage 1 - Preflight

Run before writing any files. Each one caused a real failure when skipped.

| # | Check | Failure mode / fix |
|---|---|---|
| 1 | Gitlink: `git ls-files -s <ui-folder>` | Mode `160000` = embedded repo, CI checkout is EMPTY. Move its `.git` to a backup outside the worktree, `git rm --cached <folder>`, re-add as plain files. |
| 2 | API base URL: grep the UI for relative calls (`httpResource(() => '/...')`, `http.post('/...')`) | `proxy.conf.json` does not exist in production. Add a `src/environments/` pair + an `HttpInterceptorFn` in `app.config.ts` prefixing `environment.apiUrl` (empty string in development keeps the proxy working). |
| 3 | CORS: hardcoded `WithOrigins("http://localhost:4200")` | Blocks the SWA origin. Read an `AllowedOrigins` string array from configuration with a localhost fallback; set `AllowedOrigins__0` after the SWA exists. |
| 4 | Angular dist layout | Output is `dist/<project-name>/browser`. Read the project name from `angular.json`, not the folder name. |
| 5 | Node version | Angular CLI enforces a minimum (Angular 22 needs >= 22.22.3). Use `NODE_VERSION: "22.x"`, never a stale exact pin. |
| 6 | Login state | `az account show`, `gh auth status`: verify subscription and repo before provisioning. |
| 7 | Both builds locally | `dotnet build -c Release`, `ng build --configuration=production` before pushing workflows. |

A custom domain mapped to the SWA is a SEPARATE origin: add it as another `AllowedOrigins__N`, then verify with `curl -H "Origin: https://<custom-domain>"` that the response carries `Access-Control-Allow-Origin`. A 200 without that header still fails in the browser.

## Stage 2 - IaC scripts (`infra/cli/`)

`create-resources.azcli`:

```bash
grp=<resource-group>
loc=westeurope
plan=<plan-name>
api=<api-app-name>
swa=<swa-name>

az group create -n $grp -l $loc
az appservice plan create --name $plan -g $grp --sku Free
az webapp create -g $grp -p $plan -n $api --runtime "dotnet:10" --assign-identity
az staticwebapp create --name $swa --resource-group $grp --location $loc --sku Free

swaHost=$(az staticwebapp show -n $swa -g $grp --query defaultHostname -o tsv)
az webapp config appsettings set -g $grp -n $api --settings "AllowedOrigins__0=https://$swaHost" "AllowedOrigins__1=http://localhost:4200"

az staticwebapp secrets list --name $swa --resource-group $grp --query "properties.apiKey" -o tsv
```

`create-workload-identity.azcli`: identity + Contributor + federated credential, see [oidc-github-actions.md](oidc-github-actions.md). Subject for this repo shape: `repo:<org>/<repo>:ref:refs/heads/master`.

Free-tier and script rules:

- Valid SWA regions: `westeurope`, `eastus2`, `westus2`, `centralus`, `eastasia`.
- `--sku Free` on both the App Service plan and the SWA; plan SKU shows as `F1`.
- The federated credential `subject` must exactly match the deploying branch: `repo:<org>/<repo>:ref:refs/heads/<branch>`.
- Contributor role id `b24988ac-6180-42a0-ab88-20f7382dd24c`, scoped to the resource group.
- Never commit plaintext passwords: use a `$variable` placeholder in the script, pass the value at run time.
- Connection strings map through env vars: an `ConnectionStrings__<Name>` app setting reaches `GetConnectionString("<Name>")`.

### Passwordless Azure SQL (preferred over SQL logins)

1. Create the database. Serverless with auto-pause keeps cost near zero; `--use-free-limit` fails with `ProvisioningDisabled` on servers/regions without the free offer.
2. The web app already has a system-assigned identity (`--assign-identity`). As the server's Entra admin, create a contained user in the target database:

```sql
CREATE USER [<web-app-name>] FROM EXTERNAL PROVIDER;
ALTER ROLE db_owner ADD MEMBER [<web-app-name>];
```

Run it over a token-authenticated connection (`az account get-access-token --resource https://database.windows.net`). `db_owner` is required when EF migrations run at startup.

3. Connection string with no secret:

```text
Server=tcp:<server>.database.windows.net,1433;Initial Catalog=<db>;Authentication=Active Directory Default;Encrypt=True;Connect Timeout=60
```

`Active Directory Default` resolves to the managed identity inside App Service and to `az login` credentials locally. The SQL server needs the `AllowAzureServices` (0.0.0.0) firewall rule. More: [sql-auth.md](sql-auth.md).

## Stage 3 - Workflows

Both `workflow_dispatch`, both with `permissions: id-token: write, contents: read`.

**API** (`<api>-ci-cd.yml`): `actions/setup-dotnet@v4` (`10.x`) -> `dotnet restore` / `build` / `publish` -> zip -> artifact -> `azure/login@v2` with `AZURE_CLIENT_ID` / `AZURE_TENANT_ID` / `AZURE_SUBSCRIPTION_ID` -> `azure/webapps-deploy@v2` with the zip.

**UI** (`<ui>-ci-cd.yml`): `actions/setup-node@v4` (`22.x`, npm cache keyed on the UI lockfile) -> `npm ci --legacy-peer-deps --include=optional` -> `npm rebuild lightningcss` -> `ng build --configuration=production` -> upload `dist/<project>/browser` -> `azure/static-web-apps-deploy@v1` with `azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APP_TOKEN_PROD }}`, `action: upload`, `skip_app_build: true`, `skip_api_build: true`, `is_static_export: true`, `output_location: ""`.

Never `npm install` in CI: it can re-resolve caret ranges past the lockfile and drift package versions out of lockstep. Verify locally with `npm ci --dry-run` that the lockfile is in sync.

## Stage 4 - Secrets, push, run

```bash
gh secret set AZURE_CLIENT_ID --body "<mi-client-id>" --repo <org>/<repo>
gh secret set AZURE_TENANT_ID --body "<tenant-id>" --repo <org>/<repo>
gh secret set AZURE_SUBSCRIPTION_ID --body "<subscription-id>" --repo <org>/<repo>
gh secret set AZURE_STATIC_WEB_APP_TOKEN_PROD --body "<swa-api-key>" --repo <org>/<repo>
```

Real values: the repo's `credentials.json` / `config.json` (git-ignored).

Commit and push only with explicit user approval. Then:

```bash
gh workflow run <name>.yml --repo <org>/<repo> --ref master
gh run watch <run-id> --repo <org>/<repo> --exit-status --interval 15
```

Re-run failed workflows after fixing root causes until both are green.

## Stage 5 - Verify

A green deploy job does NOT mean the app runs. Always:

```bash
curl -s -o /dev/null -w "%{http_code}\n" --max-time 120 https://<api-app>.azurewebsites.net/<endpoint>
curl -s -o /dev/null -w "%{http_code}\n" https://<swa-default-hostname>/
```

HTTP 500.30 = the ASP.NET Core app failed at startup (common with EF migrations running on boot). Get the real exception:

```bash
az webapp log download -g $grp -n $api --log-file logs.zip
unzip logs.zip && grep -o "<Data>[^<]*</Data>" LogFiles/eventlog.xml | tail
```

## Gotchas

| Symptom | Cause | Fix |
|---|---|---|
| CI builds but UI folder empty | Embedded repo gitlink (mode 160000) | Fold files into the main repo (Stage 1.1) |
| `The Angular CLI requires a minimum Node.js version` | Stale exact Node pin | `NODE_VERSION: "22.x"` |
| HTTP 500.30 after green deploy | Startup crash (DB unreachable, missing config) | Read `LogFiles/eventlog.xml` |
| SQL `error: 40` from App Service | Wrong or dead SQL host (cloudapp DNS disappears with deallocated VMs) | `nslookup` the host; confirm the current server with the user |
| SWA deploy 401 | Wrong or rotated deployment token | Re-fetch via `az staticwebapp secrets list` |
| API calls 404 on SWA | Relative URLs without interceptor | Stage 1.2 |
| CORS errors in browser | SWA origin not in allowed origins | Set `AllowedOrigins__0` app setting |
| CORS works on `*.azurestaticapps.net` but not the custom domain | Custom domain is a separate origin | Add another `AllowedOrigins__N` app setting |
| Service worker / PWA breaks after deploy to SWA | Missing `staticwebapp.config.json` (fallback excludes, `.webmanifest` MIME type, no-cache headers) | Follow the `angular-pwa-swa` skill |
| OIDC login `AADSTS70021`, `MissingSubscription` on role assignment | Identity setup | [oidc-github-actions.md](oidc-github-actions.md) |
