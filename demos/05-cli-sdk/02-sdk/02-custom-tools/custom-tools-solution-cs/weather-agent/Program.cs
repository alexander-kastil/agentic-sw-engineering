using System.ComponentModel;
using GitHub.Copilot;
using Microsoft.Extensions.AI;

var getWeather = CopilotTool.DefineTool(
    ([Description("The city name to get weather for")] string city) =>
    {
        var conditions = new[] { "sunny", "cloudy", "rainy", "partly cloudy" };
        var random = new Random();
        var temperature = random.Next(50, 80);
        var condition = conditions[random.Next(conditions.Length)];

        return new
        {
            city,
            temperature = $"{temperature}°F",
            condition,
            timestamp = DateTimeOffset.UtcNow.ToString("O"),
        };
    },
    toolOptions: new CopilotToolOptions { SkipPermission = true },
    factoryOptions: new AIFunctionFactoryOptions
    {
        Name = "get_weather",
        Description = "Get the current weather for a city",
    });

try
{
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
        if (evt is SessionIdleEvent)
        {
            Console.WriteLine("\n");
        }
    });

    await session.SendAndWaitAsync(new MessageOptions
    {
        Prompt = "What's the weather like in Seattle and Tokyo? Give me the temperatures.",
    });
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Error: {ex.Message}");
    Environment.Exit(1);
}
