# Using Open-Source Models in VS Code

The [OAI Compatible Copilot](https://marketplace.visualstudio.com/items?itemName=johnny-zhao.oai-compatible-copilot) extension registers your own OpenAI-compatible models through the VS Code Language Model Chat Provider API, so they appear under a provider named `OAI Compatible` in the model picker. Point it at DeepSeek and DeepInfra to run routine agent work on cheap open models while keeping the frontier models for the hard problems. It contributes a chat provider only, so inline ghost-text completions stay on Copilot's own models.

## What the native picker covers first

Reach for the extension when your endpoint is genuinely arbitrary, not before. VS Code has its own bring-your-own-key path: open the model picker, choose `Manage Models`, then `Add Models`, and register a provider with your API key. Two agent-host settings decide how far that reaches, and both are off by default: `chat.agentHost.byokModels.enabled` lets extension-provided BYOK models run in Agents-window sessions, and `chat.agentHost.allowSignedOutWhenUsable` opens the Agents window without forcing GitHub sign-in when the selected agent works on your own credentials.

What the native path does not cover is the arbitrary OpenAI-compatible endpoint, which is exactly the DeepSeek plus DeepInfra case below. That is the gap this extension fills.

## Setup

1. Install the extension `johnny-zhao.oai-compatible-copilot` from the Marketplace.
2. Set your API key with the Command Palette command `OAICopilot: Set OAI Compatible Apikey`, or `OAICopilot: Set OAI Compatible Multi-Provider Apikey` when you run more than one provider. Keys entered this way live in VS Code secret storage; the extension contributes no setting that holds a key.
3. Declare a default endpoint and your models in `settings.json`, or open `OAICopilot: Open Configuration UI` and fill the same values in a form. The default `oaicopilot.baseUrl` applies to every model, and any model can override it with its own `baseUrl`, which is what makes the mixed DeepSeek plus DeepInfra setup work.
4. Open the model picker, choose `Manage Models`, select the `OAI Compatible` provider, and enable the models you configured.

```json
{
  "oaicopilot.baseUrl": "https://api.deepseek.com",
  "oaicopilot.models": [
    {
      "id": "deepseek-v4-flash",
      "owned_by": "deepseek",
      "displayName": "DeepSeek V4 Flash",
      "context_length": 1000000,
      "max_tokens": 32768,
      "temperature": 0
    },
    {
      "id": "deepseek-v4-pro",
      "owned_by": "deepseek",
      "displayName": "DeepSeek V4 Pro",
      "context_length": 1000000,
      "max_tokens": 8192,
      "temperature": 0
    },
    {
      "id": "Qwen/Qwen3.6-35B-A3B",
      "owned_by": "deepinfra",
      "baseUrl": "https://api.deepinfra.com/v1",
      "displayName": "Qwen3.6 35B A3B",
      "context_length": 131072,
      "max_tokens": 8192,
      "temperature": 0
    }
  ]
}
```

> Note: Never paste a real API key into `settings.json`, which is committed or synced on most machines. Use the `OAICopilot: Set ...` commands so the key stays in secret storage, and keep only non-secret model definitions in settings.

## Usage

Once the models are enabled, pick one from the model picker and work as usual: ask, edit, and agent turns all route to the selected endpoint. Reserve a frontier model for architecture, tricky debugging, and large refactors, and drop to a cheap open model for routine turns. Two per-model options are worth knowing: `useForCommitGeneration: true` routes commit-message generation to that model, and a `configId` plus an `extra` block lets you register the same model id twice with different request bodies, which is how a thinking and a non-thinking variant sit side by side in the picker.

## Benefits and trade-offs

- Cost: open and third-party models are priced far below the frontier tier, which is the single largest saving on usage-based credits.
- Context: several of these models carry very large context windows, useful for whole-repository questions.
- Diversity: keep a fast cheap model, a reasoning model, and a frontier model side by side and switch per task.
- Data control: a DeepInfra call is a third-country transfer, so read [EU AI Act, GDPR & Accessibility Compliance](../../06-compliance/) before sending personal data.

## Demo

Configure a cheap open model and measure the difference.

1. Install the extension and set your API key with the `OAICopilot: Set ...` command.
2. Add one DeepSeek model and one DeepInfra model to `oaicopilot.models`, using a per-model `baseUrl` for the DeepInfra entry.
3. Run `Manage Models`, enable both under the `OAI Compatible` provider, and confirm they appear in the picker.
4. Run the same routine task (explain a file, generate a test) once on a frontier model and once on the cheap model, and compare the result quality.
5. Add a second entry for one model with a `configId` and an `extra` block, and confirm both variants show up separately.
6. Note which everyday tasks are good enough on the cheap model, and write down your own frontier-versus-cheap routing rule.

## Links & Resources

- [OAI Compatible Copilot on the Marketplace](https://marketplace.visualstudio.com/items?itemName=johnny-zhao.oai-compatible-copilot) - the extension, its settings keys, and the provider it registers
- [AI language models in VS Code](https://code.visualstudio.com/docs/copilot/customization/language-models) - the model picker, Manage Models, and the native bring-your-own-key flow
- [DeepSeek API documentation](https://api-docs.deepseek.com/) - base URLs, model ids, and pricing for the DeepSeek endpoint
- [DeepInfra documentation](https://deepinfra.com/docs) - the OpenAI-compatible endpoint and the catalog of hosted open models
