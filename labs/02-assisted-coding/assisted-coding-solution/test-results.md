# Test Results

Run on 2026-09-21, Windows 11, Python 3.12.10. Every command below was executed as written.

## Summary

| Check | Result |
| --- | --- |
| Starter venv created and dependencies installed | PASS |
| Starter `pytest` | PASS (2 passed) |
| Starter `GET /` redirects to `/docs` | PASS (301) |
| Starter `GET /countries` | PASS |
| Starter `GET /countries/Spain/Seville/January` | PASS |
| Starter `GET /countries/Spain` absent before the exercise | PASS (404, as expected for the starter) |
| Solution `pytest` | PASS (4 passed) |
| Solution `GET /countries/Spain` | PASS (`["Seville"]`) |
| Solution `GET /countries/Portugal` | PASS (`["Lisbon","Porto"]`) |
| Solution `GET /countries/Atlantis` | PASS (404 with detail) |
| Solution `GET /countries/Spain/Seville/January` | PASS |

## Starter app

### Environment setup

```powershell
cd labs\02-assisted-coding\webapi-py
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Output tail:

```text
Successfully installed annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 charset-normalizer-3.5.1
click-8.5.0 colorama-0.4.6 fastapi-0.109.1 h11-0.14.0 httpcore-0.18.0 httptools-0.8.0 httpx-0.25.0
idna-3.20 iniconfig-2.3.0 packaging-26.3 pluggy-1.6.0 pydantic-2.13.5 pydantic-core-2.46.5
pygments-2.21.0 pytest-9.1.1 python-dotenv-1.2.3 pyyaml-6.0.3 requests-2.32.0 sniffio-1.3.1
starlette-0.35.1 typing-extensions-4.16.0 typing-inspection-0.4.4 urllib3-2.8.0 uvicorn-0.53.0
watchfiles-1.3.0 websockets-17.1
```

### Tests

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

```text
..                                                                       [100%]
============================== warnings summary ===============================
venv\Lib\site-packages\starlette\testclient.py:31
  DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2 passed, 1 warning in 0.19s
```

### Running app

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --port 8021
```

```bash
curl -s -i http://127.0.0.1:8021/ | head -5
curl -s http://127.0.0.1:8021/countries
curl -s http://127.0.0.1:8021/countries/Spain/Seville/January
curl -s -i http://127.0.0.1:8021/countries/Spain | head -3
```

```text
=== curl -i http://127.0.0.1:8021/ ===
HTTP/1.1 301 Moved Permanently
date: Mon, 21 Sep 2026 17:50:36 GMT
server: uvicorn
content-length: 0
location: /docs
=== curl http://127.0.0.1:8021/countries ===
["England","France","Germany","Peru","Portugal","Italy","Spain"]
=== curl http://127.0.0.1:8021/countries/Spain/Seville/January ===
{"high":61,"low":41}
=== curl -i /countries/Spain (starter) ===
HTTP/1.1 404 Not Found
date: Mon, 21 Sep 2026 17:50:40 GMT
server: uvicorn
```

The 404 on `/countries/Spain` is the starting condition, not a defect: that route is what the exercise asks you to build.

## Solution

Run with the same interpreter as the starter, `..\webapi-py\venv\Scripts\python.exe`.

### Tests

```powershell
cd labs\02-assisted-coding\assisted-coding-solution
..\webapi-py\venv\Scripts\python.exe -m pytest -q
```

```text
....                                                                     [100%]
============================== warnings summary ===============================
..\webapi-py\venv\Lib\site-packages\starlette\testclient.py:31
  DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
4 passed, 1 warning in 0.21s
```

### Running app

```powershell
..\webapi-py\venv\Scripts\python.exe -m uvicorn main:app --port 8022
```

```bash
curl -s -i http://127.0.0.1:8022/ | head -5
curl -s http://127.0.0.1:8022/countries
curl -s http://127.0.0.1:8022/countries/Spain
curl -s http://127.0.0.1:8022/countries/Portugal
curl -s -i http://127.0.0.1:8022/countries/Atlantis | head -1
curl -s http://127.0.0.1:8022/countries/Spain/Seville/January
```

```text
=== / ===
HTTP/1.1 301 Moved Permanently
date: Mon, 21 Sep 2026 17:51:39 GMT
server: uvicorn
content-length: 0
location: /docs
=== /countries ===
["England","France","Germany","Peru","Portugal","Italy","Spain"]
=== /countries/Spain ===
["Seville"]
=== /countries/Portugal ===
["Lisbon","Porto"]
=== /countries/Atlantis ===
HTTP/1.1 404 Not Found
{"detail":"Country not found: Atlantis"}
=== /countries/Spain/Seville/January ===
{"high":61,"low":41}
```

## Data facts confirmed against weather.json

```powershell
python -c "import json;d=json.load(open('weather.json'));print({k:list(v.keys()) for k,v in d.items()})"
```

```text
{'England': ['London'], 'France': ['Paris'], 'Germany': ['Berlin'], 'Peru': ['Lima'],
 'Portugal': ['Lisbon', 'Porto'], 'Italy': ['Montepulciano'], 'Spain': ['Seville']}
```

Spain holds Seville, not Madrid, and month keys are full names such as `January`. A request for `/countries/Spain/Madrid/Jan` raises a `KeyError` and returns a 500.

## Guide commands re-run verbatim after the fix

```powershell
cd labs\02-assisted-coding\webapi-py
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```text
Requirement already satisfied: pygments>=2.7.2 in .\venv\Lib\site-packages (from pytest->-r requirements.txt (line 6)) (2.21.0)
D:\git-classes\agentic-sw-engineering\labs\02-assisted-coding\webapi-py\venv\Scripts\uvicorn.exe
D:\git-classes\agentic-sw-engineering\labs\02-assisted-coding\webapi-py\venv\Scripts\pytest.exe
```

`uvicorn` and `pytest` resolve inside the virtual environment, so the activation line works.

```powershell
uvicorn main:app --reload
```

```bash
curl http://127.0.0.1:8000/countries
curl http://127.0.0.1:8000/countries/Spain/Seville/January
```

```text
=== curl http://127.0.0.1:8000/countries ===
["England","France","Germany","Peru","Portugal","Italy","Spain"]
=== curl http://127.0.0.1:8000/countries/Spain/Seville/January ===
{"high":61,"low":41}
=== curl -i / ===
HTTP/1.1 301 Moved Permanently
=== /docs (following the redirect) ===
200
```

| Check | Result |
| --- | --- |
| `cd labs\02-assisted-coding\webapi-py` resolves from the repository root | PASS |
| `python -m venv venv` then `.\venv\Scripts\Activate.ps1` | PASS |
| `pip install -r requirements.txt` inside the activated venv | PASS |
| `uvicorn main:app --reload` on the default port | PASS |
| Both curl lines printed in the guide | PASS |
| `/docs` reachable through the `/` redirect | PASS (200) |
| Relative links in `../readme.md` resolve on disk | PASS (`webapi-py/`, `assisted-coding-solution/`) |
