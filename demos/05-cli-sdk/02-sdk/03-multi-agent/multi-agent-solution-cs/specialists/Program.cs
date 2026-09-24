using System.ComponentModel;
using GitHub.Copilot;
using GitHub.Copilot.Rpc;
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
            },
        };
    },
    toolOptions: new CopilotToolOptions { SkipPermission = true },
    factoryOptions: new AIFunctionFactoryOptions
    {
        Name = "list_changes",
        Description = "List the merged changes in the repository since a given tag",
    });

var agents = new List<CustomAgentConfig>
{
    new()
    {
        Name = "researcher",
        DisplayName = "Researcher",
        Description = "Retrieves repository facts and reports them without commentary",
        Tools = ["list_changes"],
        Prompt = "You are a research specialist. Call the tools you are given, then report only the facts you retrieved as a compact bullet list.",
    },
    new()
    {
        Name = "reviewer",
        DisplayName = "Reviewer",
        Description = "Checks a draft against the house style and returns a verdict",
        Tools = [],
        Prompt = "You are a style reviewer. The house style forbids em dashes and requires every bullet to carry a change id. Answer with 'VERDICT: PASS' or 'VERDICT: FAIL', then one line per violation.",
    },
};

try
{
    await using var client = new CopilotClient();
    await using var session = await client.CreateSessionAsync(new SessionConfig
    {
        Model = Model,
        Streaming = false,
        Tools = [listChanges],
        CustomAgents = agents,
        Agent = "researcher",
    });

    var registered = await session.Rpc.Agent.ListAsync(new SessionAgentListRequest());
    Console.WriteLine("registered agents:");
    foreach (var agent in registered.Agents)
    {
        Console.WriteLine($"  {agent.Name}: {agent.Description}");
    }

    var current = await session.Rpc.Agent.GetCurrentAsync();
    Console.WriteLine($"\nselected at start: {current.Agent?.Name ?? "default"}");

    var facts = await session.SendAndWaitAsync(
        new MessageOptions { Prompt = "List the changes since tag v2.1 and report them." },
        TimeSpan.FromSeconds(180));
    Console.WriteLine("\n--- researcher ---");
    Console.WriteLine(facts?.Data?.Content ?? "");

    var selected = await session.Rpc.Agent.SelectAsync("reviewer");
    Console.WriteLine($"\nselected for the next turn: {selected.Agent?.Name ?? "default"}");

    var verdict = await session.SendAndWaitAsync(
        new MessageOptions { Prompt = "Review the bullet list you just produced against the house style." },
        TimeSpan.FromSeconds(180));
    Console.WriteLine("\n--- reviewer ---");
    Console.WriteLine(verdict?.Data?.Content ?? "");
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Error: {ex.Message}");
    Environment.Exit(1);
}
