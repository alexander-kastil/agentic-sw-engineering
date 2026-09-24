import asyncio
import os

from copilot import CopilotClient, PermissionHandler, SessionEvent, SessionEventType
from copilot.rpc import FleetStartRequest

MODEL = "gpt-5-mini"


async def main():
    client = CopilotClient()
    await client.start()
    session = await client.create_session(
        model=MODEL,
        streaming=False,
        working_directory=os.getcwd(),
        on_permission_request=PermissionHandler.approve_all,
    )

    def on_event(event: SessionEvent):
        if event.type == SessionEventType.ASSISTANT_MESSAGE:
            print(f"\n--- assistant ---\n{event.data.content}")

    session.on(on_event)

    result = await session.rpc.fleet.start(
        FleetStartRequest(
            prompt=(
                "Audit coordinator.py, specialists.py and fleet.py in this directory. "
                "Give each file to its own subagent, and have each report the file name, "
                "the model string it uses, and how many SDK sessions it creates. "
                "Then print one markdown table of the three results."
            ),
            wait=True,
        )
    )

    print(f"\nfleet started: {result.started}")

    await client.stop()


asyncio.run(main())
