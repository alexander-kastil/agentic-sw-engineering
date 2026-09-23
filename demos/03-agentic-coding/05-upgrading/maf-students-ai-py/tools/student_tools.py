import json
from collections import defaultdict
from typing import Annotated

from data import describe, query


def get_student_details(
    first_name: Annotated[str, "The student's first name to search for (case-insensitive)"],
    last_name: Annotated[str, "The student's last name to search for (case-insensitive)"],
) -> str | None:
    """Retrieves detailed information about a specific student by their first and last name (case-insensitive). Returns null if student is not found."""
    rows = query(
        "SELECT * FROM Students WHERE FirstName = ? COLLATE NOCASE AND LastName = ? COLLATE NOCASE",
        (first_name, last_name),
    )
    return describe(rows[0]) if rows else None


def get_student_age(
    first_name: Annotated[str, "The student's first name to search for (case-insensitive)"],
    last_name: Annotated[str, "The student's last name to search for (case-insensitive)"],
) -> int | None:
    """Retrieves the age of a specific student identified by their full name (case-insensitive). Returns null if student is not found."""
    rows = query(
        "SELECT Age FROM Students WHERE FirstName = ? COLLATE NOCASE AND LastName = ? COLLATE NOCASE",
        (first_name, last_name),
    )
    return rows[0]["Age"] if rows else None


def get_students_by_school(
    school: Annotated[str, "The name of the school to search for students (case-insensitive)"],
) -> str | None:
    """Retrieves a list of all students enrolled in a specific school (case-insensitive). Returns the students as a JSON string, or null if no students are found."""
    rows = query("SELECT * FROM Students WHERE School = ? COLLATE NOCASE", (school,))
    return json.dumps(rows) if rows else None


def get_school_with_most_or_least_students(
    is_most: Annotated[bool, "Set to true to find the school with most students, false to find the school with least students"] = True,
) -> str | None:
    """Identifies the school with either the highest or lowest student enrollment and returns information about its student count."""
    order = "DESC" if is_most else "ASC"
    rows = query(f"SELECT School, COUNT(*) AS Total FROM Students GROUP BY School ORDER BY Total {order} LIMIT 1")
    return f"{rows[0]['School']} has {rows[0]['Total']} students" if rows else None


def get_students_in_school() -> str | None:
    """Retrieves all students grouped by their school, sorted by enrollment count in descending order. Returns the data as a JSON string."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for student in query("SELECT * FROM Students"):
        groups[student["School"]].append(student)
    ordered = dict(sorted(groups.items(), key=lambda item: len(item[1]), reverse=True))
    return json.dumps(ordered) if ordered else None


student_tools = [
    get_student_details,
    get_student_age,
    get_students_by_school,
    get_school_with_most_or_least_students,
    get_students_in_school,
]
