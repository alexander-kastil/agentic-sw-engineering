"""SQLite connection factory for the ContosoInventory database."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "App_Data" / "ContosoInventory.db"


def open_connection() -> sqlite3.Connection:
    """Open a connection with named-column rows and foreign keys enforced."""
    if not DB_PATH.exists():
        raise RuntimeError(f"Database not found at {DB_PATH}. Run: python scripts/apply_deltas.py")
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
