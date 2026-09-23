"""Application entry point: wires routers, security headers, and validation errors."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import auth, categories, products

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(name)s: %(message)s")

app = FastAPI(title="ContosoInventory API", docs_url="/swagger")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add the same security headers the ASP.NET Core version sets."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, error: RequestValidationError) -> JSONResponse:
    """Return 400 with the validation details, matching the [ApiController] behavior."""
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"detail": error.errors()}))
