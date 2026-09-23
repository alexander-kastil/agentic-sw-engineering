import os
from functools import lru_cache
from typing import Annotated

from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential
from fastapi import Depends, FastAPI, Form
from fastapi.responses import HTMLResponse

from page import render
from tools.student_tools import student_tools

model = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4o")
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]


@lru_cache
def get_student_agent() -> Agent:
    chat_client = OpenAIChatCompletionClient(
        model=model,
        azure_endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )
    return chat_client.as_agent(
        name="student-assistant",
        instructions="You help answer student roster questions. Use the provided tools to fetch data rather than guessing.",
        tools=student_tools,
    )


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return render()


@app.post("/", response_class=HTMLResponse)
async def ask(
    student_agent: Annotated[Agent, Depends(get_student_agent)],
    prompt: str = Form(...),
) -> str:
    response = await student_agent.run(prompt)
    return render(response.text or "")
