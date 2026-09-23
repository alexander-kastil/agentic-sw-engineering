import os

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory

from page import render
from plugins.student_plugin import StudentPlugin

model = os.environ["AZURE_OPENAI_MODEL"]
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]

kernel = Kernel()
kernel.add_service(AzureChatCompletion(deployment_name=model, endpoint=endpoint, api_key=api_key))
kernel.add_plugin(StudentPlugin(), plugin_name="StudentPlugin")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return render()


@app.post("/", response_class=HTMLResponse)
async def ask(prompt: str = Form(...)) -> str:
    return render(await call_function(prompt))


async def call_function(question: str) -> str:
    history = ChatHistory()
    history.add_user_message(question)
    chat_completion_service = kernel.get_service(type=ChatCompletionClientBase)
    settings = AzureChatPromptExecutionSettings(function_choice_behavior=FunctionChoiceBehavior.Auto())
    full_message = ""
    async for chunks in chat_completion_service.get_streaming_chat_message_contents(
        chat_history=history, settings=settings, kernel=kernel
    ):
        full_message += "".join(str(chunk) for chunk in chunks)
    history.add_assistant_message(full_message)
    return full_message
