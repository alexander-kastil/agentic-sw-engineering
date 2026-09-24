# Cost, AI Credits & Bring Your Own Key


GitHub Copilot bills usage as AI credits, so every interaction draws down a credit balance rather than sitting inside a flat monthly allowance. The credit cost of a turn is a function of four things: the input tokens you send, the output tokens the model returns, the cached tokens it can reuse, and the model you picked. The first three grow with the size of your context and the length of the answer, which is why a tight prompt against a focused workspace is cheaper than a sprawling one. The fourth, model choice, is the largest lever an architect controls, because a premium model can cost several times what a lighter model costs for the same task.

The tooling makes cost visible at the moment you make a decision. The model picker lists a per-model Cost (Credits per 1M Tokens) block broken out into input, output, cache read, and cache write, so choosing a model is a budget decision at the point of choice. Read this topic alongside the [Models topic in Fundamentals](../../01-fundamentals/02-models/), where model capabilities and context sizes are covered in depth.

Three readouts close the loop while and after the work runs. Session Info shows the running Session Cost next to a context-window breakdown, the Response details hover on a chat response shows that turn's model with its input, cached input, and output token counts, and the Copilot status menu shows credits used against your allowance for the billing cycle. Subagent credit cost is the one number that is off until you ask for it, because `chat.subagents.showCreditUsage` defaults to `false`.

## What consumes credits

| Cost driver | What it is |
|-------------|------------|
| Input tokens | The prompt and context you send to the model |
| Output tokens | The tokens the model generates in its response |
| Cache read tokens | Reused context, billed at the model's cache-read rate |
| Cache write tokens | Context written into the cache for the next request |
| Model choice | The per-model rate; a premium model costs more per token |

## Where cost surfaces

| Surface | What it shows |
|---------|---------------|
| Model picker | Cost (Credits per 1M Tokens) per model: input, output, cache read, cache write |
| Session Info | Session Cost and the context-window breakdown for the running session |
| Response details hover | Model, input tokens, cached input tokens, and output tokens for one response |
| Copilot status menu | Credits used against the allowance for the current billing cycle |
| Subagent duration label | Per-subagent credit usage, once `chat.subagents.showCreditUsage` is `true` |

```mermaid
flowchart LR
    A["Input tokens"] --> D["Credit cost<br/>of a turn"]
    B["Output tokens"] --> D
    C["Cached tokens"] --> D
    M["Model rate"] --> D
```

## Model choice as a budget decision

Because cost scales with the model's per-token rate, the cheapest way to control spend is to match the model to the task rather than reaching for the strongest model by reflex. A routine refactor, a doc pass, or a read-only research query rarely needs a premium model, while a hard architecture problem may justify one. Making that call once, at the model picker, is far cheaper than discovering the pattern later in Session Info. When you delegate to subagents, turn on `chat.subagents.showCreditUsage` first, so a fan-out of specialists stays attributable instead of disappearing into the session total.

> Note: Caching is the driver you can influence without changing models. A stable prefix, meaning the same instructions and the same early context reused turn after turn, keeps cache reads high; reordering or rewriting earlier turns invalidates the cache and pushes those tokens back to full input rate.

## Bring your own key

Bring your own key (BYOK) is the other lever on cost, and it changes who bills the tokens. A model registered under your own API key is billed directly by that provider and does not count against Copilot AI credits. The data path changes with it: prompts go to the provider you contracted with, which matters as much to data protection as to the budget. That makes BYOK a routing decision: a cheap open model on DeepSeek or DeepInfra for routine turns, a company Azure OpenAI or Microsoft Foundry deployment for regulated work, a local Ollama model for offline work, and the Copilot-hosted frontier models for the hard problems.

BYOK comes in two scopes. Local BYOK is set up on one machine, keeps the key on the client, and works on any plan or none. Enterprise BYOK (public preview) is configured by an enterprise or organization admin under **AI controls**, and the models then appear in every member's model picker under the enterprise or organization name. Business and Enterprise admins can also switch local BYOK in VS Code off with the "Bring Your Own Language Model Key in VS Code" policy, which is on by default.

```mermaid
flowchart LR
    A["VS Code, CLI<br/>or Copilot app"] --> B{"Model<br/>picked"}
    B -->|"Copilot-hosted"| C["GitHub Copilot<br/>AI credits"]
    B -->|"Your key"| D["DeepSeek<br/>api.deepseek.com"]
    B -->|"Your key"| E["DeepInfra<br/>api.deepinfra.com"]
    B -->|"Your key"| F["Azure OpenAI, Foundry<br/>Anthropic, Ollama"]
```

Each surface is configured on its own and shares nothing with the others, so pick the guide for the surface you work on:

| Topic | Description |
|-------|-------------|
| [Bring Your Own Key in VS Code](./01-byok-vscode/) | Add DeepSeek and DeepInfra models to the Copilot Chat model picker with the native flow or the OAI Compatible Copilot extension. |
| [Bring Your Own Key in the Copilot CLI](./02-byok-copilot-cli/) | Point the GitHub Copilot CLI at DeepSeek or DeepInfra with the native `COPILOT_PROVIDER_*` environment variables. |
| [Bring Your Own Key in the GitHub Copilot App](./03-byok-copilot-app/) | Register DeepSeek and DeepInfra as model providers in the desktop app, including a thinking variant of the same model. |

- Cost: open and third-party models are priced far below the frontier tier, and their tokens never touch the credit balance.
- Context: several of these models carry very large context windows, useful for whole-repository questions.
- Diversity: keep a fast cheap model, a reasoning model, and a frontier model side by side and switch per task.
- Data control: a DeepInfra call is a third-country transfer, so read [EU AI Act, GDPR & Accessibility Compliance](../04-compliance/) before sending personal data.

## Demo

Compare model cost and track spend inside one session.

1. In VS Code, open the model picker in Copilot Chat and read the Cost (Credits per 1M Tokens) block for two or three models. Note the gap between a lighter model and a premium one.
2. Pick a lighter model and ask the agent to complete a small, well-scoped task such as documenting one function.
3. Open Session Info and read the Session Cost and the context-window breakdown the turn produced.
4. Repeat the same task in a new session with a premium model. Compare the two Session Cost readings to see the rate difference in practice.
5. Set `chat.subagents.showCreditUsage` to `true`, delegate a follow-up to a subagent, and read the credit usage now shown next to its duration.
6. Hover a response and open Response details. Compare a first turn against a follow-up in the same session to see cached input tokens take effect.
7. Open the Copilot status menu and read credits used for the current billing cycle.
8. Pick one of the three BYOK guides, register a cheap open model, and run the task from step 2 on it. Confirm the credits used in the status menu did not move.
9. Decide which model you would set as the team default for routine work, and which work goes to your own key, and record the reasoning as a cost policy.

## Links & Resources

- [GitHub Copilot billing and usage](https://docs.github.com/en/copilot/concepts/billing) - how Copilot usage is metered and billed across plans
- [AI language models in VS Code](https://code.visualstudio.com/docs/copilot/customization/language-models) - the model picker, auto model selection, and per-model configuration
- [About bring your own key](https://docs.github.com/en/copilot/concepts/models/bring-your-own-key) - local versus enterprise BYOK, supported providers, and billing
- [Enable custom models for your enterprise](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/enable-custom-models) - admin-configured BYOK models for every member

[← Previous: Trust, Safety & the Permission Model](../01-permissions/readme.md) | [Back to Governance](../readme.md) | [Next: Enterprise Control of the Harness →](../03-enterprise-control/readme.md)
