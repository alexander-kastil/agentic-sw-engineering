# Food App Polyglot

A comprehensive testing demonstration showcasing how to test the same food shop application across different technology stacks.

This polyglot architecture example includes multiple backend- and frontend implementations, each with corresponding test suites demonstrating best practices for their respective ecosystems.

These projects can be used to achieve unit testing for individual backend services (API endpoints, business logic, data access) and frontend applications (components, services, state management).

When deployed together, they enable end-to-end (E2E) and integration testing scenarios where frontend tests interact with live backend services, validating complete user workflows across both layers.

## Table of Contents

| Project                                                           | Description                                                                               |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [Catalog Service - C#](./catalog-api/catalog-service-cs/)         | ASP.NET Core reference implementation with Entity Framework Core and Application Insights |
| [Catalog Service - Java](./catalog-api/catalog-service-java/)     | Java/Spring Boot implementation demonstrating Java ecosystem testing patterns             |
| [Catalog Service - Python](./catalog-api/catalog-service-py/)     | Python implementation demonstrating pytest and FastAPI/Flask testing patterns             |
| [Catalog Service - TypeScript](./catalog-api/catalog-service-ts/) | TypeScript/Node.js implementation demonstrating Jest/Vitest testing patterns              |
| [Food Shop - Angular](./shop-ui/food-shop-ng/)                    | Angular 18+ standalone components with unit, integration, and component testing           |
| [Food Shop - React](./shop-ui/food-shop-react/)                   | React application with hooks, components, and state management testing patterns           |
