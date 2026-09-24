using System.ComponentModel;
using GitHub.Copilot;
using Microsoft.Extensions.AI;

const string Model = "gpt-5-mini";

var listChanges = CopilotTool.DefineTool(
    ([Description("The tag to list changes since")] string since) =>
    {
        return new
        {
            since,
            changes = new[]
            {
                new { id = "a91f2c", area = "cli", summary = "add --fleet to the prompt runner" },
                new { id = "4d02be", area = "sdk", summary = "session.factory API for registered factories" },
                new { id = "7c1188", area = "sdk", summary = "customAgents accepted at session creation" },
                new { id = "be40aa", area = "docs", summary = "correct the tool permission defaults" },
            },
        };
    },
    toolOptions: new CopilotToolOptions { SkipPermission = true },
    factoryOptions: new AIFunctionFactoryOptions
    {
        Name = "list_changes",
        Description = "List the merged changes in the repository since a given tag",
    });

async Task<string> RunSpecialistAsync(CopilotSession session, string label, string prompt)
{
    Console.Write($"\n--- {label} ---\n");
    var response = await session.SendAndWaitAsync(new MessageOptions { Prompt = prompt }, TimeSpan.FromSeconds(180));
    var text = response?.Data?.Content ?? "";
    Console.WriteLine(text);
    return text;
}

try
{
    await using var client = new CopilotClient();

    async Task<CopilotSession> CreateSpecialistAsync(string systemMessage, ICollection<AIFunctionDeclaration>? tools = null) =>
        await client.CreateSessionAsync(new SessionConfig
        {
            Model = Model,
            Streaming = false,
            Tools = tools ?? [],
            AvailableTools = new ToolSet().AddCustom("*"),
            SystemMessage = new SystemMessageConfig { Mode = SystemMessageMode.Replace, Content = systemMessage },
        });

    await using var researcher = await CreateSpecialistAsync(
        "You are a research specialist. Call the tools you are given, then report only the facts you retrieved as a compact bullet list. Never write prose around them.",
        [listChanges]);

    await using var builder = await CreateSpecialistAsync(
        "You are a release-notes writer. Turn the facts you are handed into a markdown section titled '## Unreleased', one bullet per change, grouped by area. Output the markdown only.");

    await using var reviewer = await CreateSpecialistAsync(
        "You are a style reviewer. The house style forbids em dashes and requires every bullet to name its area. Answer with a verdict line 'VERDICT: PASS' or 'VERDICT: FAIL', then one line per violation.");

    var facts = await RunSpecialistAsync(
        researcher,
        "researcher",
        "List the changes since tag v2.1 and report them.");

    var draft = await RunSpecialistAsync(
        builder,
        "builder",
        $"Write the release-notes section from these facts:\n\n{facts}");

    await RunSpecialistAsync(
        reviewer,
        "reviewer",
        $"Review this release-notes section against the house style:\n\n{draft}");
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Error: {ex.Message}");
    Environment.Exit(1);
}
