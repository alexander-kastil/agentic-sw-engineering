# HR MCP Server

The same stateful MCP server in three stacks. Each exposes five employee-management tools (`list_employees`, `add_employee`, `update_employee`, `search_employees`, `remove_employee`) over Streamable HTTP, backed by a local SQLite file seeded with 8 employees on first run.

## Table of Contents

| Project                                      | Description                                                                         |
| -------------------------------------------- | ----------------------------------------------------------------------------------- |
| [HR Server - C#](./hr-mcp-server-cs)         | ASP.NET Core with the `ModelContextProtocol` SDK, EF Core and SQLite, on port 47002 |
| [HR Server - Python](./hr-mcp-server-py)     | Python with the `mcp` SDK and SQLite, pinned packages                               |
| [HR Server - TypeScript](./hr-mcp-server-ts) | Node.js with `@modelcontextprotocol/sdk` and SQLite, pinned packages                |
