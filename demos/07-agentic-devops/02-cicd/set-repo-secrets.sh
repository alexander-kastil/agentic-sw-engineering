#!/usr/bin/env bash

repo="<your-github-org>/<your-repo-name>"
environment="production"

gh auth status

# A secret from a literal value
gh secret set API_KEY --repo $repo --body "<value>"

# A secret read from stdin, so the value never lands in shell history
echo -n "<value>" | gh secret set DB_PASSWORD --repo $repo

# A secret read from a file, for multi-line values such as certificates or keys
gh secret set SIGNING_KEY --repo $repo < ./signing-key.pem

# Every key in a dotenv file becomes one secret
gh secret set --repo $repo --env-file ./.env.ci

# An Azure service principal the azure/login action can consume
az ad sp create-for-rbac \
  --name "sp-gha-$RANDOM" \
  --role Contributor \
  --scopes /subscriptions/<your-subscription-id>/resourceGroups/rg-gha \
  --json-auth | gh secret set AZURE_CREDENTIALS --repo $repo

# Environment secrets apply only to jobs targeting that environment
gh secret set DEPLOY_TOKEN --repo $repo --env $environment --body "<value>"

# Variables hold non-sensitive configuration and stay readable after they are set
gh variable set AZURE_RESOURCE_GROUP --repo $repo --body "rg-gha"
gh variable set AZURE_LOCATION --repo $repo --body "westeurope"

# Dependabot needs its own copy; repository secrets are not visible to it
gh secret set NUGET_TOKEN --repo $repo --app dependabot --body "<value>"

gh secret list --repo $repo
gh secret list --repo $repo --env $environment
gh variable list --repo $repo

# Removing a secret takes effect on the next run, not on runs already in flight
gh secret delete API_KEY --repo $repo
