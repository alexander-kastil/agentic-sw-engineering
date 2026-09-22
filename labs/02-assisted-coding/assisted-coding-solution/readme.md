# Lab 02 Solution - Assisted Coding

Completed version of the [Travel Weather API exercise](../readme.md). The starter app in [webapi-py](../webapi-py/) stays untouched, so you can compare the two folders side by side.

## What changed

| File | Change |
| --- | --- |
| `main.py` | New `GET /countries/{country}` route returning the cities of a country/region, plus a 404 for an unknown country. `HTTPException` added to the `fastapi` import. |
| `test_main.py` | Two new tests: `test_cities_spain` asserts `/countries/Spain` returns `["Seville"]`, `test_cities_unknown_country` asserts an unknown country gives 404. |
| `readme.md` | The "How to run this project" section below, the third deliverable of the exercise. |

The route reads the same `weather.json` the rest of the API uses. Spain only holds Seville in that file, which is why the test pins the exact list instead of a `in` check.

## How to run this project

Requirements: Python 3.10 or newer on the PATH.

Create the virtual environment and install the dependencies:

```powershell
cd labs\02-assisted-coding\assisted-coding-solution
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the API with reload enabled:

```powershell
uvicorn main:app --reload
```

The app serves on `http://127.0.0.1:8000`. Opening `/` redirects to the interactive Swagger UI at `/docs`.

Run the test suite:

```powershell
pytest -q
```

## Endpoints

| Method | Path | Returns |
| --- | --- | --- |
| GET | `/` | 301 redirect to `/docs` |
| GET | `/countries` | Every country/region in the data set |
| GET | `/countries/{country}` | The cities of that country/region, 404 if unknown |
| GET | `/countries/{country}/{city}/{month}` | Historical high and low for that month |

Month names are spelled out in full (`January`, not `Jan`), and each country carries only the cities listed in `weather.json`. Spain is Seville, Portugal is Lisbon and Porto.

Try it:

```bash
curl http://127.0.0.1:8000/countries
curl http://127.0.0.1:8000/countries/Spain
curl http://127.0.0.1:8000/countries/Spain/Seville/January
```

Recorded runs of every command above are in [test-results.md](test-results.md).
