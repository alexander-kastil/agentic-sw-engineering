import asyncio
import os
from typing import Annotated
from pydantic import Field
from dotenv import load_dotenv

from agent_framework.azure import AzureOpenAIChatClient

# Load environment variables
load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-01-preview")


# Define calculator function
def calculate(
    expression: Annotated[str, Field(description="Mathematical expression to evaluate, e.g. '2 + 2' or '10 * 5'")]
) -> str:
    """Evaluate a mathematical expression."""
    try:
        # Safe evaluation with limited namespace
        result = eval(
            expression,
            {"__builtins__": {}},
            {
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum,
                "pow": pow,
            }
        )
        return f"Result: {result}"
    except Exception as e:
        return f"Error: Could not calculate '{expression}'"


async def test_calculation():
    """Test the calculator with a specific example."""
    
    # Create agent with calculator tool
    agent = AzureOpenAIChatClient(
        endpoint=ENDPOINT,
        deployment_name=DEPLOYMENT,
        api_key=API_KEY,
        api_version=API_VERSION
    ).create_agent(
        instructions="You are a math assistant. Use the calculate tool for math problems.",
        name="CalculatorBot",
        tools=[calculate]
    )
    
    user_input = "55*12"
    print(f"You: {user_input}")
    print("Agent: ", end="", flush=True)
    
    async for chunk in agent.run_stream(user_input):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(test_calculation())
