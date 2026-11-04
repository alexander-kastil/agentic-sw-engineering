import { createServer } from "node:http";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { initializeDatabase } from "./data/employee-db-initializer.js";
import { registerHrTools } from "./tools/hr-tools.js";

const HOST = process.env.HOST ?? "0.0.0.0";
const PORT = Number(process.env.PORT ?? "47002");

function createMcpServer(): McpServer {
  const mcp = new McpServer({ name: "hr-mcp-server", version: "1.0.0" }, { capabilities: { logging: {} } });
  registerHrTools(mcp);
  return mcp;
}

initializeDatabase();

createServer(async (req, res) => {
  if (new URL(req.url ?? "/", "http://localhost").pathname !== "/") {
    res.writeHead(404).end();
    return;
  }

  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  res.on("close", () => transport.close());
  await createMcpServer().connect(transport);
  await transport.handleRequest(req, res);
}).listen(PORT, HOST, () => {
  console.log(`HR MCP Server listening on http://${HOST}:${PORT}`);
});
