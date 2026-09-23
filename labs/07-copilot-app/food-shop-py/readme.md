# Food Shop (Python)

The Python starter for the [Python variant of Lab 07](../readme-py.md): a FastAPI app that renders the shop landing page from `app/food.json` with a Jinja2 template. The landing page has no heading yet; adding one is the lab's first change.

| File | What it is |
|------|------------|
| `app/main.py` | The FastAPI app: `/` renders the shop page, `/api/food` returns the catalog |
| `app/templates/shop.html` | The template that renders the shop landing page |
| `app/templates/base.html` | The page shell with the navbar |
| `tests/test_shop.py` | The pytest suite, run through FastAPI's `TestClient` |

Install, test and run from this folder:

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m uvicorn app.main:app --reload
```
