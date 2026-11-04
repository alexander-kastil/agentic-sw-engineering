import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import {
  addEmployee,
  getAllEmployees,
  removeEmployee,
  searchEmployees,
  updateEmployee,
} from "../services/employee-service.js";
import { fullName, serializeEmployeeCollection, type Employee } from "./models.js";

function text(value: string) {
  return { content: [{ type: "text" as const, text: value }] };
}

function parseCommaSeparatedString(input: string | null | undefined): string[] {
  if (!input?.trim()) {
    return [];
  }

  return input
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

export function registerHrTools(mcp: McpServer): void {
  mcp.registerTool(
    "list_employees",
    {
      description: "Provides the whole list of employees",
    },
    async () => text(serializeEmployeeCollection({ employees: getAllEmployees() })),
  );

  mcp.registerTool(
    "add_employee",
    {
      description: "Adds a new employee to the list",
      inputSchema: {
        firstName: z.string().describe("First name of the employee"),
        lastName: z.string().describe("Last name of the employee"),
        email: z.string().describe("Email address of the employee"),
        currentRole: z.string().describe("Current role of the employee"),
        spokenLanguages: z.string().default("").describe("Comma-separated list of spoken languages"),
        skills: z.string().default("").describe("Comma-separated list of skills"),
      },
    },
    async ({ firstName, lastName, email, currentRole, spokenLanguages, skills }) => {
      const employee: Employee = {
        firstName: firstName.trim(),
        lastName: lastName.trim(),
        email: email.trim(),
        currentRole: currentRole.trim(),
        spokenLanguages: parseCommaSeparatedString(spokenLanguages),
        skills: parseCommaSeparatedString(skills),
      };

      if (!addEmployee(employee)) {
        return text(`Employee with email '${employee.email}' already exists.`);
      }

      return text(`Successfully added employee: ${fullName(employee)}`);
    },
  );

  mcp.registerTool(
    "update_employee",
    {
      description: "Updates an existing employee by email",
      inputSchema: {
        email: z.string().describe("Email address of the employee to update"),
        firstName: z.string().nullable().default(null).describe("New first name (optional)"),
        lastName: z.string().nullable().default(null).describe("New last name (optional)"),
        currentRole: z.string().nullable().default(null).describe("New current role (optional)"),
        spokenLanguages: z
          .string()
          .nullable()
          .default(null)
          .describe("New comma-separated list of spoken languages (optional)"),
        skills: z.string().nullable().default(null).describe("New comma-separated list of skills (optional)"),
      },
    },
    async ({ email, firstName, lastName, currentRole, spokenLanguages, skills }) => {
      const success = updateEmployee(email, (employee) => {
        if (firstName?.trim()) {
          employee.firstName = firstName.trim();
        }

        if (lastName?.trim()) {
          employee.lastName = lastName.trim();
        }

        if (currentRole?.trim()) {
          employee.currentRole = currentRole.trim();
        }

        if (spokenLanguages != null) {
          employee.spokenLanguages = parseCommaSeparatedString(spokenLanguages);
        }

        if (skills != null) {
          employee.skills = parseCommaSeparatedString(skills);
        }
      });

      if (!success) {
        return text(`Employee with email '${email}' not found.`);
      }

      return text(`Successfully updated employee with email: ${email}`);
    },
  );

  mcp.registerTool(
    "remove_employee",
    {
      description: "Removes an employee by email",
      inputSchema: {
        email: z.string().describe("Email address of the employee to remove"),
      },
    },
    async ({ email }) => {
      if (!removeEmployee(email)) {
        return text(`Employee with email '${email}' not found.`);
      }

      return text(`Successfully removed employee with email: ${email}`);
    },
  );

  mcp.registerTool(
    "search_employees",
    {
      description: "Searches for employees by name, email, skills, or current role",
      inputSchema: {
        searchTerm: z.string().describe("Search term to find in employee data"),
      },
    },
    async ({ searchTerm }) => text(serializeEmployeeCollection({ employees: searchEmployees(searchTerm) })),
  );
}
