# Declarative Templates: Worked Solution

The finished templates for the guide in [../readme.md](../readme.md), for the food-app in [`src/food-app`](../../../../../src/food-app/). Build the files yourself as you read the guide; open these when a step misbehaves.

Verified with Bicep CLI 0.44.1, Terraform 1.14.5, and the azurerm provider 4.x.

## What is Here

| Path | Contents |
|------|----------|
| `azure.yaml` | The azd service map: catalog-service as a container app, food-shop as a static web app. |
| `infra/` | The Bicep variant, which is what azd uses when no provider is set. Subscription-scoped `main.bicep` creating the resource group, one module for everything inside it. |
| `infra-terraform/` | The Terraform variant covering the food-shop frontend, matching the narrower scope the guide's Terraform prompt asks for. |

To run the Terraform variant through azd, rename `infra-terraform/` to `infra/` and add the provider setting to `azure.yaml`:

```yaml
infra:
  provider: terraform
```

## Validating Without Deploying

Neither command needs a subscription, a login, or a state backend.

```bash
az bicep build --file infra/main.bicep
```

```bash
cd infra-terraform
terraform init -backend=false
terraform validate
terraform fmt -check
```

Both pass as checked in. The container image in `resources.bicep` is the Microsoft hello-world sample, which is what azd replaces on the first `azd deploy` once the service has been built and pushed.
