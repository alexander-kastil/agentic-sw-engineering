import os
import re

from menu_assistant import complete

PASS_THRESHOLD = 4

JUDGE_SYSTEM_PROMPT = """You are an expert evaluator of groundedness. You judge whether a response is supported by a given context.
You have no tools. Use only the context, the query and the response supplied by the user."""

JUDGE_TEMPLATE = """# Definition
Groundedness measures how well the response is anchored in the provided context. A grounded response states only claims that the context supports, and it answers the query without adding information that is absent from the context or that contradicts it. Declining to answer, or saying that something is not in the context, is grounded when the context indeed does not contain it.

# Ratings
1: The response is entirely unrelated to the context or the query.
2: The response contradicts the context or consists mostly of unsupported claims.
3: The response is partly supported by the context but contains some unsupported or incorrect claims.
4: The response is supported by the context but omits relevant details the query needed.
5: Every claim in the response is supported by the context and the response fully answers the query.

# Data
CONTEXT:
{context}
QUERY:
{query}
RESPONSE:
{response}

# Output
Check every claim in the response against the context, then rate it. Reply in exactly this format and nothing else:
<S0>your step by step reasoning</S0>
<S1>one sentence explanation of the score</S1>
<S2>a single integer from 1 to 5</S2>"""

SCORE_PATTERN = re.compile(r"<S2>\s*([1-5])\s*</S2>")


class GroundednessJudge:
    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("JUDGE_MODEL", "gpt-5")

    async def score(self, query: str, response: str, context: str) -> tuple[int, str]:
        output = await complete(
            self.model,
            JUDGE_SYSTEM_PROMPT,
            JUDGE_TEMPLATE.format(context=context, query=query, response=response),
        )
        match = SCORE_PATTERN.search(output)
        return (int(match.group(1)) if match else 0), output
