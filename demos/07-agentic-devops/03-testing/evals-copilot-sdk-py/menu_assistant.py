import os
import tempfile

from copilot import CopilotClient

from menu_catalog import build_system_prompt

ISOLATED_CONFIG_DIRECTORY = os.path.join(tempfile.gettempdir(), "menu-chat-copilot")


async def complete(model: str, system_prompt: str, prompt: str) -> str:
    os.makedirs(ISOLATED_CONFIG_DIRECTORY, exist_ok=True)
    async with CopilotClient() as client:
        async with await client.create_session(
            model=model,
            system_message={"mode": "replace", "content": system_prompt},
            available_tools=[],
            config_directory=ISOLATED_CONFIG_DIRECTORY,
            disabled_mcp_servers=["github-mcp-server"],
            enable_skills=False,
        ) as session:
            response = await session.send_and_wait(prompt, timeout=120.0)
            return response.data.content if response and response.data and response.data.content else ""


class MenuAssistant:
    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("CHAT_MODEL", "gpt-5-mini")
        self.system_prompt = build_system_prompt()

    async def ask(self, question: str) -> str:
        return await complete(self.model, self.system_prompt, question)
