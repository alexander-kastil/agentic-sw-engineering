import { CopilotClient, defineTool, SessionEvent } from "@github/copilot-sdk";

const analyzeCode = defineTool("analyze_security", {
  description: "Analyze code for common security vulnerabilities",
  skipPermission: true,
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
    const issues: string[] = [];

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
  skipPermission: true,
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
      model: "gpt-5-mini",
      streaming: true,
      tools: [analyzeCode, getFileContent],
      availableTools: ["custom:*"],
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
