# Python Food Shop

FastAPI with server-rendered Jinja2 pages: the same food shop page as `devops-ng` and `devops-react`, with a heading, a greeting from the `GREETING` environment variable, an image and a click counter.

## Run

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m uvicorn main:app --port 4300
```

## Test

```bash
.venv/Scripts/python -m pytest
.venv/Scripts/python -m playwright install chromium
.venv/Scripts/python -m pytest e2e
```

The end-to-end tests expect the app on `http://localhost:4300`. The workflow `.github/workflows/devops-py-ci.yml` runs the same steps on every push and pull request that touches this folder.

## Container

```bash
docker build -t devops-py .
docker run -p 8080:80 devops-py
```
