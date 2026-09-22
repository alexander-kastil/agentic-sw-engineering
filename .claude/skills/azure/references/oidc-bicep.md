# Secret-less GitHub Actions to Azure, declared in Bicep (Microsoft Graph extension)

Same outcome as the CLI path, declared as code: an Entra **app registration** (not a managed identity) trusts the repo via a federated identity credential, `azure/login` exchanges the GitHub OIDC token, and the app's service principal holds RBAC on the target resource groups. App registration included, everything is Bicep.

For the `az` CLI equivalent, the `azure/login` step and the subject-claim rules (branch vs environment vs pull_request): [oidc-github-actions.md](oidc-github-actions.md). For the cross-tenant context this builds on (B2B guest, `MissingSubscription`, role-assignment writes): [tenant-access.md](tenant-access.md).

Placeholders (`<tenant-id>`, `<subscription-id>`, `<client-id>`, `<swa-hostname>`) are never literal. Real values: the repo's `credentials.json` / `config.json` (git-ignored).

## 1 - Declare the Graph extension

GA at `v1.0:1.0.0`. `bicepconfig.json` next to the templates:

```json
{
  "extensions": {
    "microsoftGraphV1": "br:mcr.microsoft.com/bicep/extensions/microsoftgraph/v1.0:1.0.0"
  }
}
```

Then `extension microsoftGraphV1` at the top of any module declaring Graph resources. Bicep 0.30+: the `extension` keyword is GA, no `experimentalFeaturesEnabled` flag at `1.0.0`.

## 2 - App + service principal + federated credential

```bicep
targetScope = 'subscription'   // Graph resources are tenant-scoped; any deployment scope is fine

extension microsoftGraphV1

param appName string
param gitHubSubject string      // e.g. repo:owner/repo:ref:refs/heads/main

resource app 'Microsoft.Graph/applications@v1.0' = {
  uniqueName: appName           // client-provided key => idempotent upsert (Graph uses POST, not PUT)
  displayName: appName

  // GitHub Actions trusts this app, secret-less. NOTE the Graph quirk: a federated credential's
  // name MUST be the composite '<app uniqueName>/<fic name>'.
  resource fic 'federatedIdentityCredentials@v1.0' = {
    name: '${appName}/github-oidc'
    issuer: 'https://token.actions.githubusercontent.com'
    subject: gitHubSubject
    audiences: ['api://AzureADTokenExchange']
  }
}

resource sp 'Microsoft.Graph/servicePrincipals@v1.0' = {
  appId: app.appId              // SP is keyed by appId
}

output applicationClientId string = app.appId
output servicePrincipalObjectId string = sp.id
```

Graph quirks:

| Fact | Detail |
|---|---|
| Idempotency keys | applications/groups: `uniqueName`; service principals: `appId`; federated credentials: the composite `name`. Without them, redeploys create duplicates. |
| FIC name | MUST be `'<app uniqueName>/<fic name>'`. |
| Permissions to deploy | Entra app-registration rights (Application Administrator `9b895d92-2cd3-44c7-9d02-a6ac2d5ea5c3` / Global Administrator `62e90394-69f5-4237-9190-012177145e10`). Works with `az deployment sub create` run as a *user*, including a guest Global Admin; ARM calls Graph on their behalf. |
| No passwords | `applications`/`servicePrincipals` support only `keyCredentials` and federated credentials. Exactly what OIDC wants. |
| Unsupported | `what-if`, deployment stacks, verbose output. `azd provision --preview` and `az deployment ... --what-if` choke on Graph resources: deploy directly. |

## 3 - Grant the SP RBAC in Bicep

Workflows log in as this SP, so it needs `Contributor` on each target resource group (enough to deploy SWAs / App Service and to read SWA deployment tokens).

**Assign the role in Bicep, not the CLI**: `az role assignment create` often fails `MissingSubscription` for a guest, whereas the ARM deployment carries the right tenant context.

```bicep
module spRole 'modules/rg-roleassignment.bicep' = {
  name: 'sproleassignment'
  scope: targetRg
  params: {
    principalId: appRegistration!.outputs.servicePrincipalObjectId  // `!` silences BCP318 on conditional modules
    principalType: 'ServicePrincipal'   // Contributor = b24988ac-6180-42a0-ab88-20f7382dd24c
  }
}
```

The SP is fresh, so replication delay can make the first assignment flap; a redeploy is the simplest retry. Granting at RG scope is fine even when the user is already Contributor at subscription scope.

## 4 - GitHub secrets (gh cli)

```bash
gh secret set AZURE_CLIENT_ID       --body "<app registration appId>"
gh secret set AZURE_TENANT_ID       --body "<tenant id>"          # the CUSTOMER tenant if cross-tenant
gh secret set AZURE_SUBSCRIPTION_ID --body "<subscription id>"
gh secret list
```

`gh` needs the `workflow` scope to push workflow files. Secrets are account-context, independent of the active `az` tenant.

## 5 - Workflow shape

`azure/login@v2` with the three secrets and `permissions: { id-token: write, contents: read }`: see [oidc-github-actions.md](oidc-github-actions.md).

Static Web App, prebuilt content: pull the deployment token with the OIDC login, then upload.

