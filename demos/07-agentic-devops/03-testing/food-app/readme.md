# Food App Polyglot

A comprehensive testing demonstration showcasing how to test the same food shop application across different technology stacks.

This polyglot architecture example includes multiple backend and frontend implementations of the same catalog, so the same behaviour can be tested with the idioms of each ecosystem. The C# catalog service carries an agent-generated xUnit suite in `tests/`; the other projects ship without test suites on purpose, so generating them is the exercise.

These projects can be used to achieve unit testing for individual backend services (API endpoints, business logic, data access) and frontend applications (components, services, state management).

When deployed together, they enable end-to-end (E2E) and integration testing scenarios where frontend tests interact with live backend services, validating complete user workflows across both layers.

## Table of Contents

| Project                                                           | Description                                                                               |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [Catalog Service - C#](./catalog-api/catalog-service-cs/)         | ASP.NET Core on net10.0 with EF Core 10, SQLite by default, and a generated xUnit suite |
| [Catalog Service - Java](./catalog-api/catalog-service-java/)     | Spring Boot 3.2 on Java 21 with Spring Data JPA, built with Maven                         |
| [Catalog Service - Python](./catalog-api/catalog-service-py/)     | Flask 3 with Flask-SQLAlchemy, the target for pytest generation                           |
| [Catalog Service - TypeScript](./catalog-api/catalog-service-ts/) | Express 4 on Node with SQLite, the target for Jest or Vitest generation                   |
| [Food Shop - Angular](./shop-ui/food-shop-ng/)                    | Angular 22 standalone components with NgRx, tested on the Karma and Jasmine builder       |
| [Food Shop - React](./shop-ui/food-shop-react/)                   | React 18 on react-scripts, the target for React Testing Library generation                |
