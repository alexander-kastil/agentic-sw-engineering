import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app import database, seed
from app.routers import auth, inventory, orders

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.initialize()
    seed.seed()
    logging.getLogger("contososhop").info("Database initialized and seeded")
    yield


app = FastAPI(title="ContosoShop Support Portal", lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("CONTOSOSHOP_SECRET", "contososhop-dev-secret"),
    same_site="strict",
    https_only=False,
)

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(inventory.router)

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
