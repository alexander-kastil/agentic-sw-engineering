import { CopilotClient, approveAll, type SessionEvent } from "@github/copilot-sdk";

const MODEL = "gpt-5-mini";

async function main() {
  const client = new CopilotClient();
  const session = await client.createSession({
    model: MODEL,
    streaming: false,
    workingDirectory: process.cwd(),
    onPermissionRequest: approveAll,
  });

  session.on((event: SessionEvent) => {
    if (event.type === "assistant.message") {
      console.log(`\n--- assistant ---\n${event.data.content}`);
    }
  });

  const result = await session.rpc.fleet.start({
    prompt:
      "Audit coordinator.ts, specialists.ts and fleet.ts in this directory. " +
      "Give each file to its own subagent, and have each report the file name, " +
      "the model string it uses, and how many SDK sessions it creates. " +
      "Then print one markdown table of the three results.",
    wait: true,
  });

  console.log(`\nfleet started: ${result.started}`);

  await client.stop();
  process.exit(0);
}

main();
