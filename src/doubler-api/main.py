"""
Doubler API - Returns double the value of a given input.
"""
from fastapi import FastAPI, Query

app = FastAPI(title="Doubler API")


@app.get("/double")
async def double(value: float = Query(..., description="The value to double")) -> dict[str, float]:
    return {"input": value, "result": value * 2}
