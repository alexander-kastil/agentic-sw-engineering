export interface Employee {
  firstName: string;
  lastName: string;
  email: string;
  spokenLanguages: string[];
  skills: string[];
  currentRole: string;
}

export interface EmployeeCollection {
  employees: Employee[];
}

export function fullName(employee: Employee): string {
  return `${employee.firstName} ${employee.lastName}`;
}

export function serializeEmployeeCollection(collection: EmployeeCollection): string {
  return JSON.stringify({
    employees: collection.employees.map((employee) => ({
      firstname: employee.firstName,
      lastname: employee.lastName,
      email: employee.email,
      spoken_languages: employee.spokenLanguages,
      skills: employee.skills,
      current_role: employee.currentRole,
      fullName: fullName(employee),
    })),
  });
}
