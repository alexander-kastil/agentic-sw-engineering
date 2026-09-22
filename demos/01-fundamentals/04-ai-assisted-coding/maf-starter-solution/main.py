import asyncio
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv


async def main() -> None:
    load_dotenv()
    project_endpoint = os.getenv("AZURE_PROJECT_ENDPOINT")
    model_deployment = os.getenv("AZURE_MODEL_DEPLOYMENT")

    if not project_endpoint or not model_deployment:
        print("Set AZURE_PROJECT_ENDPOINT and AZURE_MODEL_DEPLOYMENT in .env before running.")
        return

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

    result = await agent.run("tell me about the microsoft agent framework")
    print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
