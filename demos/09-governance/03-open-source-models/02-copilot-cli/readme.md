# Using Open-Source Models in the Copilot CLI

The GitHub Copilot CLI has its own bring-your-own-key path, separate from the VS Code extension. It is native GitHub functionality configured entirely through environment variables, so the same DeepSeek and DeepInfra endpoints you use in Chat can also drive the terminal agent. The `oaicopilot.*` VS Code settings do not apply here; the CLI reads only the `COPILOT_PROVIDER_*` variables below.

## Environment variables

| Variable | Required | Meaning |
|----------|----------|---------|
| `COPILOT_PROVIDER_BASE_URL` | Yes | The provider's API endpoint |
| `COPILOT_MODEL` | Yes | The model id (also settable with the `--model` flag) |
| `COPILOT_PROVIDER_TYPE` | No | `openai` (default), `azure`, or `anthropic` |
| `COPILOT_PROVIDER_API_KEY` | No | Your key for the provider (omit for unauthenticated local models) |
| `COPILOT_PROVIDER_MAX_PROMPT_TOKENS` | No | Prompt-token cap for a model the CLI does not know |
| `COPILOT_PROVIDER_MAX_OUTPUT_TOKENS` | No | Output-token cap for a model the CLI does not know |

The `openai` provider type covers OpenAI, Ollama, vLLM, Foundry Local, and any other OpenAI Chat Completions-compatible endpoint. The chosen model must support tool calling and streaming, or the CLI errors out, and a context window of at least 128k tokens is recommended.

## DeepSeek

DeepSeek's own integration guidance uses the Anthropic-compatible path for the CLI, because the plain `openai` path returns a 400 for DeepSeek. Set the provider type to `anthropic` and point at the `/anthropic` base URL.

```powershell
$env:COPILOT_PROVIDER_TYPE = "anthropic"
$env:COPILOT_PROVIDER_BASE_URL = "https://api.deepseek.com/anthropic"
$env:COPILOT_PROVIDER_API_KEY = "<your-deepseek-api-key>"
$env:COPILOT_MODEL = "deepseek-v4-flash"
copilot
```

## DeepInfra

DeepInfra exposes an OpenAI-compatible endpoint, so it uses the default `openai` provider type with the DeepInfra base URL and a model id from its catalog. Choose a model that supports tool calling and streaming.

```powershell
$env:COPILOT_PROVIDER_TYPE = "openai"
$env:COPILOT_PROVIDER_BASE_URL = "https://api.deepinfra.com/v1/openai"
$env:COPILOT_PROVIDER_API_KEY = "<your-deepinfra-api-key>"
$env:COPILOT_MODEL = "Qwen/Qwen3.6-35B-A3B"
copilot --model "Qwen/Qwen3.6-35B-A3B"
```

> Note: The DeepInfra combination is not called out in the official CLI docs. Verify your chosen model supports tool calling and streaming before relying on it, and fall back to a known-good model if the CLI reports an unsupported-capability error.

## Benefits and caveats

- The same cost saving as in Chat applies to terminal and scripted agent runs, which is where long automated jobs can burn the most credits.
- Keys live in your shell environment: set them per session or through a secret manager, never hard-coded in a committed script.
- Not every provider maps cleanly; the CLI supports only `openai`, `azure`, and `anthropic` provider types, with no interactive model picker, so you select the model through `COPILOT_MODEL` or `--model`.

## Links & Resources

- [Use BYOK models in the Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models) - the official `COPILOT_PROVIDER_*` variables, provider types, and model requirements
- [DeepSeek Copilot CLI integration](https://api-docs.deepseek.com/quick_start/agent_integrations/copilot_cli/) - the Anthropic-path base URL and model ids for DeepSeek
- [DeepInfra documentation](https://deepinfra.com/docs) - the OpenAI-compatible endpoint and hosted model catalog
