# HR MCP Server

A stateful MCP server exposing five employee-management tools over Streamable HTTP. Data lives in a local SQLite file, `hr-data.db`, created and seeded with 8 employees on first run by `EmployeeDbInitializer`. No database server, connection string, or credentials are needed.

## Run the server

```powershell
dotnet run
```

The server listens on `http://localhost:47002`, the endpoint `app.MapMcp()` exposes. Delete `hr-data.db` to reset the data and reseed on the next start.

## Connect with MCP Inspector

1. Start the server (see above).
2. Launch the inspector with the provided config:

```powershell
npx @modelcontextprotocol/inspector --config inspector.config.json --server hr-mcp
```

The config at `inspector.config.json` points the inspector at `http://localhost:47002`. The `--server` flag must reference an entry in a config file, which is why the file exists.

## Smoke test

1. Launch the inspector as above and click Connect.
2. Confirm all **5 tools** are listed:
   - `list_employees` - retrieves all employees
   - `add_employee` - adds a new employee with optional languages and skills
   - `update_employee` - updates an existing employee by email
   - `remove_employee` - removes an employee by email
   - `search_employees` - searches by name, email, skills, or current role (parameter: `searchTerm`)
3. Call `list_employees` and verify the response contains the 8 seeded employees.

The same checks run headless from the CLI:

```powershell
npx @modelcontextprotocol/inspector --cli --config inspector.config.json --server hr-mcp --method tools/list
npx @modelcontextprotocol/inspector --cli --config inspector.config.json --server hr-mcp --method tools/call --tool-name list_employees
```

## Remote (Azure) deployment

The `hr-mcp-azure-dev` entry in `inspector.config.json` selects a hosted deployment instead of the local one:

```powershell
npx @modelcontextprotocol/inspector --config inspector.config.json --server hr-mcp-azure-dev
```

> **Heads-up:** The App Service that entry names is not currently provisioned, so this path fails until the server is redeployed. The local `hr-mcp` entry is the working one. Editing `inspector.config.json` is a local workflow change; it never requires republishing the app.
