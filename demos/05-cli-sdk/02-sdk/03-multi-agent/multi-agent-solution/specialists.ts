import { CopilotClient, defineTool, type CustomAgentConfig } from "@github/copilot-sdk";

const MODEL = "gpt-5-mini";

const listChanges = defineTool<{ since: string }>("list_changes", {
  description: "List the merged changes in the repository since a given tag",
  skipPermission: true,
  parameters: {
    type: "object",
    properties: {
      since: {
        type: "string",
        description: "The tag to list changes since",
      },
    },
    required: ["since"],
  },
  handler: async (args) => ({
    since: args.since,
    changes: [
      { id: "a91f2c", area: "cli", summary: "add --fleet to the prompt runner" },
      { id: "4d02be", area: "sdk", summary: "session.factory API for registered factories" },
      { id: "7c1188", area: "sdk", summary: "customAgents accepted at session creation" },
    ],
  }),
});

const agents: CustomAgentConfig[] = [
  {
    name: "researcher",
    displayName: "Researcher",
    description: "Retrieves repository facts and reports them without commentary",
    tools: ["list_changes"],
    prompt:
      "You are a research specialist. Call the tools you are given, then report only the facts you retrieved as a compact bullet list.",
  },
  {
    name: "reviewer",
    displayName: "Reviewer",
    description: "Checks a draft against the house style and returns a verdict",
    tools: [],
    prompt:
      "You are a style reviewer. The house style forbids em dashes and requires every bullet to carry a change id. Answer with 'VERDICT: PASS' or 'VERDICT: FAIL', then one line per violation.",
  },
];

async function main() {
  const client = new CopilotClient();
  const session = await client.createSession({
    model: MODEL,
    streaming: false,
    tools: [listChanges],
    customAgents: agents,
    agent: "researcher",
  });

  const registered = await session.rpc.agent.list();
  console.log("registered agents:");
  for (const agent of registered.agents) {
    console.log(`  ${agent.name}: ${agent.description}`);
  }

  const current = await session.rpc.agent.getCurrent();
  console.log(`\nselected at start: ${current.agent?.name ?? "default"}`);

  const facts = await session.sendAndWait(
    { prompt: "List the changes since tag v2.1 and report them." },
    180_000,
  );
  console.log("\n--- researcher ---");
  console.log(facts?.data.content ?? "");

  const selected = await session.rpc.agent.select({ name: "reviewer" });
  console.log(`\nselected for the next turn: ${selected.agent?.name ?? "default"}`);

  const verdict = await session.sendAndWait(
    { prompt: "Review the bullet list you just produced against the house style." },
    180_000,
  );
  console.log("\n--- reviewer ---");
  console.log(verdict?.data.content ?? "");

  await client.stop();
  process.exit(0);
}

main();
