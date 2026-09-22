# Build and push images to Azure Container Registry

Build a Docker image per service listed in `.claude/skills/azure-deploy/deploy.json`, push to ACR. Deploy step: [deploy-aca.md](deploy-aca.md).

## Read config

```bash
cfg=.claude/skills/azure-deploy/deploy.json
ACR=$(jq -r '.ACR' $cfg)
RG=$(jq -r '.ResourceGroup' $cfg)
```

## Login

```bash
az acr login --name $ACR
```

## Build and push all services

Iterates the `Services` array in `deploy.json`.

```bash
jq -c '.Services[]' $cfg | while read svc; do
    name=$(echo $svc | jq -r '.Name')
    source=$(echo $svc | jq -r '.Source')
    df=$(echo $svc | jq -r '.Dockerfile')

    docker build \
        -f $source/$df \
        -t $ACR.azurecr.io/$name:$SHA \
        -t $ACR.azurecr.io/$name:latest \
        $source

    docker push $ACR.azurecr.io/$name --all-tags
done
```

`$SHA`: `$(git rev-parse --short HEAD)` locally, `${{ github.sha }}` in GitHub Actions.

## GitHub Actions workflow

`.github/workflows/build.yml`. Triggers on push to `main`. Secrets hold real values (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`); OIDC setup: [oidc-github-actions.md](oidc-github-actions.md).

```yaml
name: Build and Push Images

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: ${{ fromJson(needs.config.outputs.services) }}
    needs: config

    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Build and Push
        run: |
          ACR=$(jq -r '.ACR' .claude/skills/azure-deploy/deploy.json)
          az acr login --name $ACR
          docker build \
            -f ${{ matrix.service.Source }}/${{ matrix.service.Dockerfile }} \
            -t $ACR.azurecr.io/${{ matrix.service.Name }}:${{ github.sha }} \
            -t $ACR.azurecr.io/${{ matrix.service.Name }}:latest \
            ${{ matrix.service.Source }}
          docker push $ACR.azurecr.io/${{ matrix.service.Name }} --all-tags

  config:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.read.outputs.services }}
    steps:
      - uses: actions/checkout@v4
      - id: read
        run: |
          services=$(jq -c '.Services' .claude/skills/azure-deploy/deploy.json)
          echo "services=$services" >> $GITHUB_OUTPUT
```

## Verify push

```bash
az acr repository list --name $ACR -o table
az acr repository show-tags --name $ACR --repository <service-name> -o table
```

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `unauthorized: authentication required` | Not logged in to ACR | `az acr login --name $ACR` |
| `denied: requested access to the resource is denied` | WIF identity missing AcrPush | `az role assignment create --role AcrPush` ([oidc-github-actions.md](oidc-github-actions.md)) |
| `dockerfile not found` | Wrong `Source` or `Dockerfile` path in deploy.json | Verify paths match actual repo layout |
