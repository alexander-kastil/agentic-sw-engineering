import { db, ensureCreated } from "./employee-db.js";
import { addEmployee } from "../services/employee-service.js";
import type { Employee } from "../tools/models.js";

const seedEmployees: Employee[] = [
  {
    firstName: "Carlos",
    lastName: "Gomez",
    email: "carlos.gomez@restaurant.com",
    spokenLanguages: ["Spanish", "English", "French"],
    skills: ["Sous Chef", "Menu Planning", "Food Safety", "Inventory Management"],
    currentRole: "Sous Chef",
  },
  {
    firstName: "Marie",
    lastName: "Dubois",
    email: "marie.dubois@restaurant.com",
    spokenLanguages: ["French", "English", "Italian"],
    skills: ["Pastry Chef", "Dessert Creation", "Baking", "Team Leadership"],
    currentRole: "Pastry Chef",
  },
  {
    firstName: "Luca",
    lastName: "Rossi",
    email: "luca.rossi@restaurant.com",
    spokenLanguages: ["Italian", "English", "Spanish"],
    skills: ["Head Waiter", "Customer Service", "Wine Pairing", "Table Management"],
    currentRole: "Head Waiter",
  },
  {
    firstName: "Anna",
    lastName: "Schmidt",
    email: "anna.schmidt@restaurant.com",
    spokenLanguages: ["German", "English", "Russian"],
    skills: ["Restaurant Manager", "Staff Scheduling", "Budgeting", "Event Coordination"],
    currentRole: "Restaurant Manager",
  },
  {
    firstName: "Sofia",
    lastName: "Fernandez",
    email: "sofia.fernandez@restaurant.com",
    spokenLanguages: ["Portuguese", "Spanish", "English"],
    skills: ["Bartender", "Mixology", "Inventory Control", "Customer Engagement"],
    currentRole: "Bartender",
  },
  {
    firstName: "Kenji",
    lastName: "Tanaka",
    email: "kenji.tanaka@restaurant.com",
    spokenLanguages: ["Japanese", "English", "Mandarin"],
    skills: ["Sushi Chef", "Knife Skills", "Seafood Preparation", "Quality Control"],
    currentRole: "Sushi Chef",
  },
  {
    firstName: "Olga",
    lastName: "Ivanova",
    email: "olga.ivanova@restaurant.com",
    spokenLanguages: ["Russian", "English", "German"],
    skills: ["Hostess", "Reservation Management", "Multilingual Communication", "Conflict Resolution"],
    currentRole: "Hostess",
  },
  {
    firstName: "Ahmed",
    lastName: "Hassan",
    email: "ahmed.hassan@restaurant.com",
    spokenLanguages: ["Arabic", "English", "French"],
    skills: ["Grill Chef", "Meat Preparation", "Kitchen Safety", "Teamwork"],
    currentRole: "Grill Chef",
  },
];

export function initializeDatabase(): void {
  ensureCreated();

  if (db.prepare(`SELECT 1 FROM "Candidates" LIMIT 1`).get()) {
    console.log("Employee database already contains data; skipping seed.");
    return;
  }

  seedEmployees.forEach((employee) => addEmployee({ ...employee }));

  console.log(`Seeded ${seedEmployees.length} employees into the database.`);
}
