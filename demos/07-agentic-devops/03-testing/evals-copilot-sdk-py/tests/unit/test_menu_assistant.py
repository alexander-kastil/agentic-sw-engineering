import os
import tempfile
from types import SimpleNamespace

import pytest

import menu_assistant
from menu_assistant import MenuAssistant, complete
from menu_catalog import build_system_prompt


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.sent = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def send_and_wait(self, prompt, timeout):
        self.sent.append((prompt, timeout))
        return self.response


class FakeClient:
    instances = []

    def __init__(self, response):
        self.session = FakeSession(response)
        self.session_kwargs = None
        self.entered = False
        self.exited = False
        FakeClient.instances.append(self)

    async def __aenter__(self):
        self.entered = True
        return self

    async def __aexit__(self, *args):
        self.exited = True
        return False

    async def create_session(self, **kwargs):
        self.session_kwargs = kwargs
        return self.session


@pytest.fixture
def fake_client(monkeypatch, tmp_path):
    FakeClient.instances = []
    config_directory = tmp_path / "menu-chat-copilot"
    state = {"response": SimpleNamespace(data=SimpleNamespace(content="hello")), "config_directory": config_directory}
    monkeypatch.setattr(menu_assistant, "CopilotClient", lambda: FakeClient(state["response"]))
    monkeypatch.setattr(menu_assistant, "ISOLATED_CONFIG_DIRECTORY", str(config_directory))
    return state


async def test_complete_configures_session(fake_client):
    result = await complete("my-model", "system text", "user prompt")

    client = FakeClient.instances[0]
    assert result == "hello"
    assert client.entered and client.exited
    assert client.session_kwargs == {
        "model": "my-model",
        "system_message": {"mode": "replace", "content": "system text"},
        "available_tools": [],
        "config_directory": str(fake_client["config_directory"]),
        "disabled_mcp_servers": ["github-mcp-server"],
        "enable_skills": False,
    }
    assert client.session.sent == [("user prompt", 120.0)]


async def test_complete_creates_config_directory(fake_client):
    assert not fake_client["config_directory"].exists()
    await complete("m", "s", "p")
    assert fake_client["config_directory"].is_dir()


@pytest.mark.parametrize(
    "response",
    [
        None,
        SimpleNamespace(data=None),
        SimpleNamespace(data=SimpleNamespace(content=None)),
        SimpleNamespace(data=SimpleNamespace(content="")),
    ],
    ids=["no-response", "no-data", "no-content", "empty-content"],
)
async def test_complete_returns_empty_string_when_missing(fake_client, response):
    fake_client["response"] = response
    assert await complete("m", "s", "p") == ""


def test_isolated_config_directory_is_under_temp():
    assert menu_assistant.ISOLATED_CONFIG_DIRECTORY == os.path.join(tempfile.gettempdir(), "menu-chat-copilot")


def test_menu_assistant_defaults(monkeypatch):
    monkeypatch.delenv("CHAT_MODEL", raising=False)
    assistant = MenuAssistant()
    assert assistant.model == "gpt-5-mini"
    assert assistant.system_prompt == build_system_prompt()


def test_menu_assistant_chat_model_env_override(monkeypatch):
    monkeypatch.setenv("CHAT_MODEL", "claude-sonnet-4.5")
    assert MenuAssistant().model == "claude-sonnet-4.5"


def test_menu_assistant_explicit_model_wins_over_env(monkeypatch):
    monkeypatch.setenv("CHAT_MODEL", "from-env")
    assert MenuAssistant("explicit").model == "explicit"


async def test_ask_delegates_to_complete(monkeypatch):
    calls = []

    async def fake_complete(model, system_prompt, prompt):
        calls.append((model, system_prompt, prompt))
        return "answer"

    monkeypatch.setattr(menu_assistant, "complete", fake_complete)
    assert await MenuAssistant("m").ask("question?") == "answer"
    assert calls == [("m", build_system_prompt(), "question?")]
