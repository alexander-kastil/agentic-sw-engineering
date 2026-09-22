# Exercise - Update a web API with GitHub Copilot

[Exercise - Update a web API with GitHub Copilot](https://learn.microsoft.com/en-us/training/modules/advanced-github-copilot/5-exercise-update-a-web-api)

The starter app is [webapi-py](webapi-py/), a FastAPI Travel Weather API. The finished exercise is in [assisted-coding-solution](assisted-coding-solution/).

## Demo

Run these from the repository root. The virtual environment does not exist yet, so create it first.

```powershell
cd labs\02-assisted-coding\webapi-py
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

The API serves on `http://127.0.0.1:8000` and `/` redirects to the Swagger UI at `/docs`.

Check the starter works before prompting Copilot:

```bash
curl http://127.0.0.1:8000/countries
curl http://127.0.0.1:8000/countries/Spain/Seville/January
```

Spain holds only Seville in `weather.json`, and month keys are full names such as `January`. A path with a city or month that is not in the data returns a 500.

## Prompts

```text
Create a new route that exposes the cities of a country/region.
```

```text
/tests help me to create a new test for this route that uses Spain as the country/region.
```

```text
@workspace I want to document how to run this project so that other developers can get started quickly by reading the README.md file.
```

Run the tests with the virtual environment active:

```powershell
pytest -q
```
