using System.ComponentModel;
using GitHub.Copilot;
using Microsoft.Extensions.AI;

var getWeather = CopilotTool.DefineTool(
    ([Description("The city name")] string city) =>
    {
        var conditions = new[] { "sunny", "cloudy", "rainy", "partly cloudy" };
        var random = new Random();
        var temperature = random.Next(50, 80);
        var condition = conditions[random.Next(conditions.Length)];

        return new { city, temperature = $"{temperature}°F", condition };
    },
    toolOptions: new CopilotToolOptions { SkipPermission = true },
    factoryOptions: new AIFunctionFactoryOptions
    {
        Name = "get_weather",
        Description = "Get the current weather for a city",
    });

await using var client = new CopilotClient();
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5-mini",
    Streaming = true,
    Tools = [getWeather],
});

session.On<SessionEvent>(evt =>
{
    if (evt is AssistantMessageDeltaEvent delta)
    {
        Console.Write(delta.Data.DeltaContent);
    }
});

var cancelled = false;
Console.CancelKeyPress += (_, args) =>
{
    args.Cancel = true;
    cancelled = true;
};

Console.WriteLine("Weather Assistant (type 'exit' to quit)");
Console.WriteLine("Try: 'What's the weather in Paris and London?'\n");
Console.Write("You: ");

string? line;
while (!cancelled && (line = Console.ReadLine()) != null)
{
    var input = line.Trim();
    if (input.Equals("exit", StringComparison.OrdinalIgnoreCase))
    {
        break;
    }
    if (input.Length > 0)
    {
        Console.Write("Assistant: ");
        await session.SendAndWaitAsync(new MessageOptions { Prompt = input });
        Console.WriteLine("\n");
    }
    if (cancelled)
    {
        break;
    }
    Console.Write("You: ");
}
