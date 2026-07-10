---
name: azure-deploy/acr
description: Build Docker images for each service defined in deploy.json and push them to Azure Container Registry. Generates GitHub Actions workflow for CI. Keywords: acr, azure container registry, docker build, docker push, github actions, container image, build pipeline.
license: CC-BY-NC-SA-4.0
---

# ACR — Build and Push Container Images

Builds a Docker image for each service listed in `.claude/skills/azure-deploy/deploy.json` and pushes to Azure Container Registry.

### Read Configuration

```bash
cfg=.claude/skills/azure-deploy/deploy.json
ACR=$(jq -r '.ACR' $cfg)
RG=$(jq -r '.ResourceGroup' $cfg)
```

### Login to ACR

```bash
az acr login --name $ACR
```

### Build and Push — All Services

Iterates over the `Services` array in `deploy.json`:

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

Replace `$SHA` with `$(git rev-parse --short HEAD)` locally or `${{ github.sha }}` in GitHub Actions.

### GitHub Actions Workflow

Place in `.github/workflows/build.yml`. Triggers on changes to any service source path:

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

### Verify Push

```bash
az acr repository list --name $ACR -o table
az acr repository show-tags --name $ACR --repository <service-name> -o table
```

### Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `unauthorized: authentication required` | Not logged in to ACR | Run `az acr login --name $ACR` |
| `denied: requested access to the resource is denied` | WIF identity missing AcrPush | Run `az role assignment create --role AcrPush` (see wif subskill) |
| `dockerfile not found` | Wrong `Source` or `Dockerfile` path in deploy.json | Verify paths in deploy.json match the actual repo layout |
