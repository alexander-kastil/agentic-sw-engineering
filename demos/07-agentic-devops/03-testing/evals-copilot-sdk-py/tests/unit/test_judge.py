import pytest

import judge
from judge import JUDGE_SYSTEM_PROMPT, PASS_THRESHOLD, SCORE_PATTERN, GroundednessJudge


@pytest.fixture
def fake_complete(monkeypatch):
    state = {"output": "<S0>r</S0><S1>e</S1><S2>5</S2>", "calls": []}

    async def complete(model, system_prompt, prompt):
        state["calls"].append((model, system_prompt, prompt))
        return state["output"]

    monkeypatch.setattr(judge, "complete", complete)
    return state


def test_pass_threshold_is_four():
    assert PASS_THRESHOLD == 4


def test_judge_model_default(monkeypatch):
    monkeypatch.delenv("JUDGE_MODEL", raising=False)
    assert GroundednessJudge().model == "gpt-5"


def test_judge_model_env_override(monkeypatch):
    monkeypatch.setenv("JUDGE_MODEL", "claude-opus-4.5")
    assert GroundednessJudge().model == "claude-opus-4.5"


def test_judge_explicit_model_wins(monkeypatch):
    monkeypatch.setenv("JUDGE_MODEL", "from-env")
    assert GroundednessJudge("explicit").model == "explicit"


async def test_score_prompt_contains_context_query_response(fake_complete):
    await GroundednessJudge("judge-model").score("the query", "the response", "the context")

    model, system_prompt, prompt = fake_complete["calls"][0]
    assert model == "judge-model"
    assert system_prompt == JUDGE_SYSTEM_PROMPT
    assert "CONTEXT:\nthe context\nQUERY:\nthe query\nRESPONSE:\nthe response\n" in prompt
    assert "<S2>a single integer from 1 to 5</S2>" in prompt


async def test_score_returns_score_and_raw_output(fake_complete):
    fake_complete["output"] = "<S0>ok</S0><S1>fine</S1><S2>4</S2>"
    assert await GroundednessJudge("m").score("q", "r", "c") == (4, "<S0>ok</S0><S1>fine</S1><S2>4</S2>")


@pytest.mark.parametrize(
    "output, expected",
    [
        ("<S2>1</S2>", 1),
        ("<S2>3</S2>", 3),
        ("<S2>5</S2>", 5),
        ("<S2> 2 </S2>", 2),
        ("<S2>\n4\n</S2>", 4),
        ("", 0),
        ("no tags at all", 0),
        ("<S2>0</S2>", 0),
        ("<S2>6</S2>", 0),
        ("<S2>10</S2>", 0),
        ("<S2>five</S2>", 0),
        ("<S2>4", 0),
    ],
)
async def test_score_parsing(fake_complete, output, expected):
    fake_complete["output"] = output
    score, raw = await GroundednessJudge("m").score("q", "r", "c")
    assert score == expected
    assert raw == output


@pytest.mark.parametrize("score, passes", [(0, False), (3, False), (4, True), (5, True)])
async def test_threshold_pass_fail(fake_complete, score, passes):
    fake_complete["output"] = f"<S2>{score}</S2>" if score else "malformed"
    result, _ = await GroundednessJudge("m").score("q", "r", "c")
    assert (result >= PASS_THRESHOLD) is passes


def test_score_pattern_takes_first_match():
    assert SCORE_PATTERN.search("<S2>2</S2> then <S2>5</S2>").group(1) == "2"
