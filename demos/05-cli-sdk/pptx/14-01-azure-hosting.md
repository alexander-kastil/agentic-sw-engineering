---
slide: "14-01"
topic: 02-sdk/04-deploy-azure
title: "Hosting an SDK agent on Azure"
subtitle: "Your HTTP server, a token from Key Vault"
layout: diagram
visual-weight: 1/2
visual-type: photo
media-source: opus-svg
media-file: demos/05-cli-sdk/pptx/images/14-01-azure-hosting.svg
visual-prompt: >
  Opus 5.5, hand-written SVG, viewBox 0 0 1920 1080, white background, Segoe UI, visual language of
  assets/agentic-harness-architecture.svg and the module 02 diagrams. No heading inside the image. Minimum
  26px type. A dashed grey frame "Azure Container Apps" holding green "Your HTTP server" (/health, /ask),
  blue "CopilotClient" (sessions + tools) and purple "Copilot CLI runtime" (bundled or external) in a row.
  A white "Client" (POST /ask) outside on the left, a grey "Model" (Copilot-hosted or your provider)
  outside on the right. An amber "Key Vault" box below with COPILOT_GITHUB_TOKEN and an arrow labelled
  secret up into the runtime. Caption under the server: no hosting library: you write it.
order: 19
source: demos/05-cli-sdk/02-sdk/04-deploy-azure/readme.md
gamma_prompt: >
  Slide titled "Hosting an SDK agent on Azure". Left: four bullets. Right, wider: the provided hosting
  diagram. Use exactly the one image given for this card; do not generate or add any other images, icons
  or logos.
---

# Hosting an SDK agent on Azure

## Content

- **No hosting library**: you write the HTTP server, the routes and the health check
- **Bundled** runtime per container, or **external** `copilot --headless --port 4321`
- No `/login` in a container: `COPILOT_GITHUB_TOKEN` as a Key Vault secret
- A `provider` block swaps in Azure OpenAI or Foundry; the agent code does not change

## Notes

sendAndWait defaults to 60 seconds. Line the platform timeouts up behind a longer one, or a slow agent looks like a broken one.
