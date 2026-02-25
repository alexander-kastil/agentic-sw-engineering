---
description: General instructions for Azure CLI usage in this repository
---

The preferred usage of Azure CLI is in combination with Bash scripts for automation tasks.

- Use camelCase variable names for environment, resource group, location, and resource identifiers.
- Compose resource names using variable interpolation (e.g., az400-$env, $acr.azurecr.io/prime-service). But make sure they are valid. For example storage account names must be lowercase and between 3-24 characters with no special characters.
- Always declare variables at the top for easy modification and reuse.
- Use az CLI commands in logical order: resource group, extension, resource creation.
- Use $(...) for command substitution to capture output into variables.
- Prefer explicit resource names and parameters for clarity and repeatability.
- No comments, no error handling, and no extra documentation—just concise, functional script steps.
