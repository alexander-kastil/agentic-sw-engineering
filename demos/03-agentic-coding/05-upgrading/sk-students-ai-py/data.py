import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).parent / "app.db"


def query(sql: str, params: tuple = ()) -> list[dict]:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def describe(student: dict) -> str:
    return (
        f"Student ID: {student['StudentId']}, First Name: {student['FirstName']}, "
        f"Last Name: {student['LastName']}, School: {student['School']}"
    )
