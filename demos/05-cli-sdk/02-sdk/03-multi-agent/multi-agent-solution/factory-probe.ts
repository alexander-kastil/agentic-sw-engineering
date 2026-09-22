import { CopilotClient, defineFactory } from "@github/copilot-sdk";

const MODEL = "gpt-5-mini";

const auditPipeline = defineFactory<{ files: string[] }>({
  meta: {
    name: "audit-pipeline",
    description: "Fans one subagent out per file and merges the findings. args: { files: string[] }",
    phases: [{ title: "Audit" }, { title: "Merge" }],
    argsSchema: {
      type: "object",
      required: ["files"],
      properties: {
        files: { type: "array", items: { type: "string" } },
      },
    },
  },
  run: async (ctx) => {
    ctx.phase("Audit");
    const findings = await ctx.parallel(
      ctx.args.files.map(
        (file) => () => ctx.agent(`Report the model string used in ${file}`, { label: file }),
      ),
    );

    ctx.phase("Merge");
    return await ctx.step("merge", () => ({
      findings: findings.map((finding) => (typeof finding === "string" ? finding : null)),
    }));
  },
});

async function main() {
  const client = new CopilotClient();
  const session = await client.createSession({ model: MODEL, streaming: false });

  console.log(`factory defined: ${auditPipeline.meta.name}`);
  console.log(`phases: ${auditPipeline.meta.phases.map((phase) => phase.title).join(", ")}`);

  try {
    const run = await session.factory.run(auditPipeline, {
      args: { files: ["coordinator.ts"] },
    });
    console.log(`run status: ${run.status}`);
    console.log(run.result);
  } catch (error) {
    console.log(`\nsession.factory.run rejected: ${(error as Error).message}`);
    console.log(
      "A handle from defineFactory is only registered by joinSession({ factories }) in a CLI extension.",
    );
  }

  await client.stop();
  process.exit(0);
}

main();
