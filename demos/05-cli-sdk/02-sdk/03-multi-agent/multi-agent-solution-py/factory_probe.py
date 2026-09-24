import asyncio

import copilot
from copilot import CopilotClient
from copilot.rpc import FactoryRunRequest

MODEL = "gpt-5-mini"


async def main():
    client = CopilotClient()
    await client.start()
    session = await client.create_session(model=MODEL, streaming=False)

    print(f"define_factory exported: {hasattr(copilot, 'define_factory')}")
    print(f"session.rpc.factory.run available: {hasattr(session.rpc.factory, 'run')}")

    try:
        run = await session.rpc.factory.run(
            FactoryRunRequest(name="audit-pipeline", args={"files": ["coordinator.py"]})
        )
        print(f"run status: {run.status}")
        print(run.result)
    except Exception as error:
        print(f"\nsession.rpc.factory.run rejected: {error}")
        print(
            "The Python SDK ships no define_factory and no extension join_session, so nothing in a Python program can register a factory by name."
        )

    await client.stop()


asyncio.run(main())
