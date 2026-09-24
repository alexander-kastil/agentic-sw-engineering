import asyncio
import random
from datetime import datetime, timezone

from copilot import CopilotClient, define_tool
from copilot.session_events import AssistantMessageDeltaData, SessionIdleData
from pydantic import BaseModel, Field


class GetWeatherParams(BaseModel):
    city: str = Field(description="The city name to get weather for")


@define_tool("get_weather", description="Get the current weather for a city", skip_permission=True)
async def get_weather(params: GetWeatherParams) -> dict:
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    temp = random.randint(50, 79)
    condition = random.choice(conditions)

    return {
        "city": params.city,
        "temperature": f"{temp}°F",
        "condition": condition,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def on_event(event):
    match event.data:
        case AssistantMessageDeltaData() as data:
            print(data.delta_content, end="", flush=True)
        case SessionIdleData():
            print("\n")


async def main():
    client = CopilotClient()
    session = await client.create_session(
        model="gpt-5-mini",
        streaming=True,
        tools=[get_weather],
    )

    session.on(on_event)

    await session.send_and_wait(
        "What's the weather like in Seattle and Tokyo? Give me the temperatures."
    )

    await client.stop()


asyncio.run(main())