```yaml
- run: |
    SWA_TOKEN=$(az staticwebapp secrets list --name <swa> --resource-group <rg> \
      --query "properties.apiKey" -o tsv)
    echo "::add-mask::$SWA_TOKEN"
    echo "SWA_DEPLOYMENT_TOKEN=$SWA_TOKEN" >> $GITHUB_ENV
- uses: azure/static-web-apps-deploy@v1
  with:
    azure_static_web_apps_api_token: ${{ env.SWA_DEPLOYMENT_TOKEN }}
    repo_token: ${{ secrets.GITHUB_TOKEN }}
    action: upload
    app_location: <built output dir>
    output_location: ""
    skip_app_build: true          # already built in a prior step (Hugo/Angular), or static content
```

App Service (.NET etc.): build/publish, then `Azure/webapps-deploy@v3` with `app-name`. Details: [deploy-swa.md](deploy-swa.md), [deploy-appservice.md](deploy-appservice.md).

Use `paths:` filters so each app's workflow fires only on its own subtree, and keep `workflow_dispatch:` to trigger the first run with `gh workflow run <file> --ref <branch>` (a path-filtered push will not fire a workflow whose subtree did not change).

## 6 - Naming gotchas (azd + App Service)

- **App Service site names are GLOBALLY unique.** Reusing a name that exists in another tenant/sub fails `Conflict: Website with given name X already exists`. Pick a distinct name per environment.
- **azd matches the `azd-service-name` TAG, not the resource name.** Give the resource a globally-unique name, tag it `azd-service-name: <service key>`, and use the same key in `azure.yaml`.
- **Deploying the same app to a SECOND tenant** hits the global-name rule: add a per-environment suffix (e.g. `-bp`). Renaming the App Service means updating every client that hard-codes its hostname (e.g. an Angular SPA's prod `environment.ts` `apiBase`), or the frontend calls the wrong (first-tenant) API.
- **SWA CLI config discovery:** `swa deploy <folder>` searches the workspace and may pick up a *different* `staticwebapp.config.json` than the one in your folder. Confirm the "Found configuration file" line; harmless only when the configs are equivalent.

## 7 - Operating after the first provision

- **Change a plan/resource SKU IN PLACE.** App Service plan B1 to F1: `az appservice plan update -g <rg> -n <plan> --sku F1`. A full `az deployment sub create` re-runs every module (including `@secure()` params) and clobbers real app settings / connection strings with the **placeholder** values from the params file. Edit the Bicep SKU too so the next clean provision matches, but apply the live change with the CLI.
- **Keep real secrets out of the params file, and expect the push to need a human.** Use a sentinel like `PLACEHOLDER_SET_VIA_CLI_ONLY` in `*.parameters.json` and inject the real secret as an App Service app setting (or inline at deploy time). A secret-scanning auto-classifier may still **block `git push` on the placeholder** (false positive): verify the committed blob with `git show HEAD:infra/<file>.parameters.json`, then push from a context that can authorize it.
- **A .NET API with fail-fast config 503s with no logs when a required app setting is missing.** Set every key the app validates at startup (e.g. a JWT signing key >= 32 chars) before declaring success. Proof the app booted with valid config is a `401` on a protected endpoint, not a `503`/`ContainerTimeout`.

## Verification

```bash
# Workflows green
gh run list --limit 5

# Endpoints up (SWAs return 200; an API with no root route may 200 only on /scalar|/openapi)
curl -s -o /dev/null -w "%{http_code}\n" https://<swa-hostname>/

# SP roles (scope-based, avoids the cross-tenant Graph lookup)
az role assignment list --scope "/subscriptions/<sub>/resourceGroups/<rg>" \
  --query "[?principalId=='<sp oid>'].roleDefinitionName" -o tsv
```

## Common issues

| Symptom | Cause / Fix |
|---|---|
| `Conflict: Website with given name X already exists` | App Service global-name clash: rename the site, keep the azd key via the `azd-service-name` tag. |
| Second-tenant deploy fails `Website ... already exists` | Same clash against the first deployment: add an env suffix and update any client hard-coding the hostname. |
| Federated credential rejected / duplicate | FIC `name` must be `'<app uniqueName>/<fic name>'`; `subject` must match `repo:owner/repo:ref:refs/heads/<branch>` exactly. |
| `az role assignment create` -> `MissingSubscription` (guest) | Assign the role in Bicep; the deployment runs in the correct tenant ARM context. |
| `what-if` / `azd provision --preview` fails with Graph resources | Not supported for extensible resources: deploy without preview. |
| Workflow did not run after push | `paths:` filter did not match: trigger with `gh workflow run <file> --ref <branch>`. |
| `azure/login` AADSTS70021 (no matching federated credential) | Subject mismatch (branch/environment) or SP/FIC not yet replicated: re-check `subject`, retry. |
| App Service `503` / `ContainerTimeout` with no log output | Required fail-fast app setting missing (e.g. JWT signing key): set it. A healthy app returns `401` on protected routes. |
| `git push` blocked for a secret that is not actually committed | Secret-scanning false positive on a `PLACEHOLDER_*` value: verify `git show HEAD:<file>`, push from an authorized context. |
| Redeploy wiped the real signing key / connection string | Full `az deployment sub create` re-applied placeholder params: change SKUs/settings in place via CLI. |
