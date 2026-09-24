import asyncio

from pydantic import BaseModel, Field

from copilot import CopilotClient, define_tool
from copilot.rpc import AgentSelectRequest
from copilot.session import CustomAgentConfig

MODEL = "gpt-5-mini"


class ListChangesParams(BaseModel):
    since: str = Field(description="The tag to list changes since")


@define_tool(
    "list_changes",
    description="List the merged changes in the repository since a given tag",
    skip_permission=True,
)
async def list_changes(params: ListChangesParams) -> dict:
    return {
        "since": params.since,
        "changes": [
            {"id": "a91f2c", "area": "cli", "summary": "add --fleet to the prompt runner"},
            {"id": "4d02be", "area": "sdk", "summary": "session.factory API for registered factories"},
            {"id": "7c1188", "area": "sdk", "summary": "customAgents accepted at session creation"},
        ],
    }


agents: list[CustomAgentConfig] = [
    {
        "name": "researcher",
        "display_name": "Researcher",
        "description": "Retrieves repository facts and reports them without commentary",
        "tools": ["list_changes"],
        "prompt": "You are a research specialist. Call the tools you are given, then report only the facts you retrieved as a compact bullet list.",
    },
    {
        "name": "reviewer",
        "display_name": "Reviewer",
        "description": "Checks a draft against the house style and returns a verdict",
        "tools": [],
        "prompt": "You are a style reviewer. The house style forbids em dashes and requires every bullet to carry a change id. Answer with 'VERDICT: PASS' or 'VERDICT: FAIL', then one line per violation.",
    },
]


async def main():
    client = CopilotClient()
    await client.start()
    session = await client.create_session(
        model=MODEL,
        streaming=False,
        tools=[list_changes],
        custom_agents=agents,
        agent="researcher",
    )

    registered = await session.rpc.agent.list()
    print("registered agents:")
    for agent in registered.agents:
        print(f"  {agent.name}: {agent.description}")

    current = await session.rpc.agent.get_current()
    print(f"\nselected at start: {current.agent.name if current.agent else 'default'}")

    facts = await session.send_and_wait(
        "List the changes since tag v2.1 and report them.",
        timeout=180.0,
    )
    print("\n--- researcher ---")
    print(facts.data.content if facts else "")

    selected = await session.rpc.agent.select(AgentSelectRequest(name="reviewer"))
    print(f"\nselected for the next turn: {selected.agent.name if selected.agent else 'default'}")

    verdict = await session.send_and_wait(
        "Review the bullet list you just produced against the house style.",
        timeout=180.0,
    )
    print("\n--- reviewer ---")
    print(verdict.data.content if verdict else "")

    await client.stop()


asyncio.run(main())
