import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Python Food Shop")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
greeting = os.getenv("GREETING", "Hello Development Environment")


@app.get("/", response_class=HTMLResponse)
def index(request: Request, count: int = 0) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {"greeting": greeting, "count": count})


app.mount("/", StaticFiles(directory=BASE_DIR / "static"), name="static")
