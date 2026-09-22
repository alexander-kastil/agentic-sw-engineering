import { CopilotClient, defineTool, SessionEvent } from "@github/copilot-sdk";

// Define a custom tool that Copilot can call automatically
const getWeather = defineTool("get_weather", {
  description: "Get the current weather for a city",
  skipPermission: true,
  parameters: {
    type: "object",
    properties: {
      city: {
        type: "string",
        description: "The city name to get weather for",
      },
    },
    required: ["city"],
  },
  handler: async (args: { city: string }) => {
    // In a real app, this would call a weather API
    const conditions = ["sunny", "cloudy", "rainy", "partly cloudy"];
    const temp = Math.floor(Math.random() * 30) + 50;
    const condition = conditions[Math.floor(Math.random() * conditions.length)];

    return {
      city: args.city,
      temperature: `${temp}°F`,
      condition,
      timestamp: new Date().toISOString(),
    };
  },
});

async function main() {
  try {
    const client = new CopilotClient();
    const session = await client.createSession({
      model: "gpt-5-mini",
      streaming: true,
      tools: [getWeather],
    });

    // Stream responses as they arrive
    session.on((event: SessionEvent) => {
      if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
      }
      if (event.type === "session.idle") {
        console.log("\n");
      }
    });

    // Send a prompt that requires the agent to use tools
    await session.sendAndWait({
      prompt: "What's the weather like in Seattle and Tokyo? Give me the temperatures.",
    });

    await client.stop();
    process.exit(0);
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

main();
