import asyncio
import json
from pathlib import Path

from copilot import CopilotClient


async def main() -> None:
    config = json.loads((Path(__file__).parent / "appsettings.json").read_text())
    model = config.get("model", "gpt-5-mini")
    prompt = config.get("prompt", "What are the use cases for Copilot SDK?")

    print(f"Model: {model}")
    print(f"Prompt: {prompt}")
    print("-" * 60)

    async with CopilotClient() as client:
        async with await client.create_session(model=model) as session:
            response = await session.send_and_wait(prompt)

            if response and response.data and response.data.content:
                print("\nResponse:")
                print(response.data.content)
            else:
                print("No response received.")


asyncio.run(main())
