import asyncio
import os

from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv


async def main() -> None:
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")

    if not project_endpoint or not model_deployment:
        print("Set PROJECT_ENDPOINT and MODEL_DEPLOYMENT in .env before running.")
        return

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
        result = await agent.run("tell me about the microsoft agent framework")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
