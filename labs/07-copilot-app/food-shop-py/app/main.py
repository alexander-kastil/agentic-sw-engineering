import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Food Shop")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def load_food():
    return json.loads((BASE_DIR / "food.json").read_text(encoding="utf-8"))


@app.get("/", response_class=HTMLResponse)
def shop(request: Request):
    return templates.TemplateResponse(request, "shop.html", {"food": load_food()})


@app.get("/api/food")
def food():
    return load_food()
