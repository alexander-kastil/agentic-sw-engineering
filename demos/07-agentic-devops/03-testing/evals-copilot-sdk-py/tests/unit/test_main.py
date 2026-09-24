import runpy
from pathlib import Path

import pytest

import menu_assistant

MAIN = str(Path(__file__).resolve().parents[2] / "main.py")


class FakeAssistant:
    questions = []

    async def ask(self, question):
        FakeAssistant.questions.append(question)
        return f"answer to {question}"


@pytest.fixture
def fake_assistant(monkeypatch):
    FakeAssistant.questions = []
    monkeypatch.setattr(menu_assistant, "MenuAssistant", FakeAssistant)
    return FakeAssistant


def test_argv_question_is_joined_and_answered_once(monkeypatch, capsys, fake_assistant):
    monkeypatch.setattr("sys.argv", ["main.py", "what", "is", "cheap?"])
    monkeypatch.setattr("builtins.input", lambda prompt: pytest.fail("input must not be called"))

    runpy.run_path(MAIN, run_name="__main__")

    assert fake_assistant.questions == ["what is cheap?"]
    assert capsys.readouterr().out == "answer to what is cheap?\n"


def test_input_loop_until_blank_line(monkeypatch, capsys, fake_assistant):
    lines = iter(["  first  ", "second", "   ", "never"])
    prompts = []

    def fake_input(prompt):
        prompts.append(prompt)
        return next(lines)

    monkeypatch.setattr("sys.argv", ["main.py"])
    monkeypatch.setattr("builtins.input", fake_input)

    runpy.run_path(MAIN, run_name="__main__")

    assert fake_assistant.questions == ["first", "second"]
    assert prompts == ["> ", "> ", "> "]
    assert capsys.readouterr().out == "answer to first\nanswer to second\n"


def test_input_loop_exits_immediately_on_empty(monkeypatch, capsys, fake_assistant):
    monkeypatch.setattr("sys.argv", ["main.py"])
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    runpy.run_path(MAIN, run_name="__main__")

    assert fake_assistant.questions == []
    assert capsys.readouterr().out == ""
