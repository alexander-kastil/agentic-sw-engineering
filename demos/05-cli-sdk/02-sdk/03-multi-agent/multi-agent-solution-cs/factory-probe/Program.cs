using GitHub.Copilot;

const string Model = "gpt-5-mini";
const string FactoryName = "audit-pipeline";
var phases = new[] { "Audit", "Merge" };

try
{
    await using var client = new CopilotClient();
    await using var session = await client.CreateSessionAsync(new SessionConfig { Model = Model, Streaming = false });

    Console.WriteLine($"factory defined: {FactoryName}");
    Console.WriteLine($"phases: {string.Join(", ", phases)}");

    try
    {
        var run = await session.Rpc.Factory.RunAsync(
            FactoryName,
            new { files = new[] { "coordinator/Program.cs" } },
            options: null);
        Console.WriteLine($"run status: {run.Status}");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"\nsession.Rpc.Factory.RunAsync rejected: {ex.Message}");
        Console.WriteLine(
            "The .NET SDK 1.0.14 has no defineFactory builder at all: GitHub.Copilot.SDK.dll exposes only the low-level " +
            "session.Rpc.Factory RPC surface (RunAsync, ExecuteAsync, AgentAsync, ...), which invokes a factory " +
            "already registered under that name. Registration itself is only possible from a CLI extension process, " +
            "which the .NET SDK has no host API for either.");
    }
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Error: {ex.Message}");
    Environment.Exit(1);
}
