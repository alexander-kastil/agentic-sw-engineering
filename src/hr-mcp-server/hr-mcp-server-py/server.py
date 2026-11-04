#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp==2.3.0",
#     "uvicorn==0.54.0",
#     "starlette==1.10.0",
# ]
# ///
import json
import logging
import os
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Annotated

import uvicorn
from mcp.server.mcpserver import MCPServer
from pydantic import Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hr-mcp-server")

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "47002"))
DB_PATH = Path(__file__).parent / "hr-data.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS "Candidates" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Candidates" PRIMARY KEY AUTOINCREMENT,
    "FirstName" TEXT NOT NULL,
    "LastName" TEXT NOT NULL,
    "Email" TEXT NOT NULL,
    "SpokenLanguagesData" TEXT NOT NULL,
    "SkillsData" TEXT NOT NULL,
    "CurrentRole" TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS "IX_Candidates_Email" ON "Candidates" ("Email");
"""

SEED_EMPLOYEES = [
    ("Carlos", "Gomez", "carlos.gomez@restaurant.com", ["Spanish", "English", "French"], ["Sous Chef", "Menu Planning", "Food Safety", "Inventory Management"], "Sous Chef"),
    ("Marie", "Dubois", "marie.dubois@restaurant.com", ["French", "English", "Italian"], ["Pastry Chef", "Dessert Creation", "Baking", "Team Leadership"], "Pastry Chef"),
    ("Luca", "Rossi", "luca.rossi@restaurant.com", ["Italian", "English", "Spanish"], ["Head Waiter", "Customer Service", "Wine Pairing", "Table Management"], "Head Waiter"),
    ("Anna", "Schmidt", "anna.schmidt@restaurant.com", ["German", "English", "Russian"], ["Restaurant Manager", "Staff Scheduling", "Budgeting", "Event Coordination"], "Restaurant Manager"),
    ("Sofia", "Fernandez", "sofia.fernandez@restaurant.com", ["Portuguese", "Spanish", "English"], ["Bartender", "Mixology", "Inventory Control", "Customer Engagement"], "Bartender"),
    ("Kenji", "Tanaka", "kenji.tanaka@restaurant.com", ["Japanese", "English", "Mandarin"], ["Sushi Chef", "Knife Skills", "Seafood Preparation", "Quality Control"], "Sushi Chef"),
    ("Olga", "Ivanova", "olga.ivanova@restaurant.com", ["Russian", "English", "German"], ["Hostess", "Reservation Management", "Multilingual Communication", "Conflict Resolution"], "Hostess"),
    ("Ahmed", "Hassan", "ahmed.hassan@restaurant.com", ["Arabic", "English", "French"], ["Grill Chef", "Meat Preparation", "Kitchen Safety", "Teamwork"], "Grill Chef"),
]

mcp = MCPServer("hr-mcp-server")


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def to_json_list(values: list[str]) -> str:
    return json.dumps(values, separators=(",", ":"))


def parse_comma_separated(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def normalize_email(email: str) -> str:
    if not email.strip():
        raise ValueError("Email cannot be null or empty")
    return email.strip()


def to_employee(row: sqlite3.Row) -> dict:
    return {
        "firstname": row["FirstName"],
        "lastname": row["LastName"],
        "email": row["Email"],
        "spoken_languages": json.loads(row["SpokenLanguagesData"]),
        "skills": json.loads(row["SkillsData"]),
        "current_role": row["CurrentRole"],
        "fullName": f"{row['FirstName']} {row['LastName']}",
    }


def to_collection(rows: list[sqlite3.Row]) -> str:
    return json.dumps({"employees": [to_employee(row) for row in rows]}, separators=(",", ":"))


def initialize_database() -> None:
    with closing(connect()) as db, db:
        db.executescript(SCHEMA)
        if db.execute('SELECT EXISTS (SELECT 1 FROM "Candidates")').fetchone()[0]:
            logger.info("Employee database already contains data; skipping seed.")
            return
        db.executemany(
            'INSERT INTO "Candidates" ("FirstName", "LastName", "Email", "SpokenLanguagesData", "SkillsData", "CurrentRole") VALUES (?, ?, ?, ?, ?, ?)',
            [(first, last, email, to_json_list(languages), to_json_list(skills), role) for first, last, email, languages, skills, role in SEED_EMPLOYEES],
        )
        logger.info("Seeded %d employees into the database.", len(SEED_EMPLOYEES))


def all_employees(db: sqlite3.Connection) -> list[sqlite3.Row]:
    return db.execute('SELECT * FROM "Candidates" ORDER BY "LastName", "FirstName"').fetchall()


@mcp.tool(description="Provides the whole list of employees", structured_output=False)
def list_employees() -> str:
    with closing(connect()) as db:
        return to_collection(all_employees(db))


@mcp.tool(description="Adds a new employee to the list", structured_output=False)
def add_employee(
    firstName: Annotated[str, Field(description="First name of the employee")],
    lastName: Annotated[str, Field(description="Last name of the employee")],
    email: Annotated[str, Field(description="Email address of the employee")],
    currentRole: Annotated[str, Field(description="Current role of the employee")],
    spokenLanguages: Annotated[str, Field(description="Comma-separated list of spoken languages")] = "",
    skills: Annotated[str, Field(description="Comma-separated list of skills")] = "",
) -> str:
    first_name = firstName.strip()
    last_name = lastName.strip()
    email = email.strip()
    full_name = f"{first_name} {last_name}"
    with closing(connect()) as db, db:
        if db.execute('SELECT 1 FROM "Candidates" WHERE "Email" = ?', (email,)).fetchone():
            return f"Employee with email '{email}' already exists."
        db.execute(
            'INSERT INTO "Candidates" ("FirstName", "LastName", "Email", "SpokenLanguagesData", "SkillsData", "CurrentRole") VALUES (?, ?, ?, ?, ?, ?)',
            (first_name, last_name, email, to_json_list(parse_comma_separated(spokenLanguages)), to_json_list(parse_comma_separated(skills)), currentRole.strip()),
        )
    logger.info("Added new employee: %s (%s)", full_name, email)
    return f"Successfully added employee: {full_name}"


@mcp.tool(description="Updates an existing employee by email", structured_output=False)
def update_employee(
    email: Annotated[str, Field(description="Email address of the employee to update")],
    firstName: Annotated[str | None, Field(description="New first name (optional)")] = None,
    lastName: Annotated[str | None, Field(description="New last name (optional)")] = None,
    currentRole: Annotated[str | None, Field(description="New current role (optional)")] = None,
    spokenLanguages: Annotated[str | None, Field(description="New comma-separated list of spoken languages (optional)")] = None,
    skills: Annotated[str | None, Field(description="New comma-separated list of skills (optional)")] = None,
) -> str:
    normalized_email = normalize_email(email)
    with closing(connect()) as db, db:
        row = db.execute('SELECT * FROM "Candidates" WHERE "Email" = ?', (normalized_email,)).fetchone()
        if row is None:
            return f"Employee with email '{email}' not found."
        updated = dict(row)
        if firstName and firstName.strip():
            updated["FirstName"] = firstName.strip()
        if lastName and lastName.strip():
            updated["LastName"] = lastName.strip()
        if currentRole and currentRole.strip():
            updated["CurrentRole"] = currentRole.strip()
        if spokenLanguages is not None:
            updated["SpokenLanguagesData"] = to_json_list(parse_comma_separated(spokenLanguages))
        if skills is not None:
            updated["SkillsData"] = to_json_list(parse_comma_separated(skills))
        db.execute(
            'UPDATE "Candidates" SET "FirstName" = :FirstName, "LastName" = :LastName, "CurrentRole" = :CurrentRole, "SpokenLanguagesData" = :SpokenLanguagesData, "SkillsData" = :SkillsData WHERE "Id" = :Id',
            updated,
        )
    logger.info("Updated employee with email: %s", normalized_email)
    return f"Successfully updated employee with email: {email}"


@mcp.tool(description="Removes an employee by email", structured_output=False)
def remove_employee(
    email: Annotated[str, Field(description="Email address of the employee to remove")],
) -> str:
    normalized_email = normalize_email(email)
    with closing(connect()) as db, db:
        if db.execute('DELETE FROM "Candidates" WHERE "Email" = ?', (normalized_email,)).rowcount == 0:
            return f"Employee with email '{email}' not found."
    logger.info("Removed employee with email: %s", normalized_email)
    return f"Successfully removed employee with email: {email}"


@mcp.tool(description="Searches for employees by name, email, skills, or current role", structured_output=False)
def search_employees(
    searchTerm: Annotated[str, Field(description="Search term to find in employee data")],
) -> str:
    with closing(connect()) as db:
        if not searchTerm.strip():
            return to_collection(all_employees(db))
        rows = db.execute('SELECT * FROM "Candidates"').fetchall()
    term = searchTerm.strip().lower()
    matches = [
        row
        for row in rows
        if term in row["FirstName"].lower()
        or term in row["LastName"].lower()
        or term in row["Email"].lower()
        or term in row["CurrentRole"].lower()
        or any(term in skill.lower() for skill in json.loads(row["SkillsData"]))
        or any(term in language.lower() for language in json.loads(row["SpokenLanguagesData"]))
    ]
    return to_collection(matches)


if __name__ == "__main__":
    initialize_database()
    uvicorn.run(mcp.streamable_http_app(streamable_http_path="/", host=HOST), host=HOST, port=PORT)
