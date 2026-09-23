import json
from collections import defaultdict
from typing import Annotated

from semantic_kernel.functions import kernel_function

from data import describe, query


class StudentPlugin:
    @kernel_function(description="Retrieves detailed information about a specific student by their first and last name (case-insensitive). Returns null if student is not found.")
    def get_student_details(
        self,
        first_name: Annotated[str, "The student's first name to search for (case-insensitive)"],
        last_name: Annotated[str, "The student's last name to search for (case-insensitive)"],
    ) -> str | None:
        rows = query(
            "SELECT * FROM Students WHERE FirstName = ? COLLATE NOCASE AND LastName = ? COLLATE NOCASE",
            (first_name, last_name),
        )
        return describe(rows[0]) if rows else None

    @kernel_function(description="Retrieves the age of a specific student identified by their full name (case-insensitive). Returns null if student is not found.")
    def get_student_age(
        self,
        first_name: Annotated[str, "The student's first name to search for (case-insensitive)"],
        last_name: Annotated[str, "The student's last name to search for (case-insensitive)"],
    ) -> int | None:
        rows = query(
            "SELECT Age FROM Students WHERE FirstName = ? COLLATE NOCASE AND LastName = ? COLLATE NOCASE",
            (first_name, last_name),
        )
        return rows[0]["Age"] if rows else None

    @kernel_function(description="Retrieves a list of all students enrolled in a specific school (case-insensitive). Returns the students as a JSON string, or null if no students are found.")
    def get_students_by_school(
        self,
        school: Annotated[str, "The name of the school to search for students (case-insensitive)"],
    ) -> str | None:
        rows = query("SELECT * FROM Students WHERE School = ? COLLATE NOCASE", (school,))
        return json.dumps(rows) if rows else None

    @kernel_function(description="Identifies the school with either the highest or lowest student enrollment and returns information about its student count.")
    def get_school_with_most_or_least_students(
        self,
        is_most: Annotated[bool, "Set to true to find the school with most students, false to find the school with least students"] = True,
    ) -> str | None:
        order = "DESC" if is_most else "ASC"
        rows = query(f"SELECT School, COUNT(*) AS Total FROM Students GROUP BY School ORDER BY Total {order} LIMIT 1")
        return f"{rows[0]['School']} has {rows[0]['Total']} students" if rows else None

    @kernel_function(description="Retrieves all students grouped by their school, sorted by enrollment count in descending order. Returns the data as a JSON string.")
    def get_students_in_school(self) -> str | None:
        groups: dict[str, list[dict]] = defaultdict(list)
        for student in query("SELECT * FROM Students"):
            groups[student["School"]].append(student)
        ordered = dict(sorted(groups.items(), key=lambda item: len(item[1]), reverse=True))
        return json.dumps(ordered) if ordered else None
