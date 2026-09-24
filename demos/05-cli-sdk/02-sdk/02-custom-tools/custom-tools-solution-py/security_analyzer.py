import asyncio
import re
from datetime import datetime, timezone

from copilot import CopilotClient, define_tool
from copilot.session_events import AssistantMessageDeltaData, SessionIdleData
from pydantic import BaseModel, Field


class AnalyzeSecurityParams(BaseModel):
    code: str = Field(description="The code snippet to analyze")


class ReadCodeFileParams(BaseModel):
    filename: str = Field(description="The filename to read")


@define_tool(
    "analyze_security",
    description="Analyze code for common security vulnerabilities",
    skip_permission=True,
)
async def analyze_code(params: AnalyzeSecurityParams) -> dict:
    issues = []

    if "eval(" in params.code:
        issues.append("Dangerous eval() detected")
    if "innerHTML" in params.code:
        issues.append("Potential XSS via innerHTML")
    if re.search(r"\bpassword\b.*=.*['\"][^'\"]*['\"]", params.code, re.IGNORECASE):
        issues.append("Hardcoded secret/password detected")
    if "try" not in params.code and "fetch" in params.code:
        issues.append("Unhandled Promise in fetch")

    return {
        "issues": issues if issues else ["No major issues detected"],
        "severity": "high" if len(issues) > 2 else "medium" if issues else "low",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@define_tool("read_code_file", description="Read a code file to analyze", skip_permission=True)
async def get_file_content(params: ReadCodeFileParams) -> dict:
    sample_code = """
      const password = "admin123";
      fetch('/api/data').then(r => r.json())
        .then(data => document.getElementById('container').innerHTML = data);
    """
    return {"filename": params.filename, "content": sample_code}


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
        tools=[analyze_code, get_file_content],
        available_tools=["custom:*"],
        system_message={
            "content": "You are a security-focused code reviewer. Be thorough and specific in your analysis.",
        },
    )

    session.on(on_event)

    await session.send_and_wait(
        "Read the code file 'app.js' and analyze it for security vulnerabilities."
    )

    await client.stop()


asyncio.run(main())
