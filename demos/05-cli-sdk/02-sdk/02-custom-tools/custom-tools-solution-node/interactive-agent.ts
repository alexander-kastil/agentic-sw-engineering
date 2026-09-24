import { CopilotClient, defineTool, SessionEvent } from "@github/copilot-sdk";
import { createInterface } from "node:readline";

const getWeather = defineTool("get_weather", {
  description: "Get the current weather for a city",
  skipPermission: true,
  parameters: {
    type: "object",
    properties: {
      city: {
        type: "string",
        description: "The city name",
      },
    },
    required: ["city"],
  },
  handler: async ({ city }: { city: string }) => {
    const conditions = ["sunny", "cloudy", "rainy", "partly cloudy"];
    const temp = Math.floor(Math.random() * 30) + 50;
    const condition = conditions[Math.floor(Math.random() * conditions.length)];
    return { city, temperature: `${temp}°F`, condition };
  },
});

async function main() {
  const client = new CopilotClient();
  const session = await client.createSession({
    model: "gpt-5-mini",
    streaming: true,
    tools: [getWeather],
  });

  session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
      process.stdout.write(event.data.deltaContent);
    }
  });

  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: "You: ",
  });

  let closed = false;
  rl.on("close", () => {
    closed = true;
  });
  process.on("SIGINT", () => rl.close());

  console.log("Weather Assistant (type 'exit' to quit)");
  console.log("Try: 'What's the weather in Paris and London?'\n");
  rl.prompt();

  for await (const line of rl) {
    const input = line.trim();
    if (input.toLowerCase() === "exit") {
      break;
    }
    if (input.length > 0) {
      process.stdout.write("Assistant: ");
      await session.sendAndWait({ prompt: input });
      console.log("\n");
    }
    if (closed) {
      break;
    }
    rl.prompt();
  }

  rl.close();
  await client.stop();
}

main().catch((error) => {
  console.error("Error:", error);
  process.exit(1);
});
