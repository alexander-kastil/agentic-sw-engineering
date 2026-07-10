---
name: maf-skill
description: Microsoft Agent Framework (MAF) Python reference. Use when creating, configuring, or explaining MAF Python agents, selecting the correct packages, understanding the FoundryChatClient/Agent API, managing credentials with AzureCliCredential, or setting up Azure AI Foundry projects. Covers GA v1+ patterns, package names, imports, env vars, and key rules. Subskills available: maf-update (for migrating outdated MAF samples).
---

# Microsoft Agent Framework — Python Reference

> **MAF evolves rapidly.** Always consult the [Microsoft Learn MCP docs](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview) before implementing or reviewing code. Never rely on cached internal knowledge of MAF APIs.

## Package

```bash
pip install agent-framework
```

`requirements.txt` entry:

```
agent-framework
azure-identity
python-dotenv
```

Do **not** use `agent-framework-azure-ai` — that is the old pre-GA package name.

## Canonical Imports

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential   # sync, NOT azure.identity.aio
from dotenv import load_dotenv
```

## Agent Setup Pattern

```python
import asyncio
import os
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

async def main() -> None:
    load_dotenv()  # MAF does NOT auto-load .env

    client = FoundryChatClient(
        project_endpoint=os.getenv("AZURE_PROJECT_ENDPOINT"),
        model=os.getenv("AZURE_MODEL_DEPLOYMENT"),
        credential=AzureCliCredential(),
    )
    agent = Agent(
        client=client,
        name="MyAgent",
        instructions="You are a helpful assistant.",
    )

    result = await agent.run("Hello")
    print(f"Agent: {result}")   # result is a plain string

if __name__ == "__main__":
    asyncio.run(main())
```

## Key Rules

| Rule | Detail |
|------|--------|
| Package | `agent-framework` (not `agent-framework-azure-ai`) |
| Credential | `azure.identity.AzureCliCredential` (sync) — not the `.aio` variant |
| Context manager | Do **not** use async context managers (`async with`) for client or agent |
| `load_dotenv()` | Must be called explicitly — MAF never auto-loads `.env` |
| `agent.run()` result | Returns a plain `str` — no `.text` attribute |
| Env var prefix | Always use `AZURE_` prefix: `AZURE_PROJECT_ENDPOINT`, `AZURE_MODEL_DEPLOYMENT` |
| Model default | Use `gpt-4o-mini` as the default model unless otherwise specified |
| Auth in production | Prefer `ManagedIdentityCredential` over `AzureCliCredential` for deployed workloads |

## Environment Variables

```env
AZURE_PROJECT_ENDPOINT=https://<project>.services.ai.azure.com/api/projects/<name>
AZURE_MODEL_DEPLOYMENT=gpt-4o-mini
```

## Streaming

```python
print("Agent: ", end="", flush=True)
async for chunk in agent.run("Tell me a fun fact.", stream=True):
    if chunk.text:
        print(chunk.text, end="", flush=True)
print()
```

## References

- [MAF Overview](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)
- [Your First Agent](https://learn.microsoft.com/agent-framework/get-started/your-first-agent)
- [Python samples repo](https://github.com/microsoft/agent-framework/tree/main/python/samples)
- [maf-update subskill](./maf-update/SKILL.md) — use to migrate outdated MAF samples to GA v1+
