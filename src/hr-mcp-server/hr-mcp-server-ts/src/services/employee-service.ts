import type { SQLOutputValue } from "node:sqlite";
import { db } from "../data/employee-db.js";
import type { Employee } from "../tools/models.js";

interface EmployeeRow extends Record<string, SQLOutputValue> {
  Id: number;
  FirstName: string;
  LastName: string;
  Email: string;
  SpokenLanguagesData: string;
  SkillsData: string;
  CurrentRole: string;
}

function toEmployee(row: EmployeeRow): Employee {
  return {
    firstName: row.FirstName,
    lastName: row.LastName,
    email: row.Email,
    spokenLanguages: JSON.parse(row.SpokenLanguagesData),
    skills: JSON.parse(row.SkillsData),
    currentRole: row.CurrentRole,
  };
}

function findRowByEmail(email: string): EmployeeRow | undefined {
  return db.prepare(`SELECT * FROM "Candidates" WHERE "Email" = ? LIMIT 1`).get(email) as EmployeeRow | undefined;
}

export function getAllEmployees(): Employee[] {
  const rows = db.prepare(`SELECT * FROM "Candidates" ORDER BY "LastName", "FirstName"`).all() as EmployeeRow[];
  return rows.map(toEmployee);
}

export function addEmployee(employee: Employee): boolean {
  const email = employee.email.trim();

  if (findRowByEmail(email)) {
    return false;
  }

  employee.email = email;

  db.prepare(
    `INSERT INTO "Candidates" ("CurrentRole", "Email", "FirstName", "LastName", "SkillsData", "SpokenLanguagesData") VALUES (?, ?, ?, ?, ?, ?)`,
  ).run(
    employee.currentRole,
    employee.email,
    employee.firstName,
    employee.lastName,
    JSON.stringify(employee.skills),
    JSON.stringify(employee.spokenLanguages),
  );

  return true;
}

export function updateEmployee(email: string, updateAction: (employee: Employee) => void): boolean {
  const row = findRowByEmail(email.trim());

  if (!row) {
    return false;
  }

  const employee = toEmployee(row);
  updateAction(employee);

  db.prepare(
    `UPDATE "Candidates" SET "CurrentRole" = ?, "FirstName" = ?, "LastName" = ?, "SkillsData" = ?, "SpokenLanguagesData" = ? WHERE "Id" = ?`,
  ).run(
    employee.currentRole,
    employee.firstName,
    employee.lastName,
    JSON.stringify(employee.skills),
    JSON.stringify(employee.spokenLanguages),
    row.Id,
  );

  return true;
}

export function removeEmployee(email: string): boolean {
  const row = findRowByEmail(email.trim());

  if (!row) {
    return false;
  }

  db.prepare(`DELETE FROM "Candidates" WHERE "Id" = ?`).run(row.Id);
  return true;
}

export function searchEmployees(searchTerm: string): Employee[] {
  if (!searchTerm.trim()) {
    return getAllEmployees();
  }

  const searchTermLower = searchTerm.trim().toLowerCase();
  const rows = db.prepare(`SELECT * FROM "Candidates"`).all() as EmployeeRow[];

  return rows
    .map(toEmployee)
    .filter(
      (employee) =>
        employee.firstName.toLowerCase().includes(searchTermLower) ||
        employee.lastName.toLowerCase().includes(searchTermLower) ||
        employee.email.toLowerCase().includes(searchTermLower) ||
        employee.currentRole.toLowerCase().includes(searchTermLower) ||
        employee.skills.some((skill) => skill.toLowerCase().includes(searchTermLower)) ||
        employee.spokenLanguages.some((language) => language.toLowerCase().includes(searchTermLower)),
    );
}
