---
name: maf-update
description: Migrate outdated Microsoft Agent Framework Python samples to the GA v1+ API. Use when an existing MAF Python project uses the old package (agent-framework-azure-ai), AzureAIClient, async context managers for client/agent, azure.identity.aio credential, result.text access pattern, or missing AZURE_ env var prefix. Produces an updated requirements.txt, main.py, and .env template aligned to the GA agent-framework package.
---

# maf-update — Migrate MAF Python Samples to GA v1+

Parent skill: [maf-skill](../SKILL.md) — consult for authoritative package and API rules.

> Always fetch the latest patterns from [Microsoft Learn](https://learn.microsoft.com/agent-framework/get-started/your-first-agent) before applying changes. MAF evolves rapidly; do not rely on cached knowledge.

## When to Use This Skill

- A project has `agent-framework-azure-ai` in `requirements.txt`
- Imports reference `agent_framework.azure.AzureAIClient`
- Credential is `azure.identity.aio.AzureCliCredential` (async variant)
- Agent/client are set up inside `async with` context managers
- Result is accessed as `result.text` instead of `result`
- Env vars are named `PROJECT_ENDPOINT` / `MODEL_DEPLOYMENT` (missing `AZURE_` prefix)

## Step-by-Step Migration Workflow

### 1. Audit the project

Check these files:

- `requirements.txt` — look for `agent-framework-azure-ai`
- `main.py` (or entry point) — look for old imports and patterns
- `.env` / `.env copy` — look for missing `AZURE_` prefix on var names

### 2. Update `requirements.txt`

| Old | New |
|-----|-----|
| `agent-framework-azure-ai` | `agent-framework` |

Keep `azure-identity` and `python-dotenv` unchanged.

### 3. Update imports in `main.py`

| Old import | New import |
|-----------|-----------|
| `from agent_framework.azure import AzureAIClient` | `from agent_framework import Agent` |
| *(no Agent import)* | `from agent_framework.foundry import FoundryChatClient` |
| `from azure.identity.aio import AzureCliCredential` | `from azure.identity import AzureCliCredential` |

### 4. Replace the client/agent setup

**Old pattern (pre-GA):**

```python
async with (
    AzureCliCredential() as credential,
    AzureAIClient(
        project_endpoint=project_endpoint,
        model_deployment_name=model_deployment,
        credential=credential,
    ).as_agent(
        name="HelloAgent",
        instructions="You are a helpful assistant.",
    ) as agent,
):
    result = await agent.run("...")
    print(result.text)
```

**New pattern (GA v1+):**

```python
client = FoundryChatClient(
    project_endpoint=project_endpoint,
    model=model_deployment,
    credential=AzureCliCredential(),
)
agent = Agent(
    client=client,
    name="HelloAgent",
    instructions="You are a helpful assistant.",
)
result = await agent.run("...")
print(f"Agent: {result}")
```

Key differences:
- No `async with` — `FoundryChatClient` and `Agent` are plain objects
- Credential is created inline, not as a context manager
- `model_deployment_name=` → `model=`
- `result` is a `str` — no `.text` attribute
- `.as_agent(...)` method does not exist in v1+

### 5. Update env var names

| Old name | New name |
|----------|----------|
| `PROJECT_ENDPOINT` | `AZURE_PROJECT_ENDPOINT` |
| `MODEL_DEPLOYMENT` | `AZURE_MODEL_DEPLOYMENT` |

Update both the `.env` file **and** all `os.getenv(...)` calls in Python code.

Also update any `.env copy` / `.env.example` template files.

### 6. Verify the error message string

If the code has a guard print like `"Set PROJECT_ENDPOINT and MODEL_DEPLOYMENT..."`, update it to reference the new var names.

## Completion Checklist

- [ ] `requirements.txt` uses `agent-framework` (not `agent-framework-azure-ai`)
- [ ] No `async with` wrapping client or agent
- [ ] Credential is `azure.identity.AzureCliCredential` (sync)
- [ ] `FoundryChatClient` uses `model=` (not `model_deployment_name=`)
- [ ] `result` is printed directly, not as `result.text`
- [ ] All env vars use `AZURE_` prefix in both `.env` files and `os.getenv()` calls
- [ ] `load_dotenv()` is called before any `os.getenv()`

## References

- [maf-skill](../SKILL.md) — GA v1+ package rules and canonical patterns
- [MAF Get Started](https://learn.microsoft.com/agent-framework/get-started/your-first-agent)
- [Python samples](https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/01_hello_agent.py)
