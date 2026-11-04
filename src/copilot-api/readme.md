# Copilot Instructions API

The same small REST API in two stacks. Each serves a read-only list of instructions, each with a name and a description, at `GET /api/instructions` and `GET /api/instructions/{name}`. The .NET version is the result of the scaffold demo in [01-scaffold-net](../../demos/01-fundamentals/05-agent-mode-basics/01-scaffold-net/readme.md).

## Table of Contents

| Project                                  | Description                                                            |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| [Copilot API - C#](./copilot-api-cs)     | ASP.NET Core Web API with an `InstructionsController` and Scalar UI    |
| [Copilot API - Python](./copilot-api-py) | FastAPI with the same routes, OpenAPI docs at `/docs`, and pytest tests |
