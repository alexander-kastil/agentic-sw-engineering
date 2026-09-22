import {
  CopilotClient,
  defineTool,
  type CopilotSession,
  type SessionConfig,
} from "@github/copilot-sdk";

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
      { id: "be40aa", area: "docs", summary: "correct the tool permission defaults" },
    ],
  }),
});

async function runSpecialist(
  session: CopilotSession,
  label: string,
  prompt: string,
): Promise<string> {
  process.stdout.write(`\n--- ${label} ---\n`);
  const response = await session.sendAndWait({ prompt }, 180_000);
  const text = response?.data.content ?? "";
  console.log(text);
  return text;
}

async function main() {
  const client = new CopilotClient();

  const specialist = (systemMessage: string, tools: SessionConfig["tools"] = []) =>
    client.createSession({
      model: MODEL,
      streaming: false,
      tools,
      availableTools: ["custom:*"],
      systemMessage: { mode: "replace", content: systemMessage },
    });

  const researcher = await specialist(
    "You are a research specialist. Call the tools you are given, then report only the facts you retrieved as a compact bullet list. Never write prose around them.",
    [listChanges],
  );

  const builder = await specialist(
    "You are a release-notes writer. Turn the facts you are handed into a markdown section titled '## Unreleased', one bullet per change, grouped by area. Output the markdown only.",
  );

  const reviewer = await specialist(
    "You are a style reviewer. The house style forbids em dashes and requires every bullet to name its area. Answer with a verdict line 'VERDICT: PASS' or 'VERDICT: FAIL', then one line per violation.",
  );

  const facts = await runSpecialist(
    researcher,
    "researcher",
    "List the changes since tag v2.1 and report them.",
  );

  const draft = await runSpecialist(
    builder,
    "builder",
    `Write the release-notes section from these facts:\n\n${facts}`,
  );

  await runSpecialist(
    reviewer,
    "reviewer",
    `Review this release-notes section against the house style:\n\n${draft}`,
  );

  await client.stop();
  process.exit(0);
}

main();
