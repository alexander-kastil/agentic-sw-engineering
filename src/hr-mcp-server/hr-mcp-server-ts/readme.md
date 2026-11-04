# HR MCP Server (TypeScript)

A stateful MCP server exposing five employee-management tools over Streamable HTTP, built with the official `@modelcontextprotocol/sdk`. Data lives in a local SQLite file, `hr-data.db`, created and seeded with 8 employees on first run by `src/data/employee-db-initializer.ts`. It uses `node:sqlite`, built into Node 24, so no database server, native build, connection string, or credentials are needed.

## Run the server

```powershell
npm install
npm run build
npm start
```

The server listens on `http://localhost:47002`, at the root path `/`. Set `PORT` to listen on another port. Delete `hr-data.db` to reset the data and reseed on the next start.

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
