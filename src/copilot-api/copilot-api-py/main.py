import logging

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from routes import router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Copilot API")
app.include_router(router)


@app.get("/", response_class=PlainTextResponse)
def root() -> str:
    return "Copilot API - Visit /docs for API documentation"
