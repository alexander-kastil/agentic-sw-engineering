import asyncio
import random
import sys

from copilot import CopilotClient, define_tool
from copilot.session_events import AssistantMessageDeltaData
from pydantic import BaseModel, Field


class GetWeatherParams(BaseModel):
    city: str = Field(description="The city name")


@define_tool("get_weather", description="Get the current weather for a city", skip_permission=True)
async def get_weather(params: GetWeatherParams) -> dict:
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    temp = random.randint(50, 79)
    condition = random.choice(conditions)
    return {"city": params.city, "temperature": f"{temp}°F", "condition": condition}


def on_event(event):
    match event.data:
        case AssistantMessageDeltaData() as data:
            print(data.delta_content, end="", flush=True)


async def main():
    client = CopilotClient()
    session = await client.create_session(
        model="gpt-5-mini",
        streaming=True,
        tools=[get_weather],
    )

    session.on(on_event)

    print("Weather Assistant (type 'exit' to quit)")
    print("Try: 'What's the weather in Paris and London?'\n")

    while True:
        print("You: ", end="", flush=True)
        line = await asyncio.to_thread(sys.stdin.readline)
        if not line:
            break
        user_input = line.strip()
        if user_input.lower() == "exit":
            break
        if user_input:
            print("Assistant: ", end="", flush=True)
            await session.send_and_wait(user_input)
            print("\n")

    await client.stop()


asyncio.run(main())
