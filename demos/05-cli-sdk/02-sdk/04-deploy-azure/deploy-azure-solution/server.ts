import { createServer, IncomingMessage, ServerResponse } from "node:http";
import { CopilotClient, RuntimeConnection, defineTool } from "@github/copilot-sdk";

const PORT = Number(process.env.PORT ?? 8080);
const MODEL = process.env.COPILOT_MODEL ?? "gpt-5-mini";
const RUNTIME_URL = process.env.COPILOT_RUNTIME_URL;

const getServiceStatus = defineTool<{ service: string }>("get_service_status", {
  description: "Get the current deployment status of an internal service",
  skipPermission: true,
  parameters: {
    type: "object",
    properties: {
      service: { type: "string", description: "The service name" },
    },
    required: ["service"],
  },
  handler: async ({ service }) => ({
    service,
    status: "running",
    revision: process.env.CONTAINER_APP_REVISION ?? "local",
    region: process.env.AZURE_REGION ?? "local",
  }),
});

const client = new CopilotClient(
  RUNTIME_URL ? { connection: RuntimeConnection.forUri(RUNTIME_URL) } : {},
);

let ready = false;

async function ask(prompt: string): Promise<string> {
  const session = await client.createSession({
    model: MODEL,
    tools: [getServiceStatus],
    availableTools: ["custom:*"],
  });
  const response = await session.sendAndWait({ prompt });
  return response?.data.content ?? "";
}

function json(res: ServerResponse, status: number, body: unknown) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    "content-type": "application/json",
    "content-length": Buffer.byteLength(payload),
  });
  res.end(payload);
}

function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve) => {
    let raw = "";
    req.on("data", (chunk) => (raw += chunk));
    req.on("end", () => resolve(raw));
  });
}

const server = createServer(async (req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    return json(res, ready ? 200 : 503, {
      status: ready ? "ok" : "starting",
      model: MODEL,
      runtime: RUNTIME_URL ?? "bundled",
    });
  }

  if (req.method === "POST" && req.url === "/ask") {
    const body = await readBody(req);
    const prompt = (JSON.parse(body || "{}") as { prompt?: string }).prompt;
    if (!prompt) {
      return json(res, 400, { error: "body must be {\"prompt\": \"...\"}" });
    }
    return json(res, 200, { answer: await ask(prompt) });
  }

  return json(res, 404, { error: "try GET /health or POST /ask" });
});

async function main() {
  await client.start();
  ready = true;
  server.listen(PORT, () => console.log(`listening on ${PORT}, model ${MODEL}`));
}

async function shutdown() {
  server.close();
  await client.stop();
  process.exit(0);
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

main();
