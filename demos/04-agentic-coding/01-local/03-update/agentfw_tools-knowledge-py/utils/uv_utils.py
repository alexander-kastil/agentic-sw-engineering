import shutil
import subprocess
import sys
from pathlib import Path


def resolve_uvx() -> str:
    """
    Resolve the absolute path to `uvx`.
    Order:
    1) PATH via shutil.which
    2) Common local virtualenv locations (.venv/venv)
    3) Attempt to install `uv` into current interpreter, then retry 1 and 2
    Raises FileNotFoundError if still not found.
    """
    uvx_path = shutil.which("uvx")
    if uvx_path:
        return uvx_path

    cwd = Path.cwd()
    for rel in (".venv/Scripts/uvx.exe", ".venv/bin/uvx", "venv/Scripts/uvx.exe", "venv/bin/uvx"):
        candidate = (cwd / rel).resolve()
        if candidate.exists():
            return str(candidate)

    print("\n'uvx' not found. Attempting to install 'uv' into the current environment...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
    except Exception as inst_err:
        raise FileNotFoundError("uvx not found and auto-install failed") from inst_err

    uvx_path = shutil.which("uvx")
    if uvx_path:
        return uvx_path

    for rel in (".venv/Scripts/uvx.exe", ".venv/bin/uvx", "venv/Scripts/uvx.exe", "venv/bin/uvx"):
        candidate = (cwd / rel).resolve()
        if candidate.exists():
            return str(candidate)

    raise FileNotFoundError("uvx still not found after installing 'uv'")
