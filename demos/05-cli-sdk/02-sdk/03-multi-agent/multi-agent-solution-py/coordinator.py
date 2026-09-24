import asyncio

from pydantic import BaseModel, Field

from copilot import CopilotClient, CopilotSession, Tool, define_tool

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
            {"id": "be40aa", "area": "docs", "summary": "correct the tool permission defaults"},
        ],
    }


async def run_specialist(session: CopilotSession, label: str, prompt: str) -> str:
    print(f"\n--- {label} ---")
    response = await session.send_and_wait(prompt, timeout=180.0)
    text = response.data.content if response else ""
    print(text)
    return text


async def main():
    client = CopilotClient()
    await client.start()

    async def specialist(system_message: str, tools: list[Tool] | None = None) -> CopilotSession:
        return await client.create_session(
            model=MODEL,
            streaming=False,
            tools=tools or [],
            available_tools=["custom:*"],
            system_message={"mode": "replace", "content": system_message},
        )

    researcher = await specialist(
        "You are a research specialist. Call the tools you are given, then report only the facts you retrieved as a compact bullet list. Never write prose around them.",
        [list_changes],
    )

    builder = await specialist(
        "You are a release-notes writer. Turn the facts you are handed into a markdown section titled '## Unreleased', one bullet per change, grouped by area. Output the markdown only.",
    )

    reviewer = await specialist(
        "You are a style reviewer. The house style forbids em dashes and requires every bullet to name its area. Answer with a verdict line 'VERDICT: PASS' or 'VERDICT: FAIL', then one line per violation.",
    )

    facts = await run_specialist(
        researcher,
        "researcher",
        "List the changes since tag v2.1 and report them.",
    )

    draft = await run_specialist(
        builder,
        "builder",
        f"Write the release-notes section from these facts:\n\n{facts}",
    )

    await run_specialist(
        reviewer,
        "reviewer",
        f"Review this release-notes section against the house style:\n\n{draft}",
    )

    await client.stop()


asyncio.run(main())
