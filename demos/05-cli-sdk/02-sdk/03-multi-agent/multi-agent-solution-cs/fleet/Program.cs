using GitHub.Copilot;

const string Model = "gpt-5-mini";

var solutionRoot = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", ".."));

try
{
    await using var client = new CopilotClient();
    await using var session = await client.CreateSessionAsync(new SessionConfig
    {
        Model = Model,
        Streaming = false,
        WorkingDirectory = solutionRoot,
        OnPermissionRequest = PermissionHandler.ApproveAll,
    });

    session.On<SessionEvent>(evt =>
    {
        if (evt is AssistantMessageEvent msg)
        {
            Console.WriteLine($"\n--- assistant ---\n{msg.Data.Content}");
        }
    });

    var result = await session.Rpc.Fleet.StartAsync(
        prompt: "Audit coordinator/Program.cs, specialists/Program.cs and fleet/Program.cs under this directory. " +
            "Give each file to its own subagent, and have each report the file name, " +
            "the model string it uses, and how many SDK sessions it creates. " +
            "Then print one markdown table of the three results.",
        wait: true);

    Console.WriteLine($"\nfleet started: {result.Started}");
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Error: {ex.Message}");
    Environment.Exit(1);
}
