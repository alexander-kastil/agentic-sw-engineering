# Copilot SDK Demos

The GitHub Copilot SDK enables you to embed AI-powered agentic workflows directly into your applications. These demos show how to build intelligent agents that understand code context and execute complex tasks autonomously, from code review and security auditing to weather lookup and document analysis. The SDK handles planning, tool invocation, and code execution—you define the behavior using TypeScript and Node.js, and Copilot handles the rest. Whether you are creating development tools, security auditors, documentation generators, or specialized analysis agents, the SDK provides a straightforward way to define custom tools and let AI decide when to use them.

## Building a Weather Assistant Agent (5 minutes)

This demo walks through building a practical agent that can query weather for multiple cities. You will learn how to define custom tools, create a session with streaming, and let the AI agent decide when to call your tools.

### Prerequisites

Ensure you have Node.js 18+ installed and the Copilot CLI authenticated:

```bash
copilot --version
```

If you have not authenticated yet, run `/login` in the Copilot CLI to authenticate with your GitHub account.

### Step 1: Create a Node.js Project and Install the SDK

Create a new directory and initialize your project:

```bash
mkdir copilot-weather-agent
cd copilot-weather-agent
npm init -y --init-type module
npm install @github/copilot-sdk tsx
```

### Step 2: Define a Custom Tool for Weather Lookup

Create a file named `agent.ts`:

```typescript
import { CopilotClient, defineTool, SessionEvent } from "@github/copilot-sdk";

// Define a custom tool that Copilot can call automatically
const getWeather = defineTool("get_weather", {
  description: "Get the current weather for a city",
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
      model: "gpt-4.1",
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
```

### Step 3: Run the Agent

Execute the agent:

```bash
npx tsx agent.ts
```

The Copilot agent analyzes your prompt, calls the `get_weather` tool for each city, and streams the response back to your terminal in real-time.

### Step 4: Build an Interactive CLI Assistant

Extend your agent to be a multi-turn interactive assistant:

```typescript
import { CopilotClient, defineTool, SessionEvent } from "@github/copilot-sdk";
import * as readline from "readline";

const getWeather = defineTool("get_weather", {
  description: "Get the current weather for a city",
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
  handler: async ({ city }) => {
    const conditions = ["sunny", "cloudy", "rainy", "partly cloudy"];
    const temp = Math.floor(Math.random() * 30) + 50;
    const condition = conditions[Math.floor(Math.random() * conditions.length)];
    return { city, temperature: `${temp}°F`, condition };
  },
});

async function main() {
  const client = new CopilotClient();
  const session = await client.createSession({
    model: "gpt-4.1",
    streaming: true,
    tools: [getWeather],
  });

  session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
      process.stdout.write(event.data.deltaContent);
    }
  });

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  console.log("Weather Assistant (type 'exit' to quit)");
  console.log("Try: 'What's the weather in Paris and London?'\n");

  const prompt = () => {
    rl.question("You: ", async (input) => {
      if (input.toLowerCase() === "exit") {
        await client.stop();
        rl.close();
        process.exit(0);
        return;
      }

      process.stdout.write("Assistant: ");
      await session.sendAndWait({ prompt: input });
      console.log("\n");
      prompt();
    });
  };

  prompt();
}

main().catch(console.error);
```

### Step 5: Add Code Analysis Tools

Extend your agent with multiple specialized tools to build a code security analyzer:

```typescript
import { CopilotClient, defineTool, SessionEvent } from "@github/copilot-sdk";

const analyzeCode = defineTool("analyze_security", {
  description: "Analyze code for common security vulnerabilities",
  parameters: {
    type: "object",
    properties: {
      code: {
        type: "string",
        description: "The code snippet to analyze",
      },
    },
    required: ["code"],
  },
  handler: async (args: { code: string }) => {
    const issues = [];

    if (args.code.includes("eval(")) issues.push("Dangerous eval() detected");
    if (args.code.includes("innerHTML"))
      issues.push("Potential XSS via innerHTML");
    if (args.code.match(/\bpassword\b.*=.*['"][^'"]*['"]/i))
      issues.push("Hardcoded secret/password detected");
    if (!args.code.includes("try") && args.code.includes("fetch"))
      issues.push("Unhandled Promise in fetch");

    return {
      issues: issues.length > 0 ? issues : ["No major issues detected"],
      severity: issues.length > 2 ? "high" : issues.length > 0 ? "medium" : "low",
      timestamp: new Date().toISOString(),
    };
  },
});

const getFileContent = defineTool("read_code_file", {
  description: "Read a code file to analyze",
  parameters: {
    type: "object",
    properties: {
      filename: {
        type: "string",
        description: "The filename to read",
      },
    },
    required: ["filename"],
  },
  handler: async (args: { filename: string }) => {
    // Simulate reading a file
    const sampleCode = `
      const password = "admin123";
      fetch('/api/data').then(r => r.json())
        .then(data => document.getElementById('container').innerHTML = data);
    `;
    return { filename: args.filename, content: sampleCode };
  },
});

async function main() {
  try {
    const client = new CopilotClient();
    const session = await client.createSession({
      model: "gpt-4.1",
      streaming: true,
      tools: [analyzeCode, getFileContent],
      systemMessage: {
        content:
          "You are a security-focused code reviewer. Be thorough and specific in your analysis.",
      },
    });

    session.on((event: SessionEvent) => {
      if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
      }
      if (event.type === "session.idle") {
        console.log("\n");
      }
    });

    await session.sendAndWait({
      prompt:
        "Read the code file 'app.js' and analyze it for security vulnerabilities.",
    });

    await client.stop();
    process.exit(0);
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

main();
```

## Key Concepts

A CopilotClient connects to the Copilot runtime. A session represents a conversation where Copilot maintains context and manages tool definitions. When you define a tool, you tell Copilot its description, parameter schema, and handler function—Copilot then automatically invokes it when appropriate based on the user's prompt. Streaming via session events like `assistant.message_delta` lets you process responses incrementally. System messages shape agent behavior, allowing you to define specialized roles like security auditors or code reviewers.

When tool execution completes, the result is sent back to Copilot for incorporation into the final response. Multiple tools can work together—Copilot orchestrates their execution based on reasoning about what the user needs.

## Error Handling

Always wrap your code in try-catch and ensure cleanup:

```typescript
try {
  const client = new CopilotClient();
  const session = await client.createSession({ model: "gpt-4.1" });
  // ... use session ...
} catch (error) {
  if ((error as any).code === "ENOENT") {
    console.error("Copilot CLI not installed");
  } else {
    console.error("Error:", (error as any).message);
  }
} finally {
  await client.stop();
}
```

## Links & Resources

- [GitHub Copilot SDK Repository](https://github.com/github/copilot-sdk)
- [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/tutorials/first-app.md)
- [Custom Tools Documentation](https://github.com/github/copilot-sdk/blob/main/docs/guides/tools.md)
- [MCP Server Integration](https://github.com/github/copilot-sdk/blob/main/docs/mcp/overview.md)
- [GitHub SDK Cookbook](https://github.com/github/copilot-sdk/tree/main/cookbook)
