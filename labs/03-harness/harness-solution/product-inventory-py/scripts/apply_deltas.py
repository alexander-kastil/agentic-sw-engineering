"""Apply every SQL delta script in db/deltas/ to the SQLite database, in file name order."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "App_Data" / "ContosoInventory.db"
DELTAS = ROOT / "db" / "deltas"

DB_PATH.parent.mkdir(exist_ok=True)
with sqlite3.connect(DB_PATH) as connection:
    for script in sorted(DELTAS.glob("*.sql")):
        connection.executescript(script.read_text(encoding="utf-8"))
        print(f"Applied {script.name}")
